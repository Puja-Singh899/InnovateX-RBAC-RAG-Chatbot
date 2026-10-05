import json
from backend.indexer import index_document

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from pathlib import Path
from backend.rag import generate_rag_response
from backend.auth import (
    authenticate_user,
    create_access_token,
    verify_access_token
)
from backend.database import (
    initialize_database,
    save_search_history,
    get_connection
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI RBAC RAG Chatbot API",
    description="Role-Based Access Control RAG API",
    version="1.0.0"
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()


# ============================================================
# AUTHENTICATION
# ============================================================

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    user = verify_access_token(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return user


# ============================================================
# REQUEST MODELS
# ============================================================

class ChatRequest(BaseModel):
    question: str


class LoginRequest(BaseModel):
    username: str
    password: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "AI RBAC RAG Chatbot API is running"
    }


# ============================================================
# LOGIN
# ============================================================

@app.post("/login")
def login(request: LoginRequest):

    user = authenticate_user(
        request.username,
        request.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        user["username"],
        user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ============================================================
# CHAT
# ============================================================

@app.post("/chat")
def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):

    # Generate RAG response using authenticated user's role
    result = generate_rag_response(
        question=request.question,
        user_role=current_user["role"]
    )

    # Save search history
    save_search_history(
        username=current_user["username"],
        question=request.question,
        answer=result["answer"],
        sources=json.dumps(
            result.get("sources", [])
        )
    )

    return result


# ============================================================
# SEARCH HISTORY
# ============================================================

@app.get("/history")
def get_history(
    current_user: dict = Depends(get_current_user)
):

    username = current_user["username"]

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            question,
            answer,
            sources,
            created_at
        FROM search_history
        WHERE username = ?
        ORDER BY created_at DESC
        """,
        (username,)
    )

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:

        try:
            sources = json.loads(row["sources"])
        except (TypeError, json.JSONDecodeError):
            sources = []

        history.append(
            {
                "id": row["id"],
                "username": row["username"],
                "question": row["question"],
                "answer": row["answer"],
                "sources": sources,
                "created_at": row["created_at"]
            }
        )

    return {
        "history": history
    }

# =========================================================
# DOCUMENT UPLOAD
# =========================================================

UPLOAD_DIR = Path("data")

ALLOWED_DEPARTMENTS = {
    "finance",
    "marketing",
    "hr",
    "engineering",
    "general"
}

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt"
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    department: str = Form(...),
    current_user: dict = Depends(get_current_user)
):

    # 1. Validate department
    department = department.strip().lower()
        # =====================================================
    # UPLOAD AUTHORIZATION
    # =====================================================

    user_role = current_user["role"].lower()

    # Executive can upload to any department
    if user_role == "executive":
        pass

    # Other departments can upload only to their own department
    elif user_role == department:
        pass

    # Employees cannot upload documents
    else:
        raise HTTPException(
            status_code=403,
            detail=(
                f"Role '{user_role}' is not authorized "
                f"to upload documents to '{department}'."
            )
        )

    if department not in ALLOWED_DEPARTMENTS:
        raise HTTPException(
            status_code=400,
            detail="Invalid department"
        )

    # 2. Validate file
    filename = Path(
        file.filename or ""
    ).name

    extension = Path(
        filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed"
        )

    # 3. Read file and check size
    content = await file.read(
        MAX_FILE_SIZE + 1
    )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the 10 MB limit"
        )

    # 4. Create department folder
    department_dir = (
        UPLOAD_DIR / department
    )

    department_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # 5. Create unique filename
    import uuid

    stored_filename = (
        f"{uuid.uuid4().hex}_{filename}"
    )

    # 6. Create complete file path
    file_path = (
        department_dir / stored_filename
    )

    # 7. Save the document
    with open(
        file_path,
        "wb"
    ) as output:
        output.write(content)

    # =====================================================
    # AUTOMATIC INDEXING
    # =====================================================

    if extension in {".txt", ".pdf"}:

        try:

            indexing_result = index_document(
                file_path=str(file_path),
                department=department,
                source_name=filename
            )

        except Exception as e:

            # Remove file if indexing fails
            file_path.unlink(
                missing_ok=True
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    f"Document indexing failed: {str(e)}"
                )
            )

        return {
            "message": (
                "Document uploaded and "
                "indexed successfully"
            ),
            "filename": filename,
            "department": department,
            "status": "indexed",
            "chunks": indexing_result["chunks"]
        }

    # PDFs are saved but not indexed yet
    return {
        "message": "Document uploaded successfully",
        "filename": filename,
        "department": department,
        "status": "saved_not_indexed"
    }
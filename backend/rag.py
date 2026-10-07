import os

import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv

load_dotenv()


# Load models
embedding_model = None


def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return embedding_model

gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Connect to Chroma
chroma_client = chromadb.PersistentClient(
    path="vectorstore"
)

collection = chroma_client.get_collection(
    name="company_documents"
)


# RBAC permissions
ROLE_PERMISSIONS = {
    "finance": ["finance", "general"],
    "marketing": ["marketing", "general"],
    "hr": ["hr", "general"],
    "engineering": ["engineering", "general"],
    "executive": ["finance", "marketing", "hr", "engineering", "general"],
    "employee": ["general"],
}


def generate_rag_response(question: str, user_role: str):
    allowed_departments = ROLE_PERMISSIONS[user_role]

    question_embedding = get_embedding_model().encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=2,
        where={"department": {"$in": allowed_departments}}
    )

    # Combine retrieved chunks
    context = "\n\n".join(
        results["documents"][0]
    )

    # Get sources from metadata
    sources = set()

    for metadata in results["metadatas"][0]:
        sources.add(metadata["source"])

    # Create prompt
    prompt = f"""
You are a company assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context, respond with
exactly:

I do not have enough information to answer this question.

Do not make assumptions or use outside knowledge.

Context:
{context}

Question:
{question}
"""

    # Generate answer
    interaction = gemini_client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )
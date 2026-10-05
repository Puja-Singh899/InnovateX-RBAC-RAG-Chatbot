import requests
import streamlit as st
import json
import html


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="InnovateX AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# GLOBAL CSS
# =========================================================

st.html("""
<style>

.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

.ix-topbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 66px;
    display: flex;
    align-items: center;
    padding: 0 42px;
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    z-index: 9999;
}

.ix-brand {
    display: flex;
    align-items: center;
    gap: 11px;
}

.ix-symbol {
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #111827;
    color: white;
    border-radius: 9px;
    font-size: 18px;
    font-weight: 700;
}

.ix-brand-name {
    font-size: 18px;
    font-weight: 700;
    color: #111827;
}

.ix-brand-subtitle {
    font-size: 13px;
    color: #6b7280;
    margin-left: 6px;
}

.ix-login-heading {
    text-align: center;
    margin-top: 88px;
    margin-bottom: 18px;
}

.ix-login-heading h1 {
    margin: 0 0 6px 0;
    color: #111827;
    font-size: 31px;
    line-height: 1.2;
    font-weight: 700;
    letter-spacing: -0.8px;
}

.ix-login-heading p {
    margin: 0;
    color: #6b7280;
    font-size: 14px;
}

.ix-security {
    text-align: center;
    margin-top: 15px;
    color: #6b7280;
    font-size: 11px;
}

.ix-page-eyebrow {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.4px;
    color: #6b7280;
    margin-top: 20px;
    margin-bottom: 7px;
}

.ix-page-title {
    font-size: 30px;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.7px;
    margin-bottom: 5px;
}

.ix-page-subtitle {
    color: #6b7280;
    font-size: 14px;
    margin-bottom: 25px;
}

.ix-info-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
}

.ix-info-title {
    font-size: 16px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 7px;
}

.ix-info-text {
    color: #6b7280;
    font-size: 14px;
    line-height: 1.6;
}

.ix-sidebar-brand {
    font-size: 20px;
    font-weight: 750;
    color: #111827;
}

.ix-sidebar-subtitle {
    color: #6b7280;
    font-size: 12px;
    margin-top: 2px;
}

.ix-status {
    color: #6b7280;
    font-size: 12px;
    margin-top: 10px;
}

.ix-status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 6px;
}

</style>
""")


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "logged_in": False,
    "token": None,
    "username": None,
    "role": None,
    "page": "Chat",
    "chat_history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# CONFIGURATION
# =========================================================

API_URL = "http://127.0.0.1:8000"

ROLE_MAP = {
    "alice": "Finance",
    "bob": "Marketing",
    "carol": "HR",
    "david": "Engineering",
    "eve": "Executive",
    "john": "Employee"
}


# =========================================================
# FETCH PERSISTENT SEARCH HISTORY
# =========================================================

def fetch_search_history():

    try:

        response = requests.get(
            f"{API_URL}/history",
            headers={
                "Authorization": (
                    f"Bearer {st.session_state.token}"
                )
            },
            timeout=15
        )

        if response.status_code == 200:

            return response.json()

        elif response.status_code == 401:

            st.session_state.clear()

            st.warning(
                "Your session has expired. Please sign in again."
            )

            st.rerun()

        else:

            st.error(
                f"Failed to fetch history: "
                f"HTTP {response.status_code}"
            )

            return []

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to the InnovateX backend."
        )

        return []

    except requests.exceptions.Timeout:

        st.error(
            "Loading history timed out. Please try again."
        )

        return []

    except requests.exceptions.RequestException as e:

        st.error(f"Error fetching history: {e}")

        return []


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    st.html("""
    <div class="ix-topbar">
        <div class="ix-brand">
            <div class="ix-symbol">✦</div>
            <div>
                <span class="ix-brand-name">InnovateX</span>
                <span class="ix-brand-subtitle">
                    AI Enterprise Assistant
                </span>
            </div>
        </div>
    </div>
    """)

    st.html("""
    <div class="ix-login-heading">
        <h1>Welcome back</h1>
        <p>
            Sign in to your secure enterprise AI workspace
        </p>
    </div>
    """)

    left, center, right = st.columns([1, 1.05, 1])

    with center:

        with st.container(border=True):

            st.markdown("### Sign in")

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )

            login_clicked = st.button(
                "Sign in",
                type="primary",
                use_container_width=True
            )

            st.html("""
            <div class="ix-security">
                🔐 Secure authentication
                &nbsp; • &nbsp;
                Role-based access
                &nbsp; • &nbsp;
                Protected company data
            </div>
            """)

            if login_clicked:

                if not username.strip() or not password:

                    st.error(
                        "Please enter both username and password."
                    )

                else:

                    try:

                        response = requests.post(
                            f"{API_URL}/login",
                            json={
                                "username": username.strip(),
                                "password": password
                            },
                            timeout=10
                        )

                        if response.status_code == 200:

                            data = response.json()

                            st.session_state.logged_in = True

                            st.session_state.token = (
                                data["access_token"]
                            )

                            st.session_state.username = (
                                username.strip()
                            )

                            st.session_state.role = ROLE_MAP.get(
                                username.strip().lower(),
                                "Employee"
                            )

                            st.session_state.page = "Chat"

                            st.session_state.chat_history = []

                            st.rerun()

                        elif response.status_code == 401:

                            st.error(
                                "Invalid username or password."
                            )

                        else:

                            st.error(
                                f"Login failed: "
                                f"HTTP {response.status_code}"
                            )

                    except requests.exceptions.ConnectionError:

                        st.error(
                            "Unable to connect to backend. "
                            "Make sure FastAPI is running."
                        )

                    except requests.exceptions.RequestException as e:

                        st.error(f"Login request failed: {e}")

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.html("""
    <div class="ix-sidebar-brand">
        ✦ InnovateX
    </div>

    <div class="ix-sidebar-subtitle">
        AI Enterprise Workspace
    </div>
    """)

    st.write("")


    # -----------------------------------------------------
    # NEW CHAT
    # -----------------------------------------------------

    if st.button(
        "＋  New chat",
        use_container_width=True
    ):

        st.session_state.chat_history = []

        st.session_state.page = "Chat"

        st.rerun()


    # -----------------------------------------------------
    # RECENT SEARCHES
    # -----------------------------------------------------

    if st.button(
        "◷  Recent searches",
        use_container_width=True
    ):

        st.session_state.page = "Recent"

        st.rerun()


    # -----------------------------------------------------
    # SEARCH HISTORY
    # -----------------------------------------------------

    if st.button(
        "⌕  Search history",
        use_container_width=True
    ):

        st.session_state.page = "History"

        st.rerun()


    # -----------------------------------------------------
    # UPLOAD DOCUMENT
    # -----------------------------------------------------

    if st.button(
        "⬆  Upload document",
        use_container_width=True,
        key="upload_button"
    ):

        st.session_state.page = "Upload"

        st.rerun()


    # -----------------------------------------------------
    # ABOUT
    # -----------------------------------------------------

    if st.button(
        "ⓘ  About InnovateX",
        use_container_width=True
    ):

        st.session_state.page = "About"

        st.rerun()


    st.divider()


    # -----------------------------------------------------
    # USER
    # -----------------------------------------------------

    username = st.session_state.username or "User"

    role = st.session_state.role or "Employee"

    avatar = username[0].upper()

    safe_username = html.escape(username.title())

    safe_role = html.escape(role)

    st.html(f"""
<div style="
    padding:12px;
    border:1px solid #e5e7eb;
    border-radius:12px;
    background:#ffffff;
">

    <div style="
        display:flex;
        align-items:center;
        gap:10px;
    ">

        <div style="
            width:36px;
            height:36px;
            border-radius:50%;
            background:#111827;
            color:white;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:700;
        ">

            {avatar}

        </div>

        <div>

            <div style="
                font-weight:700;
                color:#111827;
                font-size:14px;
            ">

                {safe_username}

            </div>

            <div style="
                color:#6b7280;
                font-size:12px;
                margin-top:2px;
            ">

                {safe_role} workspace

            </div>

        </div>

    </div>

</div>
""")


    st.html("""
    <div class="ix-status">

        <span class="ix-status-dot"></span>

        Secure session active

    </div>
    """)


    st.write("")


    # -----------------------------------------------------
    # SIGN OUT
    # -----------------------------------------------------

    if st.button(
        "↪  Sign out",
        use_container_width=True
    ):

        st.session_state.clear()

        st.rerun()

# =========================================================
# CHAT PAGE
# =========================================================

if st.session_state.page == "Chat":

    safe_username = html.escape(
        st.session_state.username.title()
    )

    safe_role = html.escape(
        st.session_state.role
    )

    st.html("""
    <div class="ix-page-eyebrow">
        AI WORKSPACE
    </div>
    """)

    st.html(f"""
    <div class="ix-page-title">
        Good morning, {safe_username}.
    </div>

    <div class="ix-page-subtitle">
        Ask questions about the information available
        to your {safe_role} workspace.
    </div>
    """)
        # =========================================================
    # DEPARTMENT-WISE SUGGESTED QUESTIONS
    # =========================================================

    department_questions = {
        "finance": [
            "What was the company's Q2 revenue?",
            "What were the major expenses in Q2?",
            "How much was spent on equipment?",
            "What was the total reimbursement amount?"
        ],

        "marketing": [
            "Which campaign generated the most leads?",
            "What was the conversion rate of Campaign Alpha?",
            "What was the total marketing sales?",
            "What was the customer acquisition cost?"
        ],

        "hr": [
            "How many employees are currently in the company?",
            "What is the employee attendance rate?",
            "What is the total payroll?",
            "How many training programs were conducted?"
        ],

        "engineering": [
            "Which programming language is used for backend development?",
            "What is the software development workflow?",
            "How does the engineering team manage code reviews?",
            "What testing happens before deployment?"
        ],

        "executive": [
            "What was the company's Q2 revenue?",
            "Which campaign generated the most leads?",
            "How many employees are currently in the company?",
            "What is the engineering development workflow?"
        ],

        "employee": [
            "What are the company's working hours?",
            "How can employees apply for leave?",
            "How are company town halls conducted?",
            "Who should employees contact for IT support?"
        ]
    }

    user_role = st.session_state.role.lower()

    st.markdown("### ✨ Suggested Questions")
    st.caption("Choose a question to explore your department's knowledge.")

    suggestions = department_questions.get(
        user_role,
        department_questions["employee"]
    )

    for question in suggestions:
        if st.button(
            f"💡 {question}",
            key=f"suggestion_{question}"
        ):
            st.session_state.question_input = question
            st.rerun()

    question = st.text_area(
        "Ask InnovateX",
        placeholder=(
            "Ask something like: "
            "How much was spent on equipment in Q2 2026?"
        ),
        height=110,
        label_visibility="collapsed",
        key="question_input"
    )

    if st.button(
        "Ask InnovateX  →",
        type="primary",
        key="ask_button"
    ):

        if not question.strip():

            st.warning("Enter a question first.")

        else:

            try:

                with st.spinner(
                    "Searching your authorized knowledge..."
                ):

                    response = requests.post(
                        f"{API_URL}/chat",
                        headers={
                            "Authorization": (
                                f"Bearer {st.session_state.token}"
                            )
                        },
                        json={
                            "question": question.strip()
                        },
                        timeout=90
                    )

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No answer was returned."
                    )

                    sources = data.get("sources", [])

                    st.session_state.chat_history.append({
                        "question": question.strip(),
                        "answer": answer,
                        "sources": sources
                    })

                    st.markdown("### ✦ InnovateX AI")

                    st.markdown(answer)

                    if sources:

                        st.markdown("**Sources**")

                        for source in sources:

                            st.markdown(f"📄 `{source}`")

                elif response.status_code == 401:

                    st.session_state.clear()

                    st.warning(
                        "Your session has expired. "
                        "Please sign in again."
                    )

                    st.rerun()

                else:

                    st.error(
                        f"Backend returned "
                        f"HTTP {response.status_code}"
                    )

                    st.code(response.text)

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to the InnovateX backend."
                )

                st.code(
                    "uvicorn backend.main:app --reload"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. "
                    "The AI backend took too long to respond."
                )

            except requests.exceptions.RequestException as e:

                st.error(f"Request failed: {e}")

    # Display current session conversation

    if st.session_state.chat_history:

        st.markdown("---")

        st.markdown("### Conversation")

        for chat in st.session_state.chat_history:

            st.markdown(
                f"**You:** {chat['question']}"
            )

            st.markdown(
                f"**✦ InnovateX AI:** {chat['answer']}"
            )

            if chat["sources"]:

                st.markdown("**Sources:**")

                for source in chat["sources"]:

                    st.markdown(f"📄 `{source}`")

            st.markdown("---")


# =========================================================
# RECENT SEARCHES
# =========================================================

elif st.session_state.page == "Recent":

    st.html("""
    <div class="ix-page-eyebrow">
        ACTIVITY
    </div>

    <div class="ix-page-title">
        Recent searches
    </div>

    <div class="ix-page-subtitle">
        Your latest questions in this session.
    </div>
    """)

    if not st.session_state.chat_history:

        st.info("No recent searches yet.")

    else:

        for chat in reversed(
            st.session_state.chat_history[-10:]
        ):

            with st.container(border=True):

                st.markdown(
                    f"### 🔎 {chat['question']}"
                )

                st.write(chat["answer"])


# =========================================================
# SEARCH HISTORY - PERSISTENT SQLITE
# =========================================================

elif st.session_state.page == "History":

    st.title("Search History")
    st.caption("Your previously asked questions and AI responses.")

    history_items = fetch_search_history()

    # Handle unexpected response formats
    if isinstance(history_items, str):
        try:
            history_items = json.loads(history_items)
        except json.JSONDecodeError:
            st.error("Unable to read search history.")
            st.stop()

    if isinstance(history_items, dict):
        history_items = history_items.get("history", [])

    if not isinstance(history_items, list):
        st.error("Unexpected history response format.")
        st.stop()

    if not history_items:
        st.info("No search history found.")
    else:
        for number, item in enumerate(history_items, start=1):

            # Skip records that are not dictionaries
            if isinstance(item, str):
                try:
                    item = json.loads(item)
                except json.JSONDecodeError:
                    st.warning(f"Invalid history record {number}.")
                    continue

            if not isinstance(item, dict):
                continue

            question = item.get("question", "No question available")
            answer = item.get("answer", "No answer available")
            sources = item.get("sources", [])
            created_at = item.get("created_at", "Date unavailable")

            # Convert sources into a list if needed
            if isinstance(sources, str):
                try:
                    sources = json.loads(sources)
                except json.JSONDecodeError:
                    sources = [sources] if sources else []

            with st.container(border=True):

                st.caption(
                    f"SEARCH {number}  •  {created_at}"
                )

                st.markdown(f"**You:** {question}")

                st.markdown(
                    f"**✦ InnovateX AI:** {answer}"
                )

                if sources:
                    st.markdown("**Sources**")

                    for source in sources:
                        st.caption(f"📄 {source}")

# =========================================================
# DOCUMENT UPLOAD
# =========================================================

elif st.session_state.page == "Upload":

    st.html("""
    <div class="ix-page-eyebrow">
        DOCUMENTS
    </div>

    <div class="ix-page-title">
        Upload Document
    </div>

    <div class="ix-page-subtitle">
        Add a PDF or TXT document to the company knowledge base.
    </div>
    """)

    user_role = st.session_state.role.lower()

    allowed_departments = {
        "finance": ["finance"],
        "marketing": ["marketing"],
        "hr": ["hr"],
        "engineering": ["engineering"],
        "executive": [
            "finance",
            "marketing",
            "hr",
            "engineering",
            "general"
        ]
    }

    departments = allowed_departments.get(
        user_role,
        []
    )

    if not departments:

        st.warning(
            "Your role is not authorized to upload documents."
        )

    else:

        department = st.selectbox(
            "Select Department",
            departments
        )

        uploaded_file = st.file_uploader(
            "Choose a PDF or TXT file",
            type=["pdf", "txt"]
        )

        if uploaded_file is not None:

            st.info(
                f"Selected file: {uploaded_file.name}"
            )

            if st.button(
                "⬆️ Upload & Index Document",
                type="primary",
                use_container_width=True
            ):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                data = {
                    "department": department
                }

                headers = {
                    "Authorization": (
                        f"Bearer {st.session_state.token}"
                    )
                }

                try:

                    response = requests.post(
                        f"{API_URL}/upload",
                        files=files,
                        data=data,
                        headers=headers,
                        timeout=120
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.success(
                            "Document uploaded and indexed successfully!"
                        )

                        st.write(
                            f"**File:** {result['filename']}"
                        )

                        st.write(
                            f"**Department:** {result['department']}"
                        )

                        st.write(
                            f"**Chunks created:** {result['chunks']}"
                        )

                    else:

                        try:
                            error = response.json().get(
                                "detail",
                                "Upload failed"
                            )
                        except Exception:
                            error = response.text

                        st.error(
                            f"Upload failed: {error}"
                        )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Could not connect to backend: {e}"
                    )

# =========================================================
# ABOUT PAGE
# =========================================================

elif st.session_state.page == "About":

    st.html("""
    <div class="ix-page-eyebrow">
        PRODUCT
    </div>

    <div class="ix-page-title">
        About InnovateX AI
    </div>

    <div class="ix-page-subtitle">
        A secure enterprise Retrieval-Augmented Generation assistant.
    </div>
    """)


    st.html("""
    <div class="ix-info-card">

        <div class="ix-info-title">
            ✦ What is InnovateX AI?
        </div>

        <div class="ix-info-text">
            InnovateX AI combines Retrieval-Augmented Generation
            with Role-Based Access Control to provide users with
            answers based only on company information they are
            authorized to access.
        </div>

    </div>
    """)


    col1, col2 = st.columns(2)


    with col1:

        st.html("""
        <div class="ix-info-card">

            <div class="ix-info-title">
                🧠 AI Stack
            </div>

            <div class="ix-info-text">
                Gemini<br>
                ChromaDB<br>
                Sentence Transformers<br>
                Retrieval-Augmented Generation
            </div>

        </div>
        """)


    with col2:

        st.html("""
        <div class="ix-info-card">

            <div class="ix-info-title">
                🔐 Security
            </div>

            <div class="ix-info-text">
                JWT authentication<br>
                Argon2 password hashing<br>
                Role-Based Access Control<br>
                Permission-aware retrieval
            </div>

        </div>
        """)


    st.html("""
    <div class="ix-info-card">

        <div class="ix-info-title">
            ⚙️ Technology
        </div>

        <div class="ix-info-text">
            Streamlit • FastAPI • Python • ChromaDB • Gemini
        </div>

    </div>
    """)
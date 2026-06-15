import streamlit as st
from PIL import Image
from utils.gemini_helper import get_response
from pypdf import PdfReader
import base64

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Smart Career Guidance Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ---------------- LOAD LOGO ---------------- #

logo = Image.open("assets/logo.png")

# ---------------- BACKGROUND FUNCTION ---------------- #

def add_bg_from_local(image_file):

    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>

        /* Background */

        .stApp {{
            background-image:
            linear-gradient(
                rgba(0,0,0,0.85),
                rgba(0,0,0,0.85)
            ),
            url("data:image/png;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Sidebar */

        section[data-testid="stSidebar"] {{
            background: rgba(15,15,15,0.93);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255,255,255,0.08);
        }}

        /* Hero Title */

        .hero-title {{
            font-size: 62px;
            font-weight: 800;
            color: white;
            text-align: center;
            margin-top: 60px;
            line-height: 1.2;
        }}

        /* Hero Subtitle */

        .hero-subtitle {{
            color: #d1d5db;
            font-size: 22px;
            text-align: center;
            margin-top: 15px;
            margin-bottom: 40px;
        }}

        /* Sidebar Cards */

        .feature-box {{
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 16px;
            border-radius: 14px;
            margin-bottom: 12px;
            color: white;
            font-size: 16px;
            font-weight: 500;
        }}

        /* Chat Input */

        [data-testid="stChatInput"] {{
            border-radius: 18px;
            border: 1px solid #7c3aed;
            background-color: rgba(255,255,255,0.05);
        }}

        /* File Uploader */

        [data-testid="stFileUploader"] {{
            width: 150px;
            margin-top: 5px;
        }}

        [data-testid="stFileUploader"] section {{
            padding: 0px !important;
            border: none !important;
            background: transparent !important;
        }}

        [data-testid="stFileUploaderDropzone"] {{
            min-height: 50px !important;
            padding: 5px !important;
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 12px !important;
        }}

        [data-testid="stFileUploaderDropzoneInstructions"] {{
            color: black !important;
            font-weight: 600;
        }}

        /* Chat Messages */

        [data-testid="stChatMessage"] {{
            background: rgba(255,255,255,0.06);
            border-radius: 14px;
            padding: 14px;
            margin-bottom: 14px;
            border: 1px solid rgba(255,255,255,0.08);
        }}

        /* White Text */

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] div,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] div,
        .stMarkdown {{
            color: white !important;
        }}

        /* Code */

        code {{
            color: #00ffcc !important;
            background-color: rgba(255,255,255,0.08) !important;
        }}

        pre {{
            background-color: rgba(255,255,255,0.05) !important;
            border-radius: 10px;
        }}

        /* Button */

        .stButton>button {{
            width: 100%;
            border-radius: 14px;
            background: linear-gradient(to right, #6366f1, #8b5cf6);
            color: white;
            border: none;
            padding: 12px;
            font-weight: 600;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- ADD BACKGROUND ---------------- #

add_bg_from_local("assets/background.jpg")

# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.image(logo, width=180)

    st.markdown("""
    <h2 style="
    color:white;
    margin-top:15px;
    margin-bottom:18px;">
    💡 What You Can Ask
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box">
    How can I become a Data Scientist?
    </div>

    <div class="feature-box">
    Create a roadmap for AI Engineer
    </div>

    <div class="feature-box">
    Suggest skills for Full Stack Developer
    </div>

    <div class="feature-box">
    Generate Python interview questions
    </div>

    <div class="feature-box">
    Review my resume for software jobs
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []

        st.rerun()

# ---------------- HERO SECTION ---------------- #

st.markdown("""
<div class="hero-title">
Smart Career<br>
Guidance Chatbot
</div>

<div class="hero-subtitle">
AI-powered assistant for career planning,
resume reviews, interview preparation,
and personalized learning roadmaps.
</div>
""", unsafe_allow_html=True)

# ---------------- UPLOAD SECTION ---------------- #

col1, col2 = st.columns([5, 1])

with col2:

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

# ---------------- RESUME EXTRACTION ---------------- #

resume_text = ""

if uploaded_file is not None:

    pdf_reader = PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        text = page.extract_text()

        if text:
            resume_text += text

    st.toast("✅ Resume uploaded successfully!")

# ---------------- DISPLAY CHAT ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------- CHAT INPUT ---------------- #

user_input = st.chat_input(
    "Ask about careers, AI, jobs, skills, interview preparation..."
)

# ---------------- RESPONSE ---------------- #

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):

        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            if resume_text:

                full_prompt = f"""
                Resume Content:
                {resume_text}

                User Question:
                {user_input}
                """

                response = get_response(full_prompt)

            else:

                response = get_response(user_input)

            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
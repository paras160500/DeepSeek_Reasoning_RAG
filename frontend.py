import streamlit as st
from rag_pipeline import answer_query, llm_model
from vector_database import load_pdf, upload_pdf, make_chunk_embeddings_store_vectordb
import re

st.set_page_config(page_title="LexAI - AI Lawyer", page_icon="⚖️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0c0c0f !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #0c0c0f !important;
}

[data-testid="stToolbar"], [data-testid="stDecoration"], footer, #MainMenu {
    display: none !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: 780px !important;
    padding: 0 2rem 4rem !important;
}

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 0 18px;
    border-bottom: 1px solid #1e1e2a;
    margin-bottom: 0;
}
.logo {
    display: flex;
    align-items: center;
    gap: 10px;
}
.logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #c9a84c, #f0d080);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.logo-name {
    font-family: 'Playfair Display', serif;
    font-size: 17px;
    color: #e8d5a3;
    letter-spacing: .02em;
}
.status-pill {
    display: flex; align-items: center; gap: 6px;
    background: #0f1f14;
    border: 1px solid #1a3a22;
    border-radius: 99px;
    padding: 5px 12px;
    font-size: 11px;
    color: #4ade80;
    font-weight: 500;
}
.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 6px #22c55e88;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 52px 16px 40px;
}
.hero-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .22em;
    text-transform: uppercase;
    color: #c9a84c;
    margin-bottom: 16px;
}
.hero-h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.9rem;
    font-weight: 700;
    color: #f5f0e8;
    line-height: 1.12;
    margin-bottom: 14px;
}
.hero-h1 em {
    font-style: italic;
    background: linear-gradient(90deg, #c9a84c, #f0d080, #c9a84c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: .92rem;
    color: #6b7280;
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Section label ── */
.sec-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #c9a84c88;
    margin-bottom: 8px;
    margin-top: 24px;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #111118 !important;
    border: 1.5px dashed #2a2a3a !important;
    border-radius: 16px !important;
    padding: 8px !important;
    transition: border-color .2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #c9a84c55 !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] p,
[data-testid="stFileUploaderDropzone"] span {
    color: #4b5563 !important;
    font-size: .85rem !important;
}

/* ── Textarea ── */
[data-testid="stTextArea"] textarea {
    background: #111118 !important;
    border: 1.5px solid #1e1e2a !important;
    border-radius: 14px !important;
    color: #e8e0d0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .92rem !important;
    padding: 14px 18px !important;
    caret-color: #c9a84c !important;
    transition: border-color .2s !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #c9a84c66 !important;
    box-shadow: 0 0 0 3px #c9a84c18 !important;
}
[data-testid="stTextArea"] textarea::placeholder {
    color: #3a3a4a !important;
}
[data-testid="stTextArea"] label {
    color: #4b5563 !important;
    font-size: .82rem !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #c9a84c 0%, #f0d080 50%, #c9a84c 100%) !important;
    background-size: 200% !important;
    color: #0c0c0f !important;
    border: none !important;
    border-radius: 13px !important;
    padding: 15px 2rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .98rem !important;
    font-weight: 700 !important;
    letter-spacing: .04em !important;
    cursor: pointer !important;
    transition: background-position .3s, transform .15s !important;
    box-shadow: 0 4px 20px #c9a84c33 !important;
}
[data-testid="stButton"] > button:hover {
    background-position: 100% !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px #c9a84c44 !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #111118 !important;
    border: 1px solid #1e1e2a !important;
    border-radius: 16px !important;
    padding: 14px 18px !important;
    margin-bottom: 10px !important;
}
[data-testid="stChatMessage"] p {
    color: #c9c2b0 !important;
    font-size: .9rem !important;
}

/* ── Thinking block ── */
.think-block {
    background: #0f0f18;
    border-left: 2px solid #c9a84c44;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin-bottom: 12px;
    font-size: .82rem;
    color: #4b5563;
    line-height: 1.65;
}
.think-lbl {
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #c9a84c66;
    margin-bottom: 8px;
}

/* ── Answer block ── */
.ans-block {
    background: #111118;
    border: 1px solid #1e1e2a;
    border-radius: 12px;
    padding: 16px 20px;
    font-size: .9rem;
    color: #d4cbbf;
    line-height: 1.75;
}
.ans-lbl {
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #4ade80;
    margin-bottom: 8px;
}

/* ── Divider ── */
.gold-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 28px 0 20px;
}
.gold-line { flex: 1; height: 1px; background: #1e1e2a; }
.gold-txt {
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .16em;
    text-transform: uppercase;
    color: #3a3a4a;
}

/* ── Feature row ── */
.feat-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-top: 32px;
}
.feat-card {
    background: #111118;
    border: 1px solid #1e1e2a;
    border-radius: 13px;
    padding: 16px 14px;
    text-align: center;
}
.feat-icon { font-size: 22px; margin-bottom: 7px; }
.feat-title {
    font-size: .76rem;
    font-weight: 600;
    color: #c9a84c;
    margin-bottom: 4px;
    letter-spacing: .02em;
}
.feat-sub { font-size: .7rem; color: #4b5563; line-height: 1.45; }

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: #160e0e !important;
    border: 1px solid #3a1a1a !important;
    border-radius: 12px !important;
    color: #f87171 !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] > div {
    border-top-color: #c9a84c !important;
}
</style>
""", unsafe_allow_html=True)


# ── Top bar ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="logo">
    <div class="logo-icon">⚖</div>
    <span class="logo-name">LexAI</span>
  </div>
  <div class="status-pill">
    <div class="status-dot"></div>
    AI Online
  </div>
</div>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">AI-Powered Legal Assistant</div>
  <h1 class="hero-h1">Your <em>Legal Documents</em>,<br>Instantly Understood</h1>
  <p class="hero-sub">Upload any contract, agreement or legal file. Get precise, intelligent answers in seconds.</p>
</div>
""", unsafe_allow_html=True)

# ── Upload ────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-label">Step 1 — Upload your document</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf",
    accept_multiple_files=False,
    label_visibility="collapsed",
)

# ── Query ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-label">Step 2 — Ask your question</div>', unsafe_allow_html=True)
user_query = st.text_area(
    "Your question",
    height=110,
    placeholder="e.g. What are the termination clauses and notice period required?",
    label_visibility="collapsed",
)

ask_question = st.button("⚖  Consult AI Lawyer")

# ── Feature cards ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="feat-row">
  <div class="feat-card">
    <div class="feat-icon">🔒</div>
    <div class="feat-title">Private & Secure</div>
    <div class="feat-sub">Your docs never leave your session</div>
  </div>
  <div class="feat-card">
    <div class="feat-icon">⚡</div>
    <div class="feat-title">Instant Analysis</div>
    <div class="feat-sub">Answers in under 3 seconds</div>
  </div>
  <div class="feat-card">
    <div class="feat-icon">📋</div>
    <div class="feat-title">Cites Sources</div>
    <div class="feat-sub">References exact clauses</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Logic ─────────────────────────────────────────────────────────────────────
if ask_question:
    if not uploaded_file:
        st.error("⚠️  Please upload a PDF document before asking a question.")
    elif not user_query.strip():
        st.error("⚠️  Please enter a question.")
    else:
        with st.spinner("Analysing your document…"):
            file_path = upload_pdf(uploaded_file)
            documents = load_pdf(file_path)
            faiss_obj = make_chunk_embeddings_store_vectordb(documents)

        st.markdown("""
        <div class="gold-divider">
          <div class="gold-line"></div>
          <span class="gold-txt">Response</span>
          <div class="gold-line"></div>
        </div>
        """, unsafe_allow_html=True)

        st.chat_message("user").write(user_query)

        with st.spinner("AI Lawyer is thinking…"):
            response = answer_query(llm_model, query=user_query, faiss_db=faiss_obj)

        raw_text = response.content
        reasoning_match = re.search(r"<think>(.*?)</think>", raw_text, flags=re.DOTALL)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else None
        answer = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL).strip()

        with st.chat_message("assistant"):
            if reasoning:
                st.markdown(f"""
                <div class="think-block">
                  <div class="think-lbl">💭 Reasoning</div>
                  {reasoning}
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="ans-block">
              <div class="ans-lbl">✅ Answer</div>
              {answer}
            </div>
            """, unsafe_allow_html=True)
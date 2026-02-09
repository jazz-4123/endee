import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Endee Knowledge Retrieval Framework",
    layout="wide"
)

# ---------------- Custom CSS ----------------
st.markdown(
    """
    <style>
    /* App background */
    body, .main {
        background-color: #0e1117;
        color: #dcdcdc;
    }

    /* Headings */
    h1, h2, h3 {
        color: #eaeaea;
        font-family: "Georgia", serif;
        font-weight: 600;
    }

    /* Remove default Streamlit block backgrounds */
    div[data-testid="stVerticalBlock"] > div {
        background: transparent !important;
    }

    div[data-testid="stFileUploader"],
    div[data-testid="stTextArea"],
    div[data-testid="stTextInput"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    /* Inputs */
    textarea, input {
        background-color: #0e1117 !important;
        color: #e6e6e6 !important;
        border: 1px solid #2f4f4f !important;
        border-radius: 6px !important;
        padding: 0.6rem !important;
        box-shadow: none !important;
    }

    textarea::placeholder {
        color: #8b949e;
    }

    /* File uploader cleanup */
    section[data-testid="stFileUploader"] > div {
        background-color: transparent !important;
        border: 1px dashed #2f4f4f !important;
        border-radius: 8px;
        padding: 1rem;
    }

    /* Buttons */
    .stButton > button {
        background-color: #2f4f4f;
        color: #ffffff;
        border-radius: 6px;
        border: none;
        padding: 0.45rem 1.3rem;
        font-weight: 500;
    }

    .stButton > button:hover {
        background-color: #3c6e6e;
    }

    /* Success message */
    div[data-testid="stAlert"] {
        background-color: #0f3d2e !important;
        border-left: 4px solid #2ecc71;
        color: #eafff5;
    }

    /* Confidence colors */
    .confidence-high { color: #4caf50; font-weight: 600; }
    .confidence-medium { color: #ffb74d; font-weight: 600; }
    .confidence-low { color: #ef5350; font-weight: 600; }

    /* Remove shadows */
    * {
        box-shadow: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Header ----------------
st.markdown("<h1>Endee Knowledge Retrieval Framework</h1>", unsafe_allow_html=True)
st.markdown(
    "<p>An academic semantic search system for document exploration with evidence and confidence.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- Sidebar ----------------
st.sidebar.markdown("### Retrieval Settings")

top_k = st.sidebar.slider(
    "Number of Evidence Chunks",
    min_value=1,
    max_value=5,
    value=3
)

threshold = st.sidebar.slider(
    "Similarity Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.3
)

st.sidebar.markdown(
    "<small>Higher thresholds improve precision but may reduce recall.</small>",
    unsafe_allow_html=True
)

# ---------------- Document Ingestion ----------------
st.markdown("## Document Ingestion")

with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload a PDF document for semantic indexing",
        type=["pdf"]
    )

    if uploaded_file:
        with st.spinner("Processing and indexing document..."):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{API_URL}/ingest", files=files)

        if response.status_code == 200:
            st.success("Document successfully ingested and indexed.")
        else:
            st.error("Failed to ingest document.")

    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ---------------- Research Query ----------------
st.markdown("## Research Query")

with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    question = st.text_area(
        "Enter a research question",
        height=90,
        placeholder="e.g. What is Endee and how is it used in semantic search?"
    )

    search_clicked = st.button("Run Semantic Retrieval")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Results ----------------
if search_clicked and question:
    payload = {"question": question}

    with st.spinner("Performing semantic retrieval..."):
        response = requests.post(f"{API_URL}/ask", json=payload)

    if response.status_code == 200:
        data = response.json()

        # -------- Answer --------
        st.markdown("## Answer Summary")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write(data["answer"])
        st.markdown("</div>", unsafe_allow_html=True)

        # -------- Evidence --------
        st.markdown("## Supporting Evidence")

        if data["evidence"]:
            for idx, ev in enumerate(data["evidence"], 1):
                confidence = ev.get("confidence", "Low")

                confidence_class = {
                    "High": "confidence-high",
                    "Medium": "confidence-medium",
                    "Low": "confidence-low"
                }.get(confidence, "confidence-low")

                with st.expander(f"Evidence {idx}"):
                    st.markdown(
                        f"<span class='{confidence_class}'>Confidence: {confidence}</span>",
                        unsafe_allow_html=True
                    )
                    st.write(ev["text"])
                    st.caption(f"Similarity score: {round(ev['score'], 3)}")
        else:
            st.warning("No sufficiently relevant evidence found.")

    else:
        st.error("Backend error occurred while processing the query.")

# ---------------- Footer ----------------
st.divider()
st.markdown(
    "<p style='text-align:center; color:#777; font-size:13px;'>"
    "Endee-powered Semantic Retrieval System • Academic Prototype"
    "</p>",
    unsafe_allow_html=True
)


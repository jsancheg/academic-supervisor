import streamlit as st

st.set_page_config(page_title="Academic Supervisor", layout="wide")
st.title("Academic Supervisor")
st.caption("Strict, local academic writing review — grammar, clarity, coherence, citations, structure.")

uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])

if uploaded_file is not None:
    st.success(f"Received: {uploaded_file.name} ({uploaded_file.size} bytes)")
    if uploaded_file.type == "text/plain":
        st.text_area("Preview", uploaded_file.read().decode("utf-8"), height=300)
    else:
        st.info("PDF received. Parsing pipeline not wired up yet (see issue #7/#8).")

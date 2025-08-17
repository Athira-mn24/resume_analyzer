import streamlit as st
import PyPDF2

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def analyze_resume(resume_text, job_desc):
    score = 0
    for word in job_desc.split():
        if word.lower() in resume_text.lower():
            score += 1
    return score

st.title("AI Resume Analyzer")

uploaded_resume = st.file_uploader("Upload your resume (PDF)", type="pdf")
job_description = st.text_area("Paste the Job Description")

if uploaded_resume is not None and job_description.strip():
    st.write("Analyzing your resume...")
    resume_text = extract_text_from_pdf(uploaded_resume)
    match_score = analyze_resume(resume_text, job_description)
    st.subheader("Results")
    st.write(f"Your resume matches **{match_score} keywords** from the job description!")
    st.download_button("Download Extracted Resume Text", resume_text)
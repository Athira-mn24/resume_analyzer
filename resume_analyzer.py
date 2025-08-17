import PyPDF2
import pandas as pd
import re

# ---------- STEP 1: FUNCTION TO EXTRACT TEXT FROM PDF ----------
def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

# ---------- STEP 2: FUNCTION TO CLEAN AND GET KEYWORDS ----------
def get_keywords(text):
    # Convert to lowercase, remove non-letters, split words
    words = re.findall(r"[a-zA-Z]+", text.lower())
    # Remove very short words
    words = [w for w in words if len(w) > 2]
    return set(words)

# ---------- STEP 3: INPUT RESUME + JOB DESCRIPTION ----------
resume_path = input("Enter your resume PDF file name (with .pdf): ")
job_desc = input("Paste the job description here: ")

# Extract text from resume PDF
resume_text = extract_text_from_pdf(resume_path)

# Get keywords
resume_keywords = get_keywords(resume_text)
job_keywords = get_keywords(job_desc)

# ---------- STEP 4: FIND MATCH + MISSING KEYWORDS ----------
matched_keywords = resume_keywords.intersection(job_keywords)
missing_keywords = job_keywords.difference(resume_keywords)

match_score = (len(matched_keywords) / len(job_keywords)) * 100 if len(job_keywords) > 0 else 0

# ---------- STEP 5: PRINT RESULTS ----------
print("\n===== SMART RESUME ANALYZER =====")
print(f"Total keywords in Job Description: {len(job_keywords)}")
print(f"Keywords matched in Resume: {len(matched_keywords)}")
print(f"Match Score: {match_score:.2f}%")

print("\nMatched Keywords:")
print(", ".join(matched_keywords) if matched_keywords else "None")

print("\nMissing Keywords (Add these to improve your resume):")
print(", ".join(missing_keywords) if missing_keywords else "None")

# ---------- STEP 6: SAVE RESULTS TO EXCEL ----------
df = pd.DataFrame({
    "Matched Keywords": list(matched_keywords) + [""] * (len(missing_keywords) - len(matched_keywords)) if len(matched_keywords) < len(missing_keywords) else list(matched_keywords),
    "Missing Keywords": list(missing_keywords) + [""] * (len(matched_keywords) - len(missing_keywords)) if len(missing_keywords) < len(matched_keywords) else list(missing_keywords)
})
df.to_excel("resume_analysis.xlsx", index=False)
print("\nResults saved to 'resume_analysis.xlsx'")

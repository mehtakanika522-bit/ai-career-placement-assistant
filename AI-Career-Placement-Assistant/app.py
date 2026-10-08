import streamlit as st
import re
from pathlib import Path

st.set_page_config(page_title="AI Career & Placement Assistant", page_icon="🎯", layout="wide")

st.title("🎯 AI Career & Placement Assistant")
st.caption("Resume analysis • Job matching • Skill-gap detection • Interview preparation")

SKILLS = {
    "python","java","c++","sql","excel","tableau","power bi","pandas","numpy",
    "scikit-learn","machine learning","deep learning","nlp","tensorflow","pytorch",
    "streamlit","git","github","aws","azure","docker","html","css","javascript",
    "react","data analysis","statistics","data visualization","communication"
}

def extract_text_from_pdf(uploaded_file):
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        st.error(f"Could not read PDF: {e}")
        return ""

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILLS:
        if re.search(r"(?<!\w)" + re.escape(skill) + r"(?!\w)", text):
            found.append(skill)
    return sorted(found)

def match_score(resume_skills, job_skills):
    if not job_skills:
        return 0
    return round(len(set(resume_skills) & set(job_skills)) / len(set(job_skills)) * 100)

tab1, tab2, tab3 = st.tabs(["📄 Resume Analyzer", "🎯 Job Match", "💬 Interview Prep"])

with tab1:
    st.subheader("Upload your resume")
    resume = st.file_uploader("Upload PDF", type=["pdf"], key="resume")
    if resume:
        text = extract_text_from_pdf(resume)
        skills = extract_skills(text)
        st.success("Resume processed successfully!")
        c1, c2 = st.columns(2)
        c1.metric("Skills Detected", len(skills))
        c2.metric("Resume Text", f"{len(text)} chars")
        st.write("### Detected Skills")
        st.write(", ".join(skills) if skills else "No predefined skills detected.")
        st.info("Tip: Keep your resume's Skills section clear and keyword-rich for ATS systems.")

with tab2:
    st.subheader("Check your job match")
    resume2 = st.file_uploader("Upload resume PDF", type=["pdf"], key="resume2")
    jd = st.text_area("Paste Job Description", height=220, placeholder="Paste the complete job description here...")
    if st.button("Analyze Match"):
        if not resume2 or not jd.strip():
            st.warning("Please upload a resume and paste a job description.")
        else:
            resume_text = extract_text_from_pdf(resume2)
            rs = extract_skills(resume_text)
            js = extract_skills(jd)
            score = match_score(rs, js)
            matched = sorted(set(rs) & set(js))
            missing = sorted(set(js) - set(rs))
            st.metric("Job Match Score", f"{score}%")
            st.progress(score / 100)
            a, b = st.columns(2)
            with a:
                st.write("### ✅ Matched Skills")
                st.write(", ".join(matched) if matched else "None detected")
            with b:
                st.write("### ⚠️ Skills to Improve")
                st.write(", ".join(missing) if missing else "No major skill gaps detected")

with tab3:
    st.subheader("Interview Question Generator")
    role = st.text_input("Target role", placeholder="e.g. Data Analyst")
    level = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
    if st.button("Generate Questions"):
        if not role.strip():
            st.warning("Enter a target role first.")
        else:
            banks = {
                "Beginner": [
                    f"Tell me about yourself and why you want to become a {role}.",
                    f"What are the most important skills for a {role}?",
                    "Explain one project you have worked on and your contribution.",
                    "How do you handle a problem when you do not know the answer?",
                    "What is one technical skill you are currently improving?"
                ],
                "Intermediate": [
                    f"Walk me through a challenging {role} project and how you solved it.",
                    "How would you validate the quality of a dataset?",
                    "Describe a time your analysis changed a decision.",
                    "How would you explain a technical result to a non-technical stakeholder?",
                    "What trade-offs do you consider when selecting a model or tool?"
                ],
                "Advanced": [
                    f"Design an end-to-end system for a real-world {role} problem.",
                    "How would you measure whether an ML/analytics solution creates business value?",
                    "How would you handle data drift and changing business requirements?",
                    "Discuss a technical trade-off you would make under limited compute or time.",
                    "How would you improve reliability and monitoring in production?"
                ]
            }
            for i, q in enumerate(banks[level], 1):
                st.write(f"**{i}. {q}**")

st.divider()
st.caption("Built with Python + Streamlit • Portfolio project")

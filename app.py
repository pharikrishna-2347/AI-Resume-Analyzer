import streamlit as st
import google.generativeai as genai
import fitz
import requests
from bs4 import BeautifulSoup
import json
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
ADZUNA_APP_ID = st.secrets["ADZUNA_APP_ID"]
ADZUNA_APP_KEY = st.secrets["ADZUNA_APP_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# ===============================
# PDF EXTRACTION
# ===============================

def extract_resume_text(pdf_file):

    text = ""

    pdf_bytes = pdf_file.read()

    with fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as doc:

        for page in doc:
            text += page.get_text()

    return text

def get_best_job_titles(resume_text):

    prompt = f"""
Analyze this resume.

Return ONLY JSON:

{{
  "roles": [
    "Frontend Developer",
    "Software Developer",
    "Python Developer",
    "Data Analyst",
    "Competitive Programmer"
  ]
}}

Resume:
{resume_text[:6000]}
"""

    try:

        response = model.generate_content(prompt)

        clean = response.text.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        )

        data = json.loads(clean)

        return data["roles"]

    except:

        return [
            "Software Developer",
            "Frontend Developer",
            "Python Developer"
        ]
# ===============================
# JD URL EXTRACTION
# ===============================

def get_jd_from_url(url):

    try:

        response = requests.get(
            url,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        return soup.get_text(
            separator=" ",
            strip=True
        )

    except Exception as e:

        return f"Error: {e}"


# ===============================
# ATS ANALYSIS
# ===============================

def analyze_resume(jd_text, resume_text):

    prompt = f"""
You are an expert ATS and recruiter.

JOB DESCRIPTION:
{jd_text[:4000]}

RESUME:
{resume_text[:8000]}

Provide:

# ATS Match Score
# Executive Summary
# Matching Skills
# Missing Skills
# Strengths
# Weaknesses
# Resume Improvements
# Hiring Recommendation

Return clean markdown.
"""

    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text

        return "Unable to generate ATS report."

    except Exception as e:
        return f"ATS Analysis Error: {str(e)}"

# ===============================
# SKILL EXTRACTION
# ===============================

def extract_skills(resume_text):

    prompt = f"""
Extract ONLY technical skills.

Include:
- Programming Languages
- Frameworks
- Libraries
- Databases
- Developer Tools

Exclude:
- Leadership
- Communication
- Mentorship
- Soft Skills

Return ONLY JSON.

Example:

{{
"skills":[
"Python",
"SQL",
"Machine Learning"
]
}}

Resume:
{resume_text}
"""

    response = model.generate_content(prompt)

    try:

        clean = response.text.replace(
            "```json", ""
        ).replace(
            "```", ""
        )

        data = json.loads(clean)

        return data["skills"]

    except:

        return []


# ===============================
# JOB SEARCH
# ===============================

def get_jobs(job_title):

    url = (
        f"https://api.adzuna.com/v1/api/jobs/in/search/1"
        f"?app_id={ADZUNA_APP_ID}"
        f"&app_key={ADZUNA_APP_KEY}"
        f"&results_per_page=10"
        f"&what={job_title}"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        return data.get(
            "results",
            []
        )

    except Exception as e:

        print(e)

        return []

# ===============================
# STREAMLIT UI
# ===============================

st.set_page_config(
    page_title="AI ATS + Job Recommender",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer & Job Recommender")

st.markdown(
    "Upload Resume + Job Description and get ATS score and matching jobs."
)

# ===============================
# JD INPUT
# ===============================

jd_option = st.radio(
    "Job Description Input",
    ["Paste Text", "Provide URL"]
)

jd_text = ""

if jd_option == "Paste Text":

    jd_text = st.text_area(
        "Paste Job Description",
        height=250
    )

else:

    url = st.text_input(
        "Enter Job Description URL"
    )

    if url:

        with st.spinner(
            "Loading JD..."
        ):

            jd_text = get_jd_from_url(
                url
            )

        st.success(
            "Job Description Loaded"
        )

# ===============================
# RESUME UPLOAD
# ===============================

uploaded_resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# ===============================
# ANALYZE
# ===============================

if st.button("Analyze Resume"):

    if not jd_text:

        st.warning(
            "Please provide Job Description"
        )

        st.stop()

    if uploaded_resume is None:

        st.warning(
            "Please upload Resume"
        )

        st.stop()

    with st.spinner(
        "Analyzing Resume..."
    ):

        resume_text = extract_resume_text(
            uploaded_resume
        )

        analysis = analyze_resume(
            jd_text,
            resume_text
        )

        skills = extract_skills(
            resume_text
        )

        job_titles = get_best_job_titles(
            resume_text
        )

        all_jobs = []

        for role in job_titles:
            role_jobs = get_jobs(role)

            all_jobs.extend(role_jobs)
        unique_jobs = []

        seen_titles = set()

        for job in all_jobs:

            title = job.get(
                "title",
                ""
            ).lower().strip()

            if title not in seen_titles:
                seen_titles.add(title)

                unique_jobs.append(job)

        jobs = unique_jobs[:10]

    st.success(
        "Analysis Complete"
    )

    # ===========================
    # DEBUG
    # ===========================

    st.subheader("DEBUG")

    st.write("Analysis Output:")
    st.write(analysis)

    st.write("Skills:")
    st.write(skills)

    st.write("Predicted Job Titles:")
    st.write(job_titles)

    st.write("Jobs Object:")
    st.write(jobs)

    # ===========================
    # ATS REPORT
    # ===========================

    st.header("ATS Report")

    if analysis:

        st.markdown(analysis)

    else:

        st.error(
            "ATS report generation failed."
        )

    # ===========================
    # SKILLS
    # ===========================

    st.header("Extracted Skills")

    if skills:

        st.write(skills)

    else:

        st.info(
            "No skills extracted."
        )

    # ===========================
    # JOBS
    # ===========================

    st.header("Recommended Jobs")

    if jobs:

        for job in jobs:

            title = job.get(
                "title",
                "N/A"
            )

            company = job.get(
                "company",
                {}
            ).get(
                "display_name",
                "N/A"
            )

            location = job.get(
                "location",
                {}
            ).get(
                "display_name",
                "N/A"
            )

            link = job.get(
                "redirect_url",
                "#"
            )

            salary = job.get(
                "salary_is_predicted",
                ""
            )

            st.markdown(
                f"""
### {title}

**Company:** {company}

**Location:** {location}

**Apply:** {link}

---
"""
            )


    else:

        st.warning(

            f"No live jobs found for {job_title}"

        )

        try:

            fallback_prompt = f"""

            Based on this resume:


            1. Recommend 10 suitable job roles.

            2. Explain why each role matches.

            3. Mention companies that typically hire.


            Resume:

            {resume_text[:6000]}

            """

            fallback = model.generate_content(

                fallback_prompt

            )

            st.subheader(

                "AI Recommended Career Paths"

            )

            st.markdown(

                fallback.text

            )


        except Exception as e:

            st.error(

                str(e)

            )

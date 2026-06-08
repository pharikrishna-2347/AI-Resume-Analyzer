# 📄 AI Resume Analyzer & Job Recommender

An AI-powered Applicant Tracking System (ATS) and Job Recommendation Platform built using Streamlit, Gemini AI, and Adzuna Jobs API.

This application analyzes resumes against job descriptions, generates ATS scores, identifies skill gaps, and recommends relevant job opportunities with direct application links.

---

## 🌐 Live Demo

Try the application here:

[AI Resume Analyzer](https://phk-ai-resume-analyzer-zya8ghfnv44yyvhlptzaai.streamlit.app/)

## 🚀 Features

### ATS Resume Analysis

* Upload Resume in PDF format
* Paste Job Description or provide Job Description URL
* ATS Match Score Generation
* Executive Summary of Candidate Profile
* Matching Skills Identification
* Missing Skills Detection
* Strengths and Weakness Analysis
* Resume Improvement Suggestions
* Hiring Recommendation

### Skill Extraction

* Extracts technical skills from resumes
* Identifies programming languages, tools, databases, and technologies

### AI Job Recommendation

* Predicts suitable job roles based on candidate profile
* Searches live jobs using Adzuna API
* Provides company information and application links
* Removes duplicate recommendations

### User Interface

* Built with Streamlit
* Simple and interactive UI
* Real-time analysis

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI

* Google Gemini API

### Resume Parsing

* PyMuPDF

### Web Scraping

* BeautifulSoup
* Requests

### Job Search

* Adzuna Jobs API

---

## 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
└── assets/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
ADZUNA_APP_ID=YOUR_ADZUNA_APP_ID
ADZUNA_APP_KEY=YOUR_ADZUNA_APP_KEY
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 📈 Workflow

```text
Resume PDF
     │
     ▼
Resume Parsing
     │
     ▼
Gemini Analysis
     │
     ├── ATS Score
     ├── Skill Extraction
     ├── Skill Gap Analysis
     ├── Hiring Recommendation
     │
     ▼
Role Prediction
     │
     ▼
Job Recommendation Engine
     │
     ▼
Live Job Opportunities
```

---

## 🎯 Example Output

### ATS Report

* ATS Match Score
* Executive Summary
* Matching Skills
* Missing Skills
* Strengths
* Weaknesses
* Resume Improvement Suggestions
* Hiring Recommendation

### Recommended Jobs

* Job Title
* Company Name
* Location
* Apply Link

---

## 🔮 Future Enhancements

* Multiple Resume Ranking
* Candidate Leaderboard
* PDF Report Export
* ATS Score Visualization
* Resume Improvement Tracker
* Resume-to-Resume Comparison
* Job Match Percentage Ranking
* Recruiter Dashboard

---

## 👨‍💻 Author

Hari Krishna

B.Tech CSE, IIIT Jabalpur

Interested in:

* Artificial Intelligence
* Machine Learning
* Software Development
* Data Science

---

## ⭐ If you found this project useful

Please consider giving the repository a star.

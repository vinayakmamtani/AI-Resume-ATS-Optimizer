# AI-Powered Resume & ATS Optimizer

An intelligent, transparent, and explainable Applicant Tracking System (ATS) resume diagnostic and optimization tool powered by Streamlit, rule-based NLP matching, and Google Gemini.

## Author
- **Vinayak Mamtani**

---

## Features

- **Resume Parsing & Extraction**: Extracts and structures text, sections, and contact details from PDF resumes using `pdfplumber`.
- **Intelligent Keyword & Skill Matching**: Utilizes token-sorted fuzzy matching (`thefuzz`, `Levenshtein`) against comprehensive industry skill taxonomies and job descriptions.
- **Explainable Scoring Engine**: Computes ATS match percentages, skill gap analysis, and section-by-section breakdown without black-box opacity.
- **Interactive Visualizations**: Gauge meters, breakdown charts, and gap matrices powered by `Plotly`.
- **AI-Powered Tailoring Recommendations**: Generates tailored bullet points, missing skill integrations, and executive summaries using Google Gemini.

---

## Tech Stack

- **Frontend / Dashboard**: [Streamlit](https://streamlit.io/)
- **Text & PDF Extraction**: [pdfplumber](https://github.com/jsvine/pdfplumber)
- **Fuzzy Matching & NLP**: [thefuzz](https://github.com/seatgeek/thefuzz), [python-Levenshtein](https://github.com/maxbachmann/Levenshtein)
- **Data Visualization**: [Plotly](https://plotly.com/)
- **AI Engine**: Google Gemini API via [google-genai / REST]
- **Language**: Python 3.10+

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and add your Google Gemini API key:
```bash
cp .env.example .env
```
Edit `.env`:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

### 3. Run the Application
The single launcher handles dependency checks, package installation, and starts the Streamlit dashboard:
```bash
python run.py
```
Or start Streamlit directly:
```bash
streamlit run app.py
```
Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```text
├── app.py              # Main Streamlit web application & UI
├── extractor.py        # Resume parsing & PDF text extraction
├── matcher.py          # Fuzzy matching & ATS scoring engine
├── recommendations.py  # AI suggestions & Gemini LLM integrations
├── taxonomy.py         # Skills, job roles, and domain taxonomy
├── run.py              # Automated setup & launcher script
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

---

## License
MIT License

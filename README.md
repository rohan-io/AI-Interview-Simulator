# 🤖 AI Interview Simulator

An AI-powered mock interview platform that generates role-based technical interview questions and evaluates candidate answers using LLM-based structured feedback.

This system simulates real-world technical interviews by dynamically generating questions and scoring responses using Groq’s Llama-3.3-70B model integrated with LangChain.

---

## 🚀 Features

- 🔹 Role-based Interview Simulation (Frontend / Backend / Fullstack etc.)
- 🔹 Dynamic Question Generation using LLM
- 🔹 AI-powered Answer Evaluation
- 🔹 Structured Feedback:
  - Score
  - Strengths
  - Weaknesses
  - Improvement Suggestions
- 🔹 Interview Performance Analytics (Charts)
- 🔹 Interview History Tracking
- 🔹 Overall Performance Scoring
- 🔹 Resume-ready Mock Interview Reports

---

## 🧠 AI Capabilities

This system uses:

- **Groq Llama-3.3-70B** for:
  - Question Generation
  - Candidate Answer Evaluation

- **LangChain + PydanticOutputParser** for:
  - Enforcing Structured Output from LLM
  - Preventing Invalid JSON Responses
  - Reliable AI Feedback Generation

Evaluation Pipeline:

```
Candidate Answer
        ↓
LangChain Prompt
        ↓
Llama-3.3-70B (Groq)
        ↓
Pydantic Schema Validation
        ↓
Structured Feedback Object
```

This ensures AI feedback always contains:

- Score
- Strengths
- Weaknesses
- Improvement Suggestions

---

## 🛠️ Tech Stack

| Layer        | Technology |
|------------|------------|
Backend      | Django |
Database     | MySQL |
AI Model     | Groq Llama-3.3-70B |
LLM Framework| LangChain |
Validation   | Pydantic |
Frontend     | HTML + CSS |
Charts       | Chart.js |
Auth         | Django Authentication |

---

## 📊 Interview Workflow

1. Select Role & Difficulty
2. LLM Generates 5 Interview Questions
3. Candidate Submits Answers
4. Each Answer Evaluated by AI
5. Structured Feedback Generated
6. Overall Score Calculated
7. Performance Chart Displayed
8. Interview Stored in History

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/rohan-io/AI-Interview-Simulator.git
cd AI-Interview-Simulator
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Create `.env` File

Inside project root:

```
GROQ_API_KEY=your_api_key_here
```

---

### 5️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6️⃣ Start Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/interviews/
```

---

## 📈 Future Improvements

- Role-specific Tech Stack Selection
- Hiring Recommendation Engine
- AI Follow-up Questions
- Resume-based Interview Generation
- Deployment (AWS / Render)

---

## 👨‍💻 Author

**Rohan Behera**

GitHub: https://github.com/rohan-io

---

⭐ If you found this project useful, consider giving it a star!

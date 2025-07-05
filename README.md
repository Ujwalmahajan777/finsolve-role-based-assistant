# 🤖 FinSolve Role-Based Assistant

A RAG-based AI chatbot designed to deliver **secure, role-specific insights** across departments in a FinTech company. Built as part of the **Codebasics Resume Project Challenge**, this assistant empowers different teams like Finance, HR, Marketing, and C-Level to access only the data they are authorized for — using **Role-Based Access Control (RBAC)** combined with **LangChain's Retrieval-Augmented Generation (RAG)**.

---

## 🔧 Features

- 🔐 **Role-Based Access Control** (RBAC)
- 📄 Document ingestion from Markdown & CSV
- 🧠 Contextual answers powered by **LangChain + Chroma + DeepSeek**
- 🚀 FastAPI backend + Streamlit frontend UI
- 🧩 Modular codebase with loaders, retrievers, vector store, and UI

---

## 🏗️ Architecture Overview

```
User Input (via Streamlit)
    ↓
FastAPI Backend (Receives query + role)
    ↓
Role Filter (Injects role-based filter into Chroma vector store)
    ↓
Retriever (ChromaDB + ContextualCompressionRetriever)
    ↓
LLM Prompt (with role + question + docs)
    ↓
DeepSeek LLM → Final Answer
```

---

## 📂 Folder Structure

```
fintech_assistent/
├── assistent/
│   ├── main.py             # FastAPI entrypoint
│   ├── rag_chain.py        # RAG + RBAC logic
│   └── loader.py           # Markdown/CSV loader
├── streamlit_app/
│   └── app.py              # Streamlit frontend
├── finsolve_docs/          # Departmental markdown/CSV docs
├── vector_store/           # ChromaDB persistence
├── .env                    # API keys, secrets
└── requirements.txt
```

---

## ⚙️ Setup Instructions

1. **Clone the repo** (replace with your link):
   ```bash
   git clone https://github.com/YOUR_USERNAME/finsolve-assistant.git
   cd fintech_assistent
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate   
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI backend**:
   ```bash
   uvicorn assistent.main:app --reload
   ```

5. **Run the Streamlit chatbot UI**:
   ```bash
   streamlit run streamlit_app/app.py
   ```

---

## 🔐 Roles and Access Levels

| Role        | Access Level                                  |
|-------------|-----------------------------------------------|
| `finance`   | Financial reports, equipment costs, expenses  |
| `hr`        | Payroll, employee data, attendance            |
| `marketing` | Campaign metrics, customer feedback           |
| `engineering` | Tech architecture, development process     |
| `c-level`   | 🔓 Full access to all documents               |
| `employee`  | General info like FAQs, policies              |

---

## 🎯 Example Query Flow

> **HR asks:** “What is the financial report for Q1?”  
> 🔒 Response: “I don’t have access to that information.”

> **C-Level asks the same question:**  
> ✅ Response: “Revenue: $2.1B... Gross Margin: 58%... etc.”

---

## 🧰 Tech Stack

- **Python**
- **FastAPI** for backend API
- **Streamlit** for frontend chatbot interface
- **LangChain** for RAG and LLM integration
- **ChromaDB** for vector storage
- **DeepSeek LLM** for answer generation
- **HuggingFace Transformers** for embedding
- **Markdown + CSV** document handling

---

## 📽️ Demo & Presentation

- **YouTube Video Presentation:** [Watch here](https://youtu.be/5Mm8CeESBsY)
- **LinkedIn Submission Post:** [View here](https://www.linkedin.com/posts/ujwal-mahajan-01237b36b_codebasics-resumechallenge-langchain-activity-7346178831021400064-NhTG?utm_source=share&utm_medium=member_desktop&rcm=ACoAAFu2lU4BrqH0Zu5E6x7jzHW_AKe-77-fDZ8)
---

## 🙏 Acknowledgements

Special thanks to [Codebasics](https://codebasics.io/) for organizing the Resume Project Challenge and inspiring practical AI engineering.

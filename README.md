# ⚖️ Covenant — AI-Powered Contract Intelligence Platform  

Covenant is an AI-driven system that analyzes legal contracts end-to-end.  
It extracts clauses, classifies them using a fine-tuned legal model, evaluates risk & sentiment, and generates clean summaries for end-users.  

The project integrates:  
- **FastAPI backend**  
- **React + ShadCN UI**  
- **Supabase** (Auth, Storage, Database)  
- **A custom NLP/ML layer**  
- **Fine-tuned InLegalBERT classifier** (trained on CUAD)  
- **Clause extraction, classification, and analytics pipelines**

This repository contains the entire backend, ML engine, and frontend needed to run Covenant locally.

---

# 🏗️ Architecture Overview  

## **1. Frontend (React + Vite + ShadCN UI)**  
Users can:  
- Upload contracts (PDF/TXT)  
- View clause-level analysis  
- See risk & sentiment indicators  
- Read auto-generated summaries  
- Interact with a contract-specific chatbot  

The UI is designed to be clean, modern, and easy for legal teams to use.

---

## **2. Backend (FastAPI)**  
The backend manages:  
- File uploads → stored in Supabase Storage  
- Document metadata → stored in Supabase Postgres  
- Preprocessing + clause extraction  
- Model inference (classification, risk scoring, summarization)  
- APIs consumed by the frontend  

Endpoints follow REST conventions and use Pydantic for validation.

---

## **3. Machine Learning Layer (Python)**  
Located under: backend/ml_layer


Modules include:

| File              | Purpose                                                   |
|------------------|-----------------------------------------------------------|
| `preprocess.py`   | Extracts clean clauses from contract text                |
| `classify.py`     | Loads fine-tuned model and classifies each clause        |
| `risk.py`         | Computes clause-level risk scores                        |
| `summary.py`      | Generates an overall summary of the contract             |
| `chatbot.py`      | Q&A over contract text using embedding-based retrieval   |
| `models/`         | Contains the fine-tuned InLegalBERT model                |

The ML layer is completely local — no external API calls.

---

# 🧠 Machine Learning Details  

## **Fine-Tuned Model — InLegalBERT**  
The system uses a locally fine-tuned version of **InLegalBERT**, trained on:  

- **CUAD (Contract Understanding Atticus Dataset)**  
- 41 clause categories  
- Commercial SEC-filed contracts  


This enables **high-accuracy clause classification** on real contracts.

---

## 📄 Preprocessing Pipeline (`preprocess.py`)  

Steps performed:

1. Extract text from user-uploaded document  
2. Clean & normalize whitespace  
3. Split into clauses using:  
   - Numbered headings (`1.`, `2.`)  
   - Subsections (`A.`, `B.`)  
   - ALL-CAPS legal headings  
4. Return a list of clean, logically separated clauses  

Example output:

```json
[
  "1. CONFIDENTIALITY — The contractor shall maintain confidentiality of all proprietary information.",
  "2. TERMINATION — Either party may terminate with 30 days written notice."
]
```
---

## 🔎 Clause Classification Pipeline (`classify.py`)

- Loads the fine-tuned **InLegalBERT** model  
- Tokenizes each clause  
- Automatically **chunks long clauses** (>512 tokens)  
- Performs **multi-class classification**  
- Outputs a **predicted label + confidence score**

**Example Output**
```json
{
  "clause": "Either party may terminate with 30 days notice.",
  "label": "Termination for Convenience",
  "score": 0.992
}
```

---

## ⚠️ Risk Scoring (`risk.py`)

Risk scoring considers:

- Clause category  
- Sentiment polarity  
- Presence of risky keywords  
- Missing obligations  
- Severity implied within clause text  

**Possible outputs:** `low`, `medium`, `high`

**Example**
```json
{
  "clause": "The contractor shall indemnify the client for any damages...",
  "risk": "high",
  "reason": "Indemnity clause with broad liability"
}
```

---

## 📝 Contract Summary (`summary.py`)

Generates a readable overview covering:

- Key obligations  
- Payment terms  
- Termination conditions  
- Confidentiality requirements  
- Core risks  

**Example**
> This contract grants the service provider access to confidential data under strict terms...  
> Termination is permitted with 30 days notice by either party...

---

## 💬 Clause-Linked Chatbot (`chatbot.py`)

Users can ask:

- “What are the termination rights?”  
- “Is there a non-compete clause?”  
- “Who is responsible for indemnification?”  

The chatbot:

- Searches **clause embeddings**  
- Retrieves the **most relevant clause**  
- Generates an **answer with source citation**





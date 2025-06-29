# 🤖 PolicyPal AI – Your Insurance Companion
Introduction
---

PolicyPal AI is a Generative AI-powered web app that helps users understand their insurance policies by extracting, summarizing, and answering questions from policy documents (PDFs/images) in simple language.
Many people struggle to understand key terms, conditions, and coverage.
Users can upload PDFs or images and ask questions in plain English. Also help to suggest the insurance based on their monthly budget and calculate the total insurance premium.



Built using Python, Streamlit, and Meta’s LLaMA 3 model running via Ollama locally.

🧠 Features
--

- 📄 **PDF/Image Upload** – Extracts text from insurance policy documents
- 🧠 **LLaMA 3 (Ollama)** – Answers user questions and summarizes content locally
- ⏰ **Important Dates Extractor** – Detects policy deadlines, renewals, and start dates
- 💬 **Ask Any Question** – Q&A powered by LLaMA 3
- 💸 **Budget-based Plan Suggestions** – Get insurance recommendations based on what you can afford monthly
- 💰 **Insurance Premium Calculator**

System Design
----
![Gen AI policypal AI](https://github.com/user-attachments/assets/67475f95-7813-4474-9f7a-316dbbb9a28b)


⚙️ Tech Stack
--
| Area         | Tech |
|--------------|------|
| UI           | Streamlit |
| OCR          | pytesseract + PIL |
| PDF Reading  | PyPDF2 |
| GenAI        | Meta's LLaMA 3 via Ollama |
| NLP/Prompting| Custom prompt engineering |
| API Calls    | Localhost requests to Ollama |
| File Handling| Python file I/O |

🛠️ Setup Guide
--

✅ Clone the repo
--
https://github.com/priyal-06/policypal-AI.git

cd policypal-ai

📦 Create virtual environment and install dependencies
--
   
python -m venv venv

venv\Scripts\activate        # On Windows

source venv/bin/activate     # On macOS/Linux

pip install -r requirements.txt

🧠 Install and run Ollama
---

If you haven’t installed Ollama yet:

Download Ollama: https://ollama.com/download (for Windows/macOS/Linux)

Open terminal and run:
---

ollama pull llama3

ollama run llama3


🚀 Run the App
---
streamlit run app.py





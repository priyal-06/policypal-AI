import streamlit as st
from PIL import Image
import pytesseract
import PyPDF2
import re
import datetime
import requests

# ---------------------- Streamlit UI Setup ---------------------- #
st.set_page_config(page_title="PolicyPal AI", layout="wide")
st.title("🤖 PolicyPal AI – Your Insurance Companion")

# ---------------------- Sidebar ---------------------- #
st.sidebar.header("📄 Upload Policy Document")
uploaded_file = st.sidebar.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

st.sidebar.markdown("---")
st.sidebar.header("💰 Insurance Budget")
monthly_budget = st.sidebar.number_input(
    "Enter your monthly insurance budget (₹)",
    min_value=100,
    max_value=10000,
    step=100
)

# ---------------------- Extract Text ---------------------- #
extracted_text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            extracted_text += page.extract_text()
    else:
        image = Image.open(uploaded_file)
        extracted_text = pytesseract.image_to_string(image)

    st.markdown("### 📄 Extracted Policy Text")
    st.text_area("Document Text", extracted_text[:3000], height=300)

# ---------------------- LLaMA 3 (Ollama) Function ---------------------- #
def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json().get("response", "⚠️ No response from model.")
        else:
            return f"❌ GenAI error: {response.status_code} – {response.reason}"
    except Exception as e:
        return f"❌ Failed to get GenAI response.\n{str(e)}"

# ---------------------- Summarize Policy ---------------------- #
summarize = st.checkbox("🧠 Summarize Entire Policy")
if summarize and extracted_text:
    st.subheader("📄 Policy Summary")
    with st.spinner("Summarizing..."):
        prompt = f"Summarize this insurance policy in simple terms:\n{extracted_text[:2000]}"
        summary = ask_ollama(prompt)
        st.success("Summary generated successfully!")
        st.write(summary)

# ---------------------- Important Dates Extraction ---------------------- #
if extracted_text:
    st.subheader("⏰ Important Dates")
    dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', extracted_text)
    today = datetime.datetime.today()
    future_dates = []

    for date_str in dates:
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"):
            try:
                parsed_date = datetime.datetime.strptime(date_str, fmt)
                if parsed_date > today:
                    future_dates.append(parsed_date.strftime("%d %b %Y"))
                break
            except:
                continue

    if future_dates:
        for d in future_dates:
            st.info(f"📅 Future date found: {d}")
    else:
        st.info("No future dates found.")

# ---------------------- Question Answering Section ---------------------- #
st.subheader("💡 Ask a Question About Your Policy")
user_question = st.text_input("Enter your question")

if user_question and extracted_text:
    prompt = f"""
You are a smart assistant for insurance.

Based on this policy:
{extracted_text[:2000]}

Answer this question clearly: {user_question}
"""
    response = ask_ollama(prompt)
    st.success("✅ GenAI Response:")
    st.write(response)

# ---------------------- Budget-Based Insurance Suggestions ---------------------- #
st.subheader("💸 Suggested Insurance Plans Based on Your Budget")

# Static Sample Plan List
insurance_plans = [
    {"name": "SecureLife Term Plan", "type": "Term Life", "monthly": 500, "benefits": "₹50L sum assured, tax benefits"},
    {"name": "HealthGuard Plus", "type": "Health Insurance", "monthly": 700, "benefits": "₹5L coverage, free annual checkups"},
    {"name": "FutureWealth ULIP", "type": "Investment-linked", "monthly": 1200, "benefits": "Market returns + insurance"},
    {"name": "EasyLife Protection", "type": "Basic Life Cover", "monthly": 300, "benefits": "₹10L sum assured"},
    {"name": "SilverCare Senior Plan", "type": "Senior Health", "monthly": 950, "benefits": "₹3L for 60+ age with pre-existing coverage"},
    {"name": "ChildEdu Invest Plan", "type": "Child Education", "monthly": 1500, "benefits": "₹10L at maturity for education"},
]

if monthly_budget:
    st.markdown("### 🧾 Plans Within Your Budget")
    matched = [plan for plan in insurance_plans if plan["monthly"] <= monthly_budget]

    if matched:
        for plan in matched:
            st.success(
                f"**{plan['name']}** ({plan['type']}) – ₹{plan['monthly']}/month\n\n📌 {plan['benefits']}"
            )
    else:
        st.warning("No plans found within your budget. Try increasing your monthly limit.")



import streamlit as st
from PIL import Image
import pytesseract
import PyPDF2
import re
import datetime
import requests

# Streamlit UI setup
st.set_page_config(page_title="PolicyPal AI", layout="wide")
st.title("🤖 PolicyPal AI – Your Insurance Companion")

# Upload file
st.sidebar.header("📄 Upload Policy Document")
uploaded_file = st.sidebar.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

# Extract text
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

# Function to use LLaMA 3 via Ollama
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

# Summarize entire policy
summarize = st.checkbox("🧠 Summarize Entire Policy")
if summarize and extracted_text:
    st.subheader("📄 Policy Summary")
    with st.spinner("Summarizing..."):
        prompt = f"Summarize this insurance policy in simple terms:\n{extracted_text[:2000]}"
        summary = ask_ollama(prompt)
        st.success("Summary generated successfully!")
        st.write(summary)

# Extract important future dates
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

# Q&A Section
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

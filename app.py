import streamlit as st
from detector import detect_fake_news

st.set_page_config(page_title="Fake News Detector", layout="centered")

st.title("📰 Fake News Detection App")
st.write("Enter a news headline or article text, and AI will check if it's **REAL** or **FAKE**.")

user_input = st.text_area("Paste news text here:")

if st.button("Check News"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            result = detect_fake_news(user_input)

        if "REAL" in result.upper():
            st.success("✅ This news seems REAL!")
        elif "FAKE" in result.upper():
            st.error("❌ This news seems FAKE!")
        else:
            st.info("🤔 Could not determine. Try again.")

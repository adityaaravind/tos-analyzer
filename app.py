import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="📜 TOS Analyzer", layout="wide")
st.title("📜 Terms of Service Analyzer")

st.markdown("Welcome to the **TOS Analyzer** — a simple tool to help you identify potentially risky or concerning language in Terms of Service or Privacy Policy pages. 🤖🔍")

st.markdown("""
**Why this matters:**  
Most of us don't read the fine print. TOS documents often contain clauses that allow companies to:
- Track your personal data
- Share information with third parties
- Modify terms without telling you
- Avoid accountability

This tool flags such phrases so you can **be more informed** before agreeing. ✅
""")

url = st.text_input("🔗 Enter the URL of a Terms of Service or Privacy Policy page")

def fetch_and_clean_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script", "style"]): script.decompose()
        text = soup.get_text(separator=" ")
        return re.sub(r"\s+", " ", text)
    except Exception as e:
        return None

def highlight_risks(text):
    red_flags = [
        "we may share your data",
        "without notice",
        "at our discretion",
        "third-party",
        "personal information",
        "advertising partners",
        "we are not responsible",
        "may change at any time",
        "your data may be sold",
        "waive your rights",
        "we collect information about you",
        "your consent to disclose",
        "we do not guarantee",
        "we may modify these terms",
        "we may terminate your account",
        "liability is limited",
        "binding arbitration",
        "you agree to indemnify",
        "we assume no responsibility",
        "no refund",
        "non-refundable",
        "cookies and tracking technologies"
    ]
    found = [flag for flag in red_flags if flag.lower() in text.lower()]
    return found

if url:
    with st.spinner("🔍 Fetching and analyzing the document..."):
        text = fetch_and_clean_text(url)
        if text:
            st.success("✅ Text successfully extracted and analyzed!")
            found_flags = highlight_risks(text)

            st.subheader("⚠️ Potential Red Flags Detected")
            if found_flags:
                for flag in found_flags:
                    st.markdown(f"- 🔴 **{flag}**")
            else:
                st.success("No obvious red flags found — but you should still read carefully!")

            with st.expander("📝 Full Extracted Terms of Service Text"):
                st.text_area("Extracted TOS Content", text, height=300)
        else:
            st.error("❌ Failed to fetch or analyze the page. Please check the URL and try again.")
else:
    st.info("🔎 Enter a URL above to begin analyzing a Terms of Service or Privacy Policy page.")
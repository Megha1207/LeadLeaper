from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
from utils import (
    search_serper,
    extract_emails_from_text,
    llm_extract_socials,
    llm_generate_email
)

# ====================================================
# PAGE CONFIG
# ====================================================
st.set_page_config(
    page_title="AI Lead Finder & Outreach",
    layout="wide"
)

# ====================================================
# WHITE + GOLD PREMIUM UI
# ====================================================
st.markdown(
    """
    <style>

        /* GLOBAL BACKGROUND */
        body {
            background: #ffffff;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* TITLE */
        .main-title {
            font-size: 44px;
            font-weight: 700;
            text-align: center;
            margin-top: -10px;
            background: linear-gradient(90deg, #d4b870, #b99748);
            -webkit-background-clip: text;
            color: transparent;
            letter-spacing: -0.5px;
        }

        .sub-text {
            text-align: center;
            font-size: 16px;
            color: #777;
            margin-bottom: 40px;
        }

        /* GLASS CARD + GOLD BORDER */
        .card {
            background: rgba(255,255,255,0.6);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            padding: 34px;
            border-radius: 22px;
            border: 1px solid rgba(212,184,112,0.35);
            box-shadow: 0 8px 26px rgba(0,0,0,0.06);
            transition: all 0.25s ease;
        }

        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 14px 34px rgba(0,0,0,0.09);
        }

        /* SECTION HEADER */
        .section-header {
            font-size: 20px;
            font-weight: 600;
            margin-top: 45px;
            margin-bottom: 14px;
            color: #383838;
            padding-bottom: 6px;
            border-bottom: 1px solid rgba(212,184,112,0.35);
        }

        /* INPUTS */
        textarea, input {
            background-color: #f8f8f8 !important;
            color: #222 !important;
            border-radius: 12px !important;
            border: 1px solid #e5e5e5 !important;
            padding: 10px !important;
        }

        textarea:focus, input:focus {
            border: 1px solid #d2b76a !important;
            box-shadow: 0 0 0 1px #d2b76a !important;
        }

        /* BUTTONS */
        .stButton>button {
            background: linear-gradient(90deg, #d4b870, #b99748) !important;
            color: #fff !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            height: 50px;
            transition: 0.25s ease;
            border: none;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(187,150,71,0.35);
        }

        /* DOWNLOAD BUTTON */
        .stDownloadButton>button {
            background: #ffffff !important;
            color: #b99748 !important;
            border-radius: 12px !important;
            border: 1px solid #b99748 !important;
            font-weight: 600 !important;
        }

        .stDownloadButton>button:hover {
            background: #faf7ef !important;
        }

        /* SOCIAL BOXES */
        .social-box {
            background: #ffffff;
            border: 1px solid rgba(212,184,112,0.4);
            padding: 18px;
            border-radius: 14px;
            margin-bottom: 10px;
            box-shadow: 0 2px 7px rgba(0,0,0,0.06);
        }

        /* EMAIL LIST BOX */
        .email-bubble {
            background: #faf4e5;
            border: 1px solid #d4b870;
            padding: 10px 14px;
            border-radius: 12px;
            font-weight: 600;
            color: #4c3c19;
            display: inline-block;
            margin-right: 8px;
            margin-bottom: 8px;
        }

        /* EMAIL DRAFT WINDOW */
        .email-draft-box {
            background: #ffffff;
            padding: 18px;
            border-radius: 14px;
            border: 1px solid rgba(212,184,112,0.4);
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }

    </style>
    """,
    unsafe_allow_html=True,
)

# ====================================================
# HEADER
# ====================================================
st.markdown('<div class="main-title">AI Lead Finder & Outreach</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Premium automated journalist discovery and outreach drafting system</div>', unsafe_allow_html=True)

# ====================================================
# INPUT CARD
# ====================================================
st.markdown('<div class="card">', unsafe_allow_html=True)

with st.form("search_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Journalist / Lead Name", placeholder="Jane Doe")

    with col2:
        outlet = st.text_input("Outlet / Publication", placeholder="TechCrunch")

    submitted = st.form_submit_button("Search Lead")

st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# PROCESSING + RESULTS
# ====================================================
if submitted:

    if not name.strip():
        st.error("Name is required.")
    else:

        with st.spinner("Searching cross-web sources..."):
            query = f"{name} {outlet} journalist contact email" if outlet else f"{name} journalist contact email"
            results = search_serper(query)

        snippets = [item.get("snippet", "") for item in results.get("organic", [])]
        combined_text = "\n".join(snippets)

        # ====================================================
        # EMAILS
        # ====================================================
        st.markdown('<div class="section-header">Identified Email Addresses</div>', unsafe_allow_html=True)
        emails = extract_emails_from_text(combined_text)

        if emails:
            for e in emails:
                st.markdown(f"<span class='email-bubble'>{e}</span>", unsafe_allow_html=True)
        else:
            st.write("No direct email addresses discovered.")

        # ====================================================
        # SOCIALS
        # ====================================================
        st.markdown('<div class="section-header">Detected Social Profiles</div>', unsafe_allow_html=True)

        with st.spinner("Locating available social profiles..."):
            socials = llm_extract_socials(combined_text)

        if socials:
            for key, value in socials.items():
                st.markdown(f"""
                <div class="social-box">
                    <strong>{key.title()}:</strong> {value}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No social profiles detected.")

        # ====================================================
        # EMAIL DRAFT
        # ====================================================
        st.markdown('<div class="section-header">Generated Outreach Email</div>', unsafe_allow_html=True)

        with st.spinner("Composing professional outreach draft..."):
            draft = llm_generate_email(
                name=name,
                outlet=outlet,
                emails=emails,
                socials=socials
            )

        st.markdown(f"""
            <div class="email-draft-box">
                <pre style="white-space: pre-wrap; font-size: 15px; line-height: 22px;">{draft}</pre>
            </div>
        """, unsafe_allow_html=True)

        # ====================================================
        # EXPORT
        # ====================================================
        df = pd.DataFrame([{
            "Name": name,
            "Outlet": outlet,
            "Emails": ", ".join(emails),
            "Socials": str(socials),
            "Draft": draft,
        }])

        st.download_button(
            "Download Lead as CSV",
            data=df.to_csv(index=False),
            file_name="lead_details.csv",
            mime="text/csv",
        )

        # ====================================================
        # DEBUG SNIPPETS
        # ====================================================
        st.markdown('<div class="section-header">Search Snippets (Debug)</div>', unsafe_allow_html=True)
        for i, snippet in enumerate(snippets[:10], start=1):
            st.write(f"{i}. {snippet}")

import streamlit as st


def load_css():
    st.markdown(
        """
        <style>


        #MainMenu,
        footer,
        header {
            visibility: hidden;
        }

        .stApp {
            background: #f6f8fc;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 105px;
            padding-bottom: 60px;
        }

        /* =====================================================
           FIXED TOP BAR
           ===================================================== */

        .topbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 72px;

            background: rgba(255, 255, 255, 0.96);
            border-bottom: 1px solid #e5e7eb;

            display: flex;
            align-items: center;

            padding: 0 32px;

            z-index: 999999;

            backdrop-filter: blur(12px);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-mark {
            width: 38px;
            height: 38px;

            border-radius: 11px;

            background: #111827;

            color: white;

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 20px;
            font-weight: 700;
        }

        .brand-name {
            font-size: 21px;
            font-weight: 750;
            color: #111827;
            letter-spacing: -0.5px;
        }

        .brand-divider {
            height: 22px;
            width: 1px;
            background: #d1d5db;
            margin: 0 4px;
        }

        .brand-product {
            font-size: 14px;
            color: #6b7280;
        }

        /* =====================================================
           SIDEBAR
           ===================================================== */

        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e5e7eb;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 88px;
        }

        .sidebar-user {
            background: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 14px;
            margin-top: 22px;
            margin-bottom: 18px;
        }

        .avatar {
            width: 38px;
            height: 38px;

            border-radius: 50%;

            background: #111827;
            color: white;

            display: flex;
            align-items: center;
            justify-content: center;

            font-weight: 700;

            float: left;
            margin-right: 10px;
        }

        .user-name {
            font-weight: 650;
            color: #111827;
        }

        .user-role {
            font-size: 12px;
            color: #6b7280;
        }

        /* =====================================================
           LOGIN
           ===================================================== */

        .login-wrapper {
            min-height: calc(100vh - 140px);

            display: flex;
            align-items: center;
            justify-content: center;
        }

        .login-card {
            width: 430px;

            background: #ffffff;

            border: 1px solid #e5e7eb;

            border-radius: 24px;

            padding: 42px;

            box-shadow:
                0 20px 50px rgba(15, 23, 42, 0.08);
        }

        .login-brand {
            text-align: center;
            margin-bottom: 28px;
        }

        .login-brand-mark {
            width: 56px;
            height: 56px;

            margin: auto auto 18px;

            border-radius: 16px;

            background: #111827;

            color: white;

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 27px;
            font-weight: 700;
        }

        .login-title {
            font-size: 29px;
            font-weight: 750;
            color: #111827;
            letter-spacing: -0.8px;
        }

        .login-subtitle {
            margin-top: 8px;
            color: #6b7280;
            font-size: 14px;
            line-height: 1.5;
        }

        .security-note {
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #6b7280;
        }

        /* =====================================================
           INPUTS
           ===================================================== */

        div[data-baseweb="input"] {
            background: #ffffff !important;
            border: 1px solid #d1d5db !important;
            border-radius: 10px !important;
        }

        div[data-baseweb="input"]:focus-within {
            border-color: #111827 !important;
            box-shadow: 0 0 0 2px rgba(17, 24, 39, 0.08);
        }

        div[data-baseweb="input"] input {
            color: #111827 !important;
            background: transparent !important;
        }

        div[data-baseweb="input"] input::placeholder {
            color: #9ca3af !important;
        }

        label {
            color: #374151 !important;
            font-weight: 550 !important;
        }

        /* =====================================================
           BUTTONS
           ===================================================== */

        .stButton > button {
            border-radius: 10px;
            min-height: 44px;
            font-weight: 600;
            border: 1px solid #d1d5db;
            transition: all 0.15s ease;
        }

        .stButton > button:hover {
            border-color: #111827;
            transform: translateY(-1px);
        }

        /* =====================================================
           DASHBOARD
           ===================================================== */

        .eyebrow {
            font-size: 12px;
            font-weight: 700;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .page-title {
            font-size: 34px;
            font-weight: 750;
            color: #111827;
            letter-spacing: -1px;
            margin-bottom: 5px;
        }

        .page-subtitle {
            color: #6b7280;
            font-size: 15px;
            margin-bottom: 28px;
        }

        /* =====================================================
           CHAT
           ===================================================== */

        .chat-user {
            background: #111827;
            color: white;

            padding: 14px 18px;

            border-radius: 16px 16px 4px 16px;

            margin: 20px 0 10px auto;

            max-width: 78%;

            line-height: 1.55;
        }

        .chat-ai {
            background: white;
            color: #111827;

            border: 1px solid #e5e7eb;

            padding: 18px 20px;

            border-radius: 16px 16px 16px 4px;

            margin: 10px 0 22px;

            max-width: 88%;

            line-height: 1.65;

            box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03);
        }

        .ai-label {
            font-weight: 700;
            font-size: 13px;
            margin-bottom: 9px;
            color: #111827;
        }

        .source-card {
            background: #f8fafc;

            border: 1px solid #e5e7eb;

            border-radius: 10px;

            padding: 10px 13px;

            margin-top: 7px;

            font-size: 13px;

            color: #374151;
        }

        /* =====================================================
           SUGGESTIONS
           ===================================================== */

        .section-label {
            font-size: 13px;
            font-weight: 650;
            color: #6b7280;
            margin: 22px 0 10px;
        }

        .suggestion-card {
            background: white;

            border: 1px solid #e5e7eb;

            border-radius: 12px;

            padding: 14px 16px;

            min-height: 70px;

            color: #374151;

            font-size: 13px;
        }

        /* =====================================================
           INFO CARDS
           ===================================================== */

        .info-card {
            background: white;

            border: 1px solid #e5e7eb;

            border-radius: 16px;

            padding: 22px;

            margin-bottom: 15px;
        }

        .info-title {
            font-size: 17px;
            font-weight: 700;
            color: #111827;
            margin-bottom: 8px;
        }

        .info-text {
            color: #6b7280;
            line-height: 1.6;
            font-size: 14px;
        }

        /* =====================================================
           STATUS
           ===================================================== */

        .status {
            display: inline-flex;
            align-items: center;
            gap: 7px;

            padding: 6px 10px;

            border-radius: 999px;

            background: #f0fdf4;

            color: #166534;

            font-size: 12px;
            font-weight: 600;
        }

        .status-dot {
            width: 7px;
            height: 7px;

            background: #22c55e;

            border-radius: 50%;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
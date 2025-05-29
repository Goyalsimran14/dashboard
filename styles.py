import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>
        /* Global Styles */
        .stApp {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb, #90caf9, #64b5f6);
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            color: #0d47a1;
            text-align: center;
        }
        .stButton>button {
            background-color: #1976d2;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0d47a1;
            transform: scale(1.05);
        }
        /* Animations */
        @keyframes fadeIn {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }
        .fade-in {
            animation: fadeIn 1s ease-in-out;
        }
    </style>
    """, unsafe_allow_html=True)
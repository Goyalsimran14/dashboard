# ----------HOME PAGES ----------
import streamlit as st

def home_page():
    st.markdown("""
<style>
/* App background and font */
.stApp {
    # background: #lf5f7fa
    font-family: 'Segoe UI', sans-serif;
    padding-bottom: 30px;
}

/* Header titles */
.custom-title {
    font-size: 40px;
    font-weight: 700;
    text-align: center;
    color: #0d47a1;
    margin-top: 40px;
    animation: fadeInDown 1.5s ease-in-out;
}

.custom-subtitle {
    text-align: center;
    font-size: 20px;
    color: #1565c0;
    margin-bottom: 40px;
    animation: fadeIn 2.5s ease-in;
}

/* Button design */
.stButton > button {
    background-color: #1976d2;
    color: white;
    font-size: 18px;
    padding: 0.75em 2em;
    border: none;
    border-radius: 8px;
    transition: 0.3s ease-in-out;
}

.stButton > button:hover {
    background-color: #0d47a1;
    transform: scale(1.05);
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
}

/* Responsive tweaks for mobile */
@media only screen and (max-width: 768px) {
    .custom-title {
        font-size: 28px;
    }
    .custom-subtitle {
        font-size: 16px;
    }
    .stButton > button {
        width: 100%;
        font-size: 16px;
    }
}

/* Animations */
@keyframes fadeIn {
    0% {opacity: 0;}
    100% {opacity: 1;}
}

@keyframes fadeInDown {
    0% {opacity: 0; transform: translateY(-20px);}
    100% {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)


    st.markdown('<div class="custom-title">📊 Welcome to GATE CSE Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subtitle">Prepare smart, stay consistent & crack GATE 🚀</div>', unsafe_allow_html=True)
 # Navigation buttons
    if st.button("Go to Dashboard"):
        st.session_state.page = "dashboard"
    if st.button("Logout"):
        st.session_state.page = "auth"
        st.session_state.authenticated = False
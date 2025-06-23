import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt  
import random
import hashlib
import sqlite3

# Set Streamlit page configuration
st.set_page_config(page_title="GATE CSE Dashboard", layout="wide")

# Initialize SQLite database
DB_FILE = "dashboard.db"

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "auth"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "subject_progress" not in st.session_state:
    st.session_state.subject_progress = {}
if "study_log" not in st.session_state:
    st.session_state.study_log = []
if "attempted_tests" not in st.session_state:
    st.session_state.attempted_tests = {}
if "course_status" not in st.session_state:
    st.session_state.course_status = {}

# Initialize database
def init_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    # Create study_log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        subject TEXT,
        hours REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_database()

# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify credentials
def verify_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Add new user
def add_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Reset password (send new password)
def reset_password(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        new_password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        hashed_new_password = hash_password(new_password)
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new_password, username))
        conn.commit()
        conn.close()
        return new_password
    conn.close()
    return None

# Submit study log
def submit_study_log(username, subject, hours, date):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO study_log (username, subject, hours, date) VALUES (?, ?, ?, ?)", (username, subject, hours, date))
    conn.commit()
    conn.close()

# Retrieve study logs
def get_study_logs(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT subject, hours, date FROM study_log WHERE username = ?", (username,))
    logs = cursor.fetchall()
    conn.close()
    return logs
def authenticate():
    st.title("🔒 Login / Sign Up / Forgot Password")

    auth_mode = st.radio("Choose Option", ["Login", "Sign Up", "Forgot Password"], horizontal=True)

    username = st.text_input("👤 Username")

    if auth_mode == "Login":
        password = st.text_input("🔒 Password", type="password")
        if st.button("🔓 Login"):
            if verify_user(username, password):
                st.success(f"🎉 Welcome back, {username}!")
                st.session_state.page = "home"
                st.session_state.authenticated = True
                st.session_state.username = username
            else:
                st.error("❌ Invalid login credentials.")

    elif auth_mode == "Sign Up":
        password = st.text_input("🔒 Password", type="password")
        confirm_password = st.text_input("✅ Confirm Password", type="password")
        if st.button("📝 Create Account"):
            if not username or not password:
                st.error("⚠️ All fields are required.")
            elif password != confirm_password:
                st.error("❌ Passwords do not match.")
            else:
                if add_user(username, password):
                    st.success("✅ Account created! Please login now.")
                else:
                    st.warning("❌ Username already exists. Try another one.")

    elif auth_mode == "Forgot Password":
        if st.button("📧 Reset Password"):
            if not username:
                st.warning("⚠️ Please enter your username to reset your password.")
            else:
                new_password = reset_password(username)
                if new_password:
                    st.success(f"🔑 Your new password is: `{new_password}`\nPlease save it securely and use it to log in.")
                else:
                    st.error("❌ Username not found.")


# ---------- DARK THEME CSS ----------
# st.markdown("""
#     <style>
#         .stApp {
#             background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
#             font-family: 'Segoe UI', sans-serif;
#             color: white;
#         }
#         h1, h2, h3 {
#             color: #90caf9;
#             text-align: center;
#             animation: fadeIn 1.5s ease-in;
#         }
#         .stButton>button {
#             background-color: #1976d2;
#             color: black;
#             font-size: 16px;
#             padding: 0.5em 1.5em;
#             border-radius: 10px;
#             border: none;
#             transition: all 0.3s ease;
#         }
#         .stButton>button:hover {
#             background-color: #0d47a1;
#             transform: scale(1.05);
#         }
#         .stTextInput>div>div>input {
#             background-color: #1a1a1a;
#             color: white;
#         }
#         .stSlider>div {
#             color: white;
#         }
#         @keyframes fadeIn {
#             0% {opacity: 0;}
#             100% {opacity: 1;}
#         }
#     </style>
# """, unsafe_allow_html=True)
st.markdown("""
    <style>
        /* General mobile adjustments */
        @media only screen and (max-width: 768px) {
            .stApp {
                padding: 10px; /* Reduce padding for smaller screens */
            }
            .custom-title {
                font-size: 28px; /* Smaller font size for titles */
            }
            .custom-subtitle {
                font-size: 16px; /* Smaller font size for subtitles */
            }
            .stButton > button {
                width: 100%; /* Make buttons full-width */
                font-size: 16px; /* Adjust button font size */
            }
            .streamlit-expanderContent {
                padding: 10px; /* Reduce padding inside expanders */
            }
            .dataframe-container {
                overflow-x: auto; /* Enable horizontal scrolling for tables */
            }
        }

        /* Sidebar adjustments for mobile */
        @media screen and (max-width: 768px) {
            section[data-testid="stSidebar"] {
                width: 100% !important;
                max-width: 100% !important;
            }
        }

        /* Expander tweaks for better readability */
        .streamlit-expanderHeader {
            font-size: 1.1rem;
            font-weight: 600;
            color: #0d47a1;
            background-color: #e3f2fd;
        }

        /* Mobile-friendly padding inside expanders */
        @media screen and (max-width: 768px) {
            .streamlit-expanderContent {
                padding: 10px;
            }
        }
    </style>
""", unsafe_allow_html=True)


# Reminder Feature
def check_reminder():
    now = datetime.datetime.now()
    reminder_time = datetime.time(22, 0)  # 10:00 PM
    if now.time() >= reminder_time and "reminder_shown" not in st.session_state:
        st.session_state.reminder_shown = True
        st.warning("⏰ Reminder: Please update your daywise timetable for tomorrow!")

# Call the reminder function on every page
check_reminder()

# Reset reminder state at midnight
if datetime.datetime.now().time() < datetime.time(0, 1):  # Between 12:00 AM and 12:01 AM
    st.session_state.pop("reminder_shown", None)

# Subjects dictionary
subjects = {
        "Operating System": {
            "Topics": ["Process Management", "Memory Management", "File Systems"],
            "YouTube": ["https://youtube.com/playlist?list=PLG9aCp4uE-s17rFjWM8KchGlffXgOzzVP"],
            "PYQs": ["https://youtube.com/playlist?list=PLIPZ2_p3RNHixlIaarIXGPy-eggJQMxd_"],
            "NPTEL": ["https://youtube.com/playlist?list=PLyqSpQzTE6M9SYI5RqwFYtFYab94gJpWk"],
            "Textbooks": ["Operating Systems by Avi Silberschatz, Greg Gagne, and Peter Baer Galvin"],
            "Free Tests": [
                "https://gateoverflow.in/exam/32/go2017-os-1",
                "https://gateoverflow.in/exam/32/go2017-os-2",
                "https://gateoverflow.in/exam/32/go2017-os-3",
                "https://gateoverflow.in/exam/148/operating-systems-gate2020-previous-gate-2"
            ],
            "Progress": "Not Started"
        },
        "Computer Organization & Architecture": {
            "Topics": ["Machine Instructions", "Pipelining", "Memory Hierarchy"],
            "YouTube": ["https://youtube.com/playlist?list=PLG9aCp4uE-s0xddCBjwMDnEVyc523WbA2"],
            "PYQs": ["https://youtube.com/playlist?list=PLG9aCp4uE-s2qCKKu2XD3zDK-NFEvE91n"],
            "NPTEL": [
                "https://youtube.com/playlist?list=PLgHucKw979AvcnTpPNZMZyORdL5HvTr9m",
                "https://youtube.com/playlist?list=PL2F82ECDF8BB71B0C"
            ],
            "Textbooks": [
                "Computer Organisation by Carl Hamacher",
                "Computer Organization and Design: the Hardware/Software Interface by David A Patterson and John L. Hennessy"
            ],
            "Free Tests": [
                "https://gateoverflow.in/exam/46/computer-architecture",
                "https://gateoverflow.in/exam/83/computer-architecture-2",
                "https://gateoverflow.in/exam/153/co-and-architecture-gate2020-previous-gate-1",
                "https://gateoverflow.in/exam/154/co-and-architecture-gate2020-previous-gate-2"
            ],
            "Progress": "Not Started"
        },
        "Computer Networks": {
            "Topics": ["TCP/IP", "Routing Protocols", "Network Security"],
            "YouTube": ["https://youtube.com/playlist?list=PLC36xJgs4dxHT-TxTy3U1slr5RaBJGaLd"],
            "PYQs": ["https://youtube.com/playlist?list=PLIPZ2_p3RNHim3NUSNOb7ffyhaE5MSkmE"],
            "NPTEL": ["https://youtube.com/playlist?list=PLbRMhDVUMngf-peFloB7kyiA40EptH1up"],
            "Textbooks": ["Data Communications and Networking by Behrouz A. Forouzan"],
            "Free Tests": [
                "https://gateoverflow.in/exam/49/computer-networks",
                "https://gateoverflow.in/exam/143/computer-networks-gate2020-previous-gate-1",
                "https://gateoverflow.in/exam/144/computer-networks-gate2020-previous-gate-2"
            ],
            "Progress": "Not Started"
        },
               "Compiler Design": {
            "Topics": ["Lexical Analysis", "Parsing", "Syntax-Directed Translation", "Runtime Environments", "Intermediate Code Generation"],
            "YouTube": ["https://youtube.com/playlist?list=PLEbnTDJUr_IcPtUXFy2b1sGRPsLFMghhS"],
            "PYQs": ["https://youtube.com/playlist?list=PLIPZ2_p3RNHjy3eH_qRImIs5dVUTpr9ga"],
            "NPTEL": ["https://youtube.com/playlist?list=PL54i8TI-dREaHgsBFNalWnz-bC9CZkOBb"],
            "Textbooks": ["Compilers: Principles, Techniques, and Tools by Aho, Lam, Sethi, and Ullman"],
            "Free Tests": [
                "https://gateoverflow.in/exam/47/compiler-design",
                "https://gateoverflow.in/exam/151/compiler-design-gate2020-previous-gate-1",
                "https://gateoverflow.in/exam/152/compiler-design-gate2020-previous-gate-2"
            ],
            "Progress": "Not Started"
        },
        "Theory of Computation": {
            "Topics": ["Finite Automata", "Turing Machines", "Pumping Lemma"],
            "YouTube": ["https://youtube.com/playlist?list=PLC36xJgs4dxGvebewU4z2CZYo-8nB93E7"],
            "PYQs": ["https://youtube.com/playlist?list=PLIPZ2_p3RNHhXeEdbXsi34ePvUjL8I-Q9"],
            "NPTEL": ["https://youtube.com/playlist?list=PLbRMhDVUMngcwWkzVTm_kFH6JW4JCtAUM"],
            "Textbooks": ["An Introduction to Formal Languages and Automata by Peter Linz"],
            "Free Tests": [
                "https://gateoverflow.in/exam/48/theory-of-computation",
                "https://gateoverflow.in/exam/84/theory-of-computation-test-2",
                "https://gateoverflow.in/exam/86/theory-of-computation-previous-gate-1"
            ],
            "Progress": "Not Started"
        },
        "C-Programming": {
            "Topics": ["Basics of C", "Pointers", "Data Structures in C", "File Handling"],
            "YouTube": ["https://youtube.com/playlist?list=PLbE3-5DBkMUkATaUFgDIpBDbfnym0qvsQ"],
            "NPTEL": ["https://youtube.com/playlist?list=PLEAYkSg4uSQ2k6GwNhpgSHodGT8wfvgwu"],
            "Textbooks": ["The C Programming Language by Brian Kernighan and Dennis Ritchie (2E)"],
            "PYQs": ["https://github.com/GATEOverflow/GO-PDFs/releases/tag/gatecse-2025"],
            "Free Tests": [
                "https://gateoverflow.in/exam/39/go2017-programming-1",
                "https://gateoverflow.in/exam/80/go_programming-test-2",
                "https://gateoverflow.in/exam/181/programming-gate2020-previous-gate-1",
                "https://gateoverflow.in/exam/182/programming-gate2020-previous-gate-2"
            ],
            "Progress": "Not Started"
        },
    
"Data Structures (DS)": {
    "Topics": ["Arrays", "Linked Lists", "Stacks", "Queues", "Trees", "Graphs"],
    "YouTube": ["https://youtube.com/playlist?list=PLIC0AxWOdm5BvHpI_AtPqqjoADnSqcYgp&si=q_Qps7uYmU2RjuLr"],
    "PYQs": ["https://youtube.com/playlist?list=PLG9aCp4uE-s3Rs4AjzG0VcXQCggmOJJ6W&si=YgSf-sgQNlmT2tBd"],
    "NPTEL": ["https://youtube.com/playlist?list=PLBF3763AF2E1C572F&si=oiRSnIiN4ntMIPQL"],
    "Textbooks": ["Data Structures And Algorithms by Narasimha Karumanchi"],
    "Free Tests": [
        "https://gateoverflow.in/exam/52/data-structure-set-2",
        "https://gateoverflow.in/exam/177/data-structures-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/178/data-structures-gate2020-previous-gate-2",
        "https://gateoverflow.in/exam/179/data-structures-gate2020-previous-gate-3",
        "https://gateoverflow.in/exam/180/data-structures-gate2020-previous-gate-4"
    ],
    "Progress": "Not Started"
},
# Add this to the subjects dictionary in the dashboard_page function
"Algorithms": {
    "Topics": ["Sorting", "Searching", "Dynamic Programming", "Greedy Algorithms", "Graph Algorithms"],
    "YouTube": ["https://youtube.com/playlist?list=PLAXnLdrLnQpRcveZTtD644gM9uzYqJCwr&si=U_A4tdPO33X3xV8I"],
    "PYQs": ["https://youtube.com/playlist?list=PLIPZ2_p3RNHjUCHdJp-_soSSmhgmO4i0T&si=5LN5dM51DjRDMOJ1"],
    "NPTEL": ["https://youtube.com/playlist?list=PL7DC83C6B3312DF1E&si=pme4ZTL1jou81mt4"],
    "Textbooks": [
        "Introduction to Algorithms, by CLRS (3E) - ch 1-4, 6-9,10, 11.1-11.4, 12.1-21.3, 15, 16.1-16.3, 17, 21-25.2",
        "Algorithm Design, Jon Kleinberg and Éva Tardos - ch 1-6"
    ],
    "Free Tests": [
        "https://gateoverflow.in/exam/37/go2017-algorithms-1",
        "https://gateoverflow.in/exam/82/algorithm-test-2",
        "https://gateoverflow.in/exam/66/algorithms-previous-gate-1",
        "https://gateoverflow.in/exam/145/algorithms-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/146/algorithms-gate2020-previous-gate-2"
    ],
    "Progress": "Not Started"
},
# Add this to the subjects dictionary in the dashboard_page function
"Digital Logic": {
    "Topics": ["Boolean Algebra", "Combinational Circuits", "Sequential Circuits", "Minimization"],
    "YouTube": ["https://youtube.com/playlist?list=PLBlnK6fEyqRjMH3mWf6kwqiTbT798eAOm&si=4C0Z9de3YKT4zHeb"],
    "PYQs": ["https://www.youtube.com/live/h-SDoV0_pwQ?si=PmwmIQ__UHWvUorW"],
    "NPTEL": ["https://youtube.com/playlist?list=PL803563859BF7ED8C&si=OXD8r2PBFbS6gbcC"],
    "Textbooks": ["Digital Logic and Computer Design by M. Morris Mano - 1.1-1.8, 2.1-2.7, 3-7"],
    "Free Tests": [
        "https://gateoverflow.in/exam/33/go2017-digital-1",
        "https://gateoverflow.in/exam/51/digital-design-set-2",
        "https://gateoverflow.in/exam/157/digital-logic-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/158/digital-logic-gate2020-previous-gate-2",
        "https://gateoverflow.in/exam/174/digital-logic-gate2020-previous-gate-3",
        "https://gateoverflow.in/exam/175/digital-logic-gate2020-previous-gate-4"
    ],
    "Progress": "Not Started"
},
"Database Management System (DBMS)": {
    "Topics": ["ER Model", "Normalization", "Transactions", "SQL"],
    "YouTube": ["https://youtube.com/playlist?list=PLG9aCp4uE-s0bu-I8fgDXXhVLO4qVROGy&si=5Iies1OyzDGms31i"],
    "PYQs": ["https://youtube.com/playlist?list=PLIPZ2_p3RNHh3otU-TnAK-GkqrvvOO33C&si=8Kazn74m30yhUDvh"],
    "NPTEL": ["https://youtube.com/playlist?list=PL-wVMhlYPDDkRQ0XrQ8IuslSiAWPpSfuJ&si=wEyZRgIxdNZgyqXE"],
    "Textbooks": [
        "Fundamentals of Database Systems by Ramez Elmasri and Shamkant B. Navathe (7E) - ch 1.3-1.6, 2.1-2.3, 3, 5-8, 9.1, 14.1-14.5, 14.6-14.7(just overview), 15.1-15.4, 16.1-16.7, 17.1-17.6, 20.1-20.5, 21.1-21.4, 21.7"
    ],
    "Free Tests": [
        "https://gateoverflow.in/exam/50/database-systems",
        "https://gateoverflow.in/exam/85/dbms-subject-test-2",
        "https://gateoverflow.in/exam/155/databases-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/156/databases-gate2020-previous-gate-2",
        "https://gateoverflow.in/exam/172/databases-gate2020-previous-gate-3",
        "https://gateoverflow.in/exam/173/databases-gate2020-previous-gate-4"
    ],
    "Progress": "Not Started"
},
# Add this to the subjects dictionary in the dashboard_page function
"Discrete Maths": {
    "Topics": ["Propositional Logic", "Combinatorics", "Recurrence Relations", "Group Theory", "Graph Theory", "Generating Function", "Set Theory"],
    "YouTube": [
        "Propositional Logic: https://youtube.com/playlist?list=PLIPZ2_p3RNHillKxh1_iFeZhy9MftHeWW&si=4om73pMxQvuToQvh",
        "Combinatorics: https://youtube.com/playlist?list=PLIPZ2_p3RNHgm_UqwqckMxM68HS4BkjYY&si=ksPAjkwm2cb28NVn",
        "Recurrence Relations: https://youtube.com/playlist?list=PLIPZ2_p3RNHhhTH0o1JBMgscMUvxs4E_4&si=r3THjdW_19iFCAIm",
        "Group Theory: https://youtube.com/playlist?list=PLIPZ2_p3RNHhXves0XVa8d5O6F4rUi3KR&si=8-C9TfTK2XjdG6Pt",
        "Graph Theory: https://youtube.com/playlist?list=PLIPZ2_p3RNHjQoj0k-BlI9zXE0QKdl-lI&si=GGNFwhNSHxhdcJOQ",
        "Generating Function: https://youtube.com/playlist?list=PLIPZ2_p3RNHjQoj0k-BlI9zXE0QKdl-lI&si=GGNFwhNSHxhdcJOQ",
        "Set Theory: https://youtube.com/playlist?list=PLIPZ2_p3RNHjHnhdkPWFAlcizVQJ8w4TX&si=aOl21dH2q3NjaDgx"
    ],
    "PYQs": ["https://github.com/GATEOverflow/GO-PDFs/releases/tag/gatecse-2025"],
    "NPTEL": ["https://youtube.com/playlist?list=PLgMDNELGJ1Ca7hpEIYtWvMXKcTx88OD2O&si=1WcmQtcIG0sFqSlg"],
    "Textbooks": [
        "Discrete mathematics and its applications by Kenneth H. Rosen (Indian 7E) - ch 1,2, 4-8, 11.1-11.3",
        "Discrete mathematics with applications by Susanna S. Epp (4E) - ch 1, 2.1-2.3, 3, 4(optional), 5.1, 5.5-5.7, 6-10, 11-12(optional)"
    ],
    "Free Tests": [
        "https://gateoverflow.in/exam/601/go-classes-2025-weekly-quiz-5-propositional-logic",
        "https://gateoverflow.in/exam/602/go-classes-2025-weekly-quiz-6-propositional-logic",
        "https://gateoverflow.in/exam/603/go-classes-2025-weekly-quiz-7-propositional-logic",
        "https://gateoverflow.in/exam/605/go-classes-2025-weekly-quiz-8-set-theory",
        "https://gateoverflow.in/exam/614/go-classes-cs-2025-weekly-quiz-6-functions",
        "https://gateoverflow.in/exam/622/go-classes-cs-2025-weekly-quiz-7-relations",
        "https://gateoverflow.in/exam/641/go-classes-cs-2025-weekly-quiz-15-lattice-%26-poset",
        "https://gateoverflow.in/exam/438/discrete-mathematics-propositional-logic-test-1",
        "https://gateoverflow.in/exam/441/discrete-mathematics-propositional-logic-test-2",
        "https://gateoverflow.in/exam/447/discrete-mathematics-logic-test-3",
        "https://gateoverflow.in/exam/456/discrete-mathematics-logic-test-4",
        "https://gateoverflow.in/exam/191/set-theory-%26-algebra-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/192/set-theory-%26-algebra-gate2020-previous-gate-2",
        "https://gateoverflow.in/exam/193/combinatorics-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/194/mathematical-logic-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/195/mathematical-logic-gate2020-previous-gate-2",
        "https://gateoverflow.in/exam/196/graph-theory-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/87/set-theory-%26-algebra-previous-gate-1",
        "https://gateoverflow.in/exam/69/graph-theory-previous-gate-1"
    ],
    "Progress": "Not Started"
},
"Linear Algebra (LA)": {
    "Topics": ["Matrix Operations", "Vector Spaces", "Eigenvalues and Eigenvectors"],
    "YouTube": ["https://youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_&si=VpylHczkW8ylqspx"],
    "PYQs": ["https://github.com/GATEOverflow/GO-PDFs/releases/tag/gatecse-2025"],
    "NPTEL": ["https://youtube.com/playlist?list=PLFW6lRTa1g80fZ1giRbqbe_XdXPdkkyqY&si=l3-KeMND-CfmrJzv"],
    "Textbooks": ["Videos for intuition: https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=YAaXZ9srWqvlpwz8"],
    "Free Tests": [
        "https://gateoverflow.in/exam/598/go-classes-2025-weekly-quiz-3-fundamental-course-and-linear-algebra",
        "https://gateoverflow.in/exam/600/go-classes-2025-weekly-quiz-4-linear-algebra",
        "https://gateoverflow.in/exam/606/go-classes-2025-common-weekly-quiz-5-linear-algebra",
        "https://gateoverflow.in/exam/68/linear-algebra-previous-gate-1",
        "https://gateoverflow.in/exam/161/linear-algebra-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/162/linear-algebra-gate2020-previous-gate-2"
    ],
    "Progress": "Not Started"
},
"Probability": {
    "Topics": ["Conditional Probability", "Random Variables", "Probability Distributions"],
    "YouTube": ["https://youtube.com/playlist?list=PLhLZ_zxDsyOIKbQfKFM05BLYRhUZ7JP-M&si=PhhEGh77ahUsqikf"],
    "PYQs": ["https://github.com/GATEOverflow/GO-PDFs/releases/tag/gatecse-2025"],
    "NPTEL": ["https://youtube.com/playlist?list=PLyqSpQzTE6M_JcleDbrVyPnE0PixKs2JE&si=o0htQ1hAn60vNLRK"],
    "Textbooks": ["Introduction to probability models / Sheldon M. Ross"],
    "Free Tests": [
        "https://gateoverflow.in/exam/623/go-classes-cs-da-2025-weekly-quiz-6-conditional-probability",
        "https://gateoverflow.in/exam/628/go-classes-2025-weekly-quiz-13-probability-distributions",
        "https://gateoverflow.in/exam/67/probability-previous-gate-1",
        "https://gateoverflow.in/exam/159/probability-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/160/probability-gate2020-previous-gate-2"
    ],
    "Progress": "Not Started"
},
"Calculus": {
    "Topics": ["Limits", "Derivatives", "Integrals"],
    "YouTube": ["Mohit Tyagi YT videos (All videos are not relevant for GATE, I will list out the relevant videos soon)"],
    "PYQs": ["https://github.com/GATEOverflow/GO-PDFs/releases/tag/gatecse-2025"],
    "NPTEL": ["https://youtube.com/playlist?list=PLEAYkSg4uSQ0q9CDkHkJGdUTQOgH1DLDj&si=Rt5U9aaad4jiXdT_"],
    "Textbooks": ["Khan Academy: https://www.khanacademy.org/math/calculus-1"],
    "Free Tests": [
        "https://gateoverflow.in/exam/659/go-classes-2025-weekly-quiz-21-calculus",
        "https://gateoverflow.in/exam/164/calculus-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/159/probability-gate2020-previous-gate-1",
        "https://gateoverflow.in/exam/160/probability-gate2020-previous-gate-2"
    ],
    "Progress": "Not Started"
},
"Aptitude": {
    "Topics": ["General Aptitude"],
    "YouTube": ["Resources, Short Notes, List of Topics: https://youtu.be/IADuDzccEOI?si=nNrS9v50ORGVxLgN"],
    "Free Tests": [
        "https://gateoverflow.in/exam/610/go-classes-2025-monthly-quiz-1-general-aptitude",
        "https://gateoverflow.in/exam/631/go-classes-cs-da-2025-monthly-quiz-2-general-aptitude",
        "https://gateoverflow.in/exam/660/go-classes-cs-da-2025-monthly-quiz-3-general-aptitude",
        "https://gateoverflow.in/exam/36/go2017-aptitude-1",
        "https://gateoverflow.in/exam/64/general-aptitude-set-2"
    ],
    "Progress": "Not Started"
},
"Free Mock Tests": {
    "Topics": ["Full Length Mock Tests"],
    "Free Tests": [
        "https://gateoverflow.in/exam/70/go-17-mock-1",
        "https://gateoverflow.in/exam/73/go-17-mock-2",
        "https://gateoverflow.in/exam/74/go-17-mock-3",
        "https://gateoverflow.in/exam/79/go-18-mock-4",
        "https://gateoverflow.in/exam/126/test-by-ruturaj-mock-1",
        "https://gateoverflow.in/exam/136/applied-course-2019-mock1"
    ],
    "Progress": "Not Started"
},
"Notes": {
    "Topics": ["Notes from standard books for GATE CSE"],
    "Resources": [
        "Notes from standards books for GATE CSE: https://drive.google.com/drive/folders/1oGCYictHLqXE1skdkJ8PnaefBnLrRXwG",
        "Handwritten Notes: https://github.com/baquer/GATE-and-CSE-Resources-for-Students/blob/master/AnkurGuptaNotes/CompilerDesign.pdf",
        "Short Notes & Imp Questions: https://youtu.be/9HAxjug36wA?si=IkgiP3lGFiZYKAl7"
    ],
    "Progress": "Not Started"
},
"Crash Course": {
    "Topics": ["Quick revision resources for all subjects"],
    "Resources": {
        "Operating System": ["[Watch Playlist](https://youtube.com/playlist?list=PL3eEXnCBViH8YECjupENQvZRMOebYS0gX)"],
        "Computer Organization and Architecture": ["[Watch Playlist](https://youtube.com/playlist?list=PL3eEXnCBViH8OS7fH0uQdre5YGCIOhCBH)"],
        "Computer Networks": ["[Watch Playlist](https://youtube.com/playlist?list=PL3eEXnCBViH-AnU_c_8uFSaMK1OfgtDGx)"],
        "Compiler Design": [
            "[Watch Video 1](https://www.youtube.com/live/2Qdhlo1513g)",
            "[Watch Video 2](https://www.youtube.com/live/xPodJ4K4gLA)",
            "[Watch Video 3](https://www.youtube.com/live/OV2c7-NWMzY)"
        ],
        "Theory of Computation": ["[Watch Playlist](https://youtube.com/playlist?list=PL3eEXnCBViH89Y1BopKeXyR-p8CTFwL-i)"],
        "C-Programming": ["[Watch Playlist](https://youtube.com/playlist?list=PL3eEXnCBViH8K0AXG2fFkAhpNqI46emmI)"],
        "Data Structures": ["[Watch Playlist](https://youtube.com/playlist?list=PL3eEXnCBViH8qQtEEoN7iy8ldG9uaYknF)"],
        "Algorithms": ["[Watch Playlist](https://youtube.com/playlist?list=PL3eEXnCBViH_u3nCabMcv-6_D13Hky1Rx)"],
        "Digital Logic": ["[Watch Playlist](https://youtube.com/playlist?list=PL3eEXnCBViH8l2irvvEt4I_fjIirSlvxp)"],
        "Database Management System": ["[Watch Playlist](https://youtube.com/playlist?list=PL3eEXnCBViH86UibANMiagfbS72MxXusX)"],
        "Discrete Maths": ["[Watch Playlist](https://youtube.com/playlist?list=PL3eEXnCBViH_Vy3CLfkxM_wsGrKoX8dVc)"],
        "Engineering Mathematics": ["[Watch Playlist](https://youtube.com/playlist?list=PLvTTv60o7qj-9sbN77ueWdwL34cOmBPCi)"],
        "Aptitude": ["[Watch Playlist](https://youtube.com/playlist?list=PLvTTv60o7qj_JEKht0r0JYBPeV8OmPH2X)"]
    },
    "Progress": "Not Started"
},
}


# Initialize subject progress if not already set
for subject in subjects:
    if subject not in st.session_state.subject_progress:
        st.session_state.subject_progress[subject] = "Not Started"

# Sidebar Content
def add_sidebar_navigation():
    today = datetime.date.today()
    st.sidebar.markdown(f"""
        <div class="sidebar-title">📅 {today.strftime('%B %d, %Y')} ({today.strftime('%A')})</div>
    """, unsafe_allow_html=True)

    # Study Log Section
    if st.session_state.page != "new_page":
        st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-section-title">📘 Study Log</div>', unsafe_allow_html=True)
        subject = st.sidebar.selectbox("Select Subject", list(subjects.keys()), key="subject_select_sidebar")  # Include all subjects
        study_time = st.sidebar.slider("Study Hours", 0.0, 12.0, 0.0, 0.5, key="study_slider_sidebar", help="Log your study hours for today.")
        if st.sidebar.button("✅ Submit Study Log", key="submit_study_sidebar", help="Submit today's study log."):
            submit_study_log(st.session_state.username, subject, study_time, today.strftime("%Y-%m-%d"))
            st.success("Study log submitted!")
        st.sidebar.markdown('</div>', unsafe_allow_html=True)


    # Weekly Stats Section
    if st.session_state.study_log and st.session_state.page != "new_page":
        df = pd.DataFrame(st.session_state.study_log)
        df = df.drop_duplicates(subset=["Date", "subject"], keep="last")
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values(by="Date", ascending=False).head(7)
        st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-section-title">📊 Weekly Stats</div>', unsafe_allow_html=True)
        st.sidebar.dataframe(df.set_index("Date"), height=220, use_container_width=True)
        st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Navigation Section
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-section-title">🔀 Navigation</div>', unsafe_allow_html=True)

    # Always show "Back to Dashboard" button
    if st.sidebar.button("🏠 Back to Dashboard", key="back_to_dashboard_sidebar", help="Return to the main dashboard."):
        st.session_state.page = "dashboard"

    # Additional navigation options for the dashboard page
    if st.session_state.page == "dashboard":
        if st.sidebar.button("🗓️ Daywise Timetable", key="daywise_timetable", help="View your daywise timetable."):
            st.session_state.page = "daywise"
        if st.sidebar.button("📆 Weekwise Timetable", key="weekwise_timetable", help="View your weekwise timetable."):
            st.session_state.page = "weekwise"
        if st.sidebar.button("📄 Notes Section", key="notes_section", help="Access your notes section."):
            st.session_state.page = "notes"
        if st.sidebar.button("📊 Weekly Pie Chart", key="weekly_pie_chart", help="View your weekly performance pie chart."):
            st.session_state.page = "pie_chart"
        if st.sidebar.button("➡️ Next: Courses Tracker", key="go_to_courses_page", help="Go to your ongoing course roadmaps."):
            st.session_state.page = "new_page"

# ----------HOME PAGES ----------
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
    0% {
        opacity: 0;
        transform: translateY(-20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
""", unsafe_allow_html=True)


    st.markdown('<div class="custom-title">📊 Welcome to GATE CSE Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subtitle">Prepare smart, stay consistent & crack GATE 🚀</div>', unsafe_allow_html=True)

    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Go to Dashboard", key="go_dashboard"):
        st.session_state.page = "dashboard"
    st.markdown('</div>', unsafe_allow_html=True)

def dashboard_page():
    st.markdown('<h2 class="custom-title">📚 Subject-wise Study Resources</h2>', unsafe_allow_html=True)

    # ✅ GATE Deadline Timer - Shown only on dashboard
    deadline = datetime.datetime(2026, 2, 15, 0, 0, 0)
    now = datetime.datetime.now()
    time_left = deadline - now

    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    countdown_html = f"""
    <div class="countdown-container" style="position: relative; margin-top: 20px; margin-bottom: 30px; width: fit-content; background-color: rgba(0, 0, 0, 0.7); color: white; padding: 12px 20px; border-radius: 8px; font-family: 'Segoe UI', sans-serif; font-size: 16px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);">
        <div class="countdown-title">🎯 GATE Deadline Countdown</div>
        <div class="countdown-time">⏳ {days} Days, {hours} Hours, {minutes} Minutes, {seconds} Seconds left!</div>
    </div>
    """
    st.markdown(countdown_html, unsafe_allow_html=True)

    # Motivational Quotes Section
    if "show_motivation" not in st.session_state:
        st.session_state.show_motivation = True

    motivational_quotes = [
        "💡 Stay focused, stay positive, and never stop learning. You’ve got this!",
        "📚 One day, all your hard work will pay off. Keep going!",
        "🚀 Dreams don’t work unless you do. Keep grinding!",
        "🔥 Success is the sum of small efforts, repeated day in and day out.",
        "🎯 You are capable of amazing things. Believe in yourself!",
        "🏆 Your future is created by what you do today, not tomorrow.",
        "🌟 Push yourself, because no one else is going to do it for you.",
        "🧠 The expert in anything was once a beginner. Start now!"
    ]

    random_quote = random.choice(motivational_quotes)

    if st.session_state.show_motivation:
        st.markdown(f"""
            <style>
                .motivation-box {{
                    position: relative;
                    animation: fadeInTop 1s ease-in-out;
                    background-color: #f8f9fa;
                    padding: 15px 20px;
                    border-left: 4px solid #4dabf7;
                    border-radius: 10px;
                    margin-bottom: 25px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                    font-family: 'Segoe UI', sans-serif;
                }}

                .motivation-text {{
                    font-size: 16px;
                    color: #1d3557;
                    font-weight: 500;
                }}

                @keyframes fadeInTop {{
                    0% {{
                        opacity: 0;
                        transform: translateY(-20px);
                    }}
                    100% {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}
            </style>

            <div class="motivation-box">
                <div class="motivation-text">{random_quote}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("")  # Add spacing
        if st.button("✖️ Hide Message"):
            st.session_state.show_motivation = False

    # Sidebar Content
    add_sidebar_navigation()

    # Subject-wise cards
    for subject, data in subjects.items():
        with st.expander(f"📘 {subject}"):
            st.markdown("**📌 Topics Covered:**")
            st.markdown(", ".join(data["Topics"]))

            if data.get("YouTube"):
                st.markdown("📺 **YouTube Playlist:**")
                for link in data["YouTube"]:
                    st.markdown(f"- [Watch]({link})")

            if data.get("NPTEL"):
                st.markdown("🎓 **NPTEL Courses:**")
                for link in data["NPTEL"]:
                    st.markdown(f"- [View]({link})")

            if data.get("Textbooks"):
                st.markdown("📖 **Recommended Textbooks:**")
                for book in data["Textbooks"]:
                    st.markdown(f"- {book}")

            if data.get("Free Tests"):
                st.markdown("📝 **Free Tests:**")
                for test in data["Free Tests"]:
                    st.markdown(f"- [Take Test]({test})")

            # Safely access the "Free Tests" key using .get() to avoid KeyError
            free_tests = data.get("Free Tests", [])  # Default to an empty list if "Free Tests" is missing
            for i, test_link in enumerate(free_tests):
                unique_key = f"{subject}_{i}_{id(test_link)}"  # Add a unique identifier using id()
                if st.button(f"Attempt Test {i+1}", key=unique_key):
                    st.session_state.attempted_tests.setdefault(subject, set()).add(i)
                    st.success("Marked as attempted!")

            # 🔄 Progress Status
            total = len(free_tests)
            attempted = len(st.session_state.attempted_tests.get(subject, set()))
            if attempted == 0:
                progress = "🔘 Not Started"
            elif attempted < total:
                progress = "🟡 In Progress"
            else:
                progress = "🟢 Completed"

            st.markdown(f"### 📈 Progress: {progress}")
    # Fix for Notes section
    if "Notes" in subjects:
        with st.expander("📘 Notes"):
            st.markdown("**📌 Topics Covered:**")
            st.markdown(", ".join(subjects["Notes"]["Topics"]))

            if subjects["Notes"].get("Resources"):
                st.markdown("📖 **Resources:**")
                for resource in subjects["Notes"]["Resources"]:
                    st.markdown(f"- [View Resource]({resource.split(': ')[1]})")

    # Fix for Crash Course section
    if "Crash Course" in subjects:
        with st.expander("📘 Crash Course"):
            st.markdown("**📌 Topics Covered:**")
            st.markdown(", ".join(subjects["Crash Course"]["Topics"]))

            if subjects["Crash Course"].get("Resources"):
                st.markdown("📖 **Resources:**")
                for topic, resources in subjects["Crash Course"]["Resources"].items():
                    st.markdown(f"### {topic}")
                    for resource in resources:
                        st.markdown(f"- {resource}")

            # Progress calculation for Crash Course
            total_resources = sum(len(resources) for resources in subjects["Crash Course"]["Resources"].values())
            attempted_resources = len(st.session_state.attempted_tests.get("Crash Course", set()))
            if attempted_resources == 0:
                progress = "🔘 Not Started"
            elif attempted_resources < total_resources:
                progress = "🟡 In Progress"
            else:
                progress = "🟢 Completed"

            st.markdown(f"### 📈 Progress: {progress}")

    

# ---------- Daywise Timetable Page ----------
def daywise_timetable_page():
    add_sidebar_navigation()
    st.title("🗓️ Daywise Time Table")

    time_slots = [
        ("8:00 AM - 9:30 AM", "", "Not Done"),
        ("9:45 AM - 10:45 AM", "", "Not Done"),
        ("11:30 AM - 1:00 PM", "", "Not Done"),
        ("2:00 PM - 4:00 PM", "", "Not Done"),
        ("4:30 PM - 5:30 PM", "", "Not Done"),
        ("5:30 PM - 7:00 PM", "", "Not Done"),
        ("8:00 PM - 10:00 PM", "", "Not Done"),
        ("10:30 PM - 12:00 AM", "", "Not Done")
    ]

    df = pd.DataFrame(time_slots, columns=["Time", "Subject(s)", "Status"])
    for i in range(len(df)):
        df.at[i, "Subject(s)"] = st.text_input(f"Time Slot {df.at[i, 'Time']}", df.at[i, "Subject(s)"])
        df.at[i, "Status"] = st.selectbox(f"Status for {df.at[i, 'Subject(s)']}", ["Not Done", "Done"], key=f"day_status_{i}")
    st.dataframe(df)

def weekwise_timetable():
    add_sidebar_navigation()
    weeks = list(range(1, 105))

    weekwise_df = pd.DataFrame({
        'Week Number': weeks,
        'Subjects': [''] * len(weeks),
        'Status': [''] * len(weeks)
    })

    subjects_for_weeks = []
    
    for i in range(len(weekwise_df)):
        week = weekwise_df.at[i, 'Week Number']
        st.subheader(f"Week {week} Subjects")
        
        subjects_input = st.text_area(f"Enter subjects for Week {week} (comma-separated):", "")
        subjects = [subject.strip() for subject in subjects_input.split(',') if subject.strip()]
        
        if subjects:
            for j, subject in enumerate(subjects):
                st.write(f"Subject {j + 1}: {subject}")
                status = st.selectbox(f"Did you complete {subject}?", ["Not Completed", "Completed"], key=f"status_week_{week}_{j}")
                subjects_for_weeks.append((week, subject, status))

        weekwise_df.at[i, 'Subjects'] = ", ".join(subjects)
        weekwise_df.at[i, 'Status'] = ", ".join([status for _, _, status in subjects_for_weeks if _ == week])

    return weekwise_df

# Notes Section
def notes_section():
    add_sidebar_navigation()
    st.title("📄 Notes Section")
    subject = st.selectbox("📘 Select Subject for Notes", list(subjects.keys()), key="notes_subject_select")

    note_key = f"notes_{subject}"
    
    if note_key not in st.session_state:
        st.session_state[note_key] = ""
    
    notes_input = st.text_area(f"📝 Notes for {subject}", st.session_state[note_key], height=200)

    if st.button("💾 Save Notes", key="save_notes_button"):
        st.session_state[note_key] = notes_input
        st.success("Notes saved successfully!")

    if st.session_state[note_key]:
        st.subheader(f"📖 Your Notes for {subject}")
        st.write(st.session_state[note_key])
    else:
        st.info("No notes saved yet. Start writing your notes!")

# Weekly Pie Chart Section
def weekly_pie_chart():
    add_sidebar_navigation()
    st.title("📊 Weekly Performance Pie Chart")

    logs = get_study_logs(st.session_state.username)
    if logs:
        df = pd.DataFrame(logs, columns=["Subject", "Hours", "Date"])
        df["Date"] = pd.to_datetime(df["Date"])
        last_week = df[df["Date"] >= (datetime.datetime.now() - datetime.timedelta(days=7))]
        
        if not last_week.empty:
            subject_hours = last_week.groupby("Subject")["Hours"].sum()

            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(subject_hours, labels=subject_hours.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
            ax.axis("equal")
            st.pyplot(fig)
        else:
            st.info("No study data available for the last 7 days.")
    else:
        st.info("No study data available. Start logging your study hours!")


# ---------- NEW PAGE: Ongoing Courses Tracker ----------
def new_page():
    add_sidebar_navigation()
    st.title("📚 Ongoing Courses Tracker")
    st.markdown("""
        This page contains all the ongoing courses and their detailed roadmaps.
        Select a course from the sidebar to view its roadmap.
    """)

    st.markdown("""
    <style>
        /* General Styling */
        .stApp {
            font-family: 'Segoe UI', sans-serif;
            background-color: #lf5f7fa;
        }

        /* Page Title Styling */
        .new-page-title {
            font-size: 36px;
            font-weight: bold;
            color: #0d47a1;
            text-align: center;
            margin-bottom: 20px;
            animation: fadeInDown 1.5s ease-in-out;
        }

        /* Section Title Styling */
        .section-title {
            font-size: 24px;
            font-weight: bold;
            color: #1565c0;
            margin-top: 30px;
            margin-bottom: 10px;
            animation: fadeIn 1s ease-in-out;
        }

        /* Card Styling */
        .course-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            animation: fadeInUp 1s ease-in-out;
        }

        .course-card:hover {
            transform: scale(1.02);
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease-in-out;
        }

        /* Button Styling */
        .stButton > button {
            background-color: #1976d2;
            color: white;
            font-size: 16px;
            padding: 10px;
            border: none;
            border-radius: 8px;
            width: 100%;
            text-align: center;
            transition: all 0.3s ease-in-out;
        }

        .stButton > button:hover {
            background-color: #0d47a1;
            transform: scale(1.05);
            box-shadow: 0px 4px 12px rgba(13, 71, 161, 0.3);
        }

        /* Animations */
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }

        @keyframes fadeInDown {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInUp {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* Responsive Design */
        @media only screen and (max-width: 768px) {
            .new-page-title {
                font-size: 28px;
            }
            .section-title {
                font-size: 20px;
            }
            .course-card {
                padding: 15px;
            }
        }
    </style>
""", unsafe_allow_html=True)


    # Sample Course Data
    course_data = {
        "Data structure and algorithm": [
            ("📄 Striver’s A2Z DSA Course Sheet","https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2"),
            ("YouTube link","https://youtube.com/playlist?list=PLfqMhTWNBTe137I_EPQd34TsgV6IO55pt"),

            ("📅 Week 1-2: C++ Basics + Time Complexity", "✅ Topics:\n• Variables, Data Types, Input/Output\n• Conditionals, Loops, Functions, Arrays\n• Pointers, Reference Variables\n• Time & Space Complexity\n📘 Books:\n• Let Us C++ by Yashwant Kanetkar\n• Programming in C++ by Balagurusamy (Optional)\n💻 Practice:\n• GFG – C++ Basics\n• Hackerrank – C++ Practice"),
            ("📅 Week 3: Patterns + Arrays", "Topics:\n• Star & Number Patterns (loops)\n• 1D Arrays, 2D Arrays\n• Array operations: Max/Min, Reverse, Sorting basics\n💻 Practice:\n• GFG Patterns\n• LeetCode Easy Array Problems"),
            ("📅 Week 4: Searching + Sorting", "✅ Topics:\n• Linear & Binary Search\n• Bubble, Selection, Insertion Sort\n• In-built sort, Custom comparator\n• Count Sort, Merge Sort, Quick Sort\n💻 Practice:\n• GeeksforGeeks Searching\n• GeeksforGeeks Sorting\n• LeetCode Sorting"),
            ("📅 Week 5: Strings", "✅ Topics:\n• String basics\n• Palindrome, Substrings, String Reversal\n• ASCII values, Character arrays\n• STL string functions\n💻 Practice:\n• GeeksforGeeks Strings Practice\n• LeetCode String Problems"),
            ("📅 Week 6: STL (Standard Template Library)", "✅ Topics:\n• Vectors, Pairs\n• Sets, Maps, Unordered Maps\n• Stacks, Queues, Priority Queues\n• Iterators and Algorithms\n💻 Practice:\n• GFG – C++ STL\n• Codeforces STL-based Problems"),
            ("📅 Week 7: Recursion + Backtracking", "✅ Topics:\n• Basic recursion (factorial, fibonacci)\n• Subsets, Permutations\n• N-Queens, Sudoku Solver\n• Rat in Maze\n💻 Practice:\n• GeeksforGeeks Recursion Problems\n• LeetCode Backtracking"),
            ("📅 Week 8: Linked Lists", "✅ Topics:\n• Singly and Doubly Linked List\n• Insertion, Deletion, Reversal\n• Cycle Detection (Floyd’s)\n• Merge Two Sorted LL\n💻 Practice:\n• GeeksforGeeks LL Problems\n• LeetCode LL Tag"),
            ("📅 Week 9: Stacks + Queues", "✅ Topics:\n• Stack operations (Array + LL)\n• Infix/Prefix/Postfix Expressions\n• Queue + Circular Queue + Deque\n• Stack using Queues / Queues using Stacks\n💻 Practice:\n• GFG Stack Problems\n• GFG Queue Problems"),
            ("📅 Week 10: Trees + Binary Search Tree (BST)", "✅ Topics:\n• Binary Tree basics + traversals\n• Height, Diameter, Mirror Tree\n• BST Insert/Delete/Search\n• Lowest Common Ancestor\n💻 Practice:\n• LeetCode Tree Problems\n• GFG Tree Problems"),
            ("📅 Week 11: Heaps + Hashing", "✅ Topics:\n• Min/Max Heaps\n• Heap sort, Priority Queue\n• Hash Table, Hash Map, Collision Handling\n• Frequency Maps\n💻 Practice:\n• GFG Hashing\n• LeetCode Heap Problems"),
            ("📅 Week 12: Graphs – Basics to Advanced", "✅ Topics:\n• Graph Representations (Adjacency List/Matrix)\n• BFS, DFS\n• Detect Cycle (Directed/Undirected)\n• Topological Sort, Shortest Path (Dijkstra, Bellman-Ford)\n• Disjoint Set Union (DSU), Kruskal’s & Prim’s Algorithm\n💻 Practice:\n• GFG Graphs Practice\n• LeetCode Graph Problems"),
            ("📅 Week 13: Dynamic Programming (DP)", "✅ Topics:\n• Memoization & Tabulation\n• 0/1 Knapsack, Subset Sum\n• LIS, LCS, Edit Distance\n• DP on Grids, Trees, Bitmasking\n💻 Practice:\n• GFG DP Problems\n• LeetCode Dynamic Programming"),
            ("🧠 Ongoing: Problem Solving Practice", "• Start solving 1-2 problems daily on:\n  o LeetCode\n  o Codeforces\n  o GeeksforGeeks Practice\n  o InterviewBit\n• Focus on variety: easy ➝ medium ➝ hard."),
            ("📘 Recommended Books", "Book\tPurpose\nData Structures and Algorithms Made Easy – Narasimha Karumanchi\tConcept clarity\nCracking the Coding Interview – Gayle Laakmann McDowell\tInterview prep\nIntroduction to Algorithms – Cormen (CLRS)\tAdvanced reference\nLet Us C++ – Yashwant Kanetkar\tBeginner-level C++"),
            ("📑 Cheat Sheets & Notes", "• GFG DSA Sheet\n• Striver’s A2Z DSA Sheet\n• Neetcode Patterns"),
            ("🧭 Additional Tips", "• ✅ Practice Dry Run every concept before coding\n• ✅ Create your own handwritten notes — recall becomes 10x easier\n• ✅ Focus more on solving medium-level problems after 4 weeks\n• ✅ Keep a GitHub repo for all your code – helps in placements!\n• ✅ Do 2 mock interviews with friends or on platforms like Pramp")
        ],
        "Python": [
            ("Youtube link", "https://youtu.be/UrsmFxEIp5k?amp;si=qg_Vng-RM8Pz4p9J"),
            ("💡 Total Duration", "12–16 weeks (customize as per your pace)"),
            ("📌 Ideal for", "Beginners, College Students, Developers, and Data Enthusiasts"),
            ("✅ Outcome", "Strong in Python syntax, logic building, OOPs, projects, and real-world applications"),
            ("🔰 Phase 1: Python Basics (Week 1-2)", "🧠 What to Learn:\n• Installing Python + IDE (PyCharm / VS Code / Jupyter)\n• Variables, Data Types (int, float, str, bool)\n• Input/output, Type Casting\n• Conditionals (if-else), Loops (for, while)\n• Functions & Scoping\n🔗 Resources:\n• Book: Automate the Boring Stuff with Python (1st few chapters)\n• Practice: HackerRank Python Basics"),
            ("🗃️ Phase 2: Data Structures & Algorithms in Python (Week 3-5)", "🧠 What to Learn:\n• Lists, Tuples, Sets, Dictionaries\n• String Manipulation\n• Searching & Sorting (Bubble, Insertion, Merge)\n• Time Complexity Basics\n• Recursion\n🔗 Practice:\n• LeetCode Easy Problems\n• GFG Python DSA Sheet"),
            ("🎯 Phase 3: Object-Oriented Programming (Week 6)", "🧠 What to Learn:\n• Classes & Objects\n• __init__ constructor\n• self, Instance vs Class variables\n• Inheritance, Polymorphism\n• Encapsulation, Abstraction\n• @staticmethod, @classmethod\n🔗 Resources:\n• Book: Python Crash Course by Eric Matthes (OOP Chapter)\n• Practice: Make a simple Bank, Student, or Employee Management System"),
            ("⚙️ Phase 4: File Handling, Errors, Modules (Week 7)", "🧠 What to Learn:\n• Reading/writing .txt, .csv, .json files\n• try-except, Exception types\n• Creating and using custom modules\n• Built-in modules: math, random, datetime, os, sys"),
            ("🌐 Phase 5: Python Libraries for Projects (Week 8-9)", "🧠 What to Learn:\n• Web requests: requests, BeautifulSoup\n• Automation: os, shutil, time, pyautogui\n• Data: pandas, numpy, matplotlib (basic usage)"),
            ("🖥️ Phase 6: GUI & Web Development Basics (Optional)", "🧠 What to Explore:\n• GUI with tkinter\n• Basics of Flask for web apps\n• REST APIs with Flask"),
            ("🧪 Phase 7: Testing & Environment (Week 10)", "🧠 What to Learn:\n• Virtual environments (venv, pip)\n• Unit Testing (unittest)\n• Code formatting (black, flake8)"),
            ("💻 Phase 8: Projects & Practice (Week 11-13)", "👨‍💻 Beginner Project Ideas:\n• Calculator or To-Do App (Tkinter or CLI)\n• Dice Roller / Rock Paper Scissors Game\n• Contact Book / Notes App\n• PDF & Excel Automation Script\n• Web Scraper for News / Weather\n👩‍💼 Intermediate Projects:\n• Resume Parser\n• Weather Dashboard using API\n• Blog Website using Flask\n• Data Dashboard with Pandas + Matplotlib"),
            ("📦 Phase 9: GitHub Portfolio + Resume (Week 14)", "📌 What to Do:\n• Push all projects to GitHub\n• Add README files and documentation\n• Create a Python resume for job/internships\n• Write blogs on Medium / Dev.to"),
            ("📚 Recommended Python Books", "1. Automate the Boring Stuff with Python – Al Sweigart\n2. Python Crash Course – Eric Matthes\n3. Fluent Python – Luciano Ramalho (Advanced)\n4. Effective Python – Brett Slatkin"),
            ("🧠 Practice Platforms", "• LeetCode – Problem Solving\n• HackerRank – Python Practice\n• Codewars – Coding Challenges\n• Replit – Cloud IDE\n• Kaggle – Python Notebooks & Projects"),
            ("📈 Career Paths After Python", "Domain\tMust-Learn After Python\nData Analyst\tPandas, Excel, Power BI, SQL\nWeb Developer\tFlask / Django, HTML, JS, DBMS\nData Scientist\tNumpy, Scikit-learn, ML, Deep Learning\nAutomation / QA\tSelenium, PyAutoGUI, Requests\nGame Developer\tPyGame")
        ],
        "Data Analyst": [
            ("Youtube link", "https://youtu.be/VaSjiJMrq24?amp;si=4t84V9l-w-qNA2xI"),
            ("🎯 Goal", "Become a Job-Ready Data Analyst with skills in Data Cleaning, Analysis, Visualization, Excel, SQL, Python, Statistics, and real-world project experience."),
            ("📅 Week 1-2: Introduction to Data Analytics & Excel/Sheets", "🔍 What to Learn:\n• What does a Data Analyst do?\n• Introduction to spreadsheets\n• Excel formulas (SUM, IF, VLOOKUP, INDEX-MATCH, etc.)\n• Charts & Pivot Tables\n📚 Resources:\n• Book: Excel 2021 Bible by Michael Alexander\n• Kaggle: Excel Course\n• Practice: Use dummy sales datasets and create dashboards"),
            ("📅 Week 3-4: SQL for Data Analysts", "🔍 What to Learn:\n• Basics of SQL (SELECT, WHERE, GROUP BY, JOIN)\n• Aggregations & Window Functions\n• CTEs, Subqueries, Nested Queries\n🛠️ Tools:\n• MySQL / PostgreSQL / BigQuery / SQLite (any one)\n📚 Resources:\n• Platform: Mode Analytics SQL Tutorial\n• Practice: LeetCode SQL, StrataScratch"),
            ("📅 Week 5-7: Python for Data Analysis", "🔍 What to Learn:\n• Python Basics: Variables, Loops, Functions, Data Types\n• NumPy and Pandas (DataFrames, Series, filtering, grouping, joins)\n• Matplotlib & Seaborn for visualizations\n📚 Resources:\n• Book: Python for Data Analysis by Wes McKinney\n• Platform: Kaggle Python Course, Pandas Tutorial\n💻 Practice:\n• Analyze Titanic, Netflix, COVID datasets\n• Clean and visualize datasets with Pandas"),
            ("📅 Week 8-9: Data Cleaning + EDA (Exploratory Data Analysis)", "🔍 What to Learn:\n• Handling nulls, duplicates, outliers\n• Data normalization, date-time parsing\n• Grouping, filtering, sorting for insight\n• Correlation, summary stats\n📚 Resources:\n• Data Cleaning Course – Kaggle\n• EDA with Pandas"),
            ("📅 Week 10-11: Data Visualization & Dashboards", "🔍 What to Learn:\n• Visualization Principles: Storytelling with Data\n• Excel Dashboards\n• Python Dashboards (Matplotlib, Seaborn)\n• Introduction to Power BI / Tableau\n📚 Resources:\n• Book: Storytelling with Data by Cole Nussbaumer Knaflic\n• Platform: Power BI Learning, Tableau Public"),
            ("📅 Week 12: Statistics for Data Analysts", "🔍 What to Learn:\n• Descriptive Statistics (Mean, Median, Mode, Std Dev)\n• Probability Basics, Distributions\n• Hypothesis Testing, Confidence Intervals\n• A/B Testing\n📚 Resources:\n• Book: Practical Statistics for Data Scientists\n• Platform: Khan Academy Statistics"),
            ("📅 Week 13: Business Acumen & Case Studies", "🔍 What to Learn:\n• Domain knowledge: Sales, Marketing, HR, Finance\n• How data analytics supports business decisions\n• Real case studies & dashboards\n📚 Resources:\n• Maven Analytics Case Studies\n• Kaggle Datasets"),
            ("📅 Week 14-15: Projects & Portfolio Building", "🔍 Build at least 3 Projects:\n• Sales Dashboard (Excel + Power BI)\n• EDA Project (Python + Pandas + Seaborn)\n• SQL Reporting Dashboard\n📦 Upload to:\n• GitHub\n• Tableau Public / Power BI Service\n• Medium / LinkedIn blogs"),
            ("📅 Week 16: Resume, LinkedIn & Job Prep", "🧠 Practice:\n• SQL & Python interview questions\n• Statistics & Scenario-based questions\n• Mock Interviews & Portfolio Walkthrough\n📚 Resources:\n• Interview Query\n• Analytics Vidhya Blog"),
            ("🛠️ Key Tools to Learn", "Tool\tPurpose\nExcel / Sheets\tData cleaning, dashboards\nSQL\tQuerying databases\nPython (Pandas, NumPy)\tData manipulation\nPower BI / Tableau\tVisualization\nGitHub\tPortfolio & version control"),
            ("🧪 Practice Platforms", "• Kaggle\n• StrataScratch\n• LeetCode (SQL)\n• DataCamp\n• Hackerrank (SQL, Python)"),
            ("🔗 Bonus: Certifications (Optional but Helpful)", "• Google Data Analytics (Coursera)\n• IBM Data Analyst Professional Certificate\n• Microsoft Power BI Certification")
        ],
        "UI/UX": [
            ("YouTube Link","https://www.youtube.com/live/MGlKO2JrvxE?amp;si=KM22QHkOwxcaJGvz"),
            ("💡 Total Duration", "12-16 weeks (Customize based on pace)"),
            ("📌 Ideal for", "Beginners, College Students, Aspiring UI/UX Designers"),
            ("✅ Outcome", "Strong skills in User Research, Prototyping, Visual Design, UX Testing, and real-world projects"),
            ("🔰 Phase 1: Introduction to UI/UX Design (Week 1-2)", "🧠 What to Learn:\n• What is UI/UX Design?\n  o Difference between UI (User Interface) and UX (User Experience)\n  o Role of a UI/UX Designer\n  o Types of UI/UX Design (Mobile, Web, Interactive)\n• UI/UX Design Process:\n  o Research → Wireframe → Prototype → Testing → Final Design\n• Design Thinking Process:\n  o Empathize → Define → Ideate → Prototype → Test\n📚 Resources:\n• Book: Don't Make Me Think by Steve Krug\n• Platform: Coursera - Introduction to User Experience Design"),
            ("🎨 Phase 2: Basics of Design (Week 3-4)", "🧠 What to Learn:\n• Basic Design Principles:\n  o Contrast, Alignment, Repetition, Proximity\n  o Typography, Color Theory, Iconography\n  o White Space & Layouts\n• Introduction to User-Centered Design (UCD):\n  o How users interact with designs\n• Design Tools Introduction:\n  o Sketch, Adobe XD, Figma\n📚 Resources:\n• Book: The Design of Everyday Things by Don Norman\n• Platform: Figma - Getting Started\n• Practice: Create simple wireframes and layouts"),
            ("🖥️ Phase 3: User Research & Understanding Users (Week 5-6)", "🧠 What to Learn:\n• User Research Basics:\n  o Importance of understanding user needs and pain points\n  o Conducting user interviews, surveys, and focus groups\n  o User Personas\n• Journey Mapping:\n  o How users interact with your product at each step\n  o Mapping customer touchpoints\n• Competitive Analysis:\n  o Analyzing competitors' products to find areas of improvement\n📚 Resources:\n• Book: Lean UX by Jeff Gothelf\n• Platform: NNG UX Research Resources"),
            ("🔧 Phase 4: Wireframing & Prototyping (Week 7-8)", "🧠 What to Learn:\n• Wireframing:\n  o Creating low-fidelity wireframes for layout structure\n  o Tools: Figma, Balsamiq, Sketch\n• Prototyping:\n  o Making interactive prototypes to simulate user flow and interactivity\n  o Tools: Figma, InVision, Adobe XD\n• UI Kit:\n  o Using pre-designed UI kits for faster prototyping\n📚 Resources:\n• Platform: Figma - Prototyping Tutorials\n• Practice: Design basic screens for a mobile app (Login, Dashboard, Settings)"),
            ("🖌️ Phase 5: UI Design Basics & Visual Design (Week 9-10)", "🧠 What to Learn:\n• UI Design Basics:\n  o Button styles, input fields, navigation, icons, forms, and cards\n  o Consistent typography and color schemes\n• Design for Web and Mobile:\n  o Responsive design principles (Desktop vs. Mobile)\n  o Mobile-first design\n• Advanced Visual Design:\n  o Animation in UI (Microinteractions)\n  o Designing with a grid system\n📚 Resources:\n• Book: Refactoring UI by Adam Wathan & Steve Schoger\n• Platform: UI Design Course (Udemy)"),
            ("🔍 Phase 6: UX Testing & Iteration (Week 11)", "🧠 What to Learn:\n• Usability Testing:\n  o Conducting A/B testing and usability tests\n  o Gathering feedback through tools like Hotjar or UsabilityHub\n• Analyzing Feedback:\n  o Iterating on designs based on user feedback\n  o Refining prototypes\n• Accessibility (a11y):\n  o Designing for accessibility (WCAG standards, color contrast, etc.)\n📚 Resources:\n• Platform: UX Design Course - Interaction Design Foundation"),
            ("📈 Phase 7: Building a Portfolio (Week 12-13)", "🧠 What to Learn:\n• Creating a Portfolio:\n  o Showcase projects, wireframes, prototypes, and UI designs\n  o Document your design process (research, testing, iterations)\n• Presenting Your Work:\n  o Writing case studies that explain the problem, solution, and process\n  o Tools: Behance, Dribbble, or your personal website\n📚 Resources:\n• Dribbble (for inspiration and showcasing work)\n• Portfolio Guide - UX Design"),
            ("🚀 Phase 8: Job Preparation & Final Project (Week 14-16)", "🧠 What to Learn:\n• Interview Prep:\n  o Prepare for common UI/UX interview questions\n  o Build your design story and process walkthrough\n• Real-World Project:\n  o Work on a complete redesign of a website or app\n  o Show your understanding of the full design process from research to final visuals\n📚 Resources:\n• UX Design Interview Questions\n• Practice: Join design challenges on platforms like Daily UI"),
            ("📚 Recommended UI/UX Books", "1. Don't Make Me Think by Steve Krug\n2. The Design of Everyday Things by Don Norman\n3. Refactoring UI by Adam Wathan & Steve Schoger\n4. Lean UX by Jeff Gothelf\n5. The Elements of User Experience by Jesse James Garrett"),
            ("🧠 Practice Platforms", "• Dribbble - Inspiration & Showcasing\n• Behance - Portfolio Platform\n• UX Design - Blog & Tutorials\n• Figma Community - Templates & Design Files\n• Adobe XD - Free UI Design Tools\n• Interaction Design Foundation - UX/UI Courses"),
            ("📈 Portfolio Projects to Include", "• App Design: Design a food delivery or shopping app (UX/UI).\n• Website Redesign: Choose a website you believe can be improved (e.g., a small business, non-profit site).\n• Dashboard Design: Build a project management or data visualization dashboard.\n• Case Study: Showcase one end-to-end project (Research, Wireframing, Prototyping, Testing).")
        ],
        "JavaScript": [
            ("YouTube Link","https://youtube.com/playlist?list=PLGjplNEQ1it_oTvuLRNqXfz_v_0pq6unW&amp;si=5Jdk4KMXCZY4UsKk"),
            ("💡 Total Duration", "16-20 weeks (customize based on your pace)"),
            ("📌 Ideal for", "Beginners, College Students, Aspiring Full-Stack Developers"),
            ("✅ Outcome", "Proficiency in JavaScript fundamentals, React components, Next.js for server-side rendering, and MongoDB for database management"),
            ("🔰 Phase 1: JavaScript Basics (Week 1-4)", "🧠 What to Learn:\n• JavaScript Basics:\n  o Variables: let, const, var\n  o Data Types: Strings, Numbers, Arrays, Objects, Booleans\n  o Functions, Arrow Functions\n  o Conditional Statements: if, else, switch\n  o Loops: for, while, forEach\n  o Arrays Methods: map, filter, reduce\n  o Objects and Destructuring\n• DOM Manipulation:\n  o Selecting elements: getElementById, querySelector\n  o Events: click, mouseover, keydown, etc.\n  o Event listeners and DOM manipulation\n  o Modifying HTML and CSS with JavaScript\n• ES6+ Features:\n  o Template Literals\n  o Default Parameters\n  o Rest/Spread Operators\n  o async/await, Promises, Callbacks\n📚 Resources:\n• Book: Eloquent JavaScript by Marijn Haverbeke\n• Platform: MDN Web Docs - JavaScript Guide\n• Practice: JavaScript30 by Wes Bos"),
            ("⚡ Phase 2: Advanced JavaScript (Week 5-6)", "🧠 What to Learn:\n• Asynchronous JavaScript:\n  o Callbacks, Promises, async/await\n  o Handling errors with try-catch\n• JavaScript Concepts:\n  o Closures\n  o Prototypal Inheritance\n  o Modules in JavaScript\n  o this keyword and context\n• JavaScript Design Patterns:\n  o Singleton, Factory, Module, Observer\n• Advanced Array Methods:\n  o reduce, find, some, every, sort, concat\n📚 Resources:\n• Book: You Don’t Know JS (series)\n• Platform: JavaScript.info\n• Practice: LeetCode JavaScript Questions")
        ],
        "React/Next.js": [
            ("React Youtube link", "https://youtu.be/RGKi6LSPDLU?amp;si=wTBBKZ08Z2_kkseH"),
            ("Next.js Youtube link", "https://youtube.com/playlist?list=PLu0W_9lII9agtWvR_TZdb_r0dNI8-lDwG&amp;si=f6QRVVnTy9efyRsj"),
            ("💡 Total Duration", "16-20 weeks (customize based on your pace)"),
            ("📌 Ideal for", "Beginners, College Students, Aspiring Full-Stack Developers"),
            ("✅ Outcome", "Proficiency in JavaScript fundamentals, React components, Next.js for server-side rendering, and MongoDB for database management"),
            ("🔥 Phase 3: React Basics (Week 7-9)", "🧠 What to Learn:\n• React Fundamentals:\n  o What is React and why use it?\n  o JSX (JavaScript XML)\n  o Components (Functional vs. Class components)\n  o Props and State\n  o React Lifecycle Methods (for class components)\n• React Hooks:\n  o useState and useEffect\n  o Custom Hooks\n• Component Structure & Styling:\n  o Component-based architecture\n  o Styling in React (CSS Modules, Styled-components)\n• React Router:\n  o Routing and navigation\n  o Dynamic routes, Redirect, Route parameters\n📚 Resources:\n• Book: Learning React by Alex Banks and Eve Porcello\n• Platform: React Official Documentation\n• Course: Scrimba React Course\n• Practice: Frontend Mentor Challenges"),
            ("🚀 Phase 4: Advanced React (Week 10-12)", "🧠 What to Learn:\n• State Management:\n  o Context API vs. Redux\n  o Using Redux for state management\n  o useReducer and dispatch\n• Performance Optimization:\n  o Code splitting and lazy loading with React.lazy()\n  o useMemo and useCallback\n  o React's Suspense and Error Boundaries\n• Testing in React:\n  o Unit testing with Jest\n  o Testing React components with React Testing Library\n• Advanced React Patterns:\n  o Render Props\n  o Higher-Order Components (HOCs)\n📚 Resources:\n• Book: Fullstack React by Accomazzo, Murray, and Auerbach\n• Platform: React Patterns\n• Practice: Build a complex project like a To-Do List with Redux"),
            ("🌐 Phase 5: Next.js Basics (Week 13-14)", "🧠 What to Learn:\n• What is Next.js?\n  o Introduction to Next.js and its features (SSR, SSG, ISR)\n  o Pages and Static Site Generation (SSG)\n  o Dynamic Routing in Next.js\n  o API Routes in Next.js\n• Next.js Features:\n  o Image optimization with next/image\n  o Automatic Static Optimization\n  o Static and Server-Side Rendering (SSR)\n📚 Resources:\n• Platform: Next.js Documentation\n• Course: Next.js Crash Course (Traversy Media)\n• Practice: Build a Blog using Next.js"),
            ("🔥 Phase 6: Advanced Next.js (Week 15)", "🧠 What to Learn:\n• Server-Side Rendering (SSR):\n  o How SSR works and why it’s beneficial for SEO\n  o getServerSideProps and getStaticProps\n• API and Database Integration:\n  o Integrating MongoDB with Next.js\n  o Authentication with Next.js (JWT, OAuth)\n• Deploying Next.js App:\n  o Deploy on Vercel or Netlify\n📚 Resources:\n• Platform: Next.js Learn Course\n• Practice: Create an E-commerce Store with Next.js")
        ],
        "MongoDB": [
            ("Youtube link", "https://youtu.be/J6mDkcqU_ZE?amp;si=EEubPkUQVUIyhDul"),
            ("💡 Total Duration", "16-20 weeks (customize based on your pace)"),
            ("📌 Ideal for", "Beginners, College Students, Aspiring Full-Stack Developers"),
            ("✅ Outcome", "Proficiency in JavaScript fundamentals, React components, Next.js for server-side rendering, and MongoDB for database management"),
            ("🗃️ Phase 7: MongoDB Basics (Week 16-17)", "🧠 What to Learn:\n• Introduction to MongoDB:\n  o What is NoSQL and MongoDB?\n  o Setting up MongoDB locally or using MongoDB Atlas\n  o Collections and Documents\n• CRUD Operations:\n  o Insert, Find, Update, Delete documents\n  o Filtering, Sorting, Projection\n• MongoDB Aggregation:\n  o aggregate() method\n  o Aggregation pipelines\n📚 Resources:\n• Platform: MongoDB University\n• Book: MongoDB: The Definitive Guide by Kristina Chodorow\n• Practice: Build a Simple CRUD App (e.g., User Management)"),
            ("⚡ Phase 8: Full Stack Project (Week 18-20)", "🧠 What to Build:\n• Full-Stack Application:\n  o Build a MERN stack application (MongoDB, Express, React, Node.js)\n  o Authentication: JWT, Passport.js, or OAuth\n  o API Integration and Client-Server Communication\n  o Connect Next.js with MongoDB (for SSR and SSG)\n📝 Project Ideas:\n• Task Management Application (Full CRUD)\n• Blog or CMS (with Next.js for SSR)\n• E-commerce platform (MongoDB for storing product data)")
        ],
        "SQL": [
            ("Youtube link", "https://youtu.be/hlGoQC332VM?amp;si=4Xz2gBHdaegMTO_z"),
            ("💡 Duration", "6-8 weeks (can be adjusted based on individual pace)"),
            ("✅ Ideal for", "SQL Enthusiasts, Data Analysts, Data Engineers, and anyone looking to improve their SQL skills"),
            ("🎯 Outcome", "Mastery of intermediate to advanced SQL concepts, query optimization, and working with large-scale databases."),
            ("🔰 Phase 1: Review of SQL Basics (Week 1)", "🧠 What to Learn:\n• Basic SQL Queries:\n  o SELECT, WHERE, ORDER BY, LIMIT\n  o Using DISTINCT, GROUP BY, HAVING\n  o Aggregate Functions: COUNT(), SUM(), AVG(), MIN(), MAX()\n• Joins:\n  o Inner Join, Left Join, Right Join, Full Join\n  o Self Join and Cross Join\n• Subqueries:\n  o Inline Subqueries\n  o Correlated Subqueries\n  o Subqueries in WHERE, FROM, and SELECT clauses\n• Basic Data Modification:\n  o INSERT, UPDATE, DELETE\n  o Using TRUNCATE vs. DELETE\n📚 Resources:\n• SQLBolt - Interactive SQL tutorials\n• W3Schools SQL Tutorial - For basic concepts and queries\n📈 Practice:\n• Solve beginner to intermediate problems on LeetCode SQL\n• HackerRank SQL Challenges"),
            ("⚡ Phase 2: Intermediate SQL Concepts (Week 2-4)", "🧠 What to Learn:\n• Advanced Joins:\n  o NATURAL JOIN, USING, and JOIN with multiple tables\n  o JOIN with aggregation functions\n• Advanced Subqueries:\n  o Subqueries in UPDATE, DELETE\n  o EXISTS vs IN vs ANY\n• Set Operations:\n  o UNION, INTERSECT, EXCEPT (also MINUS in some DBMS)\n  o Differences between UNION ALL and UNION\n• Window Functions:\n  o ROW_NUMBER(), RANK(), DENSE_RANK()\n  o NTILE(), LEAD(), LAG()\n  o PARTITION BY and OVER()\n  o Aggregate Functions with Window Functions\n• Common Table Expressions (CTEs):\n  o Writing and using WITH clauses\n  o Recursive CTEs\n📚 Resources:\n• Book: SQL Performance Explained by Markus Winand (for advanced querying)\n• Mode Analytics SQL Tutorial - Intermediate concepts explained with practice exercises\n📈 Practice:\n• SQLZoo - Interactive SQL practice\n• LeetCode SQL Advanced Challenges"),
            ("🌐 Phase 3: Database Design and Data Normalization (Week 4-5)", "🧠 What to Learn:\n• Database Normalization:\n  o 1NF, 2NF, 3NF, BCNF, and higher normal forms\n  o De-normalization techniques and their trade-offs\n• Keys and Constraints:\n  o Primary Keys, Foreign Keys, Unique Constraints\n  o CHECK, DEFAULT, and NOT NULL constraints\n  o Composite Keys and their use\n• Entity-Relationship Models (ER Models):\n  o Translating ER Diagrams to SQL schema\n  o Relationships between tables: One-to-Many, Many-to-Many, One-to-One\n📚 Resources:\n• Book: Database Design for Mere Mortals by Michael J. Hernandez\n• Khan Academy Database Fundamentals - For understanding normalization\n📈 Practice:\n• Design your own database schema for a real-world scenario (e.g., Library System, E-commerce Store)\n• SQL Design Patterns"),
            ("🚀 Phase 4: SQL Query Optimization and Advanced Techniques (Week 6-7)", "🧠 What to Learn:\n• Query Optimization Techniques:\n  o Indexing: Types of indexes (B-tree, Bitmap, Hash)\n  o Query Execution Plan (EXPLAIN keyword in SQL)\n  o Optimizing complex joins and subqueries\n• Advanced Data Manipulation:\n  o MERGE statement (for UPSERT operations)\n  o Batch Inserts and Bulk Data Operations\n  o Optimizing INSERT INTO SELECT queries\n• Partitioning and Sharding:\n  o Horizontal vs. Vertical Partitioning\n  o Range Partitioning, List Partitioning, Hash Partitioning\n  o Distributed Databases: Sharding data for scalability\n📚 Resources:\n• Book: SQL Performance Tuning by Peter Gulutzan and Trudy Pelzer\n• SQL Server Performance Blog - Excellent for SQL performance tips\n📈 Practice:\n• Optimize a slow-running query and test the performance using EXPLAIN (in MySQL/PostgreSQL)\n• Participate in optimization challenges on Hackerrank's SQL Performance Challenges"),
            ("🌍 Phase 5: Working with Large Datasets and Advanced Topics (Week 7-8)", "🧠 What to Learn:\n• Handling Large Datasets:\n  o Querying and handling large tables (using LIMIT, OFFSET, and BULK operations)\n  o Using TEMPORARY tables\n  o Querying with joins and subqueries on massive datasets\n• Stored Procedures and Triggers:\n  o Writing and managing stored procedures and functions\n  o Triggers for automated data processing\n  o Using BEGIN and END to group multiple SQL commands\n• Database Transactions and Concurrency:\n  o BEGIN TRANSACTION, COMMIT, ROLLBACK\n  o ACID properties and Isolation Levels (READ COMMITTED, SERIALIZABLE, etc.)\n📚 Resources:\n• Book: SQL in 10 Minutes by Ben Forta (for quick tips and techniques)\n• SQL Server Documentation - For advanced SQL Server features like Transactions, Triggers, and Procedures\n📈 Practice:\n• Implement Triggers and Stored Procedures in a database (e.g., automatically update stock quantity in an e-commerce database)\n• Optimize queries on large data using indexing and partitioning"),
            ("🧠 Final Project (Week 8)", "Project Idea:\n• Build a Data Warehouse System:\n  o Design a system that handles ETL (Extract, Transform, Load) processes.\n  o Work with data from multiple sources (CSV, JSON) and load it into normalized tables.\n  o Use stored procedures, functions, and triggers to automate data processing.\n  o Optimize large datasets using indexing, partitioning, and query optimization techniques."),
            ("📚 Recommended Books for Advanced SQL", "1. SQL Performance Explained by Markus Winand\n2. SQL Tuning by Dan Tow\n3. SQL Server 2019 Query Performance Tuning by Grant Fritchey"),
            ("🧠 Practice Platforms for SQL", "• LeetCode - Great for intermediate and advanced challenges\n• Hackerrank - For improving query writing skills\n• Mode Analytics SQL Tutorial - Great resource for practicing complex SQL queries with real-life datasets\n• SQLZoo - Good for interactive learning and practice.")
        ],
        "Leetcode & Hackerrank Practice": [
            ("Daily", "DSA Problems Practice", "N/A", "Leetcode, Hackerrank Practice List"),
        ]
    }

    # ---------- Helper Functions ----------
    def format_links_for_all_courses(course_data):
        formatted_course_data = {}
        for course, data in course_data.items():
            formatted_data = []
            for entry in data:
                if "youtube link" in entry[1].lower():
                    link = f'<a youtube link="{entry[1]}" target="_blank">{entry[0]}</a>'
                    formatted_data.append((link,) + entry[2:])
                else:
                    formatted_data.append(entry)
            formatted_course_data[course] = formatted_data
        return formatted_course_data


    def format_topics(data):
        formatted_data = []
        for entry in data:
            if "Topics:" in entry[1]:
                topics_section = entry[1].split("Topics:\n")[1]
                numbered = "\n".join([f"{i+1}. {line.strip()}" for i, line in enumerate(topics_section.split("\n")) if line.strip()])
                formatted_data.append((entry[0], f"Topics:\n{numbered}", *entry[2:]))
            else:
                formatted_data.append(entry)
        return formatted_data

    def normalize_course_data(course_data):
        normalized_course_data = {}
        for course, data in course_data.items():
            temp = []
            for entry in data:
                entry = entry + ("",) * (4 - len(entry)) if len(entry) < 4 else entry
                temp.append(entry)
            temp = format_topics(temp)
            normalized_course_data[course] = temp
        return normalized_course_data

    # ---------- Data Processing ----------
    course_data = format_links_for_all_courses(course_data)
    course_data = normalize_course_data(course_data)

    # ---------- Course Selection Sidebar ----------
    selected_course = st.sidebar.radio("📘 Select a Course:", list(course_data.keys()), key="course_selection_sidebar")
    
    # ---------- Show Course Table or To-Do Tracker ----------
    data = course_data[selected_course]

    if selected_course == "Leetcode & Hackerrank Practice":
        # Initialize the practice tracker if not already in session state
        if "practice_tracker" not in st.session_state:
            st.session_state.practice_tracker = pd.DataFrame({
                "Subject": [""],  # Example subjects
                "Number of Questions": [""],  # Number of questions
                "Platform": [""],  # Platform (e.g., Leetcode, Hackerrank)
                "Date": [""],  # Date (e.g., YYYY-MM-DD)
            })

        st.markdown("### 🧾 Leetcode & Hackerrank Practice Tracker")

        # Editable DataFrame
        edited_df = st.data_editor(
            st.session_state.practice_tracker,
            num_rows="dynamic",  # Allow adding/removing rows
            use_container_width=True
        )

        # Save the updated DataFrame back to session state
        st.session_state.practice_tracker = edited_df

        # Display the updated DataFrame
        st.markdown("### 📋 Updated Practice Tracker")
        st.dataframe(st.session_state.practice_tracker, use_container_width=True)

    else:
        # Normal courses → Add status dropdown for each row
        st.markdown("### 📘 Course Roadmap")

        df = pd.DataFrame(data, columns=["Week", "Topics", "Books", "Resources"])

        status_options = ["✅ Completed", "🟡 In Progress", "🔘 Not Started"]

        if "course_status" not in st.session_state:
            st.session_state.course_status = {}

        # Render each row with status dropdown
        for i in range(len(df)):
            st.markdown(f"#### 📅 {df.at[i, 'Week']}")
            st.markdown(f"**📝 Topics:** {df.at[i, 'Topics']}")
            if df.at[i, 'Books']:
                st.markdown(f"**📚 Books:** {df.at[i, 'Books']}")
            if df.at[i, 'Resources']:
                st.markdown(f"**🔗 Resources:** {df.at[i, 'Resources']}", unsafe_allow_html=True)

            status_key = f"{selected_course}_status_{i}"
            current_status = st.session_state.course_status.get(status_key, "🔘 Not Started")
            status = st.selectbox("📌 Status:", status_options, index=status_options.index(current_status), key=status_key)
            st.session_state.course_status[status_key] = status

            st.markdown("---")

# Page Routing
if st.session_state.page == "auth":
    authenticate()
elif st.session_state.page == "home":
    home_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
elif st.session_state.page == "daywise":
    daywise_timetable_page()
elif st.session_state.page == "weekwise":
    weekwise_timetable()
elif st.session_state.page == "notes":
    notes_section()
elif st.session_state.page == "pie_chart":
    weekly_pie_chart()
elif st.session_state.page == "new_page":
    new_page()
else:
    st.error("Page not found. Please navigate using the sidebar.")

# Footer
year = datetime.datetime.now().year
st.markdown(f"<hr><footer style='text-align:center; color:gray; font-size:12px;'>© {year} GATE CSE Dashboard | Made with ❤️ by You</footer>", unsafe_allow_html=True)
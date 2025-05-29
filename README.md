# 🎓 GATE CSE Dashboard 🚀

A personalized, full-featured GATE CSE preparation dashboard built using **Streamlit** and **SQLite**, designed to manage study schedules, subject-wise resources, daily logs, and test tracking — all in one place.

> 📌 **Note:** All subject roadmaps, test links, resources, and playlists provided are from my personal point of view. You can **edit or replace them** with your own preferences easily!

---

## 🧠 Features

- ✅ **Login & Sign-Up** system with password hashing
- 📚 **Subject-wise study dashboard** with:
  - YouTube playlists
  - NPTEL courses
  - Recommended textbooks
  - GATEOverflow free test links
  - Progress tracker
- 🗓️ **Daywise Timetable** editor
- 📆 **Weekwise Roadmap**
- 📒 **Notes Section** with save/load feature
- 📊 **Weekly Pie Chart** based on study log
- 📂 **Course Tracker for Ongoing Topics** like:
  - DSA (Striver A2Z)
  - Python
  - SQL
  - UI/UX
  - JavaScript, React/Next.js
  - MongoDB, and more...
- 🧾 **Leetcode & Hackerrank Practice Tracker**
- 🔐 **Authentication** using SQLite (no more `users.csv`)
- 🧩 Beautiful UI with **responsive layout** and **dark/light theme blend**

---

## 📁 File Structure

```bash
gate-cse-dashboard/
│
├── main.py                # Main Streamlit app
├── auth.py                # SQLite database (users, study logs)
├── .gitignore                  # Git ignore config (see below)
├── README.md                   # This file
└── assets/                     # (Optional) for future logos, CSS, etc.

```

## 🛠️ Tech Stack
-🐍 Python 3

-📦 Streamlit (UI)

-🗃️ SQLite (Database)

-📊 Matplotlib & Pandas (Charts + Data)

-🔐 Hashlib (Password hashing)

---

### 🚀 Setup Instructions
1. Clone the repository:
bash
git clone https://github.com/your-username/gate-cse-dashboard.git
cd gate-cse-dashboard
2. Install dependencies:
bash
pip install -r requirements.txt
requirements.txt (you can create this using pip freeze > requirements.txt)
3. Run the app:
bash
streamlit run dashboard.py
4. Login or Sign Up to begin using your dashboard!
---

### 📌 Customization Tips
📌All subjects and resource links are stored inside subjects = { ... } in dashboard.py. You can:

 - Add new topics

- Remove links

- Replace with your own playlists, GitHub notes, or mock test links
---


https://github.com/user-attachments/assets/a6507e47-d2f3-4e9f-8a49-ed8ac4e6d970


✅All course roadmaps (DSA, Python, SQL, etc.) are editable in the new_page() function.
---

### 📂 .gitignore
- dashboard.db
- users.csv
- progress.csv
- progress.json
- topic_program.json
- __pycache__/
- *.pyc

---
## 💬 Feedback & Contributions

If you find any bugs or want to contribute improvements, feel free to create an issue or a pull request!

📬 Contact me: [goyalsimran791@gmail.com]
---

### 📄 License
Licensed under the MIT License – free to use, modify, and share.

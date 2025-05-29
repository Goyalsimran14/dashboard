import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ongoing Courses Tracker", layout="wide")

# CSS for clean layout and animations
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            font-family: 'Segoe UI', sans-serif;
            color: black; /* Change text color to black */
        }
        .course-header {
            font-size: 36px;
            font-weight: 700;
            color: #0d47a1;
            text-align: center;
            margin-top: 30px;
            margin-bottom: 20px;
        }
        .course-table {
            border-collapse: collapse;
            width: 100%;
        }
        .course-table th, .course-table td {
            border: 1px solid #90caf9;
            padding: 12px;
            text-align: left;
            color: black; /* Change table text color to black */
        }
        .course-table th {
            background-color: #1976d2;
            color: black; /* Change header text color to black */
        }
        .course-table tr:nth-child(even) {
            background-color: #e3f2fd;
        }
        .course-table tr:hover {
            background-color: #bbdefb;
        }
    </style>
""", unsafe_allow_html=True)

# Course Roadmap Data (manually extracted from roadmap.txt and cleaned)
course_data = {
    "DSA in C++": [
        ("youtube link", "https://youtube.com/playlist?list=PLfqMhTWNBTe137I_EPQd34TsgV6IO55pt&amp;si=CZK4CDC5WYw8iB3s"),
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
        ("Youtube link", "https://www.youtube.com/live/MGlKO2JrvxE?amp;si=KM22QHkOwxcaJGvz"),
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
        ("Youtube link", "https://youtube.com/playlist?list=PLGjplNEQ1it_oTvuLRNqXfz_v_0pq6unW&amp;si=5Jdk4KMXCZY4UsKk"),
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

# Sidebar for Course Selection
selected_course = st.sidebar.radio("Select a Course to View Roadmap:", list(course_data.keys()))

# Function to format YouTube links as clickable hyperlinks for all courses
def format_links_for_all_courses(course_data):
    formatted_course_data = {}
    for course, data in course_data.items():
        formatted_data = []
        for entry in data:
            if "youtube" in entry[1].lower():  # Check if the entry contains a YouTube link
                link = f'<a href="{entry[1]}" target="_blank">{entry[0]}</a>'
                formatted_data.append((link,) + entry[2:])  # Replace the first column with the hyperlink
            else:
                formatted_data.append(entry)
        formatted_course_data[course] = formatted_data
    return formatted_course_data

# Apply formatting to all courses
course_data = format_links_for_all_courses(course_data)

# Function to normalize course data to ensure all rows have 4 fields
def normalize_course_data(course_data):
    normalized_course_data = {}
    for course, data in course_data.items():
        normalized_data = []
        for entry in data:
            # Ensure each entry has exactly 4 fields
            if len(entry) < 4:
                entry = entry + ("",) * (4 - len(entry))  # Pad missing fields with empty strings
            normalized_data.append(entry)
        normalized_data = format_topics(normalized_data)  # Apply topic formatting
        normalized_course_data[course] = normalized_data
    return normalized_course_data

# Function to format topics in a structured, numbered format for all courses
def format_topics(data):
    formatted_data = []
    for entry in data:
        if "Topics:" in entry[1]:  # Check if the entry contains "Topics:"
            topics_section = entry[1].split("Topics:\n")[1]  # Extract topics section
            numbered_topics = "\n".join([f"{i+1}. {line.strip()}" for i, line in enumerate(topics_section.split("\n")) if line.strip()])
            formatted_entry = (entry[0], f"Topics:\n{numbered_topics}", *entry[2:])  # Replace topics with numbered format
            formatted_data.append(formatted_entry)
        else:
            formatted_data.append(entry)
    return formatted_data

# Apply normalization to all courses
course_data = normalize_course_data(course_data)

# Create DataFrame for the selected course
data = course_data[selected_course]
df = pd.DataFrame(data, columns=["Week", "Topics", "Books", "Resources"])
st.markdown(df.to_html(classes='course-table', index=False, escape=False), unsafe_allow_html=True)

# Footer
st.markdown("<hr><div style='text-align:center; color:gray;'>© 2025 Ongoing Courses Tracker | Designed by You</div>", unsafe_allow_html=True)

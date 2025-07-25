# Quiz Management System - SMIT

An interactive and responsive web application built with **Flask (Python)** that allows administrators to manage quizzes and 
students to take them. Developed by Rubab Akram.

---

## 🌟 Features

### 👨‍🎓 Student:

* Register & login securely
* Choose subject and take quiz
* View results with correct/incorrect answers

### 👨‍💼 Admin:

* Add new subjects
* Create questions for any subject
* View question list

---

## 📊 Tech Stack

| Frontend               | Backend        | Storage    |
| ---------------------- | -------------- | ---------- |
| HTML + CSS + Bootstrap | Flask (Python) | JSON Files |

---

## 🗓️ Folder Structure

```bash
herTechSquad_Online_quiz_management/
|│-- app.py
|│-- data/
|   |-- users.json
|   |-- questions.json
|   |-- results.json
|│-- templates/
|   |-- base.html
|   |-- login.html
|   |-- register.html
|   |-- admin.html
|   |-- choose_subject.html
|   |-- create_quiz.html
|   |-- take_quiz.html
|   |-- results.html
|│-- static/
    |-- styles.css
```

---

## 👨‍💻 Setup Instructions

1. **Clone the Repo**

```bash
git clone https://github.com/rubab783/quiz-management-app.git
cd quiz-management-app
```

2. **Create a virtual environment** *(optional but recommended)*

```bash
python -m venv venv
venv\Scripts\activate   # on Windows
```

3. **Install Dependencies**

```bash
pip install flask
```

4. **Run the App**

```bash
python app.py
```

5. **Visit** `http://127.0.0.1:5000`

---

## 🌟 Demo Credentials

| Role    | Username | Password |
| ------- | -------- | -------- |
| Admin   | admin    | admin123 |
| Student | student1 | pass123  |

---

## 🚀 Future Enhancements

* Database integration (SQLite/PostgreSQL)
* Admin dashboard with stats
* Timed quizzes
* MCQ editing and deletion

---

## 🌟 Developed By

**Rubab** ✨
Student at **SMIT - HerTechSquad Program**

[View on GitHub](https://github.com/rubab783/quiz-management-app)

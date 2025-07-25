from flask import Flask, render_template, request, redirect, url_for, session, flash
import os, json
from datetime import datetime
app = Flask(__name__)
app.secret_key = "quiz_secret"
@app.context_processor
def inject_now():
    return {'now': datetime.now}
# ========= File Handler Class =========
class FileHandler:
    @staticmethod
    def read(file):
        if not os.path.exists(file):
            FileHandler.write(file, {})
            return {}
        try:
            with open(file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    @staticmethod
    def write(file, data):
        with open(file, "w") as f:
            json.dump(data, f, indent=4)

# ========= User Manager Class =========
class UserManager:
    FILE = "data/users.json"

    @staticmethod
    def register(username, password, role):
        users = FileHandler.read(UserManager.FILE)
        if username in users:
            return False, "User already exists!"
        users[username] = {"password": password, "role": role}
        FileHandler.write(UserManager.FILE, users)
        return True, "Registration successful!"

    @staticmethod
    def login(username, password):
        users = FileHandler.read(UserManager.FILE)
        user = users.get(username)
        if user and user['password'] == password:
            return True, user['role']
        return False, None

# ========= Quiz Manager Class =========
class QuizManager:
    QUESTION_FILE = "data/questions.json"
    RESULT_FILE = "data/results.json"

    @staticmethod
    def get_subjects():
        return list(FileHandler.read(QuizManager.QUESTION_FILE).keys())

    @staticmethod
    def add_subject(subject):
        data = FileHandler.read(QuizManager.QUESTION_FILE)
        if subject in data:
            return False
        data[subject] = []
        FileHandler.write(QuizManager.QUESTION_FILE, data)
        return True

    @staticmethod
    def add_question(subject, question_data):
        data = FileHandler.read(QuizManager.QUESTION_FILE)
        data[subject].append(question_data)
        FileHandler.write(QuizManager.QUESTION_FILE, data)

    @staticmethod
    def get_questions(subject):
        return FileHandler.read(QuizManager.QUESTION_FILE).get(subject, [])

    @staticmethod
    def save_result(username, subject, score, total, answers):
        results = FileHandler.read(QuizManager.RESULT_FILE)
        if username not in results:
            results[username] = []
        results[username].append({
            "subject": subject,
            "score": score,
            "total": total,
            "answers": answers,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        FileHandler.write(QuizManager.RESULT_FILE, results)

    @staticmethod
    def get_user_results(username, subject):
        all_results = FileHandler.read(QuizManager.RESULT_FILE).get(username, [])
        return [r for r in all_results if r['subject'] == subject]

# ========= Routes =========

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        success, message = UserManager.register(username, password, role)
        flash(message, "success" if success else "danger")
        return redirect(url_for('home' if success else 'register'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    success, role = UserManager.login(username, password)
    if success:
        session['username'] = username
        session['role'] = role
        return redirect(url_for('dashboard'))
    flash("Invalid username or password!", "danger")
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    return redirect(url_for('admin_panel' if session['role'] == 'admin' else 'choose_subject'))

@app.route('/admin')
def admin_panel():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    subjects = QuizManager.get_subjects()
    return render_template('admin.html', subjects=subjects)

@app.route('/admin/add_subject', methods=['POST'])
def add_subject():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    subject = request.form['subject'].strip().capitalize()
    if QuizManager.add_subject(subject):
        flash(f"Subject '{subject}' added successfully.", "success")
    else:
        flash("Subject already exists!", "warning")
    return redirect(url_for('admin_panel'))

@app.route('/admin/add_question/<subject>', methods=['GET', 'POST'])
def add_question(subject):
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    if request.method == 'POST':
        q_text = request.form['question']
        options = {k: request.form[k] for k in ['A', 'B', 'C', 'D']}
        correct = request.form['correct'].strip().upper()
        if correct not in options:
            flash("Correct option must be A, B, C, or D.", "danger")
            return redirect(url_for('add_question', subject=subject))
        QuizManager.add_question(subject, {
            "question": q_text,
            "options": options,
            "answer": correct
        })
        flash("Question added successfully!", "success")
        return redirect(url_for('admin_panel'))
    return render_template('create_quiz.html', subject=subject)

@app.route('/choose_subject')
def choose_subject():
    if session.get('role') != 'student':
        return redirect(url_for('home'))
    subjects = QuizManager.get_subjects()
    return render_template('choose_subject.html', subjects=subjects)

@app.route('/take_quiz/<subject>', methods=['GET', 'POST'])
def take_quiz(subject):
    if session.get('role') != 'student':
        return redirect(url_for('home'))
    questions = QuizManager.get_questions(subject)
    if request.method == 'POST':
        score = 0
        answers = []
        for i, q in enumerate(questions):
            selected = request.form.get(f'q{i}')
            correct = q['answer']
            is_correct = selected == correct
            if is_correct:
                score += 1
            answers.append({
                "question": q["question"],
                "selected": selected,
                "correct": correct,
                "is_correct": is_correct
            })
        QuizManager.save_result(session['username'], subject, score, len(questions), answers)
        return redirect(url_for('view_result', subject=subject))
    return render_template('take_quiz.html', subject=subject, questions=questions)

@app.route('/result/<subject>')
def view_result(subject):
    if 'username' not in session:
        return redirect(url_for('home'))
    results = QuizManager.get_user_results(session['username'], subject)
    if not results:
        return "No results found."
    return render_template('results.html', result=results[-1])

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, abort
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SignupForm, LoginForm
from models.models import db, User, Admin, QuizQuestion, QuizResult # QuizAttempt
import csv


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Admin.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('admin.signup'))

        new_admin = Admin(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_admin)
        db.session.commit()
        flash('Signup successful. Please log in.', 'success')
        return redirect(url_for('admin_login'))
    return render_template('admin.signup.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            flash('Login successful.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials.', 'error')
    return render_template('admin/login.html')

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Please log in first.', 'error')
        quizzes = QuizQuestion.query.all()
        return redirect(url_for('admin_login'))
    return render_template('admin/dashboard.html', quizzes=quizzes)

@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/admin/quizzes', methods=['GET'])
@login_required
def manage_quizzes():
    if 'admin_id' not in session:
        return redirect(url_for('admin.admin_login'))
    quizzes = QuizQuestion.query.all()
    return render_template('admin/manage_quizzes.html', quizzes=quizzes)

@admin_bp.route('/quiz/add', methods=['GET', 'POST'])
@login_required
def add_quiz():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        explanation = request.form['explanation']
        hint = request.form['hint']
        topic = request.form['topic']

        new_quiz = QuizQuestion(
            question=question,
            answer=answer,
            explanation=explanation,
            hint=hint,
            topic=topic
        )
        db.session.add(new_quiz)
        db.session.commit()
        flash('✅ Quiz added successfully.')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/add_quiz.html')

@admin_bp.route('/quiz/edit/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(quiz_id):
    quiz = QuizQuestion.query.get_or_404(quiz_id)
    if request.method == 'POST':
        quiz.question = request.form['question']
        quiz.answer = request.form['answer']
        quiz.explanation = request.form['explanation']
        quiz.hint = request.form['hint']
        quiz.topic = request.form['topic']
        db.session.commit()
        flash('✅ Quiz updated successfully.')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/edit_quiz.html', quiz=quiz)



@admin_bp.route('/quiz/delete/<int:quiz_id>', methods=['POST'])
@login_required
def delete_quiz(quiz_id):
    quiz = QuizQuestion.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash('🗑️ Quiz deleted successfully.')
    return redirect(url_for('admin.admin_dashboard'))



@admin_bp.route('/admin/students/performance')
@login_required
def student_performance():
    if not current_user.is_admin:
        abort(403)

    from sqlalchemy.sql import func
    performance = db.session.query(
        User.id, User.email,
        func.count(QuizResult.id),
        func.avg(QuizResult.is_correct.cast(db.Float))
    ).join(QuizResult, QuizResult.user_id == User.id).group_by(User.id).all()

    return render_template('admin/student_performance.html', performance=performance)



@admin_bp.route('/admin/upload_quiz', methods=['GET', 'POST'])
@login_required
def upload_quiz():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith('.csv'):
            flash("Please upload a valid CSV file.", "danger")
            return redirect(request.url)

        reader = csv.DictReader(file.stream.read().decode("utf-8").splitlines())
        count = 0
        for row in reader:
            q = QuizQuestion(
                topic=row['topic'].strip(),
                question=row['question'].strip(),
                correct_answer=row['answer'].strip(),
                hint=row.get('hint', '').strip(),
                explanation=row.get('explanation', '').strip()
            )
            db.session.add(q)
            count += 1
        db.session.commit()
        flash(f"✅ Successfully uploaded {count} questions.", "success")
        return redirect(url_for('admin_bp.upload_quiz'))

    return render_template('admin/upload_quiz.html')
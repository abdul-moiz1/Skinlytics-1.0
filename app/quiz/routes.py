from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_required, current_user
from app.quiz import bp
from app.quiz.forms import QuizQuestionForm
from app.models import QuizQuestion, QuizResult
from app import db


SKIN_TYPE_MAP = {
    'mostly_a': {
        'type': 'Dry',
        'recommendations': 'Your skin tends to be dry and may feel tight. Focus on hydrating products with hyaluronic acid, ceramides, and rich moisturizers. Avoid harsh cleansers and use gentle, cream-based products. Always apply moisturizer while your skin is still damp.'
    },
    'mostly_b': {
        'type': 'Normal',
        'recommendations': 'You have well-balanced skin! Maintain your routine with gentle cleansers, lightweight moisturizers, and daily sunscreen. Add antioxidant serums like vitamin C for extra protection. Your skin is adaptable, so focus on prevention and maintenance.'
    },
    'mostly_c': {
        'type': 'Oily',
        'recommendations': 'Your skin produces excess oil, especially in the T-zone. Use oil-free, non-comedogenic products. Incorporate salicylic acid or niacinamide to control sebum. Don\'t skip moisturizer — use a lightweight, gel-based one. Clay masks weekly can help absorb excess oil.'
    },
}


@bp.route('/')
@login_required
def index():
    questions = QuizQuestion.query.order_by(QuizQuestion.order).all()
    return render_template('quiz/index.html', questions=questions)


@bp.route('/submit', methods=['POST'])
@login_required
def submit():
    questions = QuizQuestion.query.order_by(QuizQuestion.order).all()

    # Count answers
    counts = {'a': 0, 'b': 0, 'c': 0}
    for q in questions:
        answer = request.form.get(f'q_{q.id}')
        if answer in counts:
            counts[answer] += 1

    # Determine skin type based on most frequent answer
    dominant = max(counts, key=counts.get)
    key = f'mostly_{dominant}'
    result_data = SKIN_TYPE_MAP.get(key, SKIN_TYPE_MAP['mostly_b'])

    # Save result
    quiz_result = QuizResult(
        user_id=current_user.id,
        skin_type_result=result_data['type'],
        recommendations_text=result_data['recommendations']
    )
    db.session.add(quiz_result)
    db.session.commit()

    return redirect(url_for('quiz.result', result_id=quiz_result.id))


@bp.route('/result/<int:result_id>')
@login_required
def result(result_id):
    quiz_result = QuizResult.query.get_or_404(result_id)
    if quiz_result.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('quiz.index'))
    return render_template('quiz/result.html', result=quiz_result)


# --- Quiz Admin ---

@bp.route('/admin')
@login_required
def admin_quiz_list():
    if not current_user.is_admin:
        abort(403)
    questions = QuizQuestion.query.order_by(QuizQuestion.order).all()
    return render_template('quiz/admin/list.html', questions=questions)


@bp.route('/admin/create', methods=['GET', 'POST'])
@login_required
def admin_quiz_create():
    if not current_user.is_admin:
        abort(403)

    form = QuizQuestionForm()
    if form.validate_on_submit():
        question = QuizQuestion(
            question_text=form.question_text.data,
            option_a=form.option_a.data,
            option_b=form.option_b.data,
            option_c=form.option_c.data,
            correct_answer=form.correct_answer.data,
            order=form.order.data,
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully!', 'success')
        return redirect(url_for('quiz.admin_quiz_list'))

    return render_template('quiz/admin/form.html', form=form, title='Add Question')


@bp.route('/admin/edit/<int:question_id>', methods=['GET', 'POST'])
@login_required
def admin_quiz_edit(question_id):
    if not current_user.is_admin:
        abort(403)

    question = QuizQuestion.query.get_or_404(question_id)
    form = QuizQuestionForm(obj=question)

    if form.validate_on_submit():
        question.question_text = form.question_text.data
        question.option_a = form.option_a.data
        question.option_b = form.option_b.data
        question.option_c = form.option_c.data
        question.correct_answer = form.correct_answer.data
        question.order = form.order.data
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('quiz.admin_quiz_list'))

    return render_template('quiz/admin/form.html', form=form, title='Edit Question')


@bp.route('/admin/delete/<int:question_id>', methods=['POST'])
@login_required
def admin_quiz_delete(question_id):
    if not current_user.is_admin:
        abort(403)

    question = QuizQuestion.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted.', 'info')
    return redirect(url_for('quiz.admin_quiz_list'))

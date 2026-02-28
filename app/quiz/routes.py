from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app.quiz import bp
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

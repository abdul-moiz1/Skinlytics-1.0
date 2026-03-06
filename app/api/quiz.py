from flask import request, jsonify
from flask_login import current_user
from app.api import api_bp, api_login_required, api_admin_required
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


@api_bp.route('/quiz/questions', methods=['GET'])
@api_login_required
def api_quiz_questions():
    questions = QuizQuestion.query.order_by(QuizQuestion.order).all()
    return jsonify({'questions': [q.to_dict() for q in questions]}), 200


@api_bp.route('/quiz/submit', methods=['POST'])
@api_login_required
def api_quiz_submit():
    data = request.get_json()
    if not data or 'answers' not in data:
        return jsonify({'error': 'Answers are required. Send {"answers": {"question_id": "a/b/c", ...}}'}), 400

    answers = data['answers']
    questions = QuizQuestion.query.order_by(QuizQuestion.order).all()

    counts = {'a': 0, 'b': 0, 'c': 0}
    for q in questions:
        answer = answers.get(str(q.id))
        if answer in counts:
            counts[answer] += 1

    dominant = max(counts, key=counts.get)
    key = f'mostly_{dominant}'
    result_data = SKIN_TYPE_MAP.get(key, SKIN_TYPE_MAP['mostly_b'])

    quiz_result = QuizResult(
        user_id=current_user.id,
        skin_type_result=result_data['type'],
        recommendations_text=result_data['recommendations']
    )
    db.session.add(quiz_result)
    db.session.commit()

    return jsonify({'result': quiz_result.to_dict()}), 201


@api_bp.route('/quiz/result/<int:result_id>', methods=['GET'])
@api_login_required
def api_quiz_result(result_id):
    quiz_result = QuizResult.query.get(result_id)
    if not quiz_result:
        return jsonify({'error': 'Result not found.'}), 404

    if quiz_result.user_id != current_user.id:
        return jsonify({'error': 'Access denied.'}), 403

    return jsonify({'result': quiz_result.to_dict()}), 200


# --- Admin: Quiz Questions ---

@api_bp.route('/admin/quiz/questions', methods=['GET'])
@api_admin_required
def api_admin_quiz_questions():
    questions = QuizQuestion.query.order_by(QuizQuestion.order).all()
    return jsonify({'questions': [q.to_dict() for q in questions]}), 200


@api_bp.route('/admin/quiz/questions', methods=['POST'])
@api_admin_required
def api_admin_quiz_question_create():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    required = ['question_text', 'option_a', 'option_b', 'option_c', 'correct_answer', 'order']
    for field in required:
        if field not in data:
            return jsonify({'error': f'{field} is required.'}), 400

    question = QuizQuestion(
        question_text=data['question_text'],
        option_a=data['option_a'],
        option_b=data['option_b'],
        option_c=data['option_c'],
        correct_answer=data['correct_answer'],
        order=int(data['order']),
    )
    db.session.add(question)
    db.session.commit()

    return jsonify({'question': question.to_dict()}), 201


@api_bp.route('/admin/quiz/questions/<int:question_id>', methods=['PUT'])
@api_admin_required
def api_admin_quiz_question_update(question_id):
    question = QuizQuestion.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found.'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    if 'question_text' in data:
        question.question_text = data['question_text']
    if 'option_a' in data:
        question.option_a = data['option_a']
    if 'option_b' in data:
        question.option_b = data['option_b']
    if 'option_c' in data:
        question.option_c = data['option_c']
    if 'correct_answer' in data:
        question.correct_answer = data['correct_answer']
    if 'order' in data:
        question.order = int(data['order'])

    db.session.commit()
    return jsonify({'question': question.to_dict()}), 200


@api_bp.route('/admin/quiz/questions/<int:question_id>', methods=['DELETE'])
@api_admin_required
def api_admin_quiz_question_delete(question_id):
    question = QuizQuestion.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found.'}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted.'}), 200

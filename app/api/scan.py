import os
import uuid
from flask import request, jsonify, current_app
from flask_login import current_user
from app.api import api_bp, api_login_required
from app.models import Analysis, SkinType, Product, Ingredient
from app.analysis.analyzer import analyze_skin
from app import db

CONDITION_SKIN_TYPE_MAP = {
    'Acne': 'Oily',
    'Dryness': 'Dry',
    'Oiliness': 'Oily',
    'Hyperpigmentation': 'Combination',
    'Normal': 'Normal',
}


@api_bp.route('/scan/upload', methods=['POST'])
@api_login_required
def api_scan_upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided.'}), 400

    file = request.files['image']
    original = file.filename or 'capture.png'
    ext = original.rsplit('.', 1)[1].lower() if '.' in original else 'png'
    if ext not in ('jpg', 'jpeg', 'png'):
        return jsonify({'error': 'Only JPG and PNG images are allowed.'}), 400

    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
    file.save(filepath)

    result = analyze_skin(filepath)

    analysis = Analysis(
        user_id=current_user.id,
        image_filename=filename,
        condition=result['condition'],
        confidence=result['confidence']
    )
    db.session.add(analysis)
    db.session.commit()

    return jsonify({'analysis': analysis.to_dict()}), 201


@api_bp.route('/scan/history', methods=['GET'])
@api_login_required
def api_scan_history():
    analyses = Analysis.query.filter_by(user_id=current_user.id)\
        .order_by(Analysis.created_at.desc()).all()
    return jsonify({'analyses': [a.to_dict() for a in analyses]}), 200


@api_bp.route('/scan/result/<int:analysis_id>', methods=['GET'])
@api_login_required
def api_scan_result(analysis_id):
    analysis = Analysis.query.get(analysis_id)
    if not analysis:
        return jsonify({'error': 'Analysis not found.'}), 404

    if analysis.user_id != current_user.id:
        return jsonify({'error': 'Access denied.'}), 403

    skin_type_name = CONDITION_SKIN_TYPE_MAP.get(analysis.condition, 'Normal')
    skin_type = SkinType.query.filter_by(name=skin_type_name).first()

    products = []
    ingredients = []
    if skin_type:
        products = [p.to_dict() for p in Product.query.filter_by(skin_type_id=skin_type.id).all()]
        ingredients = [i.to_dict() for i in Ingredient.query.filter_by(skin_type_id=skin_type.id).all()]

    return jsonify({
        'analysis': analysis.to_dict(),
        'skin_type': skin_type.to_dict() if skin_type else None,
        'products': products,
        'ingredients': ingredients,
    }), 200

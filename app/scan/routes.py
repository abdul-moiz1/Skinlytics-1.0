import os
import uuid
from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.scan import bp
from app.scan.forms import UploadForm
from app.models import Analysis, SkinType, Product, Ingredient
from app.analysis.analyzer import analyze_skin
from app import db, csrf

CONDITION_INFO = {
    'Acne': {
        'skin_type': 'Oily',
        'explanation': (
            'Acne is a common skin condition where pores become clogged with oil and dead '
            'skin cells, leading to pimples, blackheads, or whiteheads. It is often '
            'associated with excess sebum production and can be managed with targeted '
            'skincare ingredients like salicylic acid and niacinamide.'
        ),
    },
    'Dryness': {
        'skin_type': 'Dry',
        'explanation': (
            'Dry skin occurs when the skin lacks sufficient moisture, resulting in '
            'tightness, flaking, or rough texture. Environmental factors, harsh cleansers, '
            'and low humidity can worsen dryness. Hydrating ingredients like hyaluronic '
            'acid and ceramides can help restore the moisture barrier.'
        ),
    },
    'Oiliness': {
        'skin_type': 'Oily',
        'explanation': (
            'Oily skin is characterized by excess sebum production, which can cause a '
            'shiny appearance and enlarged pores. While sebum is natural and protects the '
            'skin, overproduction can lead to clogged pores and breakouts. Oil-free and '
            'mattifying products help maintain balance.'
        ),
    },
    'Hyperpigmentation': {
        'skin_type': 'Combination',
        'explanation': (
            'Hyperpigmentation refers to dark patches or uneven skin tone caused by excess '
            'melanin production. It can result from sun exposure, hormonal changes, or '
            'post-inflammatory marks. Ingredients like vitamin C, niacinamide, and gentle '
            'exfoliants can help brighten and even out skin tone.'
        ),
    },
    'Normal': {
        'skin_type': 'Normal',
        'explanation': (
            'Your skin appears well-balanced with no major concerns detected. Normal skin '
            'has adequate hydration, minimal sensitivity, and a smooth texture. Maintaining '
            'a consistent skincare routine with sunscreen and antioxidants will help '
            'preserve your skin health.'
        ),
    },
}


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.image.data
        # Generate unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        file.save(filepath)

        # Run mock analysis
        result = analyze_skin(filepath)

        # Save to database
        analysis = Analysis(
            user_id=current_user.id,
            image_filename=filename,
            condition=result['condition'],
            confidence=result['confidence']
        )
        db.session.add(analysis)
        db.session.commit()

        return redirect(url_for('scan.result', analysis_id=analysis.id))

    return render_template('scan/index.html', form=form)


@bp.route('/upload-ajax', methods=['POST'])
@csrf.exempt
@login_required
def upload_ajax():
    """Handle image uploads via JavaScript fetch (webcam or file)."""
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

    return jsonify({'redirect': url_for('scan.result', analysis_id=analysis.id)})


@bp.route('/result/<int:analysis_id>')
@login_required
def result(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    if analysis.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('scan.index'))

    condition_info = CONDITION_INFO.get(analysis.condition, {})
    explanation = condition_info.get('explanation', 'No additional information available for this condition.')
    skin_type_name = condition_info.get('skin_type', 'Normal')

    skin_type = SkinType.query.filter_by(name=skin_type_name).first()
    products = []
    ingredients = []
    if skin_type:
        products = Product.query.filter_by(skin_type_id=skin_type.id).all()
        ingredients = Ingredient.query.filter_by(skin_type_id=skin_type.id).all()

    return render_template('scan/result.html',
                           analysis=analysis,
                           explanation=explanation,
                           skin_type_name=skin_type_name,
                           products=products,
                           ingredients=ingredients)


@bp.route('/history')
@login_required
def history():
    analyses = Analysis.query.filter_by(user_id=current_user.id).order_by(Analysis.created_at.desc()).all()
    return render_template('scan/history.html', analyses=analyses)

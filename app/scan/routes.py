import os
import uuid
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.scan import bp
from app.scan.forms import UploadForm
from app.models import Analysis
from app.analysis.analyzer import analyze_skin
from app import db, csrf


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


@bp.route('/upload-webcam', methods=['POST'])
@csrf.exempt
@login_required
def upload_webcam():
    """Handle webcam capture uploaded via JavaScript."""
    if 'image' not in request.files:
        flash('No image captured.', 'danger')
        return redirect(url_for('scan.index'))

    file = request.files['image']
    filename = f"{uuid.uuid4().hex}.png"
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

    return redirect(url_for('scan.result', analysis_id=analysis.id))


@bp.route('/result/<int:analysis_id>')
@login_required
def result(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    if analysis.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('scan.index'))
    return render_template('scan/result.html', analysis=analysis)

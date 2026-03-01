import os
import uuid
from flask import render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user
from app.recommendation import bp
from app.recommendation.forms import ProductForm, SkinTypeForm, IngredientForm
from app.models import SkinType, Ingredient, Product
from app import db


SKIN_TIPS = {
    'Oily': [
        'Wash your face twice daily with a gentle, oil-free cleanser.',
        'Use non-comedogenic (won\'t clog pores) moisturizers and sunscreen.',
        'Avoid touching your face frequently to prevent transferring oils.',
        'Use blotting papers throughout the day to absorb excess oil.',
        'Incorporate a clay mask once a week to draw out impurities.',
    ],
    'Dry': [
        'Use a gentle, hydrating cleanser that won\'t strip natural oils.',
        'Apply moisturizer immediately after washing while skin is still damp.',
        'Use a humidifier in dry environments to add moisture to the air.',
        'Avoid long, hot showers as they can further dry out your skin.',
        'Look for products with ceramides to strengthen your skin barrier.',
    ],
    'Combination': [
        'Use a gentle cleanser suitable for all skin types.',
        'Apply lighter moisturizer on oily areas and richer one on dry zones.',
        'Use a toner to help balance oil production across your face.',
        'Consider multi-masking: clay mask on T-zone, hydrating mask on cheeks.',
        'Exfoliate gently 1-2 times per week to maintain balance.',
    ],
    'Normal': [
        'Maintain your routine with a gentle daily cleanser.',
        'Use sunscreen every day to protect against UV damage.',
        'Stay hydrated and eat a balanced diet rich in antioxidants.',
        'Use a vitamin C serum in the morning for added protection.',
        'Don\'t over-complicate your routine — less is more for normal skin.',
    ],
    'Sensitive': [
        'Always patch-test new products before applying to your full face.',
        'Choose fragrance-free and hypoallergenic products.',
        'Avoid harsh exfoliants and opt for gentle chemical exfoliants instead.',
        'Protect your skin from extreme temperatures and wind.',
        'Keep your skincare routine simple with minimal products.',
    ],
}


@bp.route('/', methods=['GET', 'POST'])
def index():
    skin_types = SkinType.query.all()
    selected_type = None
    ingredients = []
    products = []
    tips = []

    if request.method == 'POST':
        skin_type_id = request.form.get('skin_type_id')
        if skin_type_id:
            selected_type = SkinType.query.get(int(skin_type_id))
            if selected_type:
                ingredients = Ingredient.query.filter_by(skin_type_id=selected_type.id).all()
                products = Product.query.filter_by(skin_type_id=selected_type.id).all()
                tips = SKIN_TIPS.get(selected_type.name, [])

    return render_template('recommendation/index.html',
                           skin_types=skin_types,
                           selected_type=selected_type,
                           ingredients=ingredients,
                           products=products,
                           tips=tips)


# --- Admin routes ---

@bp.route('/admin')
@login_required
def admin_list():
    if not current_user.is_admin:
        abort(403)
    products = Product.query.order_by(Product.name).all()
    return render_template('recommendation/admin/list.html', products=products)


@bp.route('/admin/create', methods=['GET', 'POST'])
@login_required
def admin_create():
    if not current_user.is_admin:
        abort(403)

    form = ProductForm()
    form.skin_type_id.choices = [(st.id, st.name) for st in SkinType.query.order_by(SkinType.name).all()]

    if form.validate_on_submit():
        filename = None
        if form.image.data:
            file = form.image.data
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"product_{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
            file.save(filepath)
            filename = 'uploads/' + filename

        product = Product(
            name=form.name.data,
            description=form.description.data,
            image_filename=filename,
            skin_type_id=form.skin_type_id.data,
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('recommendation.admin_list'))

    return render_template('recommendation/admin/form.html', form=form, title='Add Product')


@bp.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def admin_edit(product_id):
    if not current_user.is_admin:
        abort(403)

    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    form.skin_type_id.choices = [(st.id, st.name) for st in SkinType.query.order_by(SkinType.name).all()]

    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.skin_type_id = form.skin_type_id.data

        if form.image.data:
            file = form.image.data
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"product_{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
            file.save(filepath)
            product.image_filename = 'uploads/' + filename

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('recommendation.admin_list'))

    return render_template('recommendation/admin/form.html', form=form, title='Edit Product')


@bp.route('/admin/delete/<int:product_id>', methods=['POST'])
@login_required
def admin_delete(product_id):
    if not current_user.is_admin:
        abort(403)

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'info')
    return redirect(url_for('recommendation.admin_list'))


# --- Skin Types Admin ---

@bp.route('/admin/skin-types')
@login_required
def admin_skin_types():
    if not current_user.is_admin:
        abort(403)
    skin_types = SkinType.query.order_by(SkinType.name).all()
    return render_template('recommendation/admin/skin_types_list.html', skin_types=skin_types)


@bp.route('/admin/skin-types/create', methods=['GET', 'POST'])
@login_required
def admin_skin_type_create():
    if not current_user.is_admin:
        abort(403)

    form = SkinTypeForm()
    if form.validate_on_submit():
        skin_type = SkinType(name=form.name.data, description=form.description.data)
        db.session.add(skin_type)
        db.session.commit()
        flash('Skin type added successfully!', 'success')
        return redirect(url_for('recommendation.admin_skin_types'))

    return render_template('recommendation/admin/skin_type_form.html', form=form, title='Add Skin Type')


@bp.route('/admin/skin-types/edit/<int:skin_type_id>', methods=['GET', 'POST'])
@login_required
def admin_skin_type_edit(skin_type_id):
    if not current_user.is_admin:
        abort(403)

    skin_type = SkinType.query.get_or_404(skin_type_id)
    form = SkinTypeForm(obj=skin_type)

    if form.validate_on_submit():
        skin_type.name = form.name.data
        skin_type.description = form.description.data
        db.session.commit()
        flash('Skin type updated successfully!', 'success')
        return redirect(url_for('recommendation.admin_skin_types'))

    return render_template('recommendation/admin/skin_type_form.html', form=form, title='Edit Skin Type')


@bp.route('/admin/skin-types/delete/<int:skin_type_id>', methods=['POST'])
@login_required
def admin_skin_type_delete(skin_type_id):
    if not current_user.is_admin:
        abort(403)

    skin_type = SkinType.query.get_or_404(skin_type_id)
    db.session.delete(skin_type)
    db.session.commit()
    flash('Skin type deleted.', 'info')
    return redirect(url_for('recommendation.admin_skin_types'))


# --- Ingredients Admin ---

@bp.route('/admin/ingredients')
@login_required
def admin_ingredients():
    if not current_user.is_admin:
        abort(403)
    ingredients = Ingredient.query.order_by(Ingredient.name).all()
    return render_template('recommendation/admin/ingredients_list.html', ingredients=ingredients)


@bp.route('/admin/ingredients/create', methods=['GET', 'POST'])
@login_required
def admin_ingredient_create():
    if not current_user.is_admin:
        abort(403)

    form = IngredientForm()
    form.skin_type_id.choices = [(st.id, st.name) for st in SkinType.query.order_by(SkinType.name).all()]

    if form.validate_on_submit():
        ingredient = Ingredient(
            name=form.name.data,
            description=form.description.data,
            skin_type_id=form.skin_type_id.data,
        )
        db.session.add(ingredient)
        db.session.commit()
        flash('Ingredient added successfully!', 'success')
        return redirect(url_for('recommendation.admin_ingredients'))

    return render_template('recommendation/admin/ingredient_form.html', form=form, title='Add Ingredient')


@bp.route('/admin/ingredients/edit/<int:ingredient_id>', methods=['GET', 'POST'])
@login_required
def admin_ingredient_edit(ingredient_id):
    if not current_user.is_admin:
        abort(403)

    ingredient = Ingredient.query.get_or_404(ingredient_id)
    form = IngredientForm(obj=ingredient)
    form.skin_type_id.choices = [(st.id, st.name) for st in SkinType.query.order_by(SkinType.name).all()]

    if form.validate_on_submit():
        ingredient.name = form.name.data
        ingredient.description = form.description.data
        ingredient.skin_type_id = form.skin_type_id.data
        db.session.commit()
        flash('Ingredient updated successfully!', 'success')
        return redirect(url_for('recommendation.admin_ingredients'))

    return render_template('recommendation/admin/ingredient_form.html', form=form, title='Edit Ingredient')


@bp.route('/admin/ingredients/delete/<int:ingredient_id>', methods=['POST'])
@login_required
def admin_ingredient_delete(ingredient_id):
    if not current_user.is_admin:
        abort(403)

    ingredient = Ingredient.query.get_or_404(ingredient_id)
    db.session.delete(ingredient)
    db.session.commit()
    flash('Ingredient deleted.', 'info')
    return redirect(url_for('recommendation.admin_ingredients'))

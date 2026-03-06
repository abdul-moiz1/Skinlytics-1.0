import os
import uuid
from flask import request, jsonify, current_app
from app.api import api_bp, api_admin_required
from app.models import SkinType, Ingredient, Product
from app import db

SKIN_TIPS = {
    'Oily': [
        'Wash your face twice daily with a gentle, oil-free cleanser.',
        'Use non-comedogenic moisturizers and sunscreen.',
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


# --- Public Routes ---

@api_bp.route('/skin-types', methods=['GET'])
def api_skin_types():
    skin_types = SkinType.query.all()
    return jsonify({'skin_types': [st.to_dict() for st in skin_types]}), 200


@api_bp.route('/recommendations/<int:skin_type_id>', methods=['GET'])
def api_recommendations(skin_type_id):
    skin_type = SkinType.query.get(skin_type_id)
    if not skin_type:
        return jsonify({'error': 'Skin type not found.'}), 404

    ingredients = [i.to_dict() for i in Ingredient.query.filter_by(skin_type_id=skin_type.id).all()]
    products = [p.to_dict() for p in Product.query.filter_by(skin_type_id=skin_type.id).all()]
    tips = SKIN_TIPS.get(skin_type.name, [])

    return jsonify({
        'skin_type': skin_type.to_dict(),
        'ingredients': ingredients,
        'products': products,
        'tips': tips,
    }), 200


# --- Admin: Products ---

@api_bp.route('/admin/products', methods=['GET'])
@api_admin_required
def api_admin_products():
    products = Product.query.order_by(Product.name).all()
    return jsonify({'products': [p.to_dict() for p in products]}), 200


@api_bp.route('/admin/products', methods=['POST'])
@api_admin_required
def api_admin_product_create():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    skin_type_id = request.form.get('skin_type_id')

    if not name or not skin_type_id:
        return jsonify({'error': 'Name and skin_type_id are required.'}), 400

    filename = None
    if 'image' in request.files and request.files['image'].filename:
        file = request.files['image']
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext not in ('jpg', 'jpeg', 'png'):
            return jsonify({'error': 'Only JPG and PNG images are allowed.'}), 400
        filename = f"product_{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        file.save(filepath)
        filename = 'uploads/' + filename

    product = Product(
        name=name,
        description=description,
        image_filename=filename,
        skin_type_id=int(skin_type_id),
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({'product': product.to_dict()}), 201


@api_bp.route('/admin/products/<int:product_id>', methods=['PUT'])
@api_admin_required
def api_admin_product_update(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found.'}), 404

    product.name = request.form.get('name', product.name).strip()
    product.description = request.form.get('description', product.description).strip()
    skin_type_id = request.form.get('skin_type_id')
    if skin_type_id:
        product.skin_type_id = int(skin_type_id)

    if 'image' in request.files and request.files['image'].filename:
        file = request.files['image']
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext not in ('jpg', 'jpeg', 'png'):
            return jsonify({'error': 'Only JPG and PNG images are allowed.'}), 400
        filename = f"product_{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        file.save(filepath)
        product.image_filename = 'uploads/' + filename

    db.session.commit()
    return jsonify({'product': product.to_dict()}), 200


@api_bp.route('/admin/products/<int:product_id>', methods=['DELETE'])
@api_admin_required
def api_admin_product_delete(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found.'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted.'}), 200


# --- Admin: Skin Types ---

@api_bp.route('/admin/skin-types', methods=['POST'])
@api_admin_required
def api_admin_skin_type_create():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required.'}), 400

    skin_type = SkinType(name=data['name'].strip(), description=data.get('description', '').strip())
    db.session.add(skin_type)
    db.session.commit()
    return jsonify({'skin_type': skin_type.to_dict()}), 201


@api_bp.route('/admin/skin-types/<int:skin_type_id>', methods=['PUT'])
@api_admin_required
def api_admin_skin_type_update(skin_type_id):
    skin_type = SkinType.query.get(skin_type_id)
    if not skin_type:
        return jsonify({'error': 'Skin type not found.'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    if 'name' in data:
        skin_type.name = data['name'].strip()
    if 'description' in data:
        skin_type.description = data['description'].strip()

    db.session.commit()
    return jsonify({'skin_type': skin_type.to_dict()}), 200


@api_bp.route('/admin/skin-types/<int:skin_type_id>', methods=['DELETE'])
@api_admin_required
def api_admin_skin_type_delete(skin_type_id):
    skin_type = SkinType.query.get(skin_type_id)
    if not skin_type:
        return jsonify({'error': 'Skin type not found.'}), 404

    db.session.delete(skin_type)
    db.session.commit()
    return jsonify({'message': 'Skin type deleted.'}), 200


# --- Admin: Ingredients ---

@api_bp.route('/admin/ingredients', methods=['GET'])
@api_admin_required
def api_admin_ingredients():
    ingredients = Ingredient.query.order_by(Ingredient.name).all()
    return jsonify({'ingredients': [i.to_dict() for i in ingredients]}), 200


@api_bp.route('/admin/ingredients', methods=['POST'])
@api_admin_required
def api_admin_ingredient_create():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('skin_type_id'):
        return jsonify({'error': 'Name and skin_type_id are required.'}), 400

    ingredient = Ingredient(
        name=data['name'].strip(),
        description=data.get('description', '').strip(),
        skin_type_id=int(data['skin_type_id']),
    )
    db.session.add(ingredient)
    db.session.commit()
    return jsonify({'ingredient': ingredient.to_dict()}), 201


@api_bp.route('/admin/ingredients/<int:ingredient_id>', methods=['PUT'])
@api_admin_required
def api_admin_ingredient_update(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'error': 'Ingredient not found.'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    if 'name' in data:
        ingredient.name = data['name'].strip()
    if 'description' in data:
        ingredient.description = data['description'].strip()
    if 'skin_type_id' in data:
        ingredient.skin_type_id = int(data['skin_type_id'])

    db.session.commit()
    return jsonify({'ingredient': ingredient.to_dict()}), 200


@api_bp.route('/admin/ingredients/<int:ingredient_id>', methods=['DELETE'])
@api_admin_required
def api_admin_ingredient_delete(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'error': 'Ingredient not found.'}), 404

    db.session.delete(ingredient)
    db.session.commit()
    return jsonify({'message': 'Ingredient deleted.'}), 200

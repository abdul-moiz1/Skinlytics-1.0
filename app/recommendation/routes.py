from flask import render_template, request
from app.recommendation import bp
from app.models import SkinType, Ingredient, Product


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

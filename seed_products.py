"""Seed the database with famous skincare products for each skin type."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import SkinType, Product

app = create_app()

PRODUCTS = {
    'Oily': [
        {
            'name': 'CeraVe Foaming Facial Cleanser',
            'description': 'A gentle foaming cleanser with ceramides and niacinamide that removes excess oil without disrupting the skin barrier.',
            'image_filename': 'https://picsum.photos/seed/cerave-foam/400/400',
        },
        {
            'name': 'The Ordinary Niacinamide 10% + Zinc 1%',
            'description': 'A high-strength serum that reduces the appearance of blemishes, balances sebum production, and minimizes pores.',
            'image_filename': 'https://picsum.photos/seed/ordinary-niac/400/400',
        },
        {
            'name': 'Neutrogena Oil-Free Moisturizer SPF 35',
            'description': 'A lightweight, oil-free moisturizer with broad-spectrum sun protection, perfect for oily and acne-prone skin.',
            'image_filename': 'https://picsum.photos/seed/neutrogena-spf/400/400',
        },
        {
            'name': 'Aztec Secret Indian Healing Clay Mask',
            'description': 'A deep-pore cleansing clay mask made of 100% calcium bentonite clay that draws out impurities and excess oil.',
            'image_filename': 'https://picsum.photos/seed/aztec-clay/400/400',
        },
        {
            'name': 'La Roche-Posay Effaclar Mat Moisturizer',
            'description': 'A mattifying moisturizer that controls shine and tightens pores while keeping skin hydrated throughout the day.',
            'image_filename': 'https://picsum.photos/seed/laroche-mat/400/400',
        },
    ],
    'Dry': [
        {
            'name': 'CeraVe Hydrating Facial Cleanser',
            'description': 'A gentle, non-foaming cleanser with hyaluronic acid and ceramides that hydrates while cleansing dry skin.',
            'image_filename': 'https://picsum.photos/seed/cerave-hydra/400/400',
        },
        {
            'name': 'The Ordinary Hyaluronic Acid 2% + B5',
            'description': 'A hydrating serum with multi-weight hyaluronic acid that draws moisture into the skin for lasting hydration.',
            'image_filename': 'https://picsum.photos/seed/ordinary-ha/400/400',
        },
        {
            'name': 'First Aid Beauty Ultra Repair Cream',
            'description': 'A rich, whipped moisturizer with colloidal oatmeal and shea butter that instantly relieves dry, distressed skin.',
            'image_filename': 'https://picsum.photos/seed/fab-repair/400/400',
        },
        {
            'name': 'Bio-Oil Skincare Oil',
            'description': 'A specialist facial oil with vitamins A and E that nourishes and improves the appearance of dry, uneven skin.',
            'image_filename': 'https://picsum.photos/seed/bio-oil/400/400',
        },
        {
            'name': 'Supergoop Glowscreen SPF 40',
            'description': 'A hydrating sunscreen primer that provides broad-spectrum protection with a dewy, luminous finish for dry skin.',
            'image_filename': 'https://picsum.photos/seed/supergoop-glow/400/400',
        },
    ],
    'Combination': [
        {
            'name': 'Cetaphil Gentle Skin Cleanser',
            'description': 'A dermatologist-recommended gentle cleanser suitable for all skin types that cleans without over-drying.',
            'image_filename': 'https://picsum.photos/seed/cetaphil-gentle/400/400',
        },
        {
            'name': 'Paula\'s Choice 2% BHA Liquid Exfoliant',
            'description': 'A leave-on exfoliant with salicylic acid that unclogs pores, smooths wrinkles, and evens skin tone.',
            'image_filename': 'https://picsum.photos/seed/paulas-bha/400/400',
        },
        {
            'name': 'Clinique Dramatically Different Moisturizing Gel',
            'description': 'A lightweight, oil-free gel moisturizer that hydrates dry zones while keeping oily areas balanced.',
            'image_filename': 'https://picsum.photos/seed/clinique-gel/400/400',
        },
        {
            'name': 'TruSkin Vitamin C Serum',
            'description': 'A brightening serum with vitamin C, E, and hyaluronic acid that reduces dark spots and boosts radiance.',
            'image_filename': 'https://picsum.photos/seed/truskin-vitc/400/400',
        },
        {
            'name': 'EltaMD UV Clear SPF 46',
            'description': 'A lightweight broad-spectrum sunscreen with niacinamide that calms and protects sensitive, acne-prone, and combination skin.',
            'image_filename': 'https://picsum.photos/seed/eltamd-uv/400/400',
        },
    ],
    'Normal': [
        {
            'name': 'Fresh Soy Face Cleanser',
            'description': 'A gentle gel cleanser with amino acid-rich soy proteins that cleanses and tones without stripping moisture.',
            'image_filename': 'https://picsum.photos/seed/fresh-soy/400/400',
        },
        {
            'name': 'Tatcha The Water Cream',
            'description': 'An oil-free, anti-aging water cream that delivers nutrients and optimal hydration for a poreless-looking complexion.',
            'image_filename': 'https://picsum.photos/seed/tatcha-water/400/400',
        },
        {
            'name': 'Drunk Elephant C-Firma Vitamin C Serum',
            'description': 'A potent vitamin C day serum that firms, brightens, and improves signs of photoaging for radiant skin.',
            'image_filename': 'https://picsum.photos/seed/drunk-cfirma/400/400',
        },
        {
            'name': 'The Ordinary Retinol 0.5% in Squalane',
            'description': 'A gentle retinol serum in squalane that targets fine lines, uneven tone, and texture without irritation.',
            'image_filename': 'https://picsum.photos/seed/ordinary-ret/400/400',
        },
        {
            'name': 'La Roche-Posay Anthelios Melt-In Sunscreen SPF 60',
            'description': 'A fast-absorbing, non-greasy sunscreen with superior broad-spectrum protection and antioxidant cell-ox shield technology.',
            'image_filename': 'https://picsum.photos/seed/laroche-spf60/400/400',
        },
    ],
    'Sensitive': [
        {
            'name': 'Bioderma Sensibio H2O Micellar Water',
            'description': 'A gentle micellar water that cleanses and removes makeup without rinsing, specially formulated for sensitive skin.',
            'image_filename': 'https://picsum.photos/seed/bioderma-h2o/400/400',
        },
        {
            'name': 'Vanicream Moisturizing Skin Cream',
            'description': 'A fragrance-free, dye-free moisturizer recommended by dermatologists for sensitive and irritated skin.',
            'image_filename': 'https://picsum.photos/seed/vanicream-moist/400/400',
        },
        {
            'name': 'COSRX Centella Blemish Cream',
            'description': 'A soothing spot treatment with centella asiatica extract that calms redness and helps heal blemishes on sensitive skin.',
            'image_filename': 'https://picsum.photos/seed/cosrx-centella/400/400',
        },
        {
            'name': 'Aveeno Protect + Hydrate SPF 50',
            'description': 'A gentle mineral sunscreen with prebiotic oat that provides broad-spectrum protection while nourishing sensitive skin.',
            'image_filename': 'https://picsum.photos/seed/aveeno-spf50/400/400',
        },
        {
            'name': 'Dr. Jart+ Cicapair Tiger Grass Calming Mask',
            'description': 'A soothing sheet mask with centella asiatica that calms irritation, reduces redness, and strengthens the skin barrier.',
            'image_filename': 'https://picsum.photos/seed/drjart-cica/400/400',
        },
    ],
}


def seed():
    with app.app_context():
        skin_types = {st.name: st for st in SkinType.query.all()}

        if not skin_types:
            print('No skin types found in database. Please seed skin types first.')
            return

        added = 0
        updated = 0
        for type_name, products in PRODUCTS.items():
            st = skin_types.get(type_name)
            if not st:
                print(f'Skin type "{type_name}" not found, skipping...')
                continue

            for p in products:
                exists = Product.query.filter_by(name=p['name'], skin_type_id=st.id).first()
                if exists:
                    if exists.image_filename != p['image_filename']:
                        exists.image_filename = p['image_filename']
                        updated += 1
                        print(f'  Updated image: {p["name"]}')
                    else:
                        print(f'  Already up-to-date: {p["name"]}')
                    continue

                product = Product(
                    name=p['name'],
                    description=p['description'],
                    image_filename=p['image_filename'],
                    skin_type_id=st.id,
                )
                db.session.add(product)
                added += 1
                print(f'  Added: {p["name"]} ({type_name})')

        db.session.commit()
        print(f'\nDone! Added {added}, updated {updated} products.')


if __name__ == '__main__':
    seed()

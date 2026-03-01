from app.models import SkinType, User


def seed_database(db):
    # --- Admin User ---
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        admin = User(username='admin', email='admin@skinlytics.com', is_admin=True, is_super_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)

    # --- Skin Types ---
    if SkinType.query.count() == 0:
        skin_types = [
            SkinType(name='Oily', description='Skin that produces excess sebum, leading to a shiny appearance and enlarged pores.'),
            SkinType(name='Dry', description='Skin that lacks moisture, often feeling tight, rough, or flaky.'),
            SkinType(name='Combination', description='Skin that is oily in some areas (T-zone) and dry in others.'),
            SkinType(name='Normal', description='Well-balanced skin that is neither too oily nor too dry.'),
            SkinType(name='Sensitive', description='Skin that reacts easily to products and environmental factors, prone to redness and irritation.'),
        ]
        db.session.add_all(skin_types)

    db.session.commit()

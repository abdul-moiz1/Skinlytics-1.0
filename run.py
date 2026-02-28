from app import create_app, db

app = create_app()

with app.app_context():
    from app.models import User, Analysis, SkinType, Ingredient, Product, QuizQuestion, QuizResult, BlogPost
    db.create_all()

    # Seed data if tables are empty
    if SkinType.query.count() == 0:
        from seed import seed_database
        seed_database(db)
        print('Database seeded successfully!')

if __name__ == '__main__':
    app.run(debug=True)

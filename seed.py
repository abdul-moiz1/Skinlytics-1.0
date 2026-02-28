from app.models import SkinType, Ingredient, Product, QuizQuestion, BlogPost, User


def seed_database(db):
    # --- Admin User ---
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        admin = User(username='admin', email='admin@skinlytics.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.flush()

    # --- Skin Types ---
    oily = SkinType(name='Oily', description='Skin that produces excess sebum, leading to a shiny appearance and enlarged pores.')
    dry = SkinType(name='Dry', description='Skin that lacks moisture, often feeling tight, rough, or flaky.')
    combination = SkinType(name='Combination', description='Skin that is oily in some areas (T-zone) and dry in others.')
    normal = SkinType(name='Normal', description='Well-balanced skin that is neither too oily nor too dry.')
    sensitive = SkinType(name='Sensitive', description='Skin that reacts easily to products and environmental factors, prone to redness and irritation.')

    db.session.add_all([oily, dry, combination, normal, sensitive])
    db.session.flush()

    # --- Ingredients ---
    ingredients = [
        # Oily skin
        Ingredient(name='Salicylic Acid', description='A beta-hydroxy acid that penetrates pores to reduce oil and prevent breakouts.', skin_type_id=oily.id),
        Ingredient(name='Niacinamide', description='Vitamin B3 that regulates sebum production and minimizes pores.', skin_type_id=oily.id),
        Ingredient(name='Tea Tree Oil', description='Natural antibacterial ingredient that controls excess oil and fights acne.', skin_type_id=oily.id),
        # Dry skin
        Ingredient(name='Hyaluronic Acid', description='A powerful humectant that attracts and retains moisture in the skin.', skin_type_id=dry.id),
        Ingredient(name='Glycolic Acid', description='An AHA that gently exfoliates dead skin cells and promotes cell renewal.', skin_type_id=dry.id),
        Ingredient(name='Rosehip Oil', description='Rich in essential fatty acids and vitamins to deeply nourish dry skin.', skin_type_id=dry.id),
        # Combination skin
        Ingredient(name='Green Tea Extract', description='Antioxidant-rich ingredient that balances oil production while soothing dry areas.', skin_type_id=combination.id),
        Ingredient(name='Witch Hazel', description='Natural astringent that tones oily zones without over-drying.', skin_type_id=combination.id),
        Ingredient(name='Aloe Vera', description='Hydrating and soothing ingredient suitable for both oily and dry areas.', skin_type_id=combination.id),
        # Normal skin
        Ingredient(name='Vitamin C', description='Potent antioxidant that brightens skin and protects against environmental damage.', skin_type_id=normal.id),
        Ingredient(name='Peptides', description='Amino acid chains that support collagen production for firm, youthful skin.', skin_type_id=normal.id),
        Ingredient(name='Jojoba Oil', description='Lightweight oil that mimics natural sebum to maintain skin balance.', skin_type_id=normal.id),
        # Sensitive skin
        Ingredient(name='Centella Asiatica', description='Calming botanical that repairs skin barrier and reduces inflammation.', skin_type_id=sensitive.id),
        Ingredient(name='Chamomile Extract', description='Gentle anti-inflammatory ingredient that soothes irritated skin.', skin_type_id=sensitive.id),
        Ingredient(name='Oat Extract', description='Natural skin protectant that relieves itching, redness, and sensitivity.', skin_type_id=sensitive.id),
    ]
    db.session.add_all(ingredients)

    # --- Products ---
    products = [
        # Oily skin
        Product(name='Oil-Free Gel Cleanser', description='Lightweight gel formula that removes excess oil without stripping skin. Contains salicylic acid for deep pore cleansing.', image_filename='images/products/cleanser.jpg', skin_type_id=oily.id),
        Product(name='Mattifying Moisturizer SPF 30', description='Oil-free moisturizer with built-in sun protection. Controls shine throughout the day.', image_filename='images/products/sunscreen.jpg', skin_type_id=oily.id),
        # Dry skin
        Product(name='Hydrating Cream Cleanser', description='Rich, creamy cleanser that gently removes impurities while maintaining moisture balance.', image_filename='images/products/cream.jpg', skin_type_id=dry.id),
        Product(name='Intensive Moisture Repair Cream', description='Deep hydrating formula with hyaluronic acid and ceramides for lasting moisture.', image_filename='images/products/moisturizer.jpg', skin_type_id=dry.id),
        # Combination skin
        Product(name='Balancing Foam Cleanser', description='Gentle foaming cleanser that effectively cleanses oily areas while respecting dry zones.', image_filename='images/products/toner.jpg', skin_type_id=combination.id),
        Product(name='Dual-Zone Moisturizer', description='Lightweight formula that hydrates dry areas and controls oil in the T-zone simultaneously.', image_filename='images/products/gel.jpg', skin_type_id=combination.id),
        # Normal skin
        Product(name='Gentle Daily Cleanser', description='Mild, pH-balanced cleanser suitable for daily use. Maintains natural skin balance.', image_filename='images/products/cleanser.jpg', skin_type_id=normal.id),
        Product(name='Vitamin C Brightening Serum', description='Concentrated vitamin C serum that brightens complexion and boosts collagen production.', image_filename='images/products/serum.jpg', skin_type_id=normal.id),
        # Sensitive skin
        Product(name='Ultra-Gentle Micellar Water', description='Fragrance-free micellar water that cleanses without rubbing or rinsing. Perfect for reactive skin.', image_filename='images/products/micellar.jpg', skin_type_id=sensitive.id),
        Product(name='Calming Recovery Balm', description='Soothing balm with centella asiatica and chamomile to calm irritation and strengthen skin barrier.', image_filename='images/products/balm.jpg', skin_type_id=sensitive.id),
    ]
    db.session.add_all(products)

    # --- Quiz Questions ---
    questions = [
        QuizQuestion(
            question_text='How does your skin feel after washing your face?',
            option_a='Tight and dry',
            option_b='Comfortable and balanced',
            option_c='Still oily, especially on forehead and nose',
            correct_answer='b', order=1
        ),
        QuizQuestion(
            question_text='How would you describe your pores?',
            option_a='Small and barely visible',
            option_b='Medium-sized, mostly on nose',
            option_c='Large and visible, especially on T-zone',
            correct_answer='b', order=2
        ),
        QuizQuestion(
            question_text='How often do you experience breakouts?',
            option_a='Rarely or never',
            option_b='Occasionally, usually around my period or stress',
            option_c='Frequently, especially on forehead, nose, and chin',
            correct_answer='a', order=3
        ),
        QuizQuestion(
            question_text='How does your skin react to new products?',
            option_a='Often gets red, itchy, or irritated',
            option_b='Usually adapts well with no issues',
            option_c='Sometimes breaks out in certain areas',
            correct_answer='b', order=4
        ),
        QuizQuestion(
            question_text='By midday, how does your face look?',
            option_a='Dry and flaky in some areas',
            option_b='Still looks fresh and normal',
            option_c='Shiny and greasy, especially T-zone',
            correct_answer='b', order=5
        ),
        QuizQuestion(
            question_text='How does your skin handle sun exposure?',
            option_a='Burns easily, gets red quickly',
            option_b='Tans gradually with moderate exposure',
            option_c='Rarely burns, tans easily',
            correct_answer='b', order=6
        ),
        QuizQuestion(
            question_text='Do you notice different skin textures on different parts of your face?',
            option_a='No, it feels uniformly dry',
            option_b='Yes, oily T-zone but dry cheeks',
            option_c='No, it feels uniformly oily',
            correct_answer='b', order=7
        ),
        QuizQuestion(
            question_text='How does your skin feel in winter?',
            option_a='Very dry, sometimes cracking or peeling',
            option_b='Slightly drier than usual but manageable',
            option_c='About the same, still produces oil',
            correct_answer='b', order=8
        ),
        QuizQuestion(
            question_text='What is your biggest skin concern?',
            option_a='Dryness, flaking, and tightness',
            option_b='Redness, sensitivity, and irritation',
            option_c='Oiliness, acne, and large pores',
            correct_answer='a', order=9
        ),
        QuizQuestion(
            question_text='How much water do you typically drink per day?',
            option_a='Less than 4 glasses',
            option_b='4 to 8 glasses',
            option_c='More than 8 glasses',
            correct_answer='c', order=10
        ),
    ]
    db.session.add_all(questions)

    # --- Blog Posts ---
    admin = User.query.filter_by(is_admin=True).first()
    if admin:
        posts = [
            BlogPost(
                title='5 Essential Steps for a Morning Skincare Routine',
                content='''<p>A solid morning skincare routine sets the foundation for healthy, glowing skin throughout the day. Here are the five essential steps every skincare enthusiast should follow.</p>

<p><strong>Step 1: Gentle Cleanser</strong> — Start your morning with a gentle, pH-balanced cleanser to remove overnight oils and prepare your skin for the products ahead. Avoid harsh soaps that strip natural moisture.</p>

<p><strong>Step 2: Toner</strong> — Apply a hydrating toner to balance your skin's pH levels and provide a base layer of hydration. Look for ingredients like hyaluronic acid or rose water.</p>

<p><strong>Step 3: Serum</strong> — This is where targeted treatment happens. Choose a vitamin C serum for brightening, niacinamide for pore control, or hyaluronic acid for deep hydration.</p>

<p><strong>Step 4: Moisturizer</strong> — Lock in all the goodness with a moisturizer suited to your skin type. Even oily skin needs hydration — just opt for a lightweight, oil-free formula.</p>

<p><strong>Step 5: Sunscreen</strong> — The most critical step! Apply a broad-spectrum SPF 30+ sunscreen every single day, rain or shine. UV damage is the number one cause of premature aging.</p>

<p>Remember, consistency is key. Give your routine at least 4-6 weeks to show visible results.</p>''',
                featured_image='images/blog1.jpg',
                author_id=admin.id
            ),
            BlogPost(
                title='Understanding Your Skin Type: A Complete Guide',
                content='''<p>Knowing your skin type is the first step toward building an effective skincare routine. Using the wrong products for your skin type can lead to breakouts, dryness, or irritation.</p>

<p><strong>Oily Skin</strong> — Characterized by excess sebum production, enlarged pores, and a shiny appearance, especially in the T-zone. Oily skin is prone to acne and blackheads but tends to age more slowly.</p>

<p><strong>Dry Skin</strong> — Feels tight, rough, and may appear flaky or dull. Dry skin lacks natural oils and moisture, making it more susceptible to fine lines and wrinkles.</p>

<p><strong>Combination Skin</strong> — The most common skin type. Oily in the T-zone (forehead, nose, chin) but normal to dry on the cheeks. This requires a balanced approach to skincare.</p>

<p><strong>Normal Skin</strong> — Well-balanced, neither too oily nor too dry. Normal skin has a smooth texture, small pores, and few imperfections. The goal is to maintain this balance.</p>

<p><strong>Sensitive Skin</strong> — Reacts easily to products and environmental factors. May experience redness, itching, burning, or dryness. Requires gentle, fragrance-free products.</p>

<p><strong>How to determine your skin type:</strong> Wash your face with a gentle cleanser, pat dry, and wait 30 minutes without applying any products. Then examine your skin — if it feels tight, you likely have dry skin. If there is noticeable shine on your nose and forehead, you likely have combination or oily skin.</p>''',
                featured_image='images/blog2.jpg',
                author_id=admin.id
            ),
            BlogPost(
                title='Top Ingredients to Look for in Skincare Products',
                content='''<p>With thousands of skincare products on the market, knowing which ingredients actually work can save you time and money. Here are the scientifically-backed ingredients dermatologists recommend.</p>

<p><strong>Retinol (Vitamin A)</strong> — The gold standard for anti-aging. Retinol accelerates cell turnover, boosts collagen production, and helps fade dark spots. Start with a low concentration and build up gradually.</p>

<p><strong>Hyaluronic Acid</strong> — A powerful humectant that can hold up to 1000 times its weight in water. It plumps skin, reduces fine lines, and provides deep hydration without heaviness.</p>

<p><strong>Niacinamide (Vitamin B3)</strong> — A versatile ingredient that regulates oil production, minimizes pores, evens skin tone, and strengthens the skin barrier. Works well with most other ingredients.</p>

<p><strong>Vitamin C</strong> — A potent antioxidant that brightens skin, fades hyperpigmentation, and protects against environmental damage. Best used in the morning before sunscreen.</p>

<p><strong>Salicylic Acid</strong> — A BHA that penetrates deep into pores to dissolve excess oil and dead skin cells. Essential for acne-prone and oily skin types.</p>

<p><strong>Ceramides</strong> — Natural lipids that make up over 50% of the skin barrier. Products with ceramides help repair and maintain a healthy moisture barrier, preventing water loss and irritation.</p>

<p><strong>Centella Asiatica</strong> — Also known as cica, this botanical extract calms inflammation, promotes wound healing, and strengthens the skin barrier. Perfect for sensitive and acne-prone skin.</p>

<p>Always introduce new ingredients one at a time and patch test first to monitor how your skin responds.</p>''',
                featured_image='images/blog3.jpg',
                author_id=admin.id
            ),
            BlogPost(
                title='How to Build a Nighttime Skincare Routine',
                content='''<p>Your nighttime skincare routine is when the real magic happens. While you sleep, your skin enters repair mode — cell turnover increases, and your skin becomes more receptive to active ingredients. Here is how to make the most of it.</p>

<p><strong>Double Cleanse</strong> — Start with an oil-based cleanser to dissolve makeup, sunscreen, and excess sebum. Follow with a water-based cleanser to remove any remaining impurities. This two-step method ensures a perfectly clean canvas.</p>

<p><strong>Exfoliate (2-3 Times a Week)</strong> — Use a chemical exfoliant like glycolic acid or lactic acid to remove dead skin cells and promote cell renewal. Avoid physical scrubs that can cause micro-tears in the skin.</p>

<p><strong>Treatment Serums</strong> — Nighttime is the best time for potent actives. Apply retinol for anti-aging, niacinamide for pore control, or azelaic acid for hyperpigmentation. Start slow and build tolerance gradually.</p>

<p><strong>Eye Cream</strong> — The delicate skin around your eyes needs special attention. Pat a small amount of eye cream using your ring finger to avoid tugging. Look for peptides and caffeine to reduce puffiness and dark circles.</p>

<p><strong>Night Moisturizer or Sleeping Mask</strong> — Seal everything in with a rich night cream or sleeping mask. These are typically thicker than daytime moisturizers and work to restore your skin barrier overnight.</p>

<p>Consistency matters more than perfection. Even on tired nights, at minimum cleanse your face and apply moisturizer before bed.</p>''',
                featured_image='images/blog4.jpg',
                author_id=admin.id
            ),
            BlogPost(
                title='The Science Behind SPF: Why Sunscreen Matters',
                content='''<p>Sunscreen is the single most important product in your skincare routine, yet it remains the most skipped step. Understanding the science behind SPF can help you make better choices for your skin health.</p>

<p><strong>What is SPF?</strong> — SPF stands for Sun Protection Factor. It measures how well a sunscreen protects against UVB rays, the type that causes sunburn. SPF 30 blocks about 97% of UVB rays, while SPF 50 blocks about 98%.</p>

<p><strong>UVA vs UVB Rays</strong> — UVB rays cause sunburn and play a key role in skin cancer. UVA rays penetrate deeper, causing premature aging, wrinkles, and dark spots. A broad-spectrum sunscreen protects against both types.</p>

<p><strong>Chemical vs Physical Sunscreen</strong> — Chemical sunscreens absorb UV rays and convert them to heat using ingredients like avobenzone and oxybenzone. Physical sunscreens sit on top of the skin and reflect rays using zinc oxide or titanium dioxide. Both are effective — choose based on your skin type.</p>

<p><strong>How Much to Apply</strong> — Most people apply only 25-50% of the recommended amount. Use about a quarter teaspoon for your face alone, and reapply every two hours when outdoors, or immediately after swimming or sweating.</p>

<p><strong>Sunscreen Myths</strong> — Dark skin still needs SPF protection. Cloudy days still deliver up to 80% of UV radiation. Car windows block UVB but not UVA rays. Indoor workers near windows are still exposed.</p>

<p>Make sunscreen a non-negotiable daily habit, regardless of weather, season, or skin tone. Your future self will thank you.</p>''',
                featured_image='images/blog5.jpg',
                author_id=admin.id
            ),
            BlogPost(
                title='Common Skincare Mistakes You Should Avoid',
                content='''<p>Even the most dedicated skincare enthusiasts can fall into bad habits that undermine their results. Here are the most common skincare mistakes and how to fix them.</p>

<p><strong>Over-Exfoliating</strong> — Exfoliation is beneficial, but doing it daily or using multiple exfoliating products can damage your skin barrier. This leads to redness, sensitivity, and breakouts. Limit exfoliation to 2-3 times per week.</p>

<p><strong>Skipping Moisturizer on Oily Skin</strong> — Many people with oily skin avoid moisturizer, thinking it will make them oilier. In reality, dehydrated skin produces even more oil to compensate. Use a lightweight, oil-free moisturizer instead.</p>

<p><strong>Changing Products Too Often</strong> — Skincare products need time to work. Switching products every week does not give your skin a chance to adjust and show results. Commit to a routine for at least 6-8 weeks before judging its effectiveness.</p>

<p><strong>Sleeping with Makeup On</strong> — Even one night of sleeping in makeup can clog pores, cause breakouts, and accelerate aging. Keep micellar water and cotton pads on your nightstand for those exhausted evenings.</p>

<p><strong>Ignoring Your Neck and Chest</strong> — Your skincare routine should not stop at your jawline. The neck and chest area show signs of aging just as quickly as the face. Extend your cleanser, serums, and sunscreen to these areas.</p>

<p><strong>Using Hot Water to Wash Your Face</strong> — Hot water strips natural oils and can worsen conditions like rosacea and eczema. Always use lukewarm water for cleansing to keep your skin barrier intact.</p>

<p>Small adjustments to your habits can make a significant difference in your skin health over time. Focus on gentle, consistent care.</p>''',
                featured_image='images/blog6.jpg',
                author_id=admin.id
            ),
        ]
        db.session.add_all(posts)

    db.session.commit()

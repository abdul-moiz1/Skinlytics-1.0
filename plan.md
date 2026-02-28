# Skinlytics — FYP Project Proposal

## 1. Project Title
**Skinlytics: AI-Powered Skin Analysis and Skincare Recommendation Platform**

---

## 2. Introduction

### 2.1 Background
The global skincare industry is valued at over $180 billion and continues to grow rapidly. Despite increased awareness about skincare, many individuals struggle to understand their skin type, identify skin conditions, and choose appropriate products. Professional dermatological consultations are often expensive and inaccessible to the general population. There is a growing demand for accessible, technology-driven solutions that empower individuals to take control of their skin health.

### 2.2 Problem Statement
- Many people are unaware of their actual skin type and existing skin conditions
- Choosing the wrong skincare products due to lack of knowledge can worsen skin problems
- Professional dermatological advice is expensive and not always accessible
- Existing skincare apps often lack comprehensive features combining analysis, recommendations, education, and community content

### 2.3 Motivation
Skinlytics addresses these challenges by providing an all-in-one web platform that combines AI-powered skin analysis with personalized product recommendations, interactive skin health quizzes, and educational blog content from dermatology professionals. The platform democratizes skincare knowledge and makes skin health assessment accessible to everyone.

---

## 3. Objectives

### Primary Objectives
1. **Develop an AI-based skin condition detection system** that analyzes uploaded or captured skin images to identify conditions such as acne, dryness, oiliness, and other common skin concerns
2. **Build a personalized product recommendation engine** that suggests suitable skincare ingredients and products based on the user's identified skin type
3. **Create an interactive skin health quiz** that helps users understand their skin type and receive tailored skincare advice
4. **Implement a blog platform** for dermatologist-authored articles to educate users about skincare best practices

### Secondary Objectives
5. Develop a secure user authentication system for personalized experiences
6. Build an admin panel for content management (blog articles)
7. Ensure responsive, mobile-friendly design for accessibility across all devices
8. Design a modular architecture that supports future ML model integration

---

## 4. Scope

### In Scope
- Web-based application accessible via modern browsers
- 6 core modules: Home, AI Skin Analysis, Product Recommendation, AI Quiz, Blog, Authentication
- User registration and login system with session management
- Image upload and webcam capture functionality
- Mock AI analysis engine (architecture designed for real ML integration)
- Admin panel for blog content management
- Responsive design for desktop and mobile devices
- MySQL database for persistent data storage

### Out of Scope (Future Enhancements)
- Native mobile application (iOS/Android)
- Real-time skin condition tracking over time
- E-commerce integration for direct product purchasing
- Integration with actual trained ML models (TensorFlow/PyTorch)
- Social features (user comments, community forums)
- Multi-language support
- Payment processing

---

## 5. Methodology

### Development Approach: Agile (Iterative Prototyping)

The project follows an Agile development methodology with iterative cycles:

1. **Sprint 1 — Research & Planning** (Week 1-2)
   - Literature review on skin analysis technologies
   - Requirements gathering and wireframe design
   - Technology stack selection and environment setup

2. **Sprint 2 — Core Infrastructure** (Week 3-4)
   - Project structure and Flask app factory
   - Database schema design and model creation
   - Authentication system (login/register)

3. **Sprint 3 — Landing Page & Scan** (Week 5-6)
   - Home page with all sections
   - AI Skin Analysis page with upload/webcam functionality
   - Mock analysis engine implementation

4. **Sprint 4 — Recommendation & Quiz** (Week 7-8)
   - Product recommendation module
   - AI Quiz with question bank and result calculation
   - Database seeding with products, ingredients, and questions

5. **Sprint 5 — Blog & Admin** (Week 9-10)
   - Blog listing and article detail pages
   - Admin panel for CRUD operations on blog posts
   - Content population

6. **Sprint 6 — Polish & Testing** (Week 11-12)
   - Frontend styling refinement and responsive testing
   - Cross-browser testing
   - Bug fixes and performance optimization
   - Final documentation

---

## 6. System Architecture

### 6.1 Architecture Pattern
Client-Server architecture with MVC (Model-View-Controller) design pattern:

```
┌─────────────────────────────────────────────┐
│                  CLIENT                      │
│  (Browser: HTML/CSS/JavaScript)              │
│                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │   Home   │ │   Scan   │ │   Quiz   │     │
│  └──────────┘ └──────────┘ └──────────┘     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │  Recomm. │ │   Blog   │ │   Auth   │     │
│  └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────┬───────────────────────┘
                      │ HTTP Requests
                      ▼
┌─────────────────────────────────────────────┐
│                 SERVER                       │
│           Flask Application                  │
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │         Flask Blueprints              │    │
│  │  main | auth | scan | recommendation │    │
│  │  quiz | blog                          │    │
│  └──────────────┬───────────────────────┘    │
│                 │                             │
│  ┌──────────────▼───────────────────────┐    │
│  │       Business Logic Layer            │    │
│  │  Mock AI Analyzer | Quiz Engine       │    │
│  │  Recommendation Engine                │    │
│  └──────────────┬───────────────────────┘    │
│                 │                             │
│  ┌──────────────▼───────────────────────┐    │
│  │      Data Access Layer (SQLAlchemy)   │    │
│  └──────────────┬───────────────────────┘    │
└─────────────────┼───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│              DATABASE                        │
│         MySQL (skinlytics)                   │
│                                              │
│  Users | Analyses | SkinTypes | Ingredients  │
│  Products | QuizQuestions | QuizResults       │
│  BlogPosts                                   │
└─────────────────────────────────────────────┘
```

### 6.2 Flask Blueprint Structure
```
app/
├── main/           → Home page (landing)
├── auth/           → Login, Register, Logout
├── scan/           → AI Skin Analysis (upload, webcam, results)
├── recommendation/ → Product Recommendations by skin type
├── quiz/           → Interactive Skin Quiz
├── blog/           → Blog articles + Admin panel
└── analysis/       → Mock AI analysis engine
```

---

## 7. Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.10+ |
| Web Framework | Flask | 3.1.x |
| ORM | Flask-SQLAlchemy | 3.1.x |
| Authentication | Flask-Login | 0.6.x |
| Forms | Flask-WTF / WTForms | 1.2.x / 3.2.x |
| Database | MySQL | 8.x |
| DB Driver | PyMySQL | 1.1.x |
| Image Processing | Pillow | 11.x |
| Template Engine | Jinja2 | (bundled with Flask) |
| Frontend | HTML5, CSS3, JavaScript (ES6+) | — |
| Environment | python-dotenv | 1.0.x |

---

## 8. Features (Module Descriptions)

### 8.1 Home Page
The landing page serves as the primary entry point, featuring:
- Navigation bar with links to all 6 modules
- Hero section with bold branding and call-to-action
- About section introducing Skinlytics
- Mission and Vision cards
- "Why analyze your skin?" educational section
- FAQ accordion for common questions
- Footer with quick links, customer service links, and social media

### 8.2 AI Skin Analysis
The core feature of the platform:
- Users can upload a skin photo or capture one via webcam
- On-screen instructions guide proper photo capture (lighting, positioning, etc.)
- The system analyzes the image and returns a prediction with confidence score
- Results display detected conditions (e.g., acne, dryness) with visual confidence bars
- After analysis, users are directed to the AI Quiz for deeper assessment

### 8.3 Product Recommendation
Personalized skincare guidance:
- Users select their skin type (Oily, Dry, Combination)
- System returns recommended ingredients suited for that skin type
- Product cards display recommended skincare products with images and descriptions
- Skincare tips specific to the selected skin type are provided

### 8.4 AI Quiz
Interactive skin health assessment:
- 10-15 multiple-choice questions about skin characteristics and habits
- Questions cover topics like skin feel after washing, pore size, reaction to products, etc.
- Results determine the user's skin type and provide personalized care recommendations
- Quiz results are saved to the user's account for future reference

### 8.5 Blog
Educational content platform:
- Latest skincare articles authored by dermatology professionals
- Each article features an image, title, full content, and author attribution
- Articles cover topics like skincare routines, ingredient education, seasonal care, etc.
- Admin panel allows authorized users to create, edit, and delete posts

### 8.6 Authentication
Secure user management:
- Registration with username, email, and password (with confirmation)
- Login with email and password
- Session-based authentication using Flask-Login
- Password hashing using Werkzeug's security functions
- Role-based access control (regular user vs. admin)

---

## 9. Database Design

### 9.1 Entity-Relationship Summary

```
User (1) ──── (N) Analysis
User (1) ──── (N) QuizResult
User (1) ──── (N) BlogPost (as author, admin only)

SkinType (1) ──── (N) Ingredient
SkinType (1) ──── (N) Product
```

### 9.2 Table Definitions

| Table | Key Fields | Description |
|-------|-----------|-------------|
| **users** | id, username, email, password_hash, is_admin, created_at | Registered users |
| **analyses** | id, user_id (FK), image_filename, condition, confidence, created_at | Skin scan results |
| **skin_types** | id, name, description | Oily, Dry, Combination, Normal, Sensitive |
| **ingredients** | id, name, description, skin_type_id (FK) | Recommended ingredients per skin type |
| **products** | id, name, description, image_filename, skin_type_id (FK) | Recommended products per skin type |
| **quiz_questions** | id, question_text, option_a, option_b, option_c, correct_answer, order | Quiz question bank |
| **quiz_results** | id, user_id (FK), skin_type_result, recommendations_text, created_at | User quiz outcomes |
| **blog_posts** | id, title, content, featured_image, author_id (FK), created_at, updated_at | Blog articles |

---

## 10. Development Timeline

| Phase | Duration | Tasks | Deliverables |
|-------|----------|-------|-------------|
| **Phase 1: Research & Planning** | Week 1-2 | Literature review, requirements analysis, wireframing, tech stack setup | Requirements document, wireframes, project structure |
| **Phase 2: Core Infrastructure** | Week 3-4 | Flask app factory, database models, authentication system | Working login/register, database schema |
| **Phase 3: Landing & Scan** | Week 5-6 | Home page, AI Skin Analysis page, mock analysis engine | Functional landing page + skin scan feature |
| **Phase 4: Recommendation & Quiz** | Week 7-8 | Product recommendation module, AI quiz system, data seeding | Working recommendation + quiz pages |
| **Phase 5: Blog & Admin** | Week 9-10 | Blog pages, admin CRUD panel, content creation | Full blog with admin management |
| **Phase 6: Polish & Testing** | Week 11-12 | Styling refinement, responsive testing, bug fixes, documentation | Final polished application |

---

## 11. Expected Outcomes

1. A fully functional web application with 6 interconnected modules
2. AI skin analysis feature with image upload and webcam capture (mock engine, ready for real ML)
3. Personalized product recommendation system based on skin type
4. Interactive quiz that determines skin type and provides care advice
5. Blog platform with admin content management
6. Secure authentication system with role-based access
7. Responsive design working across desktop and mobile devices
8. Clean, maintainable codebase using Flask blueprints and MVC patterns

---

## 12. Future Enhancements

1. **Real ML Model Integration**: Replace mock analyzer with a trained TensorFlow/PyTorch skin condition classifier
2. **Progress Tracking**: Dashboard showing skin health changes over time with before/after comparisons
3. **Mobile Application**: Native iOS/Android app using React Native or Flutter
4. **E-Commerce Integration**: Direct product purchasing with affiliate links or integrated checkout
5. **Community Features**: User comments on blog posts, skincare routine sharing, forums
6. **Multi-Language Support**: Internationalization for broader accessibility
7. **Push Notifications**: Skincare routine reminders and new article alerts
8. **Advanced Analytics**: Admin dashboard with user engagement metrics and popular content insights

---

## 13. References

1. World Health Organization (WHO) — Skin diseases and conditions fact sheets
2. Flask Documentation — https://flask.palletsprojects.com/
3. SQLAlchemy Documentation — https://docs.sqlalchemy.org/
4. MDN Web Docs — HTML, CSS, JavaScript references
5. MySQL Documentation — https://dev.mysql.com/doc/
6. OWASP Security Guidelines — Web application security best practices
7. Nielsen Norman Group — UX design principles for healthcare applications
8. Research papers on CNN-based skin disease classification (for future ML integration)

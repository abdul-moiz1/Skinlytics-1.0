/* ============================================
   Skinlytics - Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ---- Mobile Navigation Toggle ----
    const navToggle = document.getElementById('navbarToggle');
    const navMenu = document.getElementById('navbarMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navMenu.classList.toggle('nav-open');
            navToggle.classList.toggle('active');
            // Toggle hamburger to X
            const spans = navToggle.querySelectorAll('span');
            if (navToggle.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = '';
                spans[1].style.opacity = '';
                spans[2].style.transform = '';
            }
        });
    }

    // ---- User Dropdown Toggle ----
    const userDropdown = document.getElementById('userDropdown');
    const userDropdownTrigger = document.getElementById('userDropdownTrigger');

    if (userDropdown && userDropdownTrigger) {
        userDropdownTrigger.addEventListener('click', function (e) {
            e.stopPropagation();
            userDropdown.classList.toggle('open');
        });

        // Close on click outside
        document.addEventListener('click', function (e) {
            if (!userDropdown.contains(e.target)) {
                userDropdown.classList.remove('open');
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                userDropdown.classList.remove('open');
            }
        });
    }

    // ---- Flash Message Auto-Dismiss ----
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function (msg) {
        // Auto dismiss after 5 seconds
        setTimeout(function () {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-20px)';
            setTimeout(function () { msg.remove(); }, 300);
        }, 5000);

        // Manual dismiss
        const dismissBtn = msg.querySelector('.flash-dismiss');
        if (dismissBtn) {
            dismissBtn.addEventListener('click', function () {
                msg.style.opacity = '0';
                msg.style.transform = 'translateY(-20px)';
                setTimeout(function () { msg.remove(); }, 300);
            });
        }
    });

    // ---- FAQ Accordion ----
    const faqToggles = document.querySelectorAll('.faq-question');
    faqToggles.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const item = this.closest('.faq-item');
            const answer = item.querySelector('.faq-answer');
            const icon = this.querySelector('.faq-icon');
            const isOpen = item.classList.contains('active');

            // Close all other items
            document.querySelectorAll('.faq-item.active').forEach(function (openItem) {
                openItem.classList.remove('active');
                openItem.querySelector('.faq-answer').style.maxHeight = '0';
                var openIcon = openItem.querySelector('.faq-icon');
                if (openIcon) openIcon.textContent = '+';
                openItem.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
            });

            // Toggle current
            if (!isOpen) {
                item.classList.add('active');
                answer.style.maxHeight = answer.scrollHeight + 'px';
                if (icon) icon.textContent = '\u2212';
                this.setAttribute('aria-expanded', 'true');
            }
        });
    });

    // ---- Smooth Scroll for Anchor Links ----
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
        link.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ---- Navbar Scroll Effect ----
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // ---- Skin Type Selector (Recommendation Page) ----
    const skinTypeBtns = document.querySelectorAll('.skin-type-btn');
    skinTypeBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            // Remove selected from all
            skinTypeBtns.forEach(function (b) { b.classList.remove('selected'); });
            // Add selected to clicked
            this.classList.add('selected');
            // Check the hidden radio
            const radio = this.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;
        });
    });

    // ---- Quiz Navigation ----
    const quizQuestions = document.querySelectorAll('.quiz-question');
    const prevBtn = document.getElementById('quiz-prev');
    const nextBtn = document.getElementById('quiz-next');
    const submitBtn = document.getElementById('quiz-submit');
    const progressFill = document.querySelector('.quiz-progress-fill');
    let currentQuestion = 0;

    function showQuestion(index) {
        quizQuestions.forEach(function (q, i) {
            q.style.display = i === index ? 'block' : 'none';
        });

        // Update buttons
        if (prevBtn) prevBtn.style.display = index === 0 ? 'none' : 'inline-block';
        if (nextBtn) nextBtn.style.display = index === quizQuestions.length - 1 ? 'none' : 'inline-block';
        if (submitBtn) submitBtn.style.display = index === quizQuestions.length - 1 ? 'inline-block' : 'none';

        // Update progress
        if (progressFill) {
            const progress = ((index + 1) / quizQuestions.length) * 100;
            progressFill.style.width = progress + '%';
        }

        currentQuestion = index;
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', function () {
            // Validate current question has an answer
            const currentQ = quizQuestions[currentQuestion];
            const selected = currentQ.querySelector('input[type="radio"]:checked');
            if (!selected) {
                alert('Please select an answer before proceeding.');
                return;
            }
            if (currentQuestion < quizQuestions.length - 1) {
                showQuestion(currentQuestion + 1);
            }
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', function () {
            if (currentQuestion > 0) {
                showQuestion(currentQuestion - 1);
            }
        });
    }

    // ---- Animated Confidence Bar ----
    const confidenceFill = document.querySelector('.confidence-fill');
    if (confidenceFill) {
        const targetWidth = confidenceFill.style.width;
        confidenceFill.style.width = '0';
        setTimeout(function () {
            confidenceFill.style.width = targetWidth;
        }, 300);
    }

    // ---- Active Nav Link Highlighting ----
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function (link) {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });

});

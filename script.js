// flywithpeggs.com — Main JavaScript
// Altidor Wellness LLC

document.addEventListener('DOMContentLoaded', function () {

    // --- Mobile Menu Logic ---
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            // Toggle icon between bars and X
            const icon = mobileMenuButton.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-times');
            }
        });
    }

    // --- Desktop Dropdown (Services) ---
    // Robust JS dropdown that stays open while hovering anywhere in the zone
    document.querySelectorAll('.dropdown-trigger').forEach(trigger => {
        const parent = trigger.closest('.dropdown-wrap');
        const menu = parent ? parent.querySelector('.dropdown-menu') : null;
        if (!parent || !menu) return;

        let closeTimer = null;
        let isOpen = false;

        function show() {
            if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }
            menu.classList.remove('hidden');
            // Force reflow so the transition actually plays
            void menu.offsetHeight;
            menu.classList.remove('opacity-0', 'translate-y-2');
            menu.classList.add('opacity-100', 'translate-y-0');
            isOpen = true;
        }

        function scheduleHide() {
            if (closeTimer) clearTimeout(closeTimer);
            closeTimer = setTimeout(() => {
                menu.classList.remove('opacity-100', 'translate-y-0');
                menu.classList.add('opacity-0', 'translate-y-2');
                setTimeout(() => {
                    menu.classList.add('hidden');
                    isOpen = false;
                }, 200);
            }, 400); // 400ms grace period — plenty of time to reach the menu
        }

        // Hover on parent (covers both trigger + menu since menu is inside parent)
        parent.addEventListener('mouseenter', show);
        parent.addEventListener('mouseleave', scheduleHide);

        // Also keep open when mouse enters the menu directly
        menu.addEventListener('mouseenter', show);
        menu.addEventListener('mouseleave', scheduleHide);

        // Keyboard support
        trigger.addEventListener('focus', show);
        parent.addEventListener('focusout', (e) => {
            if (!parent.contains(e.relatedTarget)) scheduleHide();
        });

        // Click/tap toggle
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (isOpen) {
                if (closeTimer) clearTimeout(closeTimer);
                menu.classList.remove('opacity-100', 'translate-y-0');
                menu.classList.add('opacity-0', 'translate-y-2');
                setTimeout(() => { menu.classList.add('hidden'); isOpen = false; }, 200);
            } else {
                show();
            }
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (isOpen && !parent.contains(e.target)) {
                if (closeTimer) clearTimeout(closeTimer);
                menu.classList.remove('opacity-100', 'translate-y-0');
                menu.classList.add('opacity-0', 'translate-y-2');
                setTimeout(() => { menu.classList.add('hidden'); isOpen = false; }, 200);
            }
        });
    });

    // --- Current Year for Footer ---
    const currentYearEl = document.getElementById('currentYear');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear();
    }

    // --- Active Navigation Link Highlighting ---
    const currentPagePath = window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1) || 'index.html';
    document.querySelectorAll('header nav a, #mobile-menu a').forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPagePath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // --- Scroll-triggered Fade-in Animations ---
    const faders = document.querySelectorAll('.fade-in-up');
    if (faders.length && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

        faders.forEach(el => observer.observe(el));
    }

    // --- Smooth number counter for stats ---
    const counters = document.querySelectorAll('[data-count]');
    if (counters.length && 'IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.getAttribute('data-count'), 10);
                    const suffix = el.getAttribute('data-suffix') || '';
                    let current = 0;
                    const step = Math.max(1, Math.floor(target / 60));
                    const timer = setInterval(() => {
                        current += step;
                        if (current >= target) {
                            current = target;
                            clearInterval(timer);
                        }
                        el.textContent = current + suffix;
                    }, 20);
                    counterObserver.unobserve(el);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(el => counterObserver.observe(el));
    }

    // --- Typing effect for hero tagline ---
    const typingEl = document.getElementById('typing-text');
    if (typingEl) {
        const phrases = [
            'Live Well.',
            'Travel Far.',
            'Build Bold.',
        ];
        let phraseIndex = 0;
        let charIndex = 0;
        let isDeleting = false;

        function type() {
            const current = phrases[phraseIndex];
            if (isDeleting) {
                typingEl.textContent = current.substring(0, charIndex--);
                if (charIndex < 0) {
                    isDeleting = false;
                    phraseIndex = (phraseIndex + 1) % phrases.length;
                    setTimeout(type, 400);
                    return;
                }
                setTimeout(type, 40);
            } else {
                typingEl.textContent = current.substring(0, charIndex++);
                if (charIndex > current.length) {
                    isDeleting = true;
                    setTimeout(type, 1800);
                    return;
                }
                setTimeout(type, 100);
            }
        }
        setTimeout(type, 600);
    }

    // --- Header background change on scroll ---
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 60) {
                header.classList.add('header-scrolled');
            } else {
                header.classList.remove('header-scrolled');
            }
        });
    }

    // --- n8n Newsletter Signup ---
    // Sends newsletter signups to an n8n webhook.
    (function initNewsletterForm() {
        // ============================================================
        // REPLACE THIS with your n8n Webhook production URL:
        const N8N_NEWSLETTER_WEBHOOK = 'YOUR_N8N_NEWSLETTER_WEBHOOK_URL';
        // ============================================================

        const form = document.getElementById('newsletter-form');
        if (!form) return;

        const emailInput = document.getElementById('newsletter-email');
        const submitBtn = document.getElementById('newsletter-btn');
        const btnText = document.getElementById('newsletter-btn-text');
        const spinner = document.getElementById('newsletter-spinner');
        const resultEl = document.getElementById('newsletter-result');
        const disclaimer = document.getElementById('newsletter-disclaimer');

        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            const email = emailInput.value.trim();
            if (!email) return;

            // Show loading state
            submitBtn.disabled = true;
            btnText.textContent = 'Subscribing...';
            spinner.classList.remove('hidden');
            resultEl.classList.add('hidden');

            try {
                const response = await fetch(N8N_NEWSLETTER_WEBHOOK, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: email,
                        source: 'flywithpeggs.com/newsletter',
                        subscribed_at: new Date().toISOString()
                    })
                });

                if (response.ok) {
                    resultEl.classList.remove('hidden');
                    resultEl.style.color = '#86efac';
                    resultEl.innerHTML = '<i class="fas fa-check-circle mr-1"></i> You\'re in! Welcome to the community.';
                    disclaimer.classList.add('hidden');
                    form.reset();
                } else {
                    throw new Error('Server returned ' + response.status);
                }
            } catch (error) {
                resultEl.classList.remove('hidden');
                resultEl.style.color = '#fca5a5';
                resultEl.innerHTML = '<i class="fas fa-exclamation-circle mr-1"></i> Something went wrong. Please try again.';
                console.error('Newsletter signup error:', error);
            } finally {
                submitBtn.disabled = false;
                btnText.textContent = 'Subscribe';
                spinner.classList.add('hidden');
            }
        });
    })();

    // --- n8n Chat Widget ---
    // Loads the @n8n/chat widget with flywithpeggs brand styling.
    // Replace the webhookUrl below with your actual n8n Chat Trigger webhook URL.
    (function initN8nChat() {
        // 1. Inject the n8n chat stylesheet
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/style.css';
        document.head.appendChild(link);

        // 2. Inject brand-override CSS variables for the chat widget
        const style = document.createElement('style');
        style.textContent = `
            :root {
                /* n8n Chat — flywithpeggs brand overrides */
                --chat--color--primary: #5D3FD3;
                --chat--color--primary-shade-50: #4A00E0;
                --chat--color--primary--shade-100: #3a00b3;
                --chat--color--secondary: #FFC000;
                --chat--color-secondary-shade-50: #e6ac00;
                --chat--color-white: #FFFFFF;
                --chat--color-light: #F5F5F5;
                --chat--color-light-shade-50: #F0E6FF;
                --chat--color-light-shade-100: #d4bfff;
                --chat--color-medium: #9966CC;
                --chat--color-dark: #1A1A3E;
                --chat--color-typing: #5D3FD3;
                --chat--font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

                /* Window */
                --chat--window--width: 380px;
                --chat--window--height: 560px;
                --chat--window--border-radius: 0.75rem;
                --chat--window--border: 1px solid rgba(93, 63, 211, 0.2);

                /* Header */
                --chat--header--background: #1A1A3E;
                --chat--header--color: #F8F8FF;

                /* Toggle button */
                --chat--toggle--background: #5D3FD3;
                --chat--toggle--hover--background: #4A00E0;
                --chat--toggle--active--background: #3a00b3;
                --chat--toggle--color: #FFC000;

                /* Messages */
                --chat--message--bot--background: #F0E6FF;
                --chat--message--bot--color: #1A1A3E;
                --chat--message--user--background: #5D3FD3;
                --chat--message--user--color: #F8F8FF;

                /* Input */
                --chat--input--background: #FFFFFF;
                --chat--input--text-color: #1A1A3E;

                /* Buttons inside chat */
                --chat--button--background--primary: #FFC000;
                --chat--button--color--primary: #1A1A3E;
                --chat--button--background--primary--hover: #e6ac00;
                --chat--button--color--primary--hover: #1A1A3E;

                /* Send button */
                --chat--input--send--button--color: #5D3FD3;
                --chat--input--send--button--color-hover: #4A00E0;

                /* Body / footer */
                --chat--body--background: #FFFFFF;
                --chat--footer--background: #F0E6FF;
                --chat--footer--color: #1A1A3E;
            }
        `;
        document.head.appendChild(style);

        // 3. Dynamically import and initialize the chat
        const script = document.createElement('script');
        script.type = 'module';
        script.textContent = `
            import { createChat } from 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/chat.bundle.es.js';

            createChat({
                webhookUrl: 'YOUR_N8N_WEBHOOK_URL',
                mode: 'window',
                showWelcomeScreen: false,
                loadPreviousSession: true,
                initialMessages: [
                    'Hey there! 👋',
                    "I'm Peggens' AI assistant. I can help with AI consulting, wellness, or travel questions. What can I do for you?"
                ],
                i18n: {
                    en: {
                        title: 'Chat with Peggens',
                        subtitle: 'AI-powered assistant — here to help 24/7.',
                        footer: 'Powered by flywithpeggs.com',
                        getStarted: 'New Conversation',
                        inputPlaceholder: 'Ask me anything...',
                    },
                },
            });
        `;
        document.body.appendChild(script);
    })();
});

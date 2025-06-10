// This file will hold the JavaScript for all pages.

document.addEventListener('DOMContentLoaded', function() {

    // --- Mobile Menu Logic ---
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // --- Current Year for Footer ---
    const currentYearEl = document.getElementById('currentYear');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear();
    }

    // --- Active Navigation Link Highlighting ---
    // This script highlights the nav link of the current page you're on.
    const currentPagePath = window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1) || 'index.html';
    document.querySelectorAll('header nav a, #mobile-menu a').forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPagePath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // NOTE: Page-specific logic, like for the Game or AI Survey, should be included
    // directly in a <script> tag on those specific HTML pages to keep this file clean.
});

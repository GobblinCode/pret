// Main JavaScript for GamblingReviews website
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all modules
    initMobileMenu();
    initTabs();
    initScrollEffects();
    initSmoothScrolling();
    initNewsletterForm();
    initHeaderScrollEffect();
    initLoadingAnimations();
    initAccessibilityFeatures();
});

// Mobile Menu Functionality
function initMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileToggle && mainNav) {
        mobileToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
            
            // Animate hamburger icon
            const icon = mobileToggle.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-times');
            }
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mainNav.contains(e.target) && !mobileToggle.contains(e.target)) {
                mainNav.classList.remove('active');
                const icon = mobileToggle.querySelector('i');
                if (icon) {
                    icon.classList.add('fa-bars');
                    icon.classList.remove('fa-times');
                }
            }
        });

        // Close mobile menu when clicking on a link
        const navLinks = mainNav.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                mainNav.classList.remove('active');
                const icon = mobileToggle.querySelector('i');
                if (icon) {
                    icon.classList.add('fa-bars');
                    icon.classList.remove('fa-times');
                }
            });
        });
    }
}

// Tab Functionality
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
            }
            
            // Animate tab change
            requestAnimationFrame(() => {
                targetContent.style.opacity = '0';
                targetContent.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    targetContent.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                    targetContent.style.opacity = '1';
                    targetContent.style.transform = 'translateY(0)';
                }, 50);
            });
        });
    });
}

// Scroll Effects
function initScrollEffects() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll('.site-card, .feature-card, .review-card');
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// Smooth Scrolling
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Newsletter Form
function initNewsletterForm() {
    const form = document.querySelector('.newsletter-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = this.querySelector('input[type="email"]').value;
            const button = this.querySelector('button');
            const originalText = button.textContent;
            
            if (validateEmail(email)) {
                // Show loading state
                button.innerHTML = '<span class="loading"></span> Subscribing...';
                button.disabled = true;
                
                // Simulate API call
                setTimeout(() => {
                    button.innerHTML = '<i class="fas fa-check"></i> Subscribed!';
                    button.style.background = '#10b981';
                    
                    // Reset form
                    this.reset();
                    
                    // Show success message
                    showNotification('Thank you for subscribing!', 'success');
                    
                    // Reset button after 3 seconds
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.disabled = false;
                        button.style.background = '';
                    }, 3000);
                }, 1500);
            } else {
                showNotification('Please enter a valid email address', 'error');
            }
        });
    }
}

// Email Validation
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Header Scroll Effect
function initHeaderScrollEffect() {
    const header = document.querySelector('.header');
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', function() {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        // Hide header when scrolling down, show when scrolling up
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollY = currentScrollY;
    });
}

// Loading Animations
function initLoadingAnimations() {
    // Add loading animation to buttons when clicked
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Don't add loading to external links
            if (this.getAttribute('href') && this.getAttribute('href').startsWith('http')) {
                return;
            }
            
            const originalContent = this.innerHTML;
            this.innerHTML = '<span class="loading"></span> Loading...';
            this.disabled = true;
            
            // Simulate loading
            setTimeout(() => {
                this.innerHTML = originalContent;
                this.disabled = false;
            }, 1000);
        });
    });
}

// Accessibility Features
function initAccessibilityFeatures() {
    // Keyboard navigation for dropdowns
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('a');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (trigger && menu) {
            trigger.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    menu.classList.toggle('show');
                }
            });
            
            // Close dropdown with Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    menu.classList.remove('show');
                }
            });
        }
    });
    
    // Focus management
    const focusableElements = document.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '2px solid #2563eb';
            this.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', function() {
            this.style.outline = '';
            this.style.outlineOffset = '';
        });
    });
}

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">×</button>
        </div>
    `;
    
    // Add notification styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#2563eb'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    requestAnimationFrame(() => {
        notification.style.transform = 'translateX(0)';
    });
    
    // Close button functionality
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', function() {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 300);
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Performance Optimization
function optimizeImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize image optimization
document.addEventListener('DOMContentLoaded', optimizeImages);

// Search Functionality (if needed)
function initSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchResults = document.querySelector('.search-results');
    
    if (searchInput && searchResults) {
        const debouncedSearch = debounce(performSearch, 300);
        
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            if (query.length > 2) {
                debouncedSearch(query);
            } else {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
            }
        });
    }
}

function performSearch(query) {
    // Simulate search API call
    // In a real implementation, this would call your search API
    console.log('Searching for:', query);
    
    // Show loading state
    const searchResults = document.querySelector('.search-results');
    searchResults.innerHTML = '<div class="search-loading">Searching...</div>';
    searchResults.style.display = 'block';
    
    // Simulate API response
    setTimeout(() => {
        const mockResults = [
            { title: 'Bovada Casino Review', url: '/reviews/bovada', type: 'review' },
            { title: 'Best Online Casinos', url: '/casinos', type: 'page' },
            { title: 'Sports Betting Guide', url: '/guides/sports-betting', type: 'guide' }
        ];
        
        displaySearchResults(mockResults);
    }, 500);
}

function displaySearchResults(results) {
    const searchResults = document.querySelector('.search-results');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="search-no-results">No results found</div>';
        return;
    }
    
    const resultsHTML = results.map(result => `
        <div class="search-result">
            <a href="${result.url}">
                <h4>${result.title}</h4>
                <span class="search-result-type">${result.type}</span>
            </a>
        </div>
    `).join('');
    
    searchResults.innerHTML = resultsHTML;
}

// Export functions for use in other modules
window.GamblingReviews = {
    showNotification,
    debounce,
    throttle,
    validateEmail
};
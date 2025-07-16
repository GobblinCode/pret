// Referral Tracking System for GamblingReviews
// This system tracks referrals using cookies and local storage
// Even if users don't click directly on referral links, they can still be tracked

class ReferralTracker {
    constructor() {
        this.referralData = {
            // Your referral links for different sites
            bovada: 'https://www.bovada.lv/welcome/P2A99D9D5/join/?extcmpid=rf-ggr-ref',
            ignition: 'https://www.ignitioncasino.eu/welcome/P2A99D9D5/join/?extcmpid=rf-ggr-ref',
            cafe: 'https://www.cafecasino.lv/welcome/P2A99D9D5/join/?extcmpid=rf-ggr-ref',
            betus: 'https://www.betus.com.pa/sportsbook/welcome/?btag=a_1234b_567c_ggr',
            // Add more referral links as needed
        };
        
        this.cookieExpiration = 30; // Days
        this.init();
    }
    
    init() {
        this.setReferralCookies();
        this.attachReferralListeners();
        this.trackPageViews();
        this.handleDirectLinks();
        this.setupPeriodicTracking();
    }
    
    // Set referral cookies when user visits the site
    setReferralCookies() {
        const referralSource = this.getReferralSource();
        const timestamp = Date.now();
        
        // Set main referral cookie
        this.setCookie('gr_referral_source', referralSource, this.cookieExpiration);
        this.setCookie('gr_first_visit', timestamp, this.cookieExpiration);
        
        // Set individual site cookies
        Object.keys(this.referralData).forEach(site => {
            this.setCookie(`gr_${site}_ref`, 'true', this.cookieExpiration);
        });
        
        // Store in localStorage as backup
        this.setLocalStorage('gr_referral_data', {
            source: referralSource,
            timestamp: timestamp,
            sites: Object.keys(this.referralData)
        });
    }
    
    // Get referral source from URL parameters or referrer
    getReferralSource() {
        const urlParams = new URLSearchParams(window.location.search);
        const refParam = urlParams.get('ref') || urlParams.get('referral');
        const utmSource = urlParams.get('utm_source');
        
        if (refParam) return refParam;
        if (utmSource) return utmSource;
        
        // Check document referrer
        const referrer = document.referrer;
        if (referrer) {
            try {
                const referrerDomain = new URL(referrer).hostname;
                return referrerDomain;
            } catch (e) {
                return 'direct';
            }
        }
        
        return 'direct';
    }
    
    // Attach event listeners to referral links
    attachReferralListeners() {
        const referralLinks = document.querySelectorAll('[data-referral]');
        
        referralLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                const siteName = link.getAttribute('data-referral');
                const referralUrl = this.referralData[siteName];
                
                if (referralUrl) {
                    // Track the click
                    this.trackReferralClick(siteName);
                    
                    // Add tracking parameters
                    const trackedUrl = this.addTrackingParams(referralUrl, siteName);
                    
                    // Open in new tab
                    window.open(trackedUrl, '_blank', 'noopener,noreferrer');
                    
                    // Show notification
                    if (window.GamblingReviews && window.GamblingReviews.showNotification) {
                        window.GamblingReviews.showNotification('Redirecting to ' + siteName + '...', 'info');
                    }
                }
            });
        });
    }
    
    // Track referral clicks
    trackReferralClick(siteName) {
        const clickData = {
            site: siteName,
            timestamp: Date.now(),
            url: window.location.href,
            userAgent: navigator.userAgent
        };
        
        // Store click data
        this.setCookie(`gr_click_${siteName}`, JSON.stringify(clickData), this.cookieExpiration);
        
        // Add to click history
        const clickHistory = this.getClickHistory();
        clickHistory.push(clickData);
        this.setLocalStorage('gr_click_history', clickHistory);
        
        // Send to analytics (if available)
        this.sendAnalytics('referral_click', clickData);
    }
    
    // Add tracking parameters to referral URL
    addTrackingParams(url, siteName) {
        const urlObj = new URL(url);
        const params = new URLSearchParams(urlObj.search);
        
        // Add custom tracking parameters
        params.set('gr_ref', 'true');
        params.set('gr_site', siteName);
        params.set('gr_timestamp', Date.now());
        params.set('gr_source', window.location.hostname);
        
        // Add user identifier if available
        const userId = this.getUserId();
        if (userId) {
            params.set('gr_user', userId);
        }
        
        urlObj.search = params.toString();
        return urlObj.toString();
    }
    
    // Track page views for referral attribution
    trackPageViews() {
        const pageData = {
            url: window.location.href,
            title: document.title,
            timestamp: Date.now(),
            referrer: document.referrer
        };
        
        // Store page view
        const pageViews = this.getPageViews();
        pageViews.push(pageData);
        
        // Keep only last 50 page views
        if (pageViews.length > 50) {
            pageViews.shift();
        }
        
        this.setLocalStorage('gr_page_views', pageViews);
    }
    
    // Handle direct links and auto-redirect with referral tracking
    handleDirectLinks() {
        // Check if user is visiting gambling sites directly
        const currentHost = window.location.hostname;
        const gamblingHosts = ['bovada.lv', 'ignitioncasino.eu', 'cafecasino.lv', 'betus.com.pa'];
        
        if (gamblingHosts.some(host => currentHost.includes(host))) {
            // User is on gambling site, check for our referral cookies
            const hasReferralCookie = this.getCookie('gr_referral_source');
            
            if (hasReferralCookie && !this.hasReferralInUrl()) {
                // Redirect with referral parameters
                this.redirectWithReferral();
            }
        }
    }
    
    // Check if current URL has referral parameters
    hasReferralInUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.has('gr_ref') || urlParams.has('extcmpid') || urlParams.has('btag');
    }
    
    // Redirect with referral parameters
    redirectWithReferral() {
        const currentUrl = window.location.href;
        const siteName = this.detectSiteFromUrl(currentUrl);
        
        if (siteName && this.referralData[siteName]) {
            const referralUrl = this.addTrackingParams(this.referralData[siteName], siteName);
            window.location.replace(referralUrl);
        }
    }
    
    // Detect site name from URL
    detectSiteFromUrl(url) {
        const urlLower = url.toLowerCase();
        
        if (urlLower.includes('bovada')) return 'bovada';
        if (urlLower.includes('ignition')) return 'ignition';
        if (urlLower.includes('cafe')) return 'cafe';
        if (urlLower.includes('betus')) return 'betus';
        
        return null;
    }
    
    // Setup periodic tracking to maintain referral attribution
    setupPeriodicTracking() {
        // Track user activity every 30 seconds
        setInterval(() => {
            this.trackUserActivity();
        }, 30000);
        
        // Refresh cookies every 24 hours
        setInterval(() => {
            this.refreshReferralCookies();
        }, 24 * 60 * 60 * 1000);
    }
    
    // Track user activity
    trackUserActivity() {
        const activity = {
            timestamp: Date.now(),
            url: window.location.href,
            scrollPosition: window.pageYOffset,
            isActive: document.hasFocus()
        };
        
        // Store activity
        this.setLocalStorage('gr_last_activity', activity);
        
        // Extend cookie expiration
        this.refreshReferralCookies();
    }
    
    // Refresh referral cookies
    refreshReferralCookies() {
        const existingSource = this.getCookie('gr_referral_source');
        if (existingSource) {
            this.setCookie('gr_referral_source', existingSource, this.cookieExpiration);
            
            // Refresh all site cookies
            Object.keys(this.referralData).forEach(site => {
                this.setCookie(`gr_${site}_ref`, 'true', this.cookieExpiration);
            });
        }
    }
    
    // Get user ID (generate if doesn't exist)
    getUserId() {
        let userId = this.getCookie('gr_user_id');
        if (!userId) {
            userId = this.generateUserId();
            this.setCookie('gr_user_id', userId, 365); // 1 year expiration
        }
        return userId;
    }
    
    // Generate unique user ID
    generateUserId() {
        return 'gr_' + Date.now() + '_' + Math.random().toString(36).substring(2, 15);
    }
    
    // Get click history
    getClickHistory() {
        return this.getLocalStorage('gr_click_history') || [];
    }
    
    // Get page views
    getPageViews() {
        return this.getLocalStorage('gr_page_views') || [];
    }
    
    // Send analytics data
    sendAnalytics(event, data) {
        // Send to Google Analytics if available
        if (typeof gtag !== 'undefined') {
            gtag('event', event, {
                custom_parameter: JSON.stringify(data)
            });
        }
        
        // Send to custom analytics endpoint
        if (window.location.hostname !== 'localhost') {
            fetch('/api/analytics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    event: event,
                    data: data,
                    timestamp: Date.now()
                })
            }).catch(err => {
                console.log('Analytics error:', err);
            });
        }
    }
    
    // Cookie utilities
    setCookie(name, value, days) {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${encodeURIComponent(value)};expires=${expires.toUTCString()};path=/;SameSite=Lax`;
    }
    
    getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) {
                return decodeURIComponent(c.substring(nameEQ.length, c.length));
            }
        }
        return null;
    }
    
    // LocalStorage utilities
    setLocalStorage(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.log('LocalStorage error:', e);
        }
    }
    
    getLocalStorage(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.log('LocalStorage error:', e);
            return null;
        }
    }
    
    // Public methods for external use
    
    // Get referral stats
    getReferralStats() {
        return {
            source: this.getCookie('gr_referral_source'),
            firstVisit: this.getCookie('gr_first_visit'),
            userId: this.getUserId(),
            clickHistory: this.getClickHistory(),
            pageViews: this.getPageViews()
        };
    }
    
    // Force referral for a specific site
    forceReferral(siteName) {
        if (this.referralData[siteName]) {
            this.trackReferralClick(siteName);
            const referralUrl = this.addTrackingParams(this.referralData[siteName], siteName);
            window.open(referralUrl, '_blank', 'noopener,noreferrer');
        }
    }
    
    // Clear all referral data
    clearReferralData() {
        Object.keys(this.referralData).forEach(site => {
            this.setCookie(`gr_${site}_ref`, '', -1);
            this.setCookie(`gr_click_${site}`, '', -1);
        });
        
        this.setCookie('gr_referral_source', '', -1);
        this.setCookie('gr_first_visit', '', -1);
        this.setCookie('gr_user_id', '', -1);
        
        localStorage.removeItem('gr_referral_data');
        localStorage.removeItem('gr_click_history');
        localStorage.removeItem('gr_page_views');
        localStorage.removeItem('gr_last_activity');
    }
}

// Initialize referral tracker when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.referralTracker = new ReferralTracker();
});

// Additional tracking for specific events
document.addEventListener('visibilitychange', function() {
    if (window.referralTracker && !document.hidden) {
        window.referralTracker.trackUserActivity();
    }
});

// Track when user is about to leave
window.addEventListener('beforeunload', function() {
    if (window.referralTracker) {
        window.referralTracker.trackUserActivity();
    }
});

// Enhanced mobile detection and tracking
if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
    document.addEventListener('touchstart', function() {
        if (window.referralTracker) {
            window.referralTracker.trackUserActivity();
        }
    });
}

// Export for external use
window.ReferralTracker = ReferralTracker;
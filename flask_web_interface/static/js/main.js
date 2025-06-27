// Main JavaScript for Chevy Casting Lookup

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert && alert.parentNode) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });

    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Searching...';
                submitBtn.disabled = true;
                
                // Re-enable button after 10 seconds as fallback
                setTimeout(function() {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 10000);
            }
        });
    });

    // Enhanced search functionality
    const castingNumberInput = document.querySelector('input[name="casting_number"]');
    if (castingNumberInput) {
        // Format casting number input (remove spaces, convert to uppercase)
        castingNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s+/g, '').toUpperCase();
            e.target.value = value;
        });

        // Add enter key support
        castingNumberInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const form = e.target.closest('form');
                if (form) {
                    form.submit();
                }
            }
        });
    }

    // Add smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy to clipboard functionality for casting numbers
    const castingNumbers = document.querySelectorAll('.casting-number-copy');
    castingNumbers.forEach(function(element) {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            const text = this.textContent.trim();
            
            if (navigator.clipboard) {
                navigator.clipboard.writeText(text).then(function() {
                    showToast('Casting number copied to clipboard!', 'success');
                });
            } else {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showToast('Casting number copied to clipboard!', 'success');
            }
        });
    });

    // Table row click functionality
    const tableRows = document.querySelectorAll('table tbody tr[data-href]');
    tableRows.forEach(function(row) {
        row.style.cursor = 'pointer';
        row.addEventListener('click', function() {
            window.location.href = this.dataset.href;
        });
    });

    // Advanced search form validation
    const advancedSearchForm = document.querySelector('form[action*="advanced_search"]');
    if (advancedSearchForm) {
        advancedSearchForm.addEventListener('submit', function(e) {
            const formData = new FormData(this);
            let hasValue = false;
            
            for (let [key, value] of formData.entries()) {
                if (value.trim() !== '') {
                    hasValue = true;
                    break;
                }
            }
            
            if (!hasValue) {
                e.preventDefault();
                showToast('Please enter at least one search criteria.', 'warning');
            }
        });
    }

    // API status checker
    function checkAPIStatus() {
        const statusBadge = document.querySelector('.api-status-badge');
        if (statusBadge) {
            fetch('/api/health')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'connected') {
                        statusBadge.className = 'badge bg-success';
                        statusBadge.textContent = 'API Connected';
                    } else {
                        statusBadge.className = 'badge bg-danger';
                        statusBadge.textContent = 'API Disconnected';
                    }
                })
                .catch(() => {
                    statusBadge.className = 'badge bg-danger';
                    statusBadge.textContent = 'API Disconnected';
                });
        }
    }

    // Check API status on page load and every 30 seconds
    checkAPIStatus();
    setInterval(checkAPIStatus, 30000);
});

// Toast notification function
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }

    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'success' ? 'success' : type === 'warning' ? 'warning' : 'info'} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 3000
    });
    
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// Utility function to format numbers
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

// Utility function to validate casting number format
function isValidCastingNumber(castingNumber) {
    // Basic validation - should be alphanumeric, typically 6-8 characters
    const pattern = /^[A-Z0-9]{6,8}$/;
    return pattern.test(castingNumber.toUpperCase());
}

// Transaction form JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize category filtering
    initializeCategoryFilter();
    
    // Initialize form validation
    initializeFormValidation();
});

function initializeCategoryFilter() {
    const transactionTypeSelect = document.getElementById('transactionType');
    const categorySelect = document.getElementById('categorySelect');
    
    if (!transactionTypeSelect || !categorySelect) return;
    
    // Categories mapping
    const categories = {
        'income': [
            'Salary', 'Freelance', 'Business', 'Investment', 'Rental', 'Gift', 'Other Income'
        ],
        'expense': [
            'Food', 'Transportation', 'Housing', 'Utilities', 'Healthcare', 'Entertainment',
            'Shopping', 'Travel', 'Education', 'Insurance', 'Debt Payment', 'Other Expenses'
        ]
    };
    
    // Update categories based on transaction type
    function updateCategories() {
        const selectedType = transactionTypeSelect.value;
        const availableCategories = categories[selectedType] || [];
        
        // Clear existing options
        categorySelect.innerHTML = '';
        
        // Add new options
        availableCategories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categorySelect.appendChild(option);
        });
        
        // Trigger change event to update form validation
        categorySelect.dispatchEvent(new Event('change'));
    }
    
    // Initialize categories on page load
    updateCategories();
    
    // Update categories when transaction type changes
    transactionTypeSelect.addEventListener('change', updateCategories);
}

function initializeFormValidation() {
    const form = document.querySelector('form');
    if (!form) return;
    
    // Add custom validation
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            e.stopPropagation();
        }
    });
    
    // Real-time validation
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            clearFieldError(this);
        });
    });
}

function validateForm() {
    const form = document.querySelector('form');
    let isValid = true;
    
    // Validate amount
    const amountInput = form.querySelector('#amount');
    if (amountInput) {
        const amount = parseFloat(amountInput.value);
        if (isNaN(amount) || amount <= 0) {
            showFieldError(amountInput, 'Please enter a valid amount greater than 0');
            isValid = false;
        }
    }
    
    // Validate date
    const dateInput = form.querySelector('#date');
    if (dateInput) {
        const selectedDate = new Date(dateInput.value);
        const today = new Date();
        const maxDate = new Date(today.getFullYear() + 1, today.getMonth(), today.getDate());
        
        if (selectedDate > maxDate) {
            showFieldError(dateInput, 'Date cannot be more than 1 year in the future');
            isValid = false;
        }
    }
    
    // Validate required fields
    const requiredFields = form.querySelectorAll('input[required], select[required]');
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        }
    });
    
    return isValid;
}

function validateField(field) {
    clearFieldError(field);
    
    if (field.hasAttribute('required') && !field.value.trim()) {
        showFieldError(field, 'This field is required');
        return false;
    }
    
    if (field.type === 'number' || field.id === 'amount') {
        const value = parseFloat(field.value);
        if (isNaN(value) || value <= 0) {
            showFieldError(field, 'Please enter a valid amount greater than 0');
            return false;
        }
    }
    
    if (field.type === 'date') {
        const selectedDate = new Date(field.value);
        const today = new Date();
        const maxDate = new Date(today.getFullYear() + 1, today.getMonth(), today.getDate());
        
        if (selectedDate > maxDate) {
            showFieldError(field, 'Date cannot be more than 1 year in the future');
            return false;
        }
    }
    
    return true;
}

function showFieldError(field, message) {
    // Remove existing error
    clearFieldError(field);
    
    // Add error class
    field.classList.add('is-invalid');
    
    // Create error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    // Insert error message
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    // Remove error class
    field.classList.remove('is-invalid');
    
    // Remove error message
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Auto-format amount input
document.addEventListener('input', function(e) {
    if (e.target.id === 'amount') {
        let value = e.target.value;
        // Remove non-numeric characters except decimal point
        value = value.replace(/[^\d.]/g, '');
        // Ensure only one decimal point
        const parts = value.split('.');
        if (parts.length > 2) {
            value = parts[0] + '.' + parts.slice(1).join('');
        }
        // Limit to 2 decimal places
        if (parts[1] && parts[1].length > 2) {
            value = parts[0] + '.' + parts[1].substring(0, 2);
        }
        e.target.value = value;
    }
});

// Export functions
window.TransactionJS = {
    updateCategories: initializeCategoryFilter,
    validateForm: validateForm
};

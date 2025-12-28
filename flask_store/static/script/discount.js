function toggleDiscountFields() {
    const type = document.querySelector('select[name="type"]').value;
    const shippingFields = document.getElementById('shipping-fields');
    const dateFields = document.getElementById('date-fields');
    
    // Hide all first
    shippingFields.style.display = 'none';
    dateFields.style.display = 'none';
    
    // Show relevant fields
    if (type === 'shipping') {
        shippingFields.style.display = 'grid';
    } else if (type === 'seasoning' || type === 'special_event') {
        dateFields.style.display = 'grid';
    }
}

// Call on page load if editing
document.addEventListener('DOMContentLoaded', function() {
    toggleDiscountFields();
});
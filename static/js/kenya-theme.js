/**
 * Kenya-specific functionality for DataLinkCRM
 * Includes date pickers, phone number formatting, and Kenya cultural elements
 */

// Kenya-specific configurations
window.KenyaConfig = {
    countryCode: '+254',
    currency: 'KES',
    currencySymbol: 'KSh',
    locale: 'en-KE',
    timezone: 'Africa/Nairobi',
    phonePattern: /^\+254[0-9]{9}$/,
    idNumberPattern: /^[0-9]{8}$/, // Kenyan ID pattern
    postalCodePattern: /^[0-9]{5}$/, // Kenyan postal codes
};

// Kenya public holidays (2024)
window.KenyaHolidays = [
    { date: '2024-01-01', name: 'New Year\'s Day', type: 'national' },
    { date: '2024-04-01', name: 'Good Friday', type: 'religious' },
    { date: '2024-04-03', name: 'Easter Monday', type: 'religious' },
    { date: '2024-05-01', name: 'Labour Day', type: 'national' },
    { date: '2024-06-17', name: 'Eid al-Adha (estimated)', type: 'religious' },
    { date: '2024-10-20', name: 'Mashujaa Day', type: 'national' },
    { date: '2024-12-12', name: 'Jamhuri Day', type: 'national' },
    { date: '2024-12-25', name: 'Christmas Day', type: 'religious' },
    { date: '2024-12-26', name: 'Boxing Day', type: 'national' }
];

// Initialize Kenya-specific functionality
document.addEventListener('DOMContentLoaded', function() {
    initKenyaDatePickers();
    initKenyaPhoneFormatting();
    initKenyaCurrencyFormatting();
    initKenyaHolidaysCheck();
    initKenyaTimeDisplay();
    initKenyaCulturalElements();
});

/**
 * Initialize Kenya-themed date pickers with no backdating
 */
function initKenyaDatePickers() {
    if (typeof flatpickr !== 'undefined') {
        // Default date picker with Kenya settings
        flatpickr('.kenya-date-picker', {
            minDate: 'today', // No backdating - users can't select past dates
            maxDate: null,    // Allow future dates
            dateFormat: 'Y-m-d',
            altInput: true,
            altFormat: 'F j, Y', // "January 1, 2024"
            theme: 'kenya',
            locale: {
                firstDayOfWeek: 1, // Monday is first day
                weekdays: {
                    shorthand: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                    longhand: [
                        'Sunday', 'Monday', 'Tuesday', 'Wednesday', 
                        'Thursday', 'Friday', 'Saturday'
                    ]
                },
                months: {
                    shorthand: [
                        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                    ],
                    longhand: [
                        'January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December'
                    ]
                },
                rangeSeparator: ' to ',
                weekAbbreviation: 'Wk',
                scrollTitle: 'Scroll to increment',
                toggleTitle: 'Click to toggle',
                time_24hr: true
            },
            disable: getKenyaHolidays(),
            onReady: function(selectedDates, dateStr, instance) {
                instance.calendarContainer.classList.add('kenya-theme');
                
                // Add Kenya flag colors to the calendar
                const calendar = instance.calendarContainer;
                calendar.style.setProperty('--kenya-green', '#006A4E');
                calendar.style.setProperty('--kenya-red', '#BE123C');
                calendar.style.setProperty('--kenya-yellow', '#FCDD09');
            },
            onDayCreate: function(dayElement, date, instance, dayIsOutOfMonth) {
                // Highlight today's date
                if (date.toDateString() === new Date().toDateString()) {
                    dayElement.classList.add('today-highlight');
                }
                
                // Highlight holidays
                const dateStr = date.toISOString().split('T')[0];
                const holiday = window.KenyaHolidays.find(h => h.date === dateStr);
                if (holiday) {
                    dayElement.classList.add('holiday-highlight');
                    dayElement.title = holiday.name;
                }
            },
            onChange: function(selectedDates, dateStr, instance) {
                // Validate date selection
                if (selectedDates.length > 0) {
                    const selectedDate = selectedDates[0];
                    const today = new Date();
                    today.setHours(0, 0, 0, 0);
                    
                    if (selectedDate < today) {
                        showKenyaNotification('Please select a future date. Past dates are not allowed.', 'warning');
                        instance.clear();
                        return false;
                    }
                }
            }
        });

        // Date and time picker
        flatpickr('.kenya-datetime-picker', {
            minDate: 'today',
            enableTime: true,
            time_24hr: true,
            dateFormat: 'Y-m-d H:i',
            altInput: true,
            altFormat: 'F j, Y \\a\\t g:i A',
            theme: 'kenya',
            locale: {
                firstDayOfWeek: 1
            },
            disable: getKenyaHolidays(),
            onReady: function(selectedDates, dateStr, instance) {
                instance.calendarContainer.classList.add('kenya-theme');
            }
        });

        // Business hours picker (8 AM - 6 PM)
        flatpickr('.kenya-business-hours', {
            minDate: 'today',
            enableTime: true,
            noCalendar: true,
            dateFormat: 'H:i',
            time_24hr: true,
            defaultDate: '09:00',
            minuteIncrement: 15,
            minTime: '08:00',
            maxTime: '18:00',
            theme: 'kenya',
            locale: {
                firstDayOfWeek: 1
            }
        });

        // Date range picker
        flatpickr('.kenya-date-range', {
            minDate: 'today',
            dateFormat: 'Y-m-d',
            altInput: true,
            altFormat: 'F j, Y',
            theme: 'kenya',
            locale: {
                firstDayOfWeek: 1
            },
            disable: getKenyaHolidays(),
            onReady: function(selectedDates, dateStr, instance) {
                instance.calendarContainer.classList.add('kenya-theme');
            }
        });
    }
}

/**
 * Initialize Kenya phone number formatting
 */
function initKenyaPhoneFormatting() {
    // Format phone number input
    document.addEventListener('input', function(event) {
        if (event.target.matches('.kenya-phone-input')) {
            const input = event.target;
            let value = input.value.replace(/\D/g, ''); // Remove non-digits
            
            // Convert to Kenya format
            if (value.startsWith('254')) {
                value = value.substring(3);
            } else if (value.startsWith('0')) {
                value = value.substring(1);
            }
            
            if (value.length > 0) {
                if (value.length <= 3) {
                    input.value = `+254 ${value}`;
                } else if (value.length <= 6) {
                    input.value = `+254 ${value.substring(0, 3)} ${value.substring(3)}`;
                } else {
                    input.value = `+254 ${value.substring(0, 3)} ${value.substring(3, 6)} ${value.substring(6, 9)}`;
                }
            }
        }
    });

    // Validate Kenya phone numbers
    document.addEventListener('blur', function(event) {
        if (event.target.matches('.kenya-phone-input')) {
            const input = event.target;
            const value = input.value.replace(/\s/g, ''); // Remove spaces
            
            if (value && !window.KenyaConfig.phonePattern.test(value)) {
                showKenyaNotification('Please enter a valid Kenya phone number (e.g., +254708101604)', 'error');
                input.focus();
            }
        }
    });

    // Add phone number formatting to existing inputs
    document.querySelectorAll('.kenya-phone-input').forEach(input => {
        input.placeholder = 'e.g., +254708101604';
        input.maxLength = 15;
    });
}

/**
 * Initialize Kenya currency formatting
 */
function initKenyaCurrencyFormatting() {
    // Format currency inputs
    document.addEventListener('input', function(event) {
        if (event.target.matches('.kenya-currency-input')) {
            const input = event.target;
            let value = input.value.replace(/[^\d.]/g, ''); // Keep only digits and decimal point
            
            if (value) {
                // Format with Kenya Shilling symbol
                input.value = `KSh ${parseFloat(value).toLocaleString('en-KE', {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 2
                })}`;
            }
        }
    });

    // Add currency formatting to existing inputs
    document.querySelectorAll('.kenya-currency-input').forEach(input => {
        input.placeholder = 'KSh 0.00';
        input.addEventListener('focus', function() {
            this.value = this.value.replace(/[^\d.]/g, '').replace(/^KSh\s*/, '');
        });
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = `KSh ${parseFloat(this.value).toLocaleString('en-KE', {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 2
                })}`;
            }
        });
    });
}

/**
 * Initialize Kenya holidays check
 */
function initKenyaHolidaysCheck() {
    // Add holiday indicator to date pickers
    document.addEventListener('change', function(event) {
        if (event.target.matches('.kenya-date-picker, .kenya-datetime-picker')) {
            const selectedDate = event.target.value;
            const holiday = window.KenyaHolidays.find(h => h.date === selectedDate);
            
            if (holiday) {
                showKenyaNotification(`Selected date is ${holiday.name}`, 'info');
            }
        }
    });
}

/**
 * Initialize Kenya time display
 */
function initKenyaTimeDisplay() {
    function updateKenyaTime() {
        const now = new Date();
        const kenyaTime = new Intl.DateTimeFormat('en-KE', {
            timeZone: 'Africa/Nairobi',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true,
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(now);
        
        const timeElements = document.querySelectorAll('.kenya-time-display');
        timeElements.forEach(element => {
            element.textContent = kenyaTime;
        });
    }
    
    // Update time every second
    updateKenyaTime();
    setInterval(updateKenyaTime, 1000);
}

/**
 * Initialize Kenya cultural elements
 */
function initKenyaCulturalElements() {
    // Add Kenya flag colors to various elements
    addKenyaFlagColors();
    
    // Add Swahili translations for common terms
    addSwahiliTranslations();
    
    // Initialize Kenya-specific UI elements
    initKenyaUI();
}

/**
 * Add Kenya flag colors to elements
 */
function addKenyaFlagColors() {
    const style = document.createElement('style');
    style.textContent = `
        .kenya-date-picker .flatpickr-calendar.kenya-theme {
            background: white;
            border: 2px solid #006A4E;
            border-radius: 15px;
        }
        
        .kenya-date-picker .flatpickr-day.selected {
            background: linear-gradient(135deg, #006A4E 0%, #008060 100%);
            color: white;
        }
        
        .kenya-date-picker .flatpickr-day.today-highlight {
            background: #FCDD09;
            color: #000000;
            font-weight: bold;
        }
        
        .kenya-date-picker .flatpickr-day.holiday-highlight {
            background: #BE123C;
            color: white;
            position: relative;
        }
        
        .kenya-date-picker .flatpickr-day.holiday-highlight::after {
            content: '★';
            position: absolute;
            top: -2px;
            right: -2px;
            font-size: 8px;
            color: #FCDD09;
        }
        
        .kenya-theme .flatpickr-current-month {
            background: #006A4E;
            color: white;
        }
        
        .kenya-theme .flatpickr-months {
            background: #006A4E;
            color: white;
        }
    `;
    document.head.appendChild(style);
}

/**
 * Add Swahili translations
 */
function addSwahiliTranslations() {
    window.KenyaTranslations = {
        en: {
            loading: 'Loading...',
            save: 'Save',
            cancel: 'Cancel',
            delete: 'Delete',
            edit: 'Edit',
            create: 'Create',
            search: 'Search',
            today: 'Today',
            tomorrow: 'Tomorrow',
            yesterday: 'Yesterday',
            next_week: 'Next Week',
            this_month: 'This Month',
            next_month: 'Next Month',
            select_date: 'Select Date',
            select_time: 'Select Time',
            contact_info: 'Contact Information',
            payment_info: 'Payment Information',
            customer_info: 'Customer Information',
            project_info: 'Project Information'
        },
        sw: {
            loading: 'Inapakia...',
            save: 'Hifadhi',
            cancel: 'Ghairi',
            delete: 'Futa',
            edit: 'Hariri',
            create: 'Unda',
            search: 'Tafuta',
            today: 'Leo',
            tomorrow: 'Kesho',
            yesterday: 'Jana',
            next_week: 'Wiki ijayo',
            this_month: 'Mwezi huu',
            next_month: 'Mwezi ujao',
            select_date: 'Chagua Tarehe',
            select_time: 'Chagua Wakati',
            contact_info: 'Maelezo ya Mawasiliano',
            payment_info: 'Maelezo ya Malipo',
            customer_info: 'Maelezo ya Mteja',
            project_info: 'Maelezo ya Mradi'
        }
    };
}

/**
 * Initialize Kenya-specific UI elements
 */
function initKenyaUI() {
    // Add Kenya time zone indicator
    const tzElements = document.querySelectorAll('.kenya-timezone');
    tzElements.forEach(element => {
        element.textContent = 'EAT (UTC+3)';
        element.title = 'East Africa Time (UTC+3)';
    });
    
    // Add Kenya currency to price displays
    const priceElements = document.querySelectorAll('.kenya-price');
    priceElements.forEach(element => {
        const value = parseFloat(element.textContent);
        if (!isNaN(value)) {
            element.textContent = `KSh ${value.toLocaleString('en-KE')}`;
        }
    });
    
    // Add phone number links
    const phoneElements = document.querySelectorAll('.kenya-phone');
    phoneElements.forEach(element => {
        const phone = element.textContent.replace(/\D/g, '');
        if (phone.length === 9) {
            element.innerHTML = `<a href="tel:+254${phone}" class="text-decoration-none">${element.textContent}</a>`;
        }
    });
    
    // Add WhatsApp links
    const whatsappElements = document.querySelectorAll('.kenya-whatsapp');
    whatsappElements.forEach(element => {
        const phone = element.textContent.replace(/\D/g, '');
        if (phone.length === 9) {
            element.innerHTML = `<a href="wa.me/254${phone}" target="_blank" class="text-decoration-none"><i class="fab fa-whatsapp text-success me-1"></i>${element.textContent}</a>`;
        }
    });
}

/**
 * Get Kenya holidays as array of dates to disable
 */
function getKenyaHolidays() {
    return window.KenyaHolidays.map(holiday => {
        const [year, month, day] = holiday.date.split('-').map(Number);
        return new Date(year, month - 1, day); // Month is 0-based in JavaScript
    });
}

/**
 * Show Kenya-specific notification
 */
function showKenyaNotification(message, type = 'info') {
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-triangle',
        warning: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle'
    };
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 350px;';
    notification.innerHTML = `
        <i class="${icons[type] || icons.info} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

/**
 * Format Kenya phone number for display
 */
function formatKenyaPhone(phone) {
    if (!phone) return '';
    
    // Remove all non-digits
    const digits = phone.replace(/\D/g, '');
    
    // Handle different formats
    if (digits.startsWith('254')) {
        // Already in international format
        return `+${digits.substring(0, 3)} ${digits.substring(3, 6)} ${digits.substring(6, 9)}`;
    } else if (digits.startsWith('0')) {
        // National format with leading 0
        return `+254 ${digits.substring(1, 4)} ${digits.substring(4, 7)} ${digits.substring(7, 10)}`;
    } else if (digits.length === 9) {
        // Just the 9 digits
        return `+254 ${digits.substring(0, 3)} ${digits.substring(3, 6)} ${digits.substring(6, 9)}`;
    }
    
    return phone; // Return original if can't format
}

/**
 * Format Kenya currency for display
 */
function formatKenyaCurrency(amount) {
    if (typeof amount === 'string') {
        amount = parseFloat(amount);
    }
    
    if (isNaN(amount)) return 'KSh 0.00';
    
    return `KSh ${amount.toLocaleString('en-KE', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })}`;
}

/**
 * Validate Kenya phone number
 */
function isValidKenyaPhone(phone) {
    if (!phone) return false;
    const cleanPhone = phone.replace(/\s/g, '');
    return window.KenyaConfig.phonePattern.test(cleanPhone);
}

/**
 * Validate Kenyan ID number
 */
function isValidKenyanId(id) {
    if (!id) return false;
    return window.KenyaConfig.idNumberPattern.test(id);
}

/**
 * Get Kenya working days between two dates
 */
function getKenyaWorkingDays(startDate, endDate) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const workingDays = [];
    
    // Skip weekends (Saturday and Sunday)
    while (start <= end) {
        const dayOfWeek = start.getDay();
        if (dayOfWeek !== 0 && dayOfWeek !== 6) { // Not Sunday (0) or Saturday (6)
            // Check if it's not a holiday
            const dateStr = start.toISOString().split('T')[0];
            const isHoliday = window.KenyaHolidays.some(holiday => holiday.date === dateStr);
            
            if (!isHoliday) {
                workingDays.push(new Date(start));
            }
        }
        start.setDate(start.getDate() + 1);
    }
    
    return workingDays;
}

// Export functions for use in other scripts
window.KenyaUtils = {
    formatKenyaPhone,
    formatKenyaCurrency,
    isValidKenyaPhone,
    isValidKenyanId,
    getKenyaWorkingDays,
    getKenyaHolidays,
    showKenyaNotification
};
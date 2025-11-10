/**
 * DataLinkCRM - Main Application JavaScript
 * Comprehensive CRM functionality with Kenya-themed UI
 */

// Global application object
window.DataLinkCRM = {
    // Configuration
    config: {
        apiUrl: '/api/v1/',
        dashboardUrl: '/dashboard/',
        csrfToken: document.querySelector('[name=csrfmiddlewaretoken]')?.value,
        debug: window.location.hostname === 'localhost'
    },

    // Initialize the application
    init: function() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupNotifications();
        this.setupRealTimeUpdates();
        this.loadDashboardData();
        
        if (this.config.debug) {
            console.log('DataLinkCRM initialized successfully');
        }
    },

    // Setup global event listeners
    setupEventListeners: function() {
        // Sidebar toggle
        const sidebarToggle = document.getElementById('sidebarToggle');
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', this.toggleSidebar);
        }

        // Form submissions
        document.addEventListener('submit', this.handleFormSubmission);

        // Search functionality
        document.addEventListener('input', this.handleSearchInput);

        // File upload
        document.addEventListener('change', this.handleFileUpload);

        // Window resize
        window.addEventListener('resize', this.handleWindowResize);

        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts);
    },

    // Initialize UI components
    initializeComponents: function() {
        // Initialize tooltips
        this.initTooltips();

        // Initialize modals
        this.initModals();

        // Initialize date pickers
        this.initDatePickers();

        // Initialize Select2
        this.initSelect2();

        // Initialize DataTables
        this.initDataTables();

        // Initialize charts
        this.initCharts();

        // Initialize map components
        this.initMaps();

        // Initialize calendar
        this.initCalendar();
    },

    // Tooltip initialization
    initTooltips: function() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    },

    // Modal initialization
    initModals: function() {
        // Auto-focus first input in modals
        document.addEventListener('shown.bs.modal', function (event) {
            const modal = event.target;
            const firstInput = modal.querySelector('input:not([type="hidden"]):not([disabled])');
            if (firstInput) {
                firstInput.focus();
            }
        });

        // Reset forms when modals are hidden
        document.addEventListener('hidden.bs.modal', function (event) {
            const modal = event.target;
            const forms = modal.querySelectorAll('form');
            forms.forEach(form => {
                if (!form.dataset.persistent) {
                    form.reset();
                }
            });
        });
    },

    // Date picker initialization with Kenya settings
    initDatePickers: function() {
        if (typeof flatpickr !== 'undefined') {
            flatpickr('.date-picker', {
                minDate: 'today', // No backdating
                maxDate: null, // Allow future dates
                dateFormat: 'Y-m-d',
                altInput: true,
                altFormat: 'F j, Y',
                theme: 'kenya',
                locale: {
                    firstDayOfWeek: 1, // Monday (Kenya follows international week)
                    weekdays: {
                        shorthand: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                        longhand: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                    },
                    months: {
                        shorthand: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                        longhand: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                    }
                },
                disable: [
                    // Disable Kenyan public holidays (you can add more)
                    new Date(2024, 0, 1),  // New Year
                    new Date(2024, 3, 1),  // Good Friday
                    new Date(2024, 3, 3),  // Easter Monday
                    new Date(2024, 4, 1),  // Labour Day
                    new Date(2024, 5, 21), // Eid al-Adha
                    new Date(2024, 9, 20), // Mashujaa Day
                    new Date(2024, 10, 12), // Jamhuri Day
                    new Date(2024, 11, 25), // Christmas Day
                    new Date(2024, 11, 26), // Boxing Day
                ],
                onOpen: function(selectedDates, dateStr, instance) {
                    instance.calendarContainer.classList.add('kenya-theme');
                }
            });

            // Initialize date-time pickers
            flatpickr('.datetime-picker', {
                minDate: 'today',
                enableTime: true,
                time_24hr: true,
                dateFormat: 'Y-m-d H:i',
                altInput: true,
                altFormat: 'F j, Y at H:i',
                theme: 'kenya',
                locale: {
                    firstDayOfWeek: 1
                }
            });
        }
    },

    // Select2 initialization
    initSelect2: function() {
        if (typeof $.fn.select2 !== 'undefined') {
            $('.select2').select2({
                theme: 'bootstrap-5',
                width: '100%',
                placeholder: 'Select an option',
                allowClear: true,
                language: {
                    noResults: function() {
                        return "No results found";
                    },
                    searching: function() {
                        return "Searching...";
                    }
                }
            });

            // Initialize with AJAX for large datasets
            $('.select2-ajax').select2({
                theme: 'bootstrap-5',
                width: '100%',
                placeholder: 'Search and select',
                allowClear: true,
                ajax: {
                    url: function() {
                        return $(this).data('url');
                    },
                    dataType: 'json',
                    delay: 250,
                    data: function(params) {
                        return {
                            q: params.term,
                            page: params.page
                        };
                    },
                    processResults: function(data, params) {
                        params.page = params.page || 1;
                        return {
                            results: data.results,
                            pagination: {
                                more: data.pagination.more
                            }
                        };
                    },
                    cache: true
                }
            });
        }
    },

    // DataTables initialization
    initDataTables: function() {
        if (typeof $.fn.DataTable !== 'undefined') {
            $('.data-table').each(function() {
                const table = $(this);
                const options = {
                    pageLength: 25,
                    responsive: true,
                    language: {
                        search: "_INPUT_",
                        searchPlaceholder: "Search...",
                        lengthMenu: "_MENU_",
                        info: "Showing _START_ to _END_ of _TOTAL_ entries",
                        infoEmpty: "No entries to show",
                        infoFiltered: "(filtered from _MAX_ total entries)",
                        paginate: {
                            first: "First",
                            last: "Last",
                            next: "Next",
                            previous: "Previous"
                        }
                    },
                    order: [[0, 'desc']],
                    columnDefs: [
                        {
                            targets: 'no-sort',
                            orderable: false
                        }
                    ]
                };

                // Add export buttons if specified
                if (table.hasClass('with-export')) {
                    options.dom = 'Bfrtip';
                    options.buttons = [
                        {
                            extend: 'excel',
                            text: '<i class="fas fa-file-excel"></i> Excel',
                            className: 'btn btn-success'
                        },
                        {
                            extend: 'pdf',
                            text: '<i class="fas fa-file-pdf"></i> PDF',
                            className: 'btn btn-danger'
                        },
                        {
                            extend: 'print',
                            text: '<i class="fas fa-print"></i> Print',
                            className: 'btn btn-info'
                        }
                    ];
                }

                table.DataTable(options);
            });
        }
    },

    // Chart initialization
    initCharts: function() {
        if (typeof Chart !== 'undefined') {
            // Chart.js global defaults
            Chart.defaults.font.family = "'Inter', 'Helvetica Neue', 'Arial', sans-serif";
            Chart.defaults.font.size = 12;
            Chart.defaults.color = '#374151';

            // Kenya-themed colors
            window.KenyaChartColors = {
                green: '#006A4E',
                red: '#BE123C',
                yellow: '#FCDD09',
                black: '#000000',
                white: '#FFFFFF',
                greenLight: '#008060',
                redLight: '#E91E63',
                yellowLight: '#FFF176'
            };

            // Initialize chart tooltips
            Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(0, 106, 78, 0.9)';
            Chart.defaults.plugins.tooltip.titleColor = '#ffffff';
            Chart.defaults.plugins.tooltip.bodyColor = '#ffffff';
            Chart.defaults.plugins.tooltip.borderColor = '#006A4E';
            Chart.defaults.plugins.tooltip.borderWidth = 1;
        }
    },

    // Map initialization
    initMaps: function() {
        // MapBox integration
        if (typeof mapboxgl !== 'undefined' && window.mapboxToken) {
            mapboxgl.accessToken = window.mapboxToken;
            
            // Initialize map containers
            $('.map-container').each(function() {
                const container = this;
                const center = [37.9062, 0.0236]; // Kenya center coordinates
                
                const map = new mapboxgl.Map({
                    container: container,
                    style: 'mapbox://styles/mapbox/streets-v11',
                    center: center,
                    zoom: 6
                });

                // Add navigation controls
                map.addControl(new mapboxgl.NavigationControl());

                // Add geolocate control
                map.addControl(
                    new mapboxgl.GeolocateControl({
                        positionOptions: {
                            enableHighAccuracy: true
                        },
                        trackUserLocation: true,
                        showUserHeading: true
                    })
                );

                // Store map instance for later use
                container.mapInstance = map;
            });
        }
    },

    // Calendar initialization
    initCalendar: function() {
        if (typeof FullCalendar !== 'undefined') {
            $('.calendar').each(function() {
                const calendarEl = this;
                const calendar = new FullCalendar.Calendar(calendarEl, {
                    initialView: 'dayGridMonth',
                    headerToolbar: {
                        left: 'prev,next today',
                        center: 'title',
                        right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
                    },
                    navLinks: true,
                    editable: true,
                    selectable: true,
                    selectMirror: true,
                    dayMaxEvents: true,
                    weekends: true,
                    businessHours: {
                        daysOfWeek: [1, 2, 3, 4, 5], // Monday - Friday
                        startTime: '08:00',
                        endTime: '18:00',
                    },
                    locale: 'en',
                    themeSystem: 'bootstrap5',
                    height: 'auto',
                    eventClick: function(info) {
                        // Handle event click
                        const event = info.event;
                        DataLinkCRM.showEventDetails(event);
                    },
                    select: function(info) {
                        // Handle date selection
                        DataLinkCRM.showCreateEventModal(info.start, info.end);
                    }
                });

                calendar.render();
                calendarEl.calendarInstance = calendar;
            });
        }
    },

    // Sidebar toggle functionality
    toggleSidebar: function() {
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        
        if (window.innerWidth <= 768) {
            sidebar.classList.toggle('show');
        } else {
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('sidebar-collapsed');
        }
    },

    // Form submission handling
    handleFormSubmission: function(event) {
        const form = event.target;
        if (form.matches('form[data-ajax]')) {
            event.preventDefault();
            
            const formData = new FormData(form);
            const url = form.action || window.location.href;
            const method = form.method || 'POST';
            
            DataLinkCRM.submitForm(url, method, formData, form);
        }
    },

    // Submit form via AJAX
    submitForm: function(url, method, formData, formElement) {
        const submitButton = formElement.querySelector('[type="submit"]');
        const originalText = submitButton?.innerHTML;
        
        // Show loading state
        if (submitButton) {
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            submitButton.disabled = true;
        }

        fetch(url, {
            method: method,
            body: formData,
            headers: {
                'X-CSRFToken': DataLinkCRM.config.csrfToken,
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                DataLinkCRM.showNotification(data.message, 'success');
                
                // Redirect if specified
                if (data.redirect) {
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 1500);
                }
                
                // Reset form if not specified otherwise
                if (!formElement.dataset.persistent) {
                    formElement.reset();
                }
                
                // Refresh page components
                DataLinkCRM.refreshComponents();
            } else {
                DataLinkCRM.showNotification(data.message || 'An error occurred', 'error');
                
                // Show field errors
                if (data.errors) {
                    DataLinkCRM.showFieldErrors(formElement, data.errors);
                }
            }
        })
        .catch(error => {
            console.error('Form submission error:', error);
            DataLinkCRM.showNotification('An error occurred while submitting the form', 'error');
        })
        .finally(() => {
            // Reset button state
            if (submitButton) {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }
        });
    },

    // Show field validation errors
    showFieldErrors: function(form, errors) {
        // Clear previous errors
        form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        
        // Add new errors
        Object.keys(errors).forEach(field => {
            const input = form.querySelector(`[name="${field}"]`);
            if (input) {
                input.classList.add('is-invalid');
                
                const errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback';
                errorDiv.textContent = errors[field];
                input.parentNode.appendChild(errorDiv);
            }
        });
    },

    // Search input handling
    handleSearchInput: function(event) {
        if (event.target.matches('input[data-search]')) {
            const input = event.target;
            const target = input.dataset.search;
            const delay = input.dataset.searchDelay || 500;
            
            clearTimeout(input.searchTimeout);
            input.searchTimeout = setTimeout(() => {
                DataLinkCRM.performSearch(input.value, target);
            }, delay);
        }
    },

    // Perform search
    performSearch: function(query, target) {
        if (query.length < 2) {
            DataLinkCRM.clearSearchResults(target);
            return;
        }

        fetch(`/api/v1/search/?q=${encodeURIComponent(query)}&target=${target}`)
            .then(response => response.json())
            .then(data => {
                DataLinkCRM.displaySearchResults(data, target);
            })
            .catch(error => {
                console.error('Search error:', error);
            });
    },

    // Display search results
    displaySearchResults: function(data, target) {
        const container = document.querySelector(`[data-search-results="${target}"]`);
        if (!container) return;

        if (data.results.length === 0) {
            container.innerHTML = '<div class="text-muted p-3">No results found</div>';
            return;
        }

        const resultsHtml = data.results.map(result => `
            <div class="search-result-item p-2 border-bottom" data-url="${result.url}">
                <div class="d-flex align-items-center">
                    <i class="fas fa-${result.icon} me-2 text-muted"></i>
                    <div>
                        <div class="fw-bold">${result.title}</div>
                        <div class="small text-muted">${result.description}</div>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = resultsHtml;
        
        // Add click handlers
        container.querySelectorAll('.search-result-item').forEach(item => {
            item.addEventListener('click', function() {
                window.location.href = this.dataset.url;
            });
        });
    },

    // Clear search results
    clearSearchResults: function(target) {
        const container = document.querySelector(`[data-search-results="${target}"]`);
        if (container) {
            container.innerHTML = '';
        }
    },

    // File upload handling
    handleFileUpload: function(event) {
        if (event.target.matches('input[type="file"][data-upload]')) {
            const input = event.target;
            const files = input.files;
            
            if (files.length > 0) {
                DataLinkCRM.uploadFile(input, files[0]);
            }
        }
    },

    // Upload file
    uploadFile: function(input, file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const progressContainer = input.parentNode.querySelector('.upload-progress');
        const progressBar = input.parentNode.querySelector('.upload-progress-bar');
        const statusText = input.parentNode.querySelector('.upload-status');
        
        // Show progress
        if (progressContainer) {
            progressContainer.style.display = 'block';
        }
        
        fetch('/api/v1/upload/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': DataLinkCRM.config.csrfToken,
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (statusText) {
                    statusText.textContent = 'Upload successful!';
                    statusText.className = 'upload-status text-success';
                }
                
                // Trigger change event
                const event = new Event('change', { bubbles: true });
                input.dispatchEvent(event);
            } else {
                if (statusText) {
                    statusText.textContent = data.message || 'Upload failed';
                    statusText.className = 'upload-status text-danger';
                }
            }
        })
        .catch(error => {
            console.error('Upload error:', error);
            if (statusText) {
                statusText.textContent = 'Upload failed';
                statusText.className = 'upload-status text-danger';
            }
        })
        .finally(() => {
            if (progressContainer) {
                setTimeout(() => {
                    progressContainer.style.display = 'none';
                    if (progressBar) progressBar.style.width = '0%';
                }, 2000);
            }
        });
        
        // Simulate progress (you might want to implement real progress tracking)
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            if (progressBar) {
                progressBar.style.width = `${progress}%`;
            }
            if (progress >= 90) {
                clearInterval(interval);
            }
        }, 200);
    },

    // Window resize handling
    handleWindowResize: function() {
        // Adjust sidebar on window resize
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('sidebar-collapsed');
        }
    },

    // Keyboard shortcuts
    handleKeyboardShortcuts: function(event) {
        // Ctrl/Cmd + K for search
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            const searchInput = document.querySelector('input[data-search]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Ctrl/Cmd + / for help
        if ((event.ctrlKey || event.metaKey) && event.key === '/') {
            event.preventDefault();
            DataLinkCRM.showHelpModal();
        }
    },

    // Setup notifications system
    setupNotifications: function() {
        // Request notification permission
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    },

    // Show notification
    showNotification: function(message, type = 'info', duration = 5000) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
        
        // Show browser notification if permission granted
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('DataLinkCRM', {
                body: message,
                icon: '/static/icons/icon-192x192.png'
            });
        }
    },

    // Setup real-time updates
    setupRealTimeUpdates: function() {
        // Use Server-Sent Events for real-time updates
        if (typeof EventSource !== 'undefined') {
            const eventSource = new EventSource('/api/v1/stream/');
            
            eventSource.addEventListener('notification', function(event) {
                const data = JSON.parse(event.data);
                DataLinkCRM.showNotification(data.message, data.type || 'info');
            });
            
            eventSource.addEventListener('dashboard-update', function(event) {
                const data = JSON.parse(event.data);
                DataLinkCRM.updateDashboardStats(data);
            });
        }
    },

    // Load dashboard data
    loadDashboardData: function() {
        fetch('/dashboard/api/dashboard-data/')
            .then(response => response.json())
            .then(data => {
                DataLinkCRM.updateDashboardStats(data.stats);
                DataLinkCRM.updateRecentActivity(data.recent_customers, data.recent_projects, data.recent_payments);
            })
            .catch(error => {
                console.error('Failed to load dashboard data:', error);
            });
    },

    // Update dashboard statistics
    updateDashboardStats: function(stats) {
        Object.keys(stats).forEach(key => {
            const element = document.querySelector(`[data-stat="${key}"]`);
            if (element) {
                element.textContent = this.formatNumber(stats[key]);
            }
        });
    },

    // Update recent activity
    updateRecentActivity: function(customers, projects, payments) {
        // Update customers section
        const customersContainer = document.querySelector('[data-section="recent-customers"]');
        if (customersContainer && customers) {
            this.updateActivityList(customersContainer, customers, 'customer');
        }
        
        // Update projects section
        const projectsContainer = document.querySelector('[data-section="recent-projects"]');
        if (projectsContainer && projects) {
            this.updateActivityList(projectsContainer, projects, 'project');
        }
        
        // Update payments section
        const paymentsContainer = document.querySelector('[data-section="recent-payments"]');
        if (paymentsContainer && payments) {
            this.updateActivityList(paymentsContainer, payments, 'payment');
        }
    },

    // Update activity list
    updateActivityList: function(container, items, type) {
        // Implementation for updating activity lists
        // This would be customized based on your specific needs
    },

    // Format numbers for display
    formatNumber: function(num) {
        if (typeof num === 'number') {
            return num.toLocaleString();
        }
        return num;
    },

    // Format currency (Kenya Shillings)
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-KE', {
            style: 'currency',
            currency: 'KES'
        }).format(amount);
    },

    // Format date for Kenya locale
    formatDate: function(date) {
        return new Intl.DateTimeFormat('en-KE', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },

    // Refresh page components
    refreshComponents: function() {
        // Refresh DataTables
        $('.data-table').each(function() {
            if ($.fn.DataTable.isDataTable(this)) {
                $(this).DataTable().ajax.reload();
            }
        });
        
        // Refresh charts
        this.refreshCharts();
        
        // Reload dashboard data
        this.loadDashboardData();
    },

    // Refresh charts
    refreshCharts: function() {
        // Implementation for refreshing charts
        // This would be customized based on your chart setup
    },

    // Show help modal
    showHelpModal: function() {
        const helpContent = `
            <h5>Keyboard Shortcuts</h5>
            <ul class="list-unstyled">
                <li><kbd>Ctrl + K</kbd> - Focus search</li>
                <li><kbd>Ctrl + /</kbd> - Show this help</li>
                <li><kbd>Esc</kbd> - Close modals</li>
            </ul>
            <hr>
            <h5>Quick Actions</h5>
            <ul class="list-unstyled">
                <li><i class="fas fa-user-plus me-2"></i>Add Customer</li>
                <li><i class="fas fa-project-diagram me-2"></i>New Project</li>
                <li><i class="fas fa-credit-card me-2"></i>Process Payment</li>
            </ul>
        `;
        
        this.showModal('Help & Shortcuts', helpContent);
    },

    // Show modal
    showModal: function(title, content) {
        const modalHtml = `
            <div class="modal fade" id="dynamicModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            ${content}
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal if any
        const existingModal = document.getElementById('dynamicModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Add new modal
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = new bootstrap.Modal(document.getElementById('dynamicModal'));
        modal.show();
        
        // Clean up after modal is hidden
        document.getElementById('dynamicModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    DataLinkCRM.init();
});

// Make DataLinkCRM globally available
window.DataLinkCRM = DataLinkCRM;
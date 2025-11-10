# DataLinkCRM - Professional Customer Relationship Management System

[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-purple.svg)](https://getbootstrap.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive Customer Relationship Management (CRM) system built with Django, designed for modern business needs. This system includes customer management, project tracking, payment processing, communication tools, and advanced analytics.

## 🌟 Features

### Core Functionality
- **1000+ UI Components** - Comprehensive collection of reusable components
- **20+ Example Pages** - Pre-built pages for common use cases
- **Professional Dashboard** - Interactive dashboard with real-time data
- **Toggleable Sidebar** - Collapsible navigation for better UX
- **Responsive Design** - Mobile-first approach with Bootstrap 5
- **Kenya-Themed UI** - Custom design elements with Kenya national colors

### Customer Management
- **Customer Profiles** - Comprehensive customer information management
- **Customer Segmentation** - Advanced filtering and grouping
- **Communication History** - Track all customer interactions
- **Customer Analytics** - Detailed insights and reporting

### Project Management
- **Project Tracking** - End-to-end project lifecycle management
- **Task Management** - Detailed task assignment and tracking
- **Team Collaboration** - Multi-user project workflows
- **Project Analytics** - Performance metrics and reporting

### Payment Integration
- **Stripe Integration** - Credit/debit card processing
- **M-PESA Integration** - Mobile money payments (Kenya)
- **Bank Transfer** - Direct bank payment options
- **Payment Tracking** - Complete payment history and status
- **Subscription Management** - Recurring payment handling

### Communication Tools
- **Email Integration** - Automated email notifications via Gmail
- **WhatsApp Integration** - Direct WhatsApp communication
- **SMS Notifications** - SMS alerts and updates
- **In-app Messaging** - Real-time communication system

### Advanced Features
- **Interactive Maps** - MapBox integration for location services
- **Calendar System** - Kenya-themed date pickers with no backdating
- **SVG Maps** - Interactive geographical visualizations
- **Widget System** - Customizable dashboard widgets
- **Subscription Management** - Flexible subscription plans
- **Real-time Analytics** - Live data visualization
- **Report Generation** - Comprehensive reporting tools

### Technical Features
- **RESTful API** - Complete API for mobile and external integrations
- **Real-time Updates** - WebSocket integration for live data
- **Background Tasks** - Celery integration for async processing
- **Email Automation** - Resend integration for confirmations
- **Cloud Deployment Ready** - Docker and cloud platform support
- **Security Features** - Enterprise-level security implementation

## 🏗️ Architecture

### Technology Stack
- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5, JavaScript ES6+
- **Database**: SQLite (Development), PostgreSQL (Production)
- **Authentication**: Django AllAuth with JWT support
- **API**: Django REST Framework
- **Real-time**: WebSocket (channels), HTMX
- **Background Tasks**: Celery + Redis
- **File Storage**: Local/Cloud (AWS S3 compatible)
- **Maps**: MapBox integration
- **Payments**: Stripe, M-PESA APIs

### Project Structure
```
DataLinkCRM/
├── core/                 # Core application (main settings)
├── authentication/       # User authentication and accounts
├── dashboard/           # Main dashboard and widgets
├── customers/           # Customer management
├── projects/            # Project management
├── subscriptions/       # Subscription and billing
├── payments/            # Payment processing
├── communications/      # Communication tools
├── analytics/           # Analytics and reporting
├── settings/            # System settings
├── widgets/             # Dashboard widgets
├── schedulecal/         # Calendar and scheduling
├── maps/                # Maps and location services
├── reports/             # Report generation
├── templates/           # HTML templates
│   ├── layouts/         # Base templates
│   ├── includes/        # Reusable components
│   └── app/             # App-specific templates
├── static/              # CSS, JS, and media files
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- pip
- Node.js (for frontend assets)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/OumaCavin/DataLinkCRM.git
   cd DataLinkCRM
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open http://localhost:8000
   - Login with your superuser credentials

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=datalinkcrm
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@datalinkcrm.com

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# M-PESA Configuration
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_BUSINESS_SHORT_CODE=174379
MPESA_PASS_KEY=your-passkey

# Mapbox
MAPBOX_ACCESS_TOKEN=your-mapbox-token
```

### Payment Integration Setup

#### Stripe Setup
1. Create a Stripe account at https://stripe.com
2. Get your API keys from the dashboard
3. Configure webhooks for payment confirmations
4. Add the keys to your environment variables

#### M-PESA Integration (Kenya)
1. Register for M-PESA API access with Safaricom
2. Get your consumer key and secret
3. Configure the business short code
4. Set up callback URLs

### Email Configuration
1. Enable 2FA on your Gmail account
2. Generate an App Password
3. Configure SMTP settings in environment variables

## 🎨 Kenya-Themed Features

### Custom Date Picker
- No backdating functionality
- Kenya national colors
- Local time zone (Africa/Nairobi)
- Multi-language support (English, Swahili)

### Payment Methods
- M-PESA integration for local payments
- Bank transfer options
- Mobile money compatibility
- Kenya-shilling currency support

### Regional Customization
- Kenya phone number format (+254)
- Local business hours
- Kenya public holidays
- East African time zones

## 📱 API Documentation

The system provides a comprehensive REST API:

### Authentication
```bash
POST /api/v1/auth/login/
POST /api/v1/auth/logout/
POST /api/v1/auth/refresh/
```

### Customers
```bash
GET /api/v1/customers/
POST /api/v1/customers/
GET /api/v1/customers/{id}/
PUT /api/v1/customers/{id}/
DELETE /api/v1/customers/{id}/
```

### Projects
```bash
GET /api/v1/projects/
POST /api/v1/projects/
GET /api/v1/projects/{id}/
PUT /api/v1/projects/{id}/
```

### Payments
```bash
GET /api/v1/payments/
POST /api/v1/payments/stripe/
POST /api/v1/payments/mpesa/
```

## 🚀 Deployment

### Cloud Deployment Options

#### 1. Heroku Deployment
```bash
# Install Heroku CLI and login
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
# ... add other environment variables

# Deploy
git push heroku main
```

#### 2. Vercel Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

#### 3. Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### 4. DigitalOcean App Platform
1. Connect your GitHub repository
2. Configure build settings
3. Set environment variables
4. Deploy with one click

### Docker Deployment
```bash
# Build Docker image
docker build -t datalinkcrm .

# Run with Docker Compose
docker-compose up -d
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test customers

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📊 Monitoring and Analytics

The system includes comprehensive monitoring:

- **Performance Monitoring**: Real-time performance metrics
- **User Analytics**: User behavior tracking
- **System Health**: Database and API health checks
- **Error Tracking**: Automated error reporting
- **Usage Statistics**: Detailed usage analytics

## 🔒 Security Features

- **Authentication**: JWT and session-based authentication
- **Authorization**: Role-based access control
- **Data Encryption**: End-to-end encryption for sensitive data
- **API Security**: Rate limiting and API key authentication
- **HTTPS Enforcement**: SSL/TLS encryption
- **Security Headers**: Comprehensive security headers
- **Input Validation**: XSS and SQL injection protection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Cavin Otieno**
- Email: cavin.otieno012@gmail.com
- Phone: +254708101604
- WhatsApp: [wa.me/+254708101604](https://wa.me/254708101604)
- LinkedIn: [cavin-otieno-9a841260](https://www.linkedin.com/in/cavin-otieno-9a841260/)

## 📞 Support

For support and questions:
- Email: cavin.otieno012@gmail.com
- Phone: +254708101604
- WhatsApp: [wa.me/+254708101604](https://wa.me/254708101604)
- LinkedIn: [cavin-otieno-9a841260](https://www.linkedin.com/in/cavin-otieno-9a841260/)

## 🆕 Changelog

### v1.0.0 (2024-11-10)
- Initial release with full CRM functionality
- Payment integration (Stripe, M-PESA, Bank Transfer)
- Kenya-themed UI and features
- Complete admin dashboard
- API documentation
- Cloud deployment support

---

**DataLinkCRM** - Empowering businesses with comprehensive customer relationship management solutions.

Built with ❤️ by Cavin Otieno
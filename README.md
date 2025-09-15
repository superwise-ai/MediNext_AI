<div align="left">



<a href="https://superwise.ai/" target="_blank">
<img src="app/assets/superwise_logo.svg" alt="SUPERWISE® Logo" width="350"/></a>

**Powered by SUPERWISE® — Leading AI Governance, Risk & Compliance Solutions**

[![Powered by SUPERWISE®](https://img.shields.io/badge/Powered%20by-SUPERWISE®-0052CC?style=for-the-badge&logo=superuser)](https://superwise.ai)
[![AI Healthcare](https://img.shields.io/badge/AI%20Healthcare-Management-00A86B?style=for-the-badge&logo=medical)](https://superwise.ai)
[![Enterprise Ready](https://img.shields.io/badge/Enterprise-Ready-gold?style=for-the-badge&logo=enterprise)](https://superwise.ai)

</div>
<h2>MediNext AI</h2>
A modern AI-powered Healthcare Management System built with Streamlit, featuring a comprehensive dashboard for healthcare professionals with Superwise AI integration.

## 🏢 **Ready for Business?**

**Transform your business operations with Superwise AI**: [Get Started with Superwise](https://docs.superwise.ai/docs/introduction-to-superwise) - Enterprise-grade AI governance, risk & compliance solutions for healthcare and other businesses.

<h3>🚀 Quick Start</h3>


### Prerequisites

- **Superwise Account**: Create account and application (see [Superwise Agent Setup Guide](docs/SUPERWISE_AGENT_SETUP_GUIDE.md#prerequisites--account-setup))

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd medinext_ai
   ```

2. **Set up environment variables**:
   
   **Linux/Mac:**
   ```bash
   cp .env.example .env
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   copy .env.example .env
   ```
   
   **Windows (PowerShell):**
   ```powershell
   Copy-Item .env.example .env
   ```
   
   **All Systems:** Edit the `.env` file with your Superwise Agent credentials (see [Superwise Agent Setup Guide](docs/SUPERWISE_AGENT_SETUP_GUIDE.md))

### Option 1: Docker (Recommended)

1. **Prerequisites**: 
   - Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

2. **Quick Launch**:
   ```bash
   # Build and run
   docker-compose up --build
   
   # Run in background
   docker-compose up -d
   
   # Stop
   docker-compose down
   ```

3. Open your browser and navigate to `http://localhost:9000`

### Option 2: Local Python Installation

1. **Prerequisites**:
   - Python 3.8+ installed

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app/main.py --server.port 9000
   ```

4. Open your browser and navigate to `http://localhost:9000`

## ✨ Features

- **📊 Dashboard Overview**: Real-time metrics and summary cards with patient analytics
- **👥 Patient Management**: Search and view patient information with AI-powered insights
- **📅 Appointment Scheduling**: Calendar and appointment management
- **💊 Prescription Management**: Medication and prescription tracking
- **📈 Reports & Analytics**: Interactive data visualization and reporting tools
- **🔔 Recent Activities**: Real-time activity monitoring with critical alerts
- **🤖 AI Integration**: Superwise AI-powered patient analysis and insights

## 🛡️ Guardrails & Telemetry

### **Guardrails System**
- **Real-time Violation Detection**: Automated monitoring of glucose (>200 mg/dL) and hemoglobin (<12 g/dL) thresholds
- **Compliance Tracking**: Visual guardrail status indicators and violation counts
- **Risk Assessment**: Patient risk scoring with critical alert prioritization
- **Activity Monitoring**: Guardrail violations appear in real-time activity feed

**Where to Find Guardrails:**
- **Dashboard**: View guardrail violations in summary cards (`/dashboard`)
- **Patient Details**: Check individual patient guardrail status (`/patient-details`)
- **Activity Feed**: Monitor real-time guardrail alerts (`/dashboard`)
- **Analytics**: Analyze guardrail compliance trends (`/analytics`)

### **Telemetry & Monitoring**
- **Performance Metrics**: Application response times and system health monitoring
- **User Analytics**: Session tracking and user behavior monitoring
- **Logging System**: Comprehensive logging with file and console output
- **Health Checks**: Docker health monitoring with Streamlit health endpoints

**Where to Find Telemetry:**
- **Logs**: Check `logs/` directory for detailed application logs
- **Docker Health**: Monitor container health via `docker-compose ps`
- **Dashboard Metrics**: View performance metrics in dashboard cards
- **Activity Feed**: Monitor system events and user activities

## 🏗️ Project Structure

```
medinext_ai/
├── app/
│   ├── components/              # Reusable UI components
│   │   ├── header.py            # Application header
│   │   ├── sidebar.py           # Navigation sidebar
│   │   ├── dashboard_cards.py   # Metric summary cards
│   │   ├── patient_table.py     # Patient data table
│   │   ├── patient_details.py   # Patient details with AI analysis
│   │   ├── activity_feed.py     # Recent activities display
│   │   ├── analytics_charts.py # Data visualization charts
│   │   └── landing_page.py     # Landing page component
│   ├── config/                  # Configuration settings
│   │   ├── settings.py          # Application settings
│   │   └── api_config.py        # Superwise API configuration
│   ├── utils/                   # Utility functions
│   │   ├── css_styles.py        # Custom CSS styles
│   │   └── logger.py           # Logging utilities
│   ├── assets/                  # Static assets
│   │   └── synthetic_ehr_data.csv # Primary patient data source for dashboard, analytics, and patient management
│   └── main.py                  # Main application entry point
├── tests/                       # Test files
├── logs/                        # Application logs
├── synthetic_data/              # Synthetic patient data files
│   ├── synthetic_ehr_data.csv   # Main patient data (CSV)
│   ├── synthetic_ehr_data.json  # Patient data (JSON)
│   └── fhir_synthetic_ehr_data.json # FHIR-formatted data
├── docs/                        # Documentation files
│   ├── DOCKER_README.md         # Docker setup guide
│   ├── PROJECT_OVERVIEW.md      # Project architecture overview
│   └── SUPERWISE_AGENT_SETUP_GUIDE.md # Superwise Agent setup guide
├── requirements.txt             # Python dependencies
├── docker-compose.yml          # Docker configuration
├── Dockerfile                  # Docker image definition
├── env.example                 # Environment variables template
└── README.md                   # This file
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **AI Integration**: Superwise API
- **Styling**: Custom CSS with Streamlit components
- **Containerization**: Docker & Docker Compose
- **Environment**: Python 3.8+

## 📚 Documentation

For detailed information about specific aspects of the project, please refer to:

- **[Docker Setup Guide](docs/DOCKER_README.md)** - Comprehensive Docker deployment instructions
- **[Project Overview](docs/PROJECT_OVERVIEW.md)** - Detailed architecture and feature descriptions
- **[Superwise Agent Setup Guide](docs/SUPERWISE_AGENT_SETUP_GUIDE.md)** - AI integration setup and usage

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Superwise API Configuration
SUPERWISE_API_URL=https://api.superwise.ai/
SUPERWISE_API_VERSION=v1
SUPERWISE_APP_ID=YOUR_SUPERWISE_APP_ID

# API Timeout Settings
API_TIMEOUT=30
MAX_RETRIES=3
RETRY_DELAY=1
```

**Note**: The Superwise API configuration is required for AI features to work properly.

## 🔒 Data Privacy & Compliance

### **Important Disclaimers**

⚠️ **This application uses SYNTHETIC DUMMY DATA for demonstration purposes only.**

- **No Real Patient Data**: All patient information in this application is artificially generated
- **Educational Purpose**: This is a demonstration/educational project, not a production healthcare system
- **Data Sources**: Patient data comes from `synthetic_ehr_data.csv` and `synthetic_ehr_data.json`

🚨 **CRITICAL SECURITY LIMITATIONS - NOT PRODUCTION READY:**

- **No Authentication**: Application has no user login or authentication system
- **No Authorization**: No access controls or user permission management
- **No Data Encryption**: Patient data is stored and transmitted without encryption
- **No Session Management**: No secure session handling or user state management
- **No Access Logging**: No audit trails for data access or user activities
- **No Input Validation**: Limited input sanitization and validation
- **No HTTPS Enforcement**: No SSL/TLS encryption for data transmission

**⚠️ DO NOT USE WITH REAL PATIENT DATA - FOR DEMONSTRATION ONLY**

### **HIPAA & PHI Considerations**

**For Production Use:**
- **HIPAA Compliance**: Ensure proper HIPAA compliance before handling real patient data
- **PHI Protection**: Implement proper safeguards for Protected Health Information (PHI)
- **Data Encryption**: Use encryption for data at rest and in transit
- **Access Controls**: Implement proper user authentication and authorization
- **Audit Logging**: Maintain comprehensive audit trails for all data access
- **Business Associate Agreements**: Ensure all third-party services (like Superwise API) have proper BAAs

**Current Implementation:**
- ✅ **Synthetic Data Only**: No real patient data is processed
- ✅ **Local Processing**: Data stays within your local environment
- ✅ **No External Storage**: No data is sent to external databases
- ⚠️ **API Integration**: Superwise API calls may transmit synthetic data (configure accordingly)

### **Security Best Practices**

1. **Environment Variables**: Never commit real API keys or sensitive data
2. **Data Validation**: Implement proper input validation and sanitization
3. **Error Handling**: Avoid exposing sensitive information in error messages
4. **Logging**: Be cautious about logging sensitive data
5. **Network Security**: Use HTTPS in production environments

**Note**: This application is for educational/demonstration purposes. For production healthcare applications, consult with legal and compliance experts regarding HIPAA requirements.

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_main.py
```

## 🔍 Code Quality & Linting

### **Docker-Based Linting (Recommended)**

Use Docker for consistent linting across different environments:

```bash
# Check for linting issues
docker-compose run --rm medinext-ai python -m flake8 app/

# Auto-fix formatting issues
docker-compose run --rm medinext-ai python -m black app/

# Check with detailed statistics
docker-compose run --rm medinext-ai python -m flake8 app/ --count --statistics

# Check specific files
docker-compose run --rm medinext-ai python -m flake8 app/components/patient_details.py

# Run tests in Docker
docker-compose run --rm medinext-ai python -m pytest
```

### **Local Linting (Alternative)**

If you prefer to run linting locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Check for linting issues
python -m flake8 app/

# Auto-fix formatting issues
python -m black app/

# Run tests
python -m pytest
```

### **Common Linting Issues**

- **E501**: Line too long (>79 characters)
- **W293**: Blank line contains whitespace
- **F401**: Unused imports
- **E402**: Module level import not at top of file
- **E722**: Bare except statements

**Note**: Docker-based linting ensures consistency across different environments and is recommended for team development.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Check the [documentation files](#documentation) above
- Review the [Docker Setup Guide](docs/DOCKER_README.md) for deployment issues
- Consult the [Superwise Agent Setup Guide](docs/SUPERWISE_AGENT_SETUP_GUIDE.md) for AI integration help

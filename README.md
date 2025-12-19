# AI Customer Support Chatbot 

## 🚀 Key Features
- **AI-Powered Core:** Driven by Google Gemini 2.0 Flash.
- **Context Management:** Utilizes **Redis** to store and retrieve chat history.
- **Automated Tagging:** Logic-based classification for `Billing`, `Tech Support`, and `Complaints`.
- **Human Escalation:** Automatically marks sessions as `is_escalated` if the AI identifies a need for a human manager.
- **Admin Dashboard:** A Django Admin interface to monitor chat sessions.

## 🛠 Tech Stack
- **Framework:** Django, Django REST Framework
- **AI Model:** Google Gemini 2.0 Flash (`google-genai` SDK)
- **Caching/Memory:** Redis
- **Database:** PostgreSQL 

## 📋 Project Setup

### 1. Environment Configuration
Create a `.env` file in the root directory and populate it with your credentials.

### Installation & Launch
# Clone the repository
git clone <repository-url>
cd ai-customer-support-chatbot

# Install dependencies
pip install -r requirements.txt

# Environment Configuration
Create a `.env` file in the root directory and populate it with your credentials.

# Run migrations
python manage.py migrate

# Start the application
python manage.py runserver

### Running Tests
# Run all tests
pytest


 # Investment Idea Planner

  A Django-based investment planning tool that sends automated email reminders and welcome messages using Celery and scheduled tasks.

  ---

  ## 🚀 Features

  - User registration and authentication
  - Investment plan creation and management
  - Automated daily email reminders for saving
  - Welcome emails for new users
  - Task scheduling using Celery Beat

  ---

  ## 🛠️ Getting Started

  ### 📦 Install Dependencies

  Make sure you have Python, pip, Redis, and a virtual environment set up.

  ```bash
  pip install -r requirements.txt
  ```

### 🔧 Running the Project
1.  Start Django Development Server
    ```bash
    python manage.py runserver
    ```


2. Run Celery Worker (for async tasks)
    ```bash
    celery -A investment worker --loglevel=info
    ```

3. Run Celery Beat (for periodic tasks)
    ```bash
    celery -A investment beat --loglevel=info
    ```

## 📫 Email Tasks
- Investment reminder: sent daily based on the notification_date of investment plans.

## 🗃️ Tech Stack
- Django

- Celery

- Redis

- django-celery-beat

- MySQL
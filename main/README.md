# QuizMaster - Course-Specific Online Quiz & Automated Grading System

A comprehensive, full-stack web application built with **Django 4** and **Tailwind CSS** for conducting course-specific online quizzes with automated grading. Designed specifically for Software Engineering education, QuizMaster provides a secure, responsive, and feature-rich platform for both students and lecturers.

---

## Features

### For Students
- **Secure Authentication** - Login/Register with username, email, and student ID
- **50 MCQ Quiz** - Software Engineering questions with 4 options each
- **Randomized Questions** - Both question order and options are shuffled per attempt
- **Countdown Timer** - Real-time timer with visual warnings (5 min, 1 min alerts)
- **Auto-Submit** - Quiz automatically submits when time expires
- **Save Answers** - Answers are saved progressively via AJAX
- **Scheduled Results** - Results released at lecturer-configured time
- **Performance Review** - Detailed review with correct/incorrect indicators
- **Quiz History** - Track all past attempts and performance trends
- **Responsive Design** - Works perfectly on desktop and mobile devices

### For Lecturers (Admin)
- **Dashboard** - Overview with statistics (students, attempts, scores)
- **Question Management** - Add, edit, delete questions with 4 options
- **Bulk Import** - Import questions from JSON or CSV files
- **Quiz Settings** - Configure duration, passing score, randomization
- **Results Scheduling** - Set specific date/time for results release
- **Student Results** - View all student scores with pass/fail status
- **Performance Analytics** - Average scores, pass rates, rankings
- **Django Admin** - Full access to all data via Django admin panel

### Technical Features
- **Session-based Quiz Handling** - Secure quiz state management
- **Anti-Cheating** - Randomized questions prevent answer sharing
- **Prevent Multiple Submissions** - One attempt per student (configurable)
- **Auto-Grading** - Immediate automated scoring upon submission
- **50 Pre-loaded SE Questions** - Management command to populate database

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2.13 (Python) |
| Frontend | HTML5, Tailwind CSS, JavaScript |
| Database | SQLite (default) |
| Authentication | Django Auth System |
| Styling | Tailwind CSS 3.4 (CDN) |
| Icons | Font Awesome 6.5 |
| Fonts | Google Fonts (Inter) |

---

## Project Structure

```
quizmaster/
|-- manage.py                  # Django management script
|-- requirements.txt           # Python dependencies
|-- .env.example              # Environment variables template
|-- README.md                 # This file
|
|-- quizmaster/               # Main project configuration
|   |-- __init__.py
|   |-- settings.py           # Django settings
|   |-- urls.py               # URL routing
|   |-- wsgi.py               # WSGI config
|   |-- asgi.py               # ASGI config
|
|-- accounts/                 # User authentication app
|   |-- models.py             # UserProfile model
|   |-- views.py              # Login, register, logout, profile
|   |-- forms.py              # Registration and login forms
|   |-- urls.py               # Account URL patterns
|   |-- admin.py              # Admin configuration
|
|-- quiz/                     # Core quiz functionality
|   |-- models.py             # Question, Option, QuizAttempt, etc.
|   |-- views.py              # All quiz views (student & admin)
|   |-- urls.py               # Quiz URL patterns
|   |-- admin.py              # Quiz admin configuration
|   |-- middleware.py         # Quiz timer middleware
|   |-- management/
|   |   |-- commands/
|   |   |   |-- load_se_questions.py  # Load 50 SE questions
|
|-- results/                  # Results display app
|   |-- models.py
|   |-- views.py
|   |-- urls.py
|
|-- templates/                # HTML templates
|   |-- base.html             # Base layout
|   |-- home.html             # Landing page
|   |-- accounts/
|   |   |-- login.html
|   |   |-- register.html
|   |   |-- profile.html
|   |-- quiz/
|   |   |-- dashboard.html
|   |   |-- take_quiz.html
|   |   |-- results.html
|   |   |-- review.html
|   |   |-- admin_dashboard.html
|   |   |-- manage_questions.html
|   |   |-- add_question.html
|   |   |-- edit_question.html
|   |   |-- settings.html
|   |   |-- view_results.html
|   |   |-- import_questions.html
|
|-- static/                   # Static files (CSS, JS, images)
|-- db.sqlite3               # SQLite database (auto-created)
```

---

## Installation & Setup (VS Code)

### Prerequisites
- Python 3.8 or higher
- VS Code with Python extension
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd quizmaster

# Or extract the project folder and navigate to it
cd quizmaster
```

### Step 2: Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy the example environment file
# On Windows:
copy .env.example .env

# On macOS/Linux:
cp .env.example .env
```

Edit the `.env` file and set your secret key:
```env
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
```

### Step 5: Run Database Migrations

```bash
python manage.py migrate
```

### Step 6: Create a Superuser (Lecturer Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin/lecturer account.

### Step 7: Load the 50 Software Engineering Questions

```bash
python manage.py load_se_questions
```

This command populates the database with 50 pre-written Software Engineering MCQ questions.

### Step 8: Run the Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to: **http://127.0.0.1:8000/**

---

## Usage Guide

### For Lecturers (Admin)

1. **Access Admin Panel** - Go to `/admin/` and login with superuser credentials
2. **Set Up Quiz** - Navigate to Quiz Settings and configure:
   - Quiz duration (default: 60 minutes)
   - Total questions (default: 50)
   - Passing score (default: 25)
   - Results release time
   - Randomization options
3. **Manage Questions** - Add, edit, or delete questions via:
   - The admin dashboard at `/quiz/admin/dashboard/`
   - Django admin panel at `/admin/`
   - Bulk import via JSON or CSV
4. **View Results** - Monitor student performance and export data

### For Students

1. **Register** - Create an account with your student ID
2. **Login** - Access your dashboard
3. **Start Quiz** - Click "Start Quiz" on the dashboard
4. **Answer Questions** - Select options (answers auto-save)
5. **Submit** - Manually submit or let auto-submit handle it
6. **View Results** - Check results after the scheduled release time

---

## JSON Import Format

```json
[
  {
    "question": "What is Software Engineering?",
    "difficulty": "easy",
    "explanation": "Software Engineering is the systematic application of engineering approaches to software development.",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 0
  }
]
```

## CSV Import Format

```csv
question,difficulty,explanation,option1,option2,option3,option4,correct
"What is SE?","easy","SE is...","A","B","C","D",0
```

---

## VS Code Configuration

### Recommended Extensions
- Python (by Microsoft)
- Django Template
- Tailwind CSS IntelliSense

### Launch Configuration

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django Server",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["runserver"],
            "django": true,
            "justMyCode": true
        },
        {
            "name": "Django Migrate",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["migrate"],
            "django": true
        },
        {
            "name": "Load Questions",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["load_se_questions"],
            "django": true
        }
    ]
}
```

### Settings

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "files.associations": {
        "*.html": "django-html"
    },
    "emmet.includeLanguages": {
        "django-html": "html"
    }
}
```

---

## Configuration Options

All quiz settings can be configured through the admin panel:

| Setting | Default | Description |
|---------|---------|-------------|
| Duration | 60 minutes | Time allowed for quiz |
| Total Questions | 50 | Number of questions per quiz |
| Passing Score | 25 | Minimum score to pass |
| Shuffle Questions | True | Randomize question order |
| Shuffle Options | True | Randomize answer options |
| Multiple Attempts | False | Allow retaking the quiz |
| Results Release | None | Scheduled results release time |

---

## Security Features

- CSRF protection on all forms
- Session-based authentication
- Quiz attempt uniqueness enforcement
- Auto-logout on session expiry
- Secure password handling (Django default)
- XSS protection via template escaping

---

## Customization

### Changing the Course
Edit the `get_or_create_default_course()` function in `quiz/views.py`:

```python
def get_or_create_default_course():
    course, created = Course.objects.get_or_create(
        code='YOUR_CODE',
        defaults={
            'name': 'Your Course Name',
            'description': 'Your course description'
        }
    )
    return course
```

### Adding More Questions
Use the management command to create a custom loader, or use the import feature in the admin dashboard.

### Changing Colors
The color scheme is defined in the Tailwind config within `templates/base.html`. Modify the `primary` and `accent` color palettes.

---

## Troubleshooting

### Common Issues

1. **"No module named 'django'"**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **"Migration errors"**
   - Delete `db.sqlite3` and run `python manage.py migrate` again

3. **"Static files not loading"**
   - Run `python manage.py collectstatic`
   - Ensure `DEBUG=True` in development

4. **"Questions not showing"**
   - Run `python manage.py load_se_questions`
   - Check that questions are marked as active in admin

---

## Requirements

```
Django==4.2.13
Pillow==10.3.0
python-dotenv==1.0.1
django-crispy-forms==2.1
crispy-tailwind==1.0.0
```

---

## License

This project is created for educational purposes. Feel free to use and modify as needed.

---

## Credits

Built with Django, Tailwind CSS, and Font Awesome. Designed for Software Engineering education.

**QuizMaster** - Making assessments smarter, fairer, and more efficient.

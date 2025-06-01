# Django PokeAPI

## Setup Instructions

### 1. Redis
- Install and run Redis on port 6380

### 2. Database
- Create your database for this project

### 3. Dependencies (Poetry)
- Install Poetry if you don't have it: https://python-poetry.org/docs/#installation
- Install project dependencies:
```bash
poetry install
```
- Activate the virtual environment:
```bash
poetry shell
```

### 4. Configuration File
- Go to `django_pokeapi/config/` folder
- Copy `dev.env` → `my-example.env`
- Modify the values as needed (mainly database information)
- **IMPORTANT: Generate your own SECRET_KEY!**

#### Generating SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Insert the generated key into `my-example.env` instead of "django-insecure-yourkey"

### 5. Running the Application

#### **Required Setup (First Time Only)**
- Before running the application, you must complete these setup steps:

**Using VSCode (Recommended):**
- Use the `Migrate` launch configuration to create database tables
- Use the `Populate DB` launch configuration to load Pokemon data

**Using Command Line:**
```bash
# Export environment file (required for command line)
export POKEAPI_CONFIG=django_pokeapi/config/my-example.env

# Create database tables
python manage.py migrate

# Load Pokemon data (takes several minutes)
python manage.py populate_db
```

#### **Running the Application**

**Option A: VSCode Launch Options (Recommended)**
The project includes pre-configured VSCode launch configurations for easy development:

1. **Full Setup (Django + Celery)**: Use the `Django/Celery` compound configuration
   - Go to `Run and Debug` VSCode panel.
   - Select `Django/Celery` from the dropdown
   - This will start both Django server and Celery worker simultaneously

2. **Individual Services**:
   - `Django` - runs only the Django development server
   - `Celery` - runs only the Celery worker

**Option B: Command Line (Alternative)**
If you prefer command line or don't use VSCode, you **must first export the environment file**:

```bash
export POKEAPI_CONFIG=django_pokeapi/config/my-example.env
```

Then you can run:

**Django Development Server Only:**
```bash
python manage.py runserver
```

**Full Setup with Celery:**
Terminal 1 - Django server:
```bash
python manage.py runserver
```

Terminal 2 - Celery worker:
```bash
celery -A django_pokeapi.apps.common worker --loglevel=info
```

**Additional populate_db options:**
```bash
# Only Pokemon types
python manage.py populate_db --types-only

# Only abilities  
python manage.py populate_db --abilities-only

# Only Pokemon data
python manage.py populate_db --pokemon-only
```

**Note:** VSCode launch options automatically handle environment variables, so export is not needed when using Option A.


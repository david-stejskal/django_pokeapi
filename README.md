# Django PokeAPI

## Setup Instructions

### 1. Redis

* [Install](https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/install-redis-on-linux/) and then run Redis

```bash
redis-server --port 6380
```

### 2. Database

```bash
sudo apt install postgresql
sudo -u postgres createdb django_pokeapi
```

### 3. Dependencies (Poetry)

* [Install](https://python-poetry.org/docs/#installing-with-pipx) Poetry
* Install project dependencies:

```bash
poetry install
```

* Activate the virtual environment:

```bash
poetry env activate
```

* Copy the output (source /.../bin/activate) and execute it.

### 4. Configuration File

* Go to `django_pokeapi/config/` folder
* Copy `dev.env` → `my-example.env`
* Modify the values as needed (mainly database information)
* **IMPORTANT: Generate your own SECRET_KEY!**

#### Generating SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Replace **"django-insecure-yourkey"** with the generated key in `my-example.env`

### 5. Running the Application - First time setup

#### Using VSCode (Recommended)

* Use the `Migrate` launch configuration to create database tables
* Use the `Populate DB` launch configuration to load Pokemon data

#### Using Command Line

```bash
# Export environment file (required for command line)
export POKEAPI_CONFIG=django_pokeapi/config/my-example.env

# Create database tables
python manage.py migrate

# Load Pokemon data (takes several minutes)
python manage.py populate_db
```

* NOTE: If you are having trouble with the authentication along with using the default postgres user, you can change the password via `ALTER USER postgres WITH PASSWORD 'new_password';` in the psql (`sudo -u postgres psql`).

### 6. Running the Application

#### Option A: VSCode Launch Options (Recommended)

The project includes pre-configured VSCode launch configurations for easy development:

1. **Full Setup (Django + Celery)**: Use the `Django/Celery` compound configuration
   * Go to `Run and Debug` VSCode panel.
   * Select `Django/Celery` from the dropdown
   * This will start both Django server and Celery worker simultaneously

2. **Individual Services**:
   * `Django` - runs only the Django development server
   * `Celery` - runs only the Celery worker

#### Option B: Command Line (Alternative)

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

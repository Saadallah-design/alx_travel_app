# Django settings for alx_travel_app project.
# alx_travel_app/alx_travel_app/settings.py

# Standard library
from pathlib import Path

# Third-party libraries
import environ
import pymysql

# Configure PyMySQL to act as MySQLdb
pymysql.install_as_MySQLdb()
# This allows Django to use PyMySQL as the MySQL database adapter.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Initialize environment variables
env = environ.Env(DEBUG=(bool, False))
env_file = BASE_DIR / '.env'
if env_file.exists():
    env.read_env(str(env_file))
# Checks if .env exists. 
# Reads .env only if the file exists.
# Safer for production if .env is optional.

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='replace-me')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
# Used to specify which hosts/domains can serve the application.
# In production, set this to your domain names.
# Using ['*'] allows all hosts, which is not recommended for production.
# I used it since it is flexible for development and testing.


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',       # DRF
    'corsheaders',          # CORS
    'drf_yasg',             # Swagger

    # Local apps
    'listings',             # your app
]

MIDDLEWARE = [
     'corsheaders.middleware.CorsMiddleware',  # at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOW_ALL_ORIGINS = True  # for now, you can restrict this in production
# CORS_ALLOWED_ORIGINS is an alternative to CORS_ALLOW_ALL_ORIGINS. it is used to specify a list of allowed origins.

ROOT_URLCONF = 'alx_travel_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'alx_travel_app.wsgi.application'


# Database
# Database (MySQL) using django-environ + .env variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',      # ← This tells Django to use MySQL
        'NAME': env('DB_NAME'),                    # ← Database name from your .env file
        'USER': env('DB_USER'),                    # ← MySQL username from .env
        'PASSWORD': env('DB_PASSWORD'),            # ← MySQL password from .env
        'HOST': env('DB_HOST', default='127.0.0.1'),
        'PORT': env('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Configuring Django REST FRAMEWORK (DRF)
# Django REST framework minimal config
# Now API is open to public access. I can restrict it in production.
# Later, I can add authentication classes as needed.
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    # add authentication classes as needed
}


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CORS Configuration
# CORS (Cross-Origin Resource Sharing) settings
# Two ways: allow all for development or explicit list from env
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False)
if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['http://localhost:3000'])
# This allows frontend apps running on these origins to access the API.
# In production, set specific allowed origins for security.


# Celery Configuration Options
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# Uses RabbitMQ (AMQP protocol) as the message broker.
# Make sure RabbitMQ server is running on localhost.
# You can change the broker URL to use other brokers like Redis if needed.
# RabbitMQ is a robust message queue system designed for high throughput and reliability.
# Tasks are sent to RabbitMQ, which stores and routes messages to workers.

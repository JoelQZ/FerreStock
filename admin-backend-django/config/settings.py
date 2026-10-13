"""
Configuración de Django para FerreStock (backend de administración).
Los datos sensibles se leen del archivo .env (ver .env.example).
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Aplicaciones

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Terceros
    'rest_framework',
    'corsheaders',
    # FerreStock
    'apps.usuarios',
    'apps.catalogo',
    'apps.inventario',
    'apps.ventas',
    'apps.caja',
    'apps.reportes',
    'apps.configuracion',
    'apps.ia',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Base de datos: MySQL (datos en el archivo .env)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {'charset': 'utf8mb4'},
        'TEST': {'CHARSET': 'utf8mb4', 'COLLATION': 'utf8mb4_unicode_ci'},
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Usuario propio (tabla `usuario`)

AUTH_USER_MODEL = 'usuarios.Usuario'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# API REST y login con token JWT

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'USER_ID_FIELD': 'id_usuario',
    'USER_ID_CLAIM': 'id_usuario',
}


# React (admin y POS) puede llamar a esta API

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:5174',
]


# Idioma y zona horaria (Perú)

LANGUAGE_CODE = 'es-pe'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_TZ = True


# Archivos estáticos

STATIC_URL = 'static/'

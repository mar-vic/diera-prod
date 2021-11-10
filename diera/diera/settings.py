"""
Django settings for diera project.

Generated by 'django-admin startproject' using Django 3.1.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import environ
import os

from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.escape_proxy = True

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)  # False if unset in the .env file

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))
# SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = env.str('SECRET_KEY')  # Read the secret key set in the .env file

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = { 'default': env.db('DATABASE_URL') }  # Read db config set in .env file

ALLOWED_HOSTS = ['*']

SITE_ID = 1  # DjangoCMS
X_FRAME_OPTIONS = 'SAMEORIGIN'  # DjangoCMS

# Application definition

INSTALLED_APPS = [
    'djangocms_admin_style',  # DjangoCMS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'cms',  # DjangoCMS
    'menus', # DjangoCMS
    'treebeard', # DjangoCMS
    'sekizai',  # DjangoCMS
    'filer',  # DjangoCMS
    'easy_thumbnails',  # DjangoCMS
    'mptt',  # DjangoCMS
    'djangocms_text_ckeditor',  # DjangoCMS
    'djangocms_link',  # DjangoCMS
    'djangocms_file',  # DjangoCMS
    'djangocms_picture', #DjangoCMS
    'djangocms_video', #DjangoCMS
    'djangocms_googlemap', #DjangoCMS
    'djangocms_snippet', #DjangoCMS
    'djangocms_style',  #DjangoCMS
    'djangocms_bootstrap4', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_alerts', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_badge', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_card', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_carousel', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_collapse', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_content', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_grid', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_link', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_media', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_picture', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_tabs', #DjangoCMS
    'djangocms_bootstrap4.contrib.bootstrap4_utilities', #DjangoCMS
    'photologue',
    'photologue_cms_integration',
    'sortedm2m',
    'diera',  # Diera Apps
    'page_extensions',  # Diera Apps
    'event_calendar',  # Diera Apps
    'calendar_cms_integration',  # Diera Apps
    'wizards',  # Diera Apps
]

THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

MIDDLEWARE = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
]

ROOT_URLCONF = 'diera.urls'

CMS_TEMPLATES = [
    # Diera (all extend base.html)
    ('home.html', 'Home'),
    ('program.html', 'Program'),
    ('festivals.html', 'Festivals'),
    ('galleries.html', 'Galleries'),
    ('about.html', 'About'),
    ('featured_article.html', 'Featured Article'),
    ('event.html', 'Event'),
    ('festival.html', 'Festival'),

    # DjangoCMS defaults
    ('fullwidth.html', 'Fullwidth'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right'),
    # ('home.html', 'Home page template'),
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

WSGI_APPLICATION = 'diera.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'sk'

TIME_ZONE = 'Europe/Bratislava'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# DjangoCMS settings for language mutations
LANGUAGES = [
    ('sk', 'Slovak'),
    ('en', 'English'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_ROOT = "/home/marvic/sites/diera-prod/diera/static"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Photologue settings
PHOTOLOGUE_GALLERY_LATEST_LIMIT = 4

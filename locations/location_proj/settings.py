"""
Django settings for app project.
Generated by 'django-admin startproject' using Django 5.1.7.
For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d1kcnem21+r64*g4oku-09-(thsm67di)^ire-#23*8$wya5k+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",#This is the rest framework we installed for communication between the frontend and backend in JSON format
    "location_app" #This is the locations microservice app we created called core
    #Add the core app to the list of installed apps
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',


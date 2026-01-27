-> Create Repo in GitHub : https://github.com/Witzcode0/ITVerse.git

-> Clont that repo in your local system

-> Choose specific location

-> Open CMD on that location

...../specific_location > git clone https://github.com/Witzcode0/ITVerse.git

...../specific_location > cd ITVerse

.../specific_location/ITVerse > 

-> Check Python is installed or not
.../specific_location/ITVerse > python
Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>

OR

.../specific_location/ITVerse > python --version
Python 3.13.5

-> NOw, create virtual ENV for ITverse project
.../specific_location/ITVerse > python -m venv {myvenv}

-> Activate and De-activate your ENV
.../specific_location/ITVerse > {myvenv}\Scripts\activate
(myvenv).../specific_location/ITVerse > {myvenv}\Scripts\deactivate

-> Make sure your ENV is Activated
(myvenv).../specific_location/ITVerse > 

-> Create requirements.txt file 
(myvenv).../specific_location/ITVerse > type nul > requirements.txt (windows)
(myvenv).../specific_location/ITVerse > touch requirements.txt (Linux/Mac)

-> Now, install django
(myvenv).../specific_location/ITVerse > pip install django

-> Add your installed modules and packages inside requirements.txt file 
(myvenv).../specific_location/ITVerse > pip freeze > requirements.txt

-> Installed or upgrade your module and packages from requirements.txt file
(myvenv).../specific_location/ITVerse > pip install -r requirements.txt

-> Now, Check Django installed or not
(myvenv).../specific_location/ITVerse > pip list
Package  Version
-------- -------
asgiref  3.11.0
Django   6.0.1
pip      25.3
sqlparse 0.5.5
tzdata   2025.3

OR

(myvenv).../specific_location/ITVerse > pip freeze
asgiref==3.11.0
Django==6.0.1
sqlparse==0.5.5
tzdata==2025.3

OR
(myvenv).../specific_location/ITVerse > python
Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> django.get_version()
'6.0.1'

OR

(myvenv).../specific_location/ITVerse > python -m django --version
6.0.1

OR 

(myvenv).../specific_location/ITVerse > pip freeze | findstr Django
Django==6.0.1

-> Now, Creating a Django project
(myvenv).../specific_location/ITVerse > django-admin startproject project .

-> Run your django project
(myvenv).../specific_location/ITVerse > python manage.py runserver 0.0.0.0:[port]
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
January 22, 2026 - 13:33:10
Django version 6.0.1, using settings 'project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.


-> Migrate you built0in table inside database
(myvenv).../specific_location/ITVerse > python manage.py migrate

-> Now, create super user
(myvenv).../specific_location/ITVerse > python manage.py createsuperuser
Username (leave blank to use 'admin'): admin
Email address: admin@gmail.com
Password: ********
Password (again): ********
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.

-> Now, lets create django apps
(myvenv).../specific_location/ITVerse > mkdir apps
(myvenv).../specific_location/ITVerse > python manage.py startapp {users} apps/{users}

    Config app's path
    go to the app dir and open apps.py

    from django.apps import AppConfig

    class MasterConfig(AppConfig):
        name = 'apps.{master}' # add apps.app-name

    Now, config you app in project/settings.py

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'apps.master', # Add new
        'apps.users', # Add new
    ]

    (Optional)

    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]

    # CUSTOM_APPS
    INSTALLED_APPS += [
        'apps.master',
        'apps.users'
    ]

    # THIRDPARTY_APPS
    INSTALLED_APPS += [
        
    ]


-> Create tamplate directory in dashboard app

(myvenv).../specific_location/ITVerse/apps/dashboard > 
    dashboard/
        - templates/ - create dir
            - dashboard/ - create dir
                - index.html
                - about.html
                - contact.html

-> Setup media and static files : project/settings.py

    import os

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    &

    Add project/settings.py/url.py

    from django.conf import settings # Add new
    from django.conf.urls.static import static # Add new

    urlpatterns = [
        path('admin/', admin.site.urls),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Add new

---------------------------------------------------------------------------------
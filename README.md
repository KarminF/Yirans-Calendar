# Yirans-Calendar
Ein Kalendar zum Terminbuchen oder so...

Do install mysqlclient
`pip install django mysqlclient`

edit your database info at settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<database_name>',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': '<database_host>',
        'PORT': '3306',
    }
```

then do

```
python manage.py makemigrations
python manage.py migrate
```

now we get started
```
python manage.py runserver
```

usages:
at week or day view, drag to book a period of time.

click on an booking to delete the booking.

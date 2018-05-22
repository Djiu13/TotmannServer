# README #

Go to https://bitbucket.org/webhamster/totmann for more details

## Setting up

An image based on this repo is uploaded on DockerHub.
* Create your settings_local.py to override the default settings
* Create a dockerfile to add the settings file and start the django application
```
FROM guillaumemabile/totmannwindows:1.1
COPY /settings_local.py totmannserver/totmann/
ENTRYPOINT python totmannserver\manage.py runserver 0.0.0.0:4000





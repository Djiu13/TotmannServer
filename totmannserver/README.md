# README #

Totmann is a dead man's switch or watchdog timer for your cron jobs. It notifies you via email when your scheduled jobs are not running on time, or when jobs finish with errors. Use it, for example, to make sure that your backup is running on time and not out of space or as a simple machine uptime monitoring tool.

A public totmann server is hosted at https://totmann.danielfett.de but setting up your own server is easy!

## How does it work? ##

Totmann provides a REST interface. Whenever a cron job finishes, it simply posts to a specific URL to let totmann know that the job finished. That means, you're only one call to wget/curl away from adding totmann to your cron jobs! Your job can optionally transfer the return code its main command to totmann to distinguish whether the command encountered errors or not.

Additionally, there are URLs for logging when the job started and to transfer the job's logfile to totmann. Using these features is optional. The logfile can be checked against regular expressions to detect warnings or malformed output.

Whenever a command did not finish successfully in a defined interval or an error condition was detected, totmann can notify you via email. You can use services such as Pushover or IFTTT to create individual notification channels. (Note that you can even call totmann from IFTTT, see below.)

totmann logs a configurable number of events for your cron jobs to assist in debugging your jobs.

## What can I do with totmann? ##

* Use it to make sure that not only your backup job is running on time, but also to detect whether the backup command finished without errors.
* Make sure that your automated compile job does not output warnings.
* Let your Raspberry Pi ping totmann to ensure that the Pi has not crashed and has internet connectivity.
* Use IFTTT to send a request to totmann every time it is raining and get a reminder to water your plants after a few days without rain.
* Use it as a real dead (wo)man's switch to reveal your master password to your loved ones if you didn't show any signs of life in the past 14 days (some IFTTT wiring needed).
* ...

### Setting up ###

totmann is a Django app and thus written in Python. It can be run with Passenger, a WSGI compliant server, which can be used in conjunction with apache, nginx, or standalone. Just follow the [instructions on how to set up passenger](https://www.phusionpassenger.com/library/walkthroughs/start/python.html) and make sure to check out this repository, not their demo repo.

Also make sure to have django and django-registration-redux installed. Both can be installed with pip -r requirements.txt.

Copy totmann/settings_local.example.py to totmann/settings_local.py and change the settings inside this file as needed. See [the Django manual](https://docs.djangoproject.com/en/1.8/ref/settings/) for a list of settings. Settings in settings_local.py override those in settings.py.

After having all the files in place, call ./manage.py migrate to initialize the database. Call ./manage.py createsuperuser to create your first user. (You can later log in at the path /admin with this user.)

You can now start passenger.

As a last step, make sure to call ./manage.py run_checks in regular intervals (ideally every minute). 

### Development ###

totmann is in development and still contains some bugs. Please file any bugs you find here in the bug tracker. Pull requests are also welcome!
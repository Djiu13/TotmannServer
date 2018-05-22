FROM python:3.6.1-windowsservercore

RUN mkdir C:\totmannserver

RUN pip install django==1.11.1
RUN pip install django-registration-redux
RUN pip install django-tagging

RUN mkdir C:\tmp

ADD totmannserver/ /totmannserver

EXPOSE 80

RUN python totmannserver\manage.py makemigrations
RUN python totmannserver\manage.py migrate

ENTRYPOINT python totmannserver\manage.py runserver 0.0.0.0:80

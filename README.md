# images-site

How to start the application via Docker:
> docker-compose up

Create superuser to manage the site:
> python manage.py createsuperuser <username>

Go to 127.0.0.1:8000/admin and log-in with the credentials made in the previous step.

Assign the desired plan to the user in UserProfiles table.

# Informations

It took more than a week to complete this task (I had to work on it in my spare time after my daily full-time job) because this assignment involves a lot of tinkering with the Django and Django Rest Framework itself. I had to overwrite methods for CreateAPIView class-based-view and use multiple multi-directional relations with intermediate tables for my database models. It was a challenging assignment by doing which I learned a lot about Django Rest Framework and how the class-based-views works underneath.


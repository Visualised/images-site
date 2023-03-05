# images-site

# How to start the application via Docker:
**Step 1**

Clone the repository
> git clone https://github.com/Visualised/images-site.git

**Step 2**
Use this docker command
> docker-compose up

**Step 3**

Create superuser to manage the site:
> docker-compose exec api python manage.py createsuperuser

**Step 4**

Follow the instructions that will appear in your console. 

**Step 5**

Go to 127.0.0.1:8000/admin and log-in with the credentials made in the previous step.

**Step 6**

Assign the desired plan to the user in UserProfiles table.

# How to start the application without Docker:

**Step 1**

Clone the repository by using git clone
> git clone https://github.com/Visualised/images-site.git

**Step 2**

Install Python requirements from pip
> pip install -r requirements.txt

**Step 3**

Create database
> python manage.py migrate

**Step 4**

Load data into the database from fixture file
> python manage.py loaddata database_models_fixture.json

**Step 5**

Add cron task for automatic database cleaning (please keep in mind that for cron to work the program must be run under GNU/Linux) 
> python manage.py crontab add

**Step 6**

Run the program
> python manage.py runserver



# Endpoints

Upload the image.
> /upload 

List your images.
> /list

# Informations

It took more than a week to complete this task (I had to work on it in my spare time after my daily full-time job) because this assignment involves a lot of tinkering with the Django and Django Rest Framework itself. I had to overwrite methods for CreateAPIView class-based-view and use multiple bi-directional relations with intermediate tables for my database models. It was a challenging assignment by doing which I learned a lot about Django Rest Framework and how the class-based-views works underneath.

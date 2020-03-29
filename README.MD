# Description
Work At Olist in a simple API that allows the user to include, delete, remove and retrieve books in the system. Each
book have one or more authors associated with it, which should be set in the system using the `importauthor` command  
(more details below).

# Installation
You can run this project locally, directly on your machine, or as alternative, we provide Docker as well. 

- Regardless your choice, the first step is to clone this repo locally

If you wish to use it without docker, here is what you have to do in order to install it
- (Optional) Setup a new virtualenv using `virtualenv <env-name>`
- Install the requirements `pip install -r requirements.txt`
- Install PostgreSQL
- Set up your DB config at settings.DATABASE 

If you decide to use Docker:
- Install Docker
- Run `docker-compose pull` to pull PostgreSQL image
- Run `docker-compose build` to build the project's image 

# Usage
## Docker-specific commands -- Ignore if you are not using it
Using Docker, to run the commands below, or any other management command, you can use `docker-compose run workatolist-bash` to
open the container's bash terminal. Running locally, you can just run the commands directly from the project root.

I also included some commands to make the life easier. For example:

`docker-compose run workatolist-test`: Migrate the DB and run the tests suite automatically

`docker-compose run workatolist-runserver`: Migrate the DB and run the server
## Migrating DB
You need to migrate the DB before running any command (in case the DB is fresh), executing `python manage.py migrate`
## Running it locally
If you wish to run it locally, all it takes is to execute `python manage.py runserver`
## Running the tests
To run the test suite, run `python manage.py test`
## Importing authors
Once the project is installed, you can import an csv file containing the authors data using the following command:
``python manage.py importauthors <filepath>``

For example:

`python manage.py importauthors "C:/Users/Hugo Pelissari/Desktop/work-at-olist/authors.csv"`
## API docs
Essentially, this API have two endpoints: 

The `/authors` is read-only and you can search for specific authors, or just get the list containing all the
authors in the DB.

The `/books` endpoint is more flexible one, you can add new books, delete or update existing ones, and also get
the full list, or a filtered version of it. 

We have [Swagger Docs available here](https://work-at-olist-testing.herokuapp.com/docs/) at your disposal. 
Swagger Docs also allows you to make API calls directly from it, so testing the functionality should be easy :)
## Live demo
If you wish to test it without having to clone and run it on your local machine, we have the API deployed
on Heroku for testing purposes:  https://work-at-olist-testing.herokuapp.com/

# How this was build
This was developed using a Windows 10 Home machine. All the code was written using PyCharm Community 
Edition. For project uses mainly `Python 3.7.7`, `Django 3.0.4` and `Django Rest Framework 3.11.0`.
To ensure consistency across `dev`, `test`, (and, one day, `prod`), `PostgreSQL` is the DB of choice for 
all the environments.

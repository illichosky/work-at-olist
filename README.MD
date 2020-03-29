# Installation
- Clone this repo locally
- (Optional) Setup a new virtualenv using `virtualenv <env-name>`
- Install the requirements `pip install -r requirements.txt`
# Usage
## Running it locally
If you wish to run it locally, all it takes is to execute `python manage.py runserver`
## Running the tests
To run the test suit, run `python manage.py test`
## Importing authors
Once the project is installed, you can import an csv file containing the authors data using the following command:
``python manage.py importauthors <filepath>``
## API docs
Essentially, this API have two endpoints: 

The `/authors` is read-only and you can search for specific authors, or just get the list containing all the
authors in the DB.

The `/books` endpoint is more flexible one, you can add new books, delete or update existing ones, and also get
the full list, or a filtered version of it. 

We have [Swagger Docs available here](https://work-at-olist-pellissari.herokuapp.com/docs/) at your disposal. 
Swagger Docs allows you to make API calls directly from it, so testing the functionality should be easy :)
## Live demo
If you wish to test it without having to clone and run it on your local machine, we have the API deployed
on Heroku for testing purposes:  https://work-at-olist-pellissari.herokuapp.com/

# How this was build
This project was developed using a Windows 10 Home machine. All the code was written using PyCharm community 
edition.
- Python 3.7.7
- virtualenv
- Django

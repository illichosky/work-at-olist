# What you'll need
- Python 3.7.7
- virtualenv
- Django
# Installation and running
- Setup a new virtualenv using `virtualenv <env-name>` (recommended)
- Install the requirements `pip install -r requirements.txt`
# Usage
## Running the tests
To run the test suit, all it takes is `python manage.py test`
## Importing authors
Once the project is installed, you can import an csv file containing the authors data using the following command:
``python manage.py importauthors <filepath>``
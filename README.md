# Nexus Tech Tracker

An e-commerce aggregator platform designed to track and compare various tech products. 

## Features
* Browse and search for various tech products.
* Compare prices and specifications.
* User authentication, Shopping cart
* Configured secure user registration and login workflows leveraging Django’s built-in authentication system. Enforced password hashing and session management to protect user profiles and wishlist data securely.

## Built With
* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite (Development)

-----------------------------------------------------------------------------------------------------


## Running the Project Locally

If you want to run this project on your own machine, follow these steps:

1. git clone https://github.com/mohammedakmalcv/Gadget_info.git

2. cd Gadget_info

3. python -m venv venv
    ### on mac or linux : source venv/bin/activate  
    ### On Windows : venv\Scripts\activate

4. pip install -r requirements.txt

5. python manage.py migrate

6. python manage.py runserver

-----------------------------------------------------------------------------------------------------------
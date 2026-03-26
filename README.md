# Nexus Tech Tracker

An e-commerce aggregator platform designed to track and compare tech products. 

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

1. 
   ```bash
   git clone https://github.com/mohammedakmalcv/Gadget_info.git
   cd Gadget_info

2. 
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

3.
    pip install -r requirements.txt

4.
    python manage.py migrate

5.
    python manage.py runserver

-----------------------------------------------------------------------------------------------------------
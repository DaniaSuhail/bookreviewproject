# Book Review Web Application

## Overview
This is a web application built with **Django** and **MongoDB**, styled with **Bootstrap**, to manage and review books. Users can register, log in, and explore books, add reviews, and categorize their reading progress. It includes CRUD functionalities for books, reviews, and user profiles.

## Features
- **User Authentication**:
  - Register, log in, and log out functionality.
- **Book Management**:
  - Add, edit, view, and delete books.
- **Review System**:
  - Post reviews with ratings and categorize books into "Currently Reading," "Finished," or "Want to Read."
- **User Profiles**:
  - Track reading goals and manage personal information.
- **Responsive Design**:
  - Fully styled with Bootstrap for a modern, user-friendly interface.

---

## **Technologies Used**
- **Backend**: Django (Python)
- **Database**: MongoDB (using Djongo for integration)
- **Frontend**: Bootstrap for styling
- **Tools**: Visual Studio Code, Git, GitHub

---

## **Setup Instructions**
1. Create a Virtual Enviroment
   -python -m venv venv

2. Activate the Virtual Enviroment
   -venv\Scripts\activate

3. Install Dependencies
   -pip install -r requirements.txt

4. Configure MongoDB
-Open bookreview/settings.py and update the DATABASES configuration:
-DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'bookreviewdb',  # Replace with your MongoDB database name
    }
}

5. Apply Migrations
   -python manage.py migrate

6.Create a Superuser
  -To access the Django Admin Panel, create a superuser account:
  -python manage.py createsuperuser

 7.Run the Development Server
   -python manage.py runserver

 8.Open the Application
   -Open your browser and navigate to:
   -http://127.0.0.1:8000/

9. Access Django Admin (Optional)
    -You can access the admin site at:
    -http://127.0.0.1:8000/admin/
   -Log in with user created in step 6


### **1. Clone the Repository**
```bash
git clone https://github.com/DaniaSuhail/bookreviewproject.git
cd bookreviewproject

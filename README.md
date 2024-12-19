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

### **1. Clone the Repository**
Clone the project from GitHub and navigate into the project directory:
```bash
git clone https://github.com/DaniaSuhail/bookreviewproject.git
cd bookreviewproject
```

---

### **2. Create a Virtual Environment**
Create a virtual environment to isolate project dependencies:
```bash
python -m venv venv
```

---

### **3. Activate the Virtual Environment**
Activate the virtual environment:
- **On Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **On Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```

---

### **4. Install Dependencies**
Install all the required libraries specified in `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### **5. Configure MongoDB**
Make sure MongoDB is running on your system or remotely. Update the `DATABASES` section in `bookreview/settings.py` to point to your MongoDB database:
```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'bookreviewdb', 
    }
}
```

---

### **6. Apply Migrations**
Run the following command to create the necessary database schema:
```bash
python manage.py migrate
```

---

### **7. Create a Superuser**
To access the Django Admin Panel, create a superuser:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up your username, email, and password.

---

### **8. Run the Development Server**
Start the development server to test the application locally:
```bash
python manage.py runserver
```

---

### **9. Open the Application**
Open your browser and navigate to:
- **Main Application**:  
  [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### **10. Access Django Admin (Optional)**
If needed, access the Django Admin Panel at:
- **Admin Panel**:  
  [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Log in using the superuser credentials created in **Step 7**.

---


### **1. Clone the Repository**
```bash
git clone https://github.com/DaniaSuhail/bookreviewproject.git
cd bookreviewproject

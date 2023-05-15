# Ecommerce_DjangoProject
## Description
With Ecommerce_DjangoProject 
* a  guest user can:
    - see all books of each category
    - search for books
    - add books to cart and make orders
    - send contact messages
* registered user can:
  - everything that a guest user can
  - add books to wishlist
  - see his/her personal info
  - edit or delete his/her profile
  - change password
  - see his/her placed orders
## Technologies
* Django 4.1.3
* Django-crispy-forms 1.14.0
* Bootstrap 5.1.3
* Fontawesome 5.11.2
## Use Project Locally:
* Project Folder and Virtual Environment:		
  - Open Visual Code Studio
  - Launch Profile/Command Prompt																										
  - Go to this path: C:\Users\User\Desktop																					
  - Create a folder for the project: C:\Users\User\Desktop>mkdir Book_DjangoProject								
  - Get inside the folder: C:\Users\User\Desktop>cd Book_DjangoProject																							
  - Create a Virtual Environment with name myenv: C:\Users\User\Desktop\Book_DjangoProject>python -m venv myenv					
  - Activate Virtual Environment: C:\Users\User\Desktop\Book_DjangoProject>myenv\Scripts\activate										
* Clone Project OR:                                                                                                                     						
  - (myenv) C:\Users\User\Desktop\Book_DjangoProject>git clone https://github.com/George-Dikas/Book_DjangoProject.git	
  - Change folder's name Book_DjangoProject inside the Project Folder into book_project			
  - (myenv) C:\Users\User\Desktop\Book_DjangoProject>cd book_project		
* Download Project:
  - Code/Download Zip
  - Extract folder and put it into Book_DjangoProject file
  - Change folder's name Book_DjangoProject-master into book_project
  - (myenv) C:\Users\User\Desktop\Book_DjangoProject>cd book_project
* Run Project: 
  - Install all requirments for the project: 
    (myenv) C:\Users\User\Desktop\Book_DjangoProject\book_project>pip install -r requirements.txt
  - Begin your local server: 
    (myenv) C:\Users\User\Desktop\Book_DjangoProject\book_project>python manage.py runserver
  - Type into your browser: http://127.0.0.1:8000/home/

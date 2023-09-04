Django Project Setup Script
Overview
This Python script automates the setup of a Django project and app, along with common configurations and templates. It streamlines the initial project creation process and helps you get started quickly.

Prerequisites
Python and Django should be installed on your system.
Usage
Step 1: Prepare Your Environment

Create a new directory where you want to set up your Django project.
Step 2: Run the Script

Save the provided script into a .py file (e.g., setup_django_project.py) in your project directory.
Open a terminal and navigate to your project directory.
Step 3: Run the Script

Run the script using the following command:
Copy code
python setup_django_project.py
Step 4: Follow the Prompts

The script will prompt you for the project name and app name.
Provide the names as requested.
Step 5: Provide HTML and Static Files

When prompted, provide the paths to the folders containing your HTML files and static files.
The script will copy these files to the appropriate locations.
Step 6: Review and Test

Review the changes made by the script in your project's files, especially in settings.py, views.py, and urls.py.
Test your Django project by running the development server:
Copy code
python manage.py runserver
Step 7: Customize Your App

You can now customize your app's views, templates, and static files as needed.
Step 8: Database Setup

Don't forget to run migrations to set up your database:
Copy code
python manage.py makemigrations
python manage.py migrate
Step 9: Congratulations!

Your Django project is now set up and ready to use.
Script Details
The script performs the following tasks:

Import Necessary Modules: Import essential Python modules for file manipulation and running terminal commands.

Run Terminal Commands: Execute Django-related terminal commands to create a project and app.

Change Current Working Directory: Ensure that subsequent commands are executed within the project's directory.

Create a Django App: Create a Django app within the project folder.

Edit settings.py: Modify the settings.py file of the project to add imports and configurations.

Create Directories: Create necessary directories for templates and static files.

Copy HTML Files: Copy HTML files from a specified source folder to the app's core templates folder.

Copy Static Files: Copy static files (e.g., CSS, JavaScript) from a specified source folder to the project's static folder.

Collect Static Files: Collect all static files from the app and project into a specified directory.

Update views.py and urls.py: Create view functions and URL patterns for each HTML file.

Update urls.py in the Project: Import view functions and add URL patterns to the project's main urls.py file.

Run Migrations: Run Django migrations to set up the database.

Completion Message: Print a completion message to indicate that the setup is complete.


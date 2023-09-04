import subprocess
import os
import shutil
from pathlib import Path

# Run terminal commands
project_name = input("Enter the project name: ")
app_name = input("Enter the app name: ")

commands = [
    f"Django-admin startproject {project_name}"
]

for command in commands:
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Command '{command}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")

# Change the current working directory
project_folder = os.path.join(os.getcwd(), project_name)
os.chdir(project_folder)

# Run the startapp command within the project folder
startapp_command = f"Django-admin startapp {app_name}"
try:
    subprocess.run(startapp_command, shell=True, check=True)
    print(f"Command '{startapp_command}' executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing command '{startapp_command}': {e}")

# Edit settings.py
settings_path = os.path.join(project_name, "settings.py")
with open(settings_path, "r") as f:
    content = f.read()

# Add necessary imports and configurations to settings.py
import_line = "import os"
installed_apps_line = f"'{app_name}',"  # Change to app_name without .core
staticfiles_dirs_line = f"STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]"
static_url_line = "STATIC_URL = '/static/'"
static_root_line = "STATIC_ROOT = os.path.join(BASE_DIR, 'assets')"

# Find the INSTALLED_APPS block and add app_name to it
installed_apps_block_start = "INSTALLED_APPS = ["
installed_apps_block_end = "]"

start_index = content.find(installed_apps_block_start)
end_index = content.find(installed_apps_block_end, start_index)

if start_index != -1 and end_index != -1:
    apps_block = content[start_index:end_index]
    apps_block = apps_block.strip()  # Remove leading/trailing whitespace
    apps_list = [line.strip() for line in apps_block.split("\n")]

    # Check if app_name is already in the list, if not, add it
    if app_name not in apps_list:
        apps_list.append("'"+app_name+"'")

    # Reconstruct the apps block
    apps_block = "\n".join(apps_list) + "," # Add a comma and newline
    content = content[:start_index] +  apps_block + "\n"+ content[end_index:]

with open(settings_path, "w") as f:
    f.write(content)

# Create the templates/core directory
app_folder = os.path.join(app_name)
templates_folder = os.path.join(app_folder, "templates")
core_templates_folder = os.path.join(templates_folder, "core")
os.makedirs(core_templates_folder, exist_ok=True)

# Create urls.py in the app_name root folder
urls_path = os.path.join(app_folder, "urls.py")
with open(urls_path, "w") as f:
    f.write("from django.urls import path\nfrom . import views\n\n")  # Add import statements

# Edit views.py to import render
views_path = os.path.join(app_folder, "views.py")
views_content = "from django.shortcuts import render\n\n"  # Add import statement
with open(views_path, "w") as f:
    f.write(views_content)

# Create static folder in the project_name root folder
static_folder = os.path.join(project_folder, "static")
os.makedirs(static_folder, exist_ok=True)

# Copy .html files from source folder to core folder
html_source_folder = input("Enter the source folder path for .html files: ")
html_files = [file for file in os.listdir(html_source_folder) if file.endswith(".html")]

for html_file in html_files:
    source_path = os.path.join(html_source_folder, html_file)
    destination_filename = html_file.replace("-", "_")  # Replace hyphens with underscores
    destination_path = os.path.join(core_templates_folder, destination_filename)
    shutil.copy(source_path, destination_path)
    print(f"File '{destination_filename}' copied to core folder.")

# Copy files from another source folder to static folder
static_source_folder = input("Enter the source folder path for static files: ")
for item in os.listdir(static_source_folder):
    source_path = os.path.join(static_source_folder, item)
    destination_path = os.path.join(static_folder, item)
    if os.path.isdir(source_path):
        shutil.copytree(source_path, destination_path)
    else:
        shutil.copy(source_path, destination_path)
    print(f"File/Folder '{item}' copied to static folder.")

# Run the collectstatic command
try:
    subprocess.run("python manage.py collectstatic", shell=True, check=True, cwd=project_folder)
    print("Command 'python manage.py collectstatic' executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing command 'python manage.py collectstatic': {e}")

# Update views.py with view functions
views_content = "from django.shortcuts import render\n\n"  # Reset content
html_files = [file for file in os.listdir(core_templates_folder) if file.endswith(".html")]

for html_file in html_files:
    view_name = html_file.split(".")[0]  # Remove .html extension
    view_function = f"def {view_name}(request):\n    return render(request, 'core/{html_file}')\n\n"
    views_content += view_function

with open(views_path, "w") as f:
    f.write(views_content)

# Update urls.py in the app_name folder with URL patterns
urls_path = os.path.join(app_folder, "urls.py")
urls_content = "from django.urls import path\nfrom . import views\n\n"  # Add import statement
with open(urls_path, "w") as f:
    f.write(urls_content)

# Generate URL patterns for each HTML file
with open(urls_path, "a") as f:
    f.write("urlpatterns = [\n")
    for html_file in html_files:
        view_name = html_file.split(".")[0]  # Remove .html extension
        url_pattern = f"    path('{view_name}/', views.{view_name}, name='{view_name}'),\n"
        f.write(url_pattern)

    # Modify the path for 'index' view to point to the root URL
    f.write("    path('', index, name='home'),\n")

    f.write("]\n")

# Update main urls.py in the project_name folder with core.views import and urlpatterns
main_urls_path = os.path.join(project_name, "urls.py")
main_urls_content = "from django.contrib import admin\nfrom django.urls import path, include\nfrom core.views import "
with open(main_urls_path, "w") as f:
    f.write(main_urls_content)

# Include paths for core views using filenames
with open(main_urls_path, "a") as f:
    filenames = [html_file.split(".")[0] for html_file in html_files]
    views_import = ", ".join(filenames)
    f.write(f"{views_import}\n")

# Add admin URL pattern
with open(main_urls_path, "a") as f:
    f.write("urlpatterns = [\n")
    for html_file in html_files:
        view_name = html_file.split(".")[0]  # Remove .html extension
        url_pattern = f"    path('{view_name}/', {view_name}, name='{view_name}'),\n"
        f.write(url_pattern)

    # Modify the path for 'index' view to point to the root URL
    f.write("    path('', index, name='home'),\n")
    f.write("    path('admin/', admin.site.urls),\n")
    f.write("]\n")

# Run migrations
migrate_commands = [
    "python manage.py makemigrations",
    "python manage.py migrate"
]

# Run migrations
for command in migrate_commands:
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Command '{command}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")

print("Script completed.")

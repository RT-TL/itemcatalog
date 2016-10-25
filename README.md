# Udacity Item Catalog

The item catalog allows to CRUD items based on social login via Facebook or Google. It is build with Python, HTML/CSS frontend, JavaScript and runs in a vagrant virtual machine. Database is running on PostgreSQL

## Table of contents

* [Quick start](#quick-start)
* [Requirements](#requirements)
* [Project Structure](#project-structure)
* [License](#license)


## Quick start

Clone repository:
```
git clone https://github.com/Roomtailors/
```

To begin install dependencies by running from root:

1. Run vagrant up to provision virtual machine.
2. Use 'vagrant ssh' to log into vm.
3. Navigate to project root directory /vagrant.
4. Run python project_user.py to fire up application.
5. Visit running application in your browser at 0.0.0.0:5000

The project already contains a dummy database. This was not added to .gitignore on purpose to avoid set up effort. You can delete the database and re-create one by running categorydata.py

## Requirements

1. Install VirtualBox and Vagrant
2. Clone git repository

All other dependencies are installed with vagrant provisioning.

## Project Structure

    |-- .gitignore
    |-- api.py // API endpoints for users and JSON API
    |-- base.py // Base file for shared functions
    |-- categorydata.db // Database, created through categorydata.py
    |-- categorydata.py // Populates a dummy database
    |-- database_setup.py // Database configuration
    |-- project_user.py // Main application file
    |-- social_login.py // Functions for google and facebook login
    |-- user_functions.py // Functions to interact with authentication
    |-- static
    |   |-- styles
    |-- templates
        |-- template files

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
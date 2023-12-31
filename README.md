﻿# Finance App Backend - Under Development

Desktop application for managing personal finances, created using Electron and React.

## Working Features

- Functionality to add and delete expenses.
- JWT authentication.

## Technologies Used Backend

- Python
- SQL (MariaDB)
- Flask
- SQLAlchemy

## Prerequisites

- Python
- MariaDB

## Database Diagram

<img src="./flaskr/static/fa-diagram.png" style="max-width:65%;margin: 0 auto;">

## Getting Started

1. Clone the repository:

   git clone https://github.com/Mokke29/finance-app-backend.git

2. Navigate to the project directory:

    cd finance-app-backend

3. Create virtual environment & activate it:

    python -m venv venv

    *Windows:*

    .\venv\Scripts\activate

    *Unix-like os:*

    ./venv/bin/activate

4. Install required packages:

    python -m pip install -r requirements.txt

5. Run project for development/testing purposes:

    *Windows:*

    $env:FLASK_APP = 'flaskr'
    $env:FLASK_ENV = 'development'
    flask run --debug

    *Unix-like os:*

    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run --debug

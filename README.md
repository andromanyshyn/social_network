# SocialNetwork and Automated Bot

This repository contains two components: **SocialNetwork** and **Automated Bot**. Follow the instructions below to set up and run each of them.

## SocialNetwork

### Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    ```

2. Install project dependencies:

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

3. Set up a PostgreSQL database:

   Ensure you have PostgreSQL installed and create a database for the project.

### Project Initialization

4. Run database migrations:

    ```bash
    ./manage.py migrate
    ```

5. Start the project:

    ```bash
    python manage.py runserver
    ```

6. Run Celery for background tasks:

    ```bash
    celery -A socialnetwork worker --loglevel=INFO
    ```

## Automated Bot

The **Automated Bot** can be found in the "automated_bot" folder.

### Bot Setup

1. Navigate to the "automated_bot" folder:

    ```bash
    cd automated_bot
    ```

2. Start the bot:

    ```bash
    ./bot.py
    ```
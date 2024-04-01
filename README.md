# Travel Planner
This project is a web application that main focus is to plan a trip. 

Key features: authentication/authorization, CRUD for altering database – add new trip, city, traveling points, attractions/activities, start-end dates, manage all data regarding stay, like hotel, taxi/car, details regarding arrival/departure dates. Integration with google maps to add pins. Budget tracking for the trip – expenses for accommodation, transportation, food, activities. Add other users as participators of the trip. Notifications with reminders. Travel Journal – for personal notes, photos upload. User reviews and ratings of the added places. Analytics – average expenses, most visited destinations.

## Table of Contents
- [Tools](#technologies-and-frameworks)
- [Docker](#docker-compose)
- [Installation](#how-to-install-and-run-the-project)
- [API](#api)
- [Tests](#tests)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Technologies and frameworks

- Frontend 

    [![HTML](https://skillicons.dev/icons?i=html)](https://skillicons.dev)
    [![CSS](https://skillicons.dev/icons?i=css)](https://skillicons.dev)
    [![JavaScript](https://skillicons.dev/icons?i=javascript)](https://skillicons.dev)
    [![TypeScript](https://skillicons.dev/icons?i=typescript)](https://skillicons.dev)
    [![Vue](https://skillicons.dev/icons?i=vue)](https://skillicons.dev)
    [![Vuetify](https://skillicons.dev/icons?i=vuetify)](https://skillicons.dev)

- Backend
    
    [![Python](https://skillicons.dev/icons?i=python)](https://skillicons.dev) 
    [![Django](https://skillicons.dev/icons?i=django)](https://skillicons.dev)
    - Django REST Framework

- Databases

    [![SQLite3](https://skillicons.dev/icons?i=sqlite)](https://skillicons.dev)
    [![PostgreSQL](https://skillicons.dev/icons?i=postgres)](https://skillicons.dev)
    
- Other

    [![GitHub](https://skillicons.dev/icons?i=github)](https://skillicons.dev)
    [![VisualStudio](https://skillicons.dev/icons?i=vscode)](https://skillicons.dev)
    [![Docker](https://skillicons.dev/icons?i=docker)](https://skillicons.dev)
    [![Postman](https://skillicons.dev/icons?i=postman)](https://skillicons.dev)

## docker-compose
Building Docker Image
<br>
` docker-compose build --no-cache `
<br>
Running Docker Container
<br>
` docker-compose up -d `

## Installation
### Running the project locally

1. Clone the repository

    ` git clone https://github.com/Ewa-Anna/travel-planner `

#### Frontend
1. Change the directory

    ` cd frontend `

2. Install dependencies

    ` npm install `

3. Run the project

    ` npm run dev `

Project will run on http://127.0.0.1:3000/

#### Backend

1. Change the directory

    ` cd backend ` 

2. Install dependencies

    ` pip install -r requirements.txt `

3. Apply database migrations

    ` python manage.py makemigrations `

    ` python manage.py migrate `

4. Run the project

    ` python manage.py runserver `

Project will run on http://127.0.0.1:8000/

### Creating .env files
In order to have full experience, you need to rename your *.env.template* file to *.env* and fill all the environmental variables.
Please note that there are two .env files - one in main directory and other in frontend.

### PostgreSQL
For PostgreSQL, you need to download PostgreSQL https://www.postgresql.org/download/. Follow the installation guide and setup a user.

You can also run project with SQLite3, which is a lightweight and easy-to-use database, by running this command:

` python manage.py runserver --settings=settings.local `

## API
All endpoints with methods are available under http://127.0.0.1:8000/swagger/

## Tests
### Backend folder
Run tests for given app
<br>
` python manage.py test <app_name> `
<br>
or run all tests
<br>
` python manage.py test --pattern="test*.py" `

## Acknowledgments
[![100commitow](frontend/public/100commitow.png)](https://100commitow.pl/)
- [djangoproject](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Vue](https://vuejs.org/)
- [Vuetify](https://vuetifyjs.com/en/)
- [Fontawesome](https://docs.fontawesome.com/)

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

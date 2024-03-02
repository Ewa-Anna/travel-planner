# Travel Planner
This project is a web application that main focus is to plan a trip. Key features: authentication/authorization, CRUD for altering database – add new trip, city, traveling points, attractions/activities, start-end dates, manage all data regarding stay, like hotel, taxi/car, details regarding arrival/departure dates, emergency contacts. Integration with google maps to add pins. Budget tracking for the trip – expenses for accommodation, transportation, food, activities. Add other users as collaborators/participators of the trip. Notifications with reminders. Travel Journal – for personal notes, photos upload. User reviews and ratings of the added places. Analytics – average expenses, most visited destinations.

## Table of Contents
- [Tools](#technologies-and-frameworks)
- [Installation](#how-to-install-and-run-the-project)
- [Tests](#tests)
- [Docker](#docker-compose)
- [Acknowledgments](#acknowledgments)
- [License](#license)


## Technologies and frameworks
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

## How to install and run the project?
### Running the project locally
1. Clone the repository

` git clone https://github.com/Ewa-Anna/travel-planner `

2. Install dependencies

` pip install -r requirements.txt `

3. Change the directory

` cd backend `

4. Run the project

` python manage.py runserver `

Project will run on http://127.0.0.1:8000/

### Creating .env file
In order to have full experience, you need to rename your *.env.template* file to *.env* and fill all the environmental variables.

### PostgreSQL
For PostgreSQL, you need to download PostgreSQL https://www.postgresql.org/download/. Follow the installation guide and setup a user.

## Tests
Run all tests
<br>
`pytest`
<br>
Or run tests for given folder
<br>
`pytest tests/<folder_name>/`

## docker-compose
Building Docker Image
<br>
` docker-compose build `
<br>
Running Docker Container
<br>
` docker-compose up -d `

## Acknowledgments
[![100commitow](100commitow.png)](https://100commitow.pl/)
- [djangoproject](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

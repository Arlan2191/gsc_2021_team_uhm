# Google Solutions Challenge 2021: Project RiSE
## Covid-19 Vaccine Application Platform

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/Arlan2191/gsc_2021_team_uhm)

Project RiSE is a two-way online platform that aids the public and local government health agencies (LGHAs) alike in implementing the vaccination plan. If you want to test out the SMS platform or Messenger platform, please email us at avgerman1.up.edu.ph so that we can make you an official tester of the platforms we used.

## Features
- It provides a three-way vaccine application system; Website, Messenger, and SMS services (WMS),
solely built for the mass - allowing both those with and without internet access to apply
for the vaccine.
- The system asks the user for their personal information for identification and requires them to answer a questionnaire regarding their medical history for the eligibility process.
- When their application is approved by our partnered LGHA within their area, a notification message will be sent to them about the key details of their scheduled appointment.
- Additionally, RiSE provides a web application for local government health agencies - giving them an interactive interface with digital tools that eases the reviewal of vaccine applications, patient vaccination scheduling, patient tracking and profiling, and lastly, facilitating a digital clinical data repository for the needed data storage.

## Deep Dive into Project RiSE

#### User-End of Solution
- It provides a three-way vaccine application system; Website, Messenger, and SMS services (WMS), solely built for the mass - allowing both those with and without internet access to apply for the vaccine. The system first requires users to subscribe to GLOBE Labs to verify their mobile number and enable it to accept messages from RiSE. After which, they are asked for the personal information to confirm their identity, and then are prompted to answer a medical history questionnaire to be used for their eligibility profiling.
- The Website is built using Angular with a Django backend; the Messenger Chatbot is built using Google’s Dialogflow platform and is deployed using Facebook’s Developer API and; the SMS service is built using Dialogflow, Django, and the GLOBE Labs API.
- After registration, users can perform the following tasks: (1) users are automatically created an account for every application they submitted - assuming each application from their mobile number is of a different person (e.g., family member). (2) Whenever they successfully submit their application, a reference ID and a PIN number will be sent to them in order to access their user profile on either the website or mobile phone. (3) There, they can view their eligibility profile, view and confirm scheduled appointments, and see nearby vaccination sites.

#### Medical Personnel-End of Solution
- In partnering with LGHAs, RiSE requires their personnel to be registered prior to accessing the solution’s digital tools and dashboard interface. After which, they are allowed to perform the following tasks: (1) RiSE provides authorized medical practitioners (MPs) to set vaccination sessions to every added vaccination site. Whenever a session is organized, RiSE automatically notifies users with the intended priority number in their reference ID of the date, time, location, steps, and protocols to follow; (2) Additionally, RiSE automatically handles the assignment of user applications to the profiling medical practitioners. This web interface provides MPs with a display of pending-to-be-reviewed applications, a display of the filtered personal information and complete medical history of the current user application being reviewed, and a simple form for setting the user’s eligibility profile. A user’s eligibility profile includes their eligibility status, their unique reference ID if their status is either “Granted” or “Granted@Risk”, and their scheduled appointments if a matching vaccination session is set. (3) Lastly, during the scheduled vaccination session, RiSE allows registered MPs access to the Tracking Information interface which grants them access to the complete personal information and medical history of a user using their unique reference ID. It is here where MPs are required to record if the user received the vaccine, the vaccine manufacturer, vaccine serial number, and the 30-minute observation summary after the vaccine was administered. To validate the form, RiSE asks for the MP’s license number - confirming that the information provided is complete and accurate, then it is stored to the clinical data repository - enabling partner LGHAs to gain immediate feedback regarding the operations and gain the lacking data needed. 

## Tech

We used the following technologies in building Project RiSE:

- [Angular]() - for frontend.
- [Dialogflow]() - for SMS and Messenger chatbots.
- [Django]() - for backend API.
- [Globe Labs]() - for sending and receiving SMS messages.
- [Google Cloud Platform]() - for SQL and Datastore Database, App Engine Deployment (TODO).

## Installation

For the Dashboard part of RiSE, it requires [Angular]() v10+ to run.

Install the dependencies and devDependencies and start the server.

```sh
cd Dashboard_Angular
npm install
ng serve # in backend, the base url is at localhost:4200 which is default
```

For the Webform part of RiSE, it requires [Angular]() v10+ to run.

Install the dependencies and devDependencies and start the server (using terminal).

```sh
cd WebForm_Angular
npm install
ng serve --port 4201 # in backend, the base url is at localhost:4201
```

For the Backend part of RiSE, it requires [Django]() v3.7+ and Python v3.9+ to run. We advise you to use a virtual environment when installing the python modules with pip.

Install the dependencies using pip. Before running server, first install google cloud sql proxy and run the following in main directory (using terminal):

```sh
cloud_sql_proxy -credential_file="secret.json" -instances=project-bakuna:asia-southeast1:project-bakuna=tcp:<HOST>:<PORT>
```

Remember to edit the HOST and PORT parts of the command. Next, go to the directory Backend_Django and edit the following in projectBakuna/settings.py:

```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'project_bakuna',
        'USER': 'root',
        'PASSWORD': 'HgkKqfmiDEeuorHO',
        'HOST': '<HOST>',
        'PORT': '<PORT>',
        'OPTIONS': {
            'ssl': {
                'ca': 'server-ca.pem'
            }
        }
    }
}
```
Then run server (using terminal), 

```sh
cd Backend_Django
pip install -r requirements.txt
py manage.py runserver
```

If the database raises an error, run the following at Backend_Django/ (using terminal):
```sh
py manage.py makemigrations
py manage.py migrate
```

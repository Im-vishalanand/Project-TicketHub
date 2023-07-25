<h1 align="center">🎟️🎫 Ticket Hub</h1>

<p align="center">
  <b>Welcome to the "Ticket Hub Application"! This application is a robust and user-friendly platform that is used to book tickets for movies, shows, and events, providing users with the ability to book and participate in these events. Hosts can be able to add movies, shows, and events in many options. Whenever you wants to book anything like movies, shows, and events, this app has got you covered.</b>
</p>

## Project-Overview

With the "Ticket Hub Application," hosts can easily list of all movies, shows, and events with just a few clicks. Users, on the other hand, can explore and book whatever an event to enjoy their time.

Whenever you're planning to enjoy your time, the "Ticket Hub Application" provides a seamless and enjoyable experience for both hosts and guests.

### Backend Technology
The backend of the "Ticket Hub Application" is built using Python and Flask, a lightweight and powerful web framework. It leverages MongoDB, a NoSQL database, to store and manage data related to movies, shows, and events and more. The backend is responsible for handling various API endpoints that enable communication between the frontend and the database.
- Python
- Flask
- MongoDB

### Frontend Innovation
The Frontend of the "Ticket Hub Application" is developed using Vue.js, a progressive JavaScript framework for building user interfaces. It communicates with the backend through API endpoints to fetch and display data to users.
- Vue.js
- HTML
- CSS
- JavaScript

---
## Features
- **Host Login:** Hosts can login providing their credentials as email and password. This allows them to list movies, shows, and events and manage users.
- **User Login:** User can login providing their credentials as email and password. This allows them to book movies, shows, and events.

## Demo
Please click this link to see project demo <br>
https://drive.google.com/drive/folders/1pY8ZIjFV7BiwykmmZuphJIKDD0c2Gd2X?usp=sharing

<!-- ## Getting_Started
### To get started with the "Hotel Renting App", follow these steps:
**1.** Clone the repository from GitHub. <br>
**2.** Set up the backend by installing Python, Flask, and MongoDB.</br>
**3.** Open this Repository with VS code or any other IDE of your choice.</br>
**4.** Go to the ***tickethub.py*** inside this repo and run it locally.(It will start the backend server).</br>
**5.** click this to start frontend '/' </br>
**6.** Access the app through your web browser and start exploring the website for movies, shows, and events or listing same as a host!</br> -->

## Setting & Installation 

**1.** Clone the Repository

```bash
git clone https://github.com/Im-vishalanand/Project-TicketHub.git
```
**2.** Set up the backend by installing Python, Flask, and MongoDB.

### Run Locally

**3.** Go to the Project Directory

```bas
Open the Backend Folder with VS code or any other IDE of your choice
```

**4.** Go to **tickethub.py** and open the terminal and write the command **python tickethub.py**


## ER- Diagram
![ER-Diagram](https://github.com/Im-vishalanand/Project-TicketHub/assets/108060013/32022a8f-2e4c-4f80-8bb6-7955b089912e)

## URL
**For Backend**

```bash
http://localhost:5000
```

**For Frontend**

```bash
http://localhost:8080
```

## API Endpoints
In this project, here are the list of your API endpoints used with description, and examples of request/response.

- POST /admin/signup - sign up for an admin
- POST /admin/login - login for an admin

- POST /user/signup - sign up for a user
- POST /user/login - login for a user
- GET /users/all - get all user
- GET /user/<string:user_id> - get a particular user

- POST /movie/add - add a movie
- GET /movies/get - get all movies

- POST /event/add - add a event
- GET /events/get - get all events


## Author

- [Kumar Vishal Anand](https://github.com/Im-vishalanand)

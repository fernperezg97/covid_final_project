# Choro-Tracker: A Full-Stack Interactive Tracker for Global COVID-19 Data
## Description
Choro-Tracker allows a user to interact with a global COVID-19 dataset through use of a Chart.js choropleth map and line graph.
## Technologies Used
Python | Javascript | React | AJAX | Flask | SQL | HTML | CSS | Bootstrap
## YouTube Video Project Presentation
[Watch an explanation of my project on YouTube!](https://www.youtube.com/watch?v=H0DfmBLnnho&ab_channel=FernandaP%C3%A9rezGuti%C3%A9rrez)
## User Flow with GIFs
### Registration and Login
The app opens on the login page where the user can either login with an existing email and password or register a new account. If registering, the user can  input their first name, last name, email, and password, and are then redirected to the login page where they can input their newly created credentials.

The Sweet Alert package was used to create beauiful, responsive, customizable, and accessible popup boxes for displaying alerts.

![](covid_project_register_login.gif)

### Map Navigation
Once the user has logged in, the first thing they are presented with is a global COVID-19 map. The map was created using the Chart.js library where I chose to use a choropleth map to diplay total cases and total deaths. A choropleth map was most suitable given its ability to clearly display an aggregate summary (e.g. total cases, total deaths, population, etc.) of a geographic characteristic.

Choro-Tracker allows a user to interact with the map through a slider where they can choose the date and hover over each country to view its data. The slider itself uses javascript to detect a change triggered by the user. In order for the correct data to appear on the map, I query the user’s chosen date on my local database with SQLAlchemy and fetch the cases and deaths data for every country on the map. The user also has the ability to search by country and see the statistics pertaining to that particular country.

![](covid_project_map_navigation.gif)

### Country Search Functionality


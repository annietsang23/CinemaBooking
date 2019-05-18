# CinemaBooking

## Overview
This is a coursework for my python programming module at UCL. It is a GUI-based cinema booking system and technology stack used includes Python Tkinter and SQLite3. A list of dummy films running from October 2018 to January 2019 were inserted into the system.

An introduction video of the cinema booking system features is available via the link below:
https://mediacentral.ucl.ac.uk/Play/16108

The codes work with Python 3.7.

Start the system by running the file launch.py

## UI Design
Python Tkinter is used primarily to create windows, text fields, buttons, tables, drop-down boxes etc. The design resembles a real cinema booking system and cinema room setting, by using Tkinter buttons as seats.

## Functionality
My cinema booking system supports two profiles - customers and employees of the cinema. 
1. Customer profile
a. New user registration - new customers are required to fill in personal information including name, phone no., email address, username and password which are validated using regex. 
b. Login/Logout and user authentication - Existing customers are required to log in using their username and password. System will perform username and password validation. They can log out the system.
c. Manage profile - customers can update their personal information e.g. password, phone no. and email address.
d. See what's on and book - Customers can select specific dates and get a list of films available with respective screening times. They can click into the film and enter the cinema room setting, where customers can check the film description and seat availability. They can click on multiple seat(s) to reserve the seat(s).
e. Manage booking - Customers can go to 'booking history' to check their past and present bookings on a real-time basis. They can cancel the booking one day prior to screening.

2. Employee profile
a. Login and user authentication - Employees are required to log in using their username and password. System will perform username and password validation. They can log out the system.
b. Check booking status - Employees can access the same view as customers do regarding film screening times and seating availability, except that employees can also see the total no. of seats and availability figures.
c. Add a new film / screening time - Employees can add a new film or screening time for existing film. The screening schedule is updated on a real-time basis.
d. Export - Employees can export a list of films (i.e. titles), dates, times and number of booked and available seats as a text file.

## Database Design
SQLite3 is used as the database for the booking system. Below is the database schema:
- customers: firstname, lastname, email, phone, username (primary key), password
- employees:firstname, lastname, username (primary key), password
- film: title (primary key), description, screening_date (primary key), screening_time (primary key), booked_seats, available_seats, booked_seats_list 
- booking: firstname (primary key), lastname (primary key), screening_date (primary key), screening_time (primary key), title, seat


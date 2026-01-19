# Study-Tool-Python-Flask-SQLite

Revision Tracker and Planner

This application tracks revision sessions and allows users to log and plan revision sessions, with the ability to view their previous session history.


Overview:

What the app does

This web application allows users to plan their own revision session, run a timer during a session and log these completed sessions using a database.



Who it’s for

This web application is designed for anyone who wishes to track and manage their revision sessions. It is particularly useful for:
- Students who are revising for exams and in-class tests
- Anyone who wishes to monitor educational progress and maintain a consistent learning routine

Users of this app can easily add and view their study sessions, as well as track their hours spent revising certain topics, allowing users to stay organised and driven with their learning.


Motivation

I built this application to use it myself. It will help me plan my study sessions for each of my modules effectively and will allow me to see what timings I have allocated to each of my modules so that I can plan in accordance with what tests/ coursework I have coming up. I feel this is a useful application to produce for myself but also for my friends and family, who also struggle to plan their study sessions. I also wanted to expand my Python knowledge and database skills, so by implementing Flask and SQLite in this project, I am able to fulfil these goals.

Features:
- Plan future revision sessions
- View previous revision sessions
- Run a timer during revision sessions
- Log completed revision sessions
- View statistics from study sessions during that week
- Receive pop-ups notifying users of overdue planned sessions


Tech stack
- Python
- Flask
- Matplotlib
- SQLite
- HTML / CSS
- JavaScript

How it works 
This project makes use of Flask to handle user requests and route these requests to the appropriate functions. SQLite is used to store completed revision sessions and planned ones. I have used HTML and CSS to display the frontend, with some JavaScript used to aid in the display of the revision session progress bar. Form submissions from the HTML are processed by the Flask routes and use SQLite to save the appropriate data in the correct tables of the database.  


Challenges and Learning
For this project to work, I had to learn quite a few new skills. Firstly, I have never used virtual environments and Flask, so that was quite a steep learning curve for me. However, I have now gained quite an insight into Flaskfrom reading it's documentation and feel confident with the frameworks it provides. It was quite fun to experiment with Flask and very rewarding when testing the code and discovering my functionalities worked! I also have minimal experience with HTML forms and JavaScript, so the displaying of the progress bar proved to be quite a difficult step in the programming process, taking nearly 2 days to finally work. It was quite a challenge for me to use Jinja templates, as it was something I had actually never heard of before, but I have now got the hang of using them in this project. 

Future improvements
In the future, there are quite a few additional functionalities I could include in this project. Firstly, I could make a visual timer, showing the minutes/seconds ticking down on the screen for the user. I could also implement user accounts and authentication, which would allow multiple users and boost security. I could also introduce an exporting system, where users can send their database or bar chart of study sessions to other applications or to other users.

Setup instructions
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install any required libraries.
4. Run application locally.
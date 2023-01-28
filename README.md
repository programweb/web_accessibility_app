# Web Accessibility App
Using: Docker MongoDB NoSQL Python Flask Node PostgreSQL JavaScript jQuery npm HTML_CodeSniffer Pa11y


Directory I built with Dockerfile, docker-compose.yml, Python files, Flask files (in templates directory), CSS/JS/Images go in the static directory.
![Screen Shot 2023-01-27 at 2 59 21 PM](https://user-images.githubusercontent.com/12736699/215224177-7c9d423b-bae3-40a0-bf5e-dacdc9a813d2.png)


These are the Flask template files for front-end code which is neatly separated from the Python.  
<img width="210" alt="Screen Shot 2023-01-27 at 3 06 43 PM" src="https://user-images.githubusercontent.com/12736699/215224178-8f161adf-56ef-4b0e-b17d-726893715236.png">


A Node.js with a NoSQL Database (MongoDB) app running in a Docker Container.  The Pa11y app uses both MongoDB and Node.js.
![Screen Shot 2023-01-27 at 1 40 06 PM](https://user-images.githubusercontent.com/12736699/215224147-790787c4-0f76-472a-961d-4ac896232aa0.png)



Start the PostgreSQL Database (I use a terminal window)



I wrote a Python/Flask app that ties together a NoSQL and Relational Database.
Start a Python/Flask Web application which does CRUD operations on both the MongoDB and PostgreSQL Databases.
![Screen Shot 2023-01-27 at 2 24 21 PM](https://user-images.githubusercontent.com/12736699/215224153-f7130d42-3b59-4915-8979-e33a9a0c8c66.png)



the code in localhost-5k.py is available [in this repo here](localhost-5k.py)





Limiting an examination to 20 rows in the task database table using the phAdmin Database Management Tool for PostgreSQL
![Screen Shot 2023-01-27 at 2 22 33 PM](https://user-images.githubusercontent.com/12736699/215224148-0ef88124-fb44-4d9b-82c2-75ce88eda7e4.png)


Here is the homepage of the app with links to many operations
<img width="1411" alt="Screen Shot 2023-01-27 at 2 25 58 PM" src="https://user-images.githubusercontent.com/12736699/215224157-64d008e8-a12e-4e35-958b-2b421033fa53.png">

Task Configuration through the UI  (page under construction)
<img width="1335" alt="Screen Shot 2023-01-27 at 2 35 50 PM" src="https://user-images.githubusercontent.com/12736699/215224160-5d2c59d4-16a0-4185-b105-1c33067c622d.png">


Add Tasks through the UI. A task is a URL to evaluate for Web Accessibility.
<img width="1338" alt="Screen Shot 2023-01-27 at 2 37 23 PM" src="https://user-images.githubusercontent.com/12736699/215224161-d2b69945-fbac-42ce-8208-a21788d10822.png">

Add Tasks through the UI continued (just to show you there are over 3000 tasks)
<img width="665" alt="Screen Shot 2023-01-27 at 2 37 46 PM" src="https://user-images.githubusercontent.com/12736699/215224163-2e513b24-1d61-4a0f-90a9-efc3e8878bc0.png">

Drag-n-Drop Sorting of task order
<img width="1311" alt="Screen Shot 2023-01-27 at 2 38 29 PM" src="https://user-images.githubusercontent.com/12736699/215224166-e4cf8200-a6ff-4883-8046-b83e90fd3770.png">

Show all tests page where any saved (saved to the PostgreSQL database) notes and solutions are displayed.
<img width="1287" alt="Screen Shot 2023-01-27 at 2 39 08 PM" src="https://user-images.githubusercontent.com/12736699/215224170-9422506d-843e-4f07-a673-b42b19e63eb3.png">


Tabulated (3 tabs), Paginated, column order-able, test results for one URL which had 58 errors, 19 warnings and 212 notices.   The results are also searchable. Data pulled from the NoSQL MongoDB Database.
<img width="1377" alt="Screen Shot 2023-01-27 at 2 40 27 PM" src="https://user-images.githubusercontent.com/12736699/215224173-3384b1bf-65a7-41db-8e04-84122eb79300.png">


Clicking an error in the sortable table above displays more detailed information about the error and notes/solutions you saved earlier.   Even if it is a brand new test, you see your notes and custom solutions for matching error codes.
<img width="1380" alt="Screen Shot 2023-01-27 at 2 40 39 PM" src="https://user-images.githubusercontent.com/12736699/215224175-59e8b915-08fd-4f3b-9d1b-629e66b792fc.png">


Edit notes (saves to PostGreSQL database)
<img width="1315" alt="Screen Shot 2023-01-27 at 2 39 36 PM" src="https://user-images.githubusercontent.com/12736699/215224172-79baf5b7-982c-4e0c-a394-867dc73c0961.png">


**Docker** - a way to package a whole system (servers, database, code, etc. in container(s) 

**MongoDB** - probably the most famous NoSQL database.

**NoSQL** - a type of database that is not so heavily relational

**Python** - main server-side code that I wrote in for this project

**Flask** - templating code to allow Python to serve web services or web pages.  In this app, I am using it mostly for the web pages.

**Node** - aka node.js; a fast, server-side JavaScript language.

**PostgreSQL** - open-source relational database

**JavaScript** - I use it for client-side scripting yet it is also a part of node.js and mongodb

**jQuery** - a well-documented JavaScript Library that hides the complexity of dealing with various browsers and browser versions from JavaScript; plus, it has a lot of nice out-of-the box features.  I use it in this app for these things 

**npm** - the Node Package Manager, the world's largest software registry

**HTML_CodeSniffer** - an application that Pa11y wraps/uses

**Pa11y** - the application my application wraps/uses



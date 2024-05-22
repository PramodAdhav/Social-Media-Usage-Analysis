# Overview

This project aims to analyze social media usage statistics based on survey data. The project collects responses from participants regarding their social media usage habits and preferences. The collected data is then processed and visualized in the form of graphs to provide insights into social media usage trends.

# Technologies Used

* Frontend: HTML, CSS & Bootstrap.
* Backend: Flask.
* Database Connection: PyODBC
* Visualization: Matplotlib, Seaborn, Pyplot.
* Database: Microsoft SQL Server.
* Additional Libraries: Pandas.

# Installation

1. Clone the repository:
```
git clone https://github.com/PramodAdhav/Social-Media-Usage-Analysis.git
```

2. Open the Project folder in Visual Studio Code (or any preferred IDE)

3. Installing necessary libraries:
Open the terminal and enter the following line
```
pip install flask pyodbc pandas matplotlib seaborn
```

4. Setting up the Database:
If you wish to reproduce the project with the same database setup, follow these steps:

Install MSSQL:
Download and install Microsoft SQL Server(SQL EXPRESS Edition is used for this project) from the official website.
Also install SSMS(SQL SERVER MANAGEMENT STUDIO) for managing database infrastructure.
Make sure the Authentication is set to "Window Authentication" and Hit Connect.

Click on 'New Query' and write a query to create a new database 'SM':
```
CREATE DATABASE SM;
```
Put the database to use:
```
USE SM;
```

Now, Add tables into the database ```SM```.
Go to databases in the Object Explorer and right-click on the database 'SM'.
Go to ```Tasks and select ```Import Flat File```. Go to the CSV file's location and choose the files one by one.
Make sure that the table name is same as the file name(without the .csv extension)
Refer the below images and change the datatypes accordingly:

TABLE 1 - 'DETAILS'
![image](https://github.com/PramodAdhav/Social-Media-Usage-Analysis/assets/125786411/013cd68f-b8b9-4eb9-9a4a-64d78b6b313f)

TABLE 2 - 'EMOTIONS'
![image](https://github.com/PramodAdhav/Social-Media-Usage-Analysis/assets/125786411/1cf945ec-4c3c-4e13-812e-02fadf8c9ba5)

TABLE 3 - 'SOCIAL_MEDIA'
![image](https://github.com/PramodAdhav/Social-Media-Usage-Analysis/assets/125786411/6df997e6-dd9e-40ee-99ae-3d4d16db83ac)

TABLE 4 - 'STATS'
![image](https://github.com/PramodAdhav/Social-Media-Usage-Analysis/assets/125786411/604f5d6f-769c-4c84-b297-915c6314cc98)

After adding all the tables into the database, open ```Visualization.py``` file and modify the Connection String to local database's 
server connection string.

# Execution

Run the ```Visualization.py``` file and ctrl+click on ```http://127.0.0.1:5000``` to start the Flask application.



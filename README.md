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
Clone the repository:

```git clone https://github.com/PramodAdhav/Social-Media-Usage-Analysis.git```

Open the Project folder in Visual Studio Code (or any preferred IDE)

Installing necessary libraries: 
Open the terminal and enter the following line

```pip install flask pyodbc pandas matplotlib seaborn```

# Setting up the Database 

If you wish to reproduce the project with the same database setup, follow these steps:
Install MSSQL: Download and install Microsoft SQL Server(SQL EXPRESS Edition is used for this project) from the official website. Also install SSMS(SQL SERVER MANAGEMENT STUDIO) for managing database infrastructure. Make sure the Authentication is set to "Window Authentication" and Hit Connect.

Click on 'New Query' and write a query to create a new database 'SM':

```CREATE DATABASE SM;```

Put the database to use:
```USE SM;```

Now, Add tables into the database SM. Go to databases in the Object Explorer and right-click on the database 'SM'. 
Go to ```Tasks``` and select ```Import Flat File```. Go to the CSV file's location and choose the files one by one. 
Make sure that the table name is same as the file name(without the .csv extension) 
Refer the below images and change the datatypes accordingly:

TABLE 1 - 'DETAILS' image
![DETAILS](https://github.com/PramodAdhav/Social-Media-Usage-Analysis/assets/125786411/d724f5ca-9d57-42fa-9b1f-a76e28098bd4)

TABLE 2 - 'EMOTIONS' 
![EMOTIONS](https://github.com/PramodAdhav/Social-Media-Usage-Analysis/assets/125786411/f47fa54d-24ed-4e83-980f-41456699cd78)

TABLE 3 - 'SOCIAL_MEDIA' image
![SOCIAL_MEDIA](https://github.com/PramodAdhav/Social-Media-Usage-Analysis/assets/125786411/c958bc22-8c8f-46fd-8e39-e091b15313de)

TABLE 4 - 'STATS' image
![STATS](https://github.com/PramodAdhav/Social-Media-Usage-Analysis/assets/125786411/20e98019-2615-4155-b4de-4c430e85375e)

After adding all the tables into the database, open ```Visualization.py``` file and modify the Connection String to the system's local database server connection string.

# Execution
Run the ```Visualization.py``` file and ctrl+click on ```http://127.0.0.1:5000``` to start the Flask application.

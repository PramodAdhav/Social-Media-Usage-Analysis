import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template
import seaborn as sns



app = Flask(__name__)

# Function to create the database "SM" if it doesn't exist
def create_database():
    cnxn_master = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=master;Trusted_Connection=yes;')
    cursor_master = cnxn_master.cursor()

    # Check if the database exists
    cursor_master.execute("SELECT COUNT(*) FROM sys.databases WHERE name = 'SM'")
    if cursor_master.fetchone()[0] == 0:
        cursor_master.execute("CREATE DATABASE SM;")

    cnxn_master.commit()
    cnxn_master.close()

# Function to create tables in the database
def create_tables():
    cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=SM;Trusted_Connection=yes;')
    cursor = cnxn.cursor()

    # Check if tables exist
    cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('DETAILS', 'EMOTIONS', 'SOCIAL_MEDIA', 'STATS')")
    tables_exist = cursor.fetchall()

    # If tables exist, skip table creation
    if tables_exist:
        print("Tables already exist. Skipping table creation.")
        cnxn.close()
        return

    # Create DETAILS table
    cursor.execute('''
        CREATE TABLE DETAILS (
            ID BIGINT PRIMARY KEY,
            E_ID NCHAR(10),
            NAME NCHAR(100),
            EMAIL_ADDRESS NCHAR(100),
            GENDER NCHAR(10),
            AGE TINYINT
        )
    ''')

    # Create SOCIAL_MEDIA table
    cursor.execute('''
        CREATE TABLE SOCIAL_MEDIA (
            ID BIGINT,
            SM_ID NCHAR(10) PRIMARY KEY,
            MOST_USED NCHAR(100),
            AVG_TIME_SPENT NCHAR(10),
            TIME_OF_DAY NCHAR(100),
            FREQUENCY NCHAR(100),
            POSTING_FREQUENCY NCHAR(100)
        )
    ''')

    # Create EMOTIONS table
    cursor.execute('''
        CREATE TABLE EMOTIONS (
            E_ID NCHAR(10) PRIMARY KEY,
            SM_ID NCHAR(10),
            PRESSURE_TO_PRESENT NVARCHAR(MAX),
            NEW_INTERACTIONS NCHAR(100),
            GROWTH_DEVELOPMENT SMALLINT,
            TRENDS NVARCHAR(MAX)
        )
    ''')

    # Create STATS table
    cursor.execute('''
        CREATE TABLE STATS (
            E_ID NCHAR(10),
            SM_ID NCHAR(10),
            PRIMARY_USE NVARCHAR(MAX),
            IMPORTANCE TINYINT,
            STRESS NCHAR(100),
            CONTROLLING_ABILITY TINYINT,
            ADDICTION_SCORE NCHAR(100),
            SLEEP_AFFECT TINYINT
        )
    ''')

    cnxn.commit()
    cnxn.close()

# Function to insert data into the database
def insert_data():
    cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=SM;Trusted_Connection=yes;')
    cursor = cnxn.cursor()

    # Check if tables exist
    cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('DETAILS', 'EMOTIONS', 'SOCIAL_MEDIA', 'STATS')")
    tables_exist = cursor.fetchall()

    # If tables exist, skip data insertion
    if tables_exist:
        print("Tables already exist. Skipping data insertion.")
        cnxn.close()
        return

    # Insert data into DETAILS table
    details_data = pd.read_csv(r'C:\Users\Pramod Adhav\Documents\GitHub\Social-Media-Usage-Analysis\csv\DETAILS.csv')
    details_data.to_sql('DETAILS', cnxn, if_exists='append', index=False)

    # Insert data into EMOTIONS table
    emotions_data = pd.read_csv(r'C:\Users\Pramod Adhav\Documents\GitHub\Social-Media-Usage-Analysis\csv\EMOTIONS.csv')
    emotions_data.to_sql('EMOTIONS', cnxn, if_exists='append', index=False)

    # Insert data into SOCIAL_MEDIA table
    social_media_data = pd.read_csv(r'C:\Users\Pramod Adhav\Documents\GitHub\Social-Media-Usage-Analysis\csv\SOCIAL_MEDIA.csv')
    social_media_data.to_sql('SOCIAL_MEDIA', cnxn, if_exists='append', index=False)

    # Insert data into STATS table
    stats_data = pd.read_csv(r'C:\Users\Pramod Adhav\Documents\GitHub\Social-Media-Usage-Analysis\csv\STATS.csv')
    stats_data.to_sql('STATS', cnxn, if_exists='append', index=False)

    cnxn.close()

@app.route('/')
def index():
    # Insert data into the database
    insert_data()

    cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=SM;Trusted_Connection=yes;')
    cursor = cnxn.cursor()

    #############  QUERY-1 ###############
    ##### Visualize the distribution of gender among respondents using a pie chart. ###
    query1 = "SELECT GENDER, COUNT(*) AS gender_count FROM DETAILS GROUP BY GENDER"
    df1 = pd.read_sql_query(query1, cnxn)

    plt.figure(figsize=(4, 4))
    plt.pie(df1['gender_count'], labels=df1['GENDER'], autopct='%1.1f%%', startangle=140)
    plt.tight_layout()
    Viz1 = 'static/Gender_Distribution.png'
    plt.savefig(Viz1)
    plt.close()

#############  QUERY-2 ###############
    ### Explore the distribution of ages among respondents using a violin plot. ###
    query2 = "SELECT AGE FROM DETAILS"
    df2 = pd.read_sql_query(query2, cnxn)

    plt.figure(figsize=(7, 4))
    sns.violinplot(data=df2, x='AGE')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.tight_layout()
    Viz2 = 'static/Age_Distribution.png'
    plt.savefig(Viz2)
    plt.close()

#############  QUERY-3 ###############
    ### Plot the most used social media platforms using a horizontal bar plot for a different perspective. ###
    query3 = """SELECT MOST_USED, COUNT(*) AS platform_count
    FROM SOCIAL_MEDIA GROUP BY MOST_USED
    """
    df3 = pd.read_sql_query(query3, cnxn)

    plt.figure(figsize=(5, 3))
    plt.barh(df3['MOST_USED'], df3['platform_count'],color = '#8856a7')
    plt.xlabel('Number of Respondents')
    plt.ylabel('Social Media Platform')
    plt.tight_layout()
    Viz3 = 'static/Most_Used_SMP.png'
    plt.savefig(Viz3)
    plt.close()



#############  QUERY-4 ###############
    ### Create a stacked bar plot to show the 
    ### distribution of time of day usage across different social media platforms.
    query4 = """
                SELECT MOST_USED, 
                    SUM(CASE WHEN TIME_OF_DAY = 'Morning (6:00 AM - 12:00 PM)' THEN 1 ELSE 0 END) AS Morning,
                    SUM(CASE WHEN TIME_OF_DAY = 'Afternoon (12:00 PM - 6:00 PM)' THEN 1 ELSE 0 END) AS Afternoon,
                    SUM(CASE WHEN TIME_OF_DAY = 'Evening (6:00 PM - 12:00 AM)' THEN 1 ELSE 0 END) AS Evening,
                    SUM(CASE WHEN TIME_OF_DAY = 'Late Night (12:00 AM - 6:00 AM)' THEN 1 ELSE 0 END) AS LateNight
                FROM SOCIAL_MEDIA
                GROUP BY MOST_USED
                """
    df4 = pd.read_sql_query(query4, cnxn)

    plt.figure(figsize=(10, 6))
    plt.bar(df4['MOST_USED'], df4['Morning'], label='Morning')
    plt.bar(df4['MOST_USED'], df4['Afternoon'], bottom=df4['Morning'], label='Afternoon')
    plt.bar(df4['MOST_USED'], df4['Evening'], bottom=df4['Morning'] + df4['Afternoon'], label='Evening')
    plt.bar(df4['MOST_USED'], df4['LateNight'], bottom=df4['Morning'] + df4['Afternoon'] + df4['Evening'], label='LateNight')
    plt.xlabel('Social Media Platform')
    plt.ylabel('Number of Respondents')
    plt.legend()
    plt.tight_layout()
    Viz4 = 'static/SM_TimeSpent.png'
    plt.savefig(Viz4)
    plt.close()

#############  QUERY-5 ###############
    ### Explore the frequency distribution of social media usage per day using a histogram. ###
    query5 = "SELECT FREQUENCY FROM SOCIAL_MEDIA"
    df5 = pd.read_sql_query(query5, cnxn)

    plt.figure(figsize=(7, 4))
    plt.hist(df5['FREQUENCY'], bins=10, edgecolor='black')
    plt.xlabel('Frequency')
    plt.ylabel('Number of Respondents')
    plt.tight_layout()
    Viz5 = 'static/Frequency.png'
    plt.savefig(Viz5)
    plt.close()

#############  QUERY-6 ###############
    ### Create a clustered bar plot to compare the primary use of social media by gender. ###
    query6 = """
                SELECT Gender, 
        SUM(CASE WHEN [PRIMARY_USE] = 'Staying connected with friends and family' THEN 1 ELSE 0 END) AS Staying_connected,
        SUM(CASE WHEN [PRIMARY_USE] = 'Sharing photos or videos' THEN 1 ELSE 0 END) AS Sharing_photos_videos,
        SUM(CASE WHEN [PRIMARY_USE] = 'Keeping up with news and current events' THEN 1 ELSE 0 END) AS Keeping_up_with_news,
        SUM(CASE WHEN [PRIMARY_USE] = 'Networking with professionals or colleagues' THEN 1 ELSE 0 END) AS Networking_with_professionals,
        SUM(CASE WHEN [PRIMARY_USE] = 'Messaging or chatting with others' THEN 1 ELSE 0 END) AS Messaging_chatting,
        SUM(CASE WHEN [PRIMARY_USE] = 'Discovering new content or entertainment' THEN 1 ELSE 0 END) AS Discovering_new_content
    FROM SOCIAL_MEDIA
    INNER JOIN STATS ON LTRIM(RTRIM(SOCIAL_MEDIA.SM_ID)) = LTRIM(RTRIM(STATS.SM_ID))
    INNER JOIN DETAILS ON LTRIM(RTRIM(SOCIAL_MEDIA.ID)) = LTRIM(RTRIM(DETAILS.ID))
    GROUP BY Gender
                """
    df6 = pd.read_sql_query(query6, cnxn)

    plt.figure(figsize=(6, 4))
    sns.barplot(data=df6, x='Gender', y='Staying_connected', color='skyblue', label='Staying connected')
    sns.barplot(data=df6, x='Gender', y='Sharing_photos_videos', color='orange', label='Sharing photos/videos', bottom=df6['Staying_connected'])
    sns.barplot(data=df6, x='Gender', y='Keeping_up_with_news', color='green', label='Keeping up with news', bottom=df6['Staying_connected'] + df6['Sharing_photos_videos'])
    sns.barplot(data=df6, x='Gender', y='Networking_with_professionals', color='red', label='Networking', bottom=df6['Staying_connected'] + df6['Sharing_photos_videos'] + df6['Keeping_up_with_news'])
    sns.barplot(data=df6, x='Gender', y='Messaging_chatting', color='purple', label='Messaging/chatting', bottom=df6['Staying_connected'] + df6['Sharing_photos_videos'] + df6['Keeping_up_with_news'] + df6['Networking_with_professionals'])
    sns.barplot(data=df6, x='Gender', y='Discovering_new_content', color='yellow', label='Discovering content', bottom=df6['Staying_connected'] + df6['Sharing_photos_videos'] + df6['Keeping_up_with_news'] + df6['Networking_with_professionals'] + df6['Messaging_chatting'])
    plt.xlabel('Gender')
    plt.ylabel('Number of Respondents')
    plt.legend()
    plt.tight_layout()
    Viz6 = 'static/Primary_Use_Gender.png'
    plt.savefig(Viz6)
    plt.close()


#############  QUERY-7 ###############
    ### Visualize the distribution of responses regarding the importance of social media 
    ### in daily life using a line plot. ###
    query7 = "SELECT IMPORTANCE FROM STATS"
    df7 = pd.read_sql_query(query7, cnxn)

    plt.figure(figsize=(12, 4))
    df7['IMPORTANCE'].value_counts().sort_index().plot(marker='o', color = 'violet')
    plt.xlabel('Importance Level')
    plt.ylabel('Number of Respondents')
    plt.grid(True)
    plt.tight_layout()
    Viz7 = 'static/Importance.png'
    plt.savefig(Viz7)
    plt.close()

    #############  QUERY-8 ###############
        ### Explore the relationship between age and confidence in 
        ### controlling social media usage using a scatter plot.
    query8 = """
                SELECT AGE, CONTROLLING_ABILITY
                FROM DETAILS
                INNER JOIN STATS ON DETAILS.E_ID = STATS.E_ID
                """
    df8 = pd.read_sql_query(query8, cnxn)

    plt.figure(figsize=(12, 4))
    plt.scatter(df8['AGE'], df8['CONTROLLING_ABILITY'], alpha=0.5, color = 'green')
    plt.xlabel('Age')
    plt.ylabel('Confidence in Controlling Usage')
    plt.grid(True)
    plt.tight_layout()
    Viz8 = 'static/Age_Confidence.png'
    plt.savefig(Viz8)
    plt.close()

#############  QUERY-9 ###############
    ### Create a grouped box plot to compare the sleep impact 
    ### due to social media between different genders.
    query9 = """
                SELECT GENDER, SLEEP_AFFECT
                FROM DETAILS
                INNER JOIN STATS ON DETAILS.E_ID = STATS.E_ID
                """
    df9 = pd.read_sql_query(query9, cnxn)

    plt.figure(figsize=(5, 3))
    sns.boxplot(x='GENDER', y='SLEEP_AFFECT', data=df9, palette='pastel')
    plt.xlabel('Gender')
    plt.ylabel('Sleep Impact')
    plt.grid(True)
    plt.tight_layout()
    Viz9 = 'static/Sleep_Gender.png'
    plt.savefig(Viz9)
    plt.close()



#############  QUERY-10 ###############
    ### Use a pair plot to visualize pairwise relationships between 
    ### different variables, such as age, time spent on social media, and sleep impact.
    query10 = """
                SELECT Age, Avg_time_spent, Sleep_Affect
                FROM SOCIAL_MEDIA
                INNER JOIN STATS ON SOCIAL_MEDIA.SM_ID = STATS.SM_ID
                INNER JOIN DETAILS ON DETAILS.ID = SOCIAL_MEDIA.ID
                INNER JOIN EMOTIONS ON SOCIAL_MEDIA.SM_ID = EMOTIONS.SM_ID
                """
    df10 = pd.read_sql_query(query10, cnxn)

    sns.set_theme(style="ticks")
    sns.pairplot(df10, palette='husl')
    plt.title('Pairwise Relationships')
    plt.tight_layout()
    Viz10 = 'static/Age_Time_Sleep.png'
    plt.savefig(Viz10)
    plt.close()

#############  QUERY-11 ###############
    ### Compare the frequency of content posting 
    ### across different social media platforms using a clustered bar plot.
    query11 = """
                SELECT SM.MOST_USED, SM.POSTING_FREQUENCY
                FROM SOCIAL_MEDIA SM ORDER BY ID
                """
    df11 = pd.read_sql_query(query11, cnxn)
    plt.figure(figsize=(8, 5))
    sns.barplot(x='MOST_USED', y='POSTING_FREQUENCY', data=df11, ci=None)
    plt.xlabel('Social Media Platform')
    plt.ylabel('Frequency of Content Posting')
    plt.xticks(rotation=45)  # Rotate x-axis labels by 45 degrees for better readability
    plt.tight_layout()
    Viz11 = 'static/Post_Frequency.png'
    plt.savefig(Viz11)
    plt.close()


#############  QUERY-12 ###############
    ### Create a grouped bar plot to compare the pressure to present 
    ### a certain image on social media between different age groups.
    query12 = """
                SELECT AGE, PRESSURE_TO_PRESENT
                FROM DETAILS
                INNER JOIN EMOTIONS ON DETAILS.E_ID = EMOTIONS.E_ID ORDER BY ID
                """
    df12 = pd.read_sql_query(query12, cnxn)
    custom_labels = ['Not Sure', 'Comfortable\n being genuine', 'Sometimes/\nDepends', 'Feel pressured\nto present']

    plt.figure(figsize=(4, 6))  # Increase the figure size
    sns.barplot(x='PRESSURE_TO_PRESENT', y='AGE', data=df12, errorbar=None, palette = 'magma')
    plt.xlabel('Pressure to Present Image')
    plt.ylabel('No of Respondants')
    plt.xticks(ticks=range(len(custom_labels)), labels=custom_labels, rotation=45)  # Set custom x-axis labels
    plt.tight_layout()
    Viz12 = 'static/pressure_present.png'
    plt.savefig(Viz12)
    plt.close()

#############  QUERY-13 ###############
    ### Visualize the frequency of interacting with new people 
    ### on social media by platform using a stacked bar plot.
    query13 = """
                SELECT SM.MOST_USED, E.NEW_INTERACTIONS
                FROM SOCIAL_MEDIA SM
                INNER JOIN STATS S ON SM.SM_ID = S.SM_ID
                INNER JOIN EMOTIONS E ON S.E_ID = E.E_ID ORDER BY ID
                """
    df13 = pd.read_sql_query(query13, cnxn)
    cnxn.close()
    df_pivot = df13.pivot_table(index='MOST_USED', columns='NEW_INTERACTIONS', aggfunc='size', fill_value=0)
    plt.figure(figsize=(5, 3))
    df_pivot.plot(kind='bar', stacked=True)
    plt.xlabel('Social Media Platform')
    plt.ylabel('Frequency of Interaction')
    plt.tight_layout()
    Viz13 = 'static/New_Interactions.png'
    plt.savefig(Viz13)
    plt.close()
    return render_template('index.html', Viz1 = 'static/Gender_Distribution.png', 
                           Viz2 = 'static/Age_Distribution.png',
                           Viz3 = 'static/Most_Used_SMP.png',
                           Viz4 = 'static/SM_TimeSpent.png',
                           Viz5 = 'static/Frequency.png',
                           Viz6 = 'static/Primary_Use_Gender.png',
                           Viz7 = 'static/Importance.png',
                           Viz8 = 'static/Age_Confidence.png',
                           Viz9 = 'static/Sleep_Gender.png',
                           Viz10 = 'static/Age_Time_Sleep.png',
                           Viz11 = 'static/Post_Frequency.png',
                           Viz12 = 'static/pressure_present.png',
                           Viz13 = 'static/New_Interactions.png',
                           )

if __name__ == '__main__':
    app.run(debug=True)



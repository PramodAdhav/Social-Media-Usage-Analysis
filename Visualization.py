import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template
import seaborn as sns



app = Flask(__name__)

@app.route('/')
def index():

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
    ### Create a grouped bar plot to compare the pressure to present 
    ### a certain image on social media between different age groups.
    query10 = """
                SELECT AGE, PRESSURE_TO_PRESENT
                FROM DETAILS
                INNER JOIN EMOTIONS ON DETAILS.E_ID = EMOTIONS.E_ID ORDER BY ID
                """
    df10 = pd.read_sql_query(query10, cnxn)
    custom_labels = ['Not Sure', 'Comfortable\n being genuine', 'Sometimes/\nDepends', 'Feel pressured\nto present']

    plt.figure(figsize=(4, 6))  
    sns.barplot(x='PRESSURE_TO_PRESENT', y='AGE', data=df10, errorbar=None, palette = 'magma')
    plt.xlabel('Pressure to Present Image')
    plt.ylabel('No of Respondants')
    plt.xticks(ticks=range(len(custom_labels)), labels=custom_labels, rotation=45)  
    plt.tight_layout()
    Viz10 = 'static/pressure_present.png'
    plt.savefig(Viz10)
    plt.close()

#############  QUERY-11 ###############
    ### Visualize the frequency of interacting with new people 
    ### on social media by platform using a stacked bar plot.
    query11 = """
                SELECT SM.MOST_USED, E.NEW_INTERACTIONS
                FROM SOCIAL_MEDIA SM
                INNER JOIN STATS S ON SM.SM_ID = S.SM_ID
                INNER JOIN EMOTIONS E ON S.E_ID = E.E_ID ORDER BY ID
                """
    df11 = pd.read_sql_query(query11, cnxn)
    cnxn.close()
    df_pivot = df11.pivot_table(index='MOST_USED', columns='NEW_INTERACTIONS', aggfunc='size', fill_value=0)
    plt.figure(figsize=(5, 3))
    df_pivot.plot(kind='bar', stacked=True)
    plt.xlabel('Social Media Platform')
    plt.ylabel('Frequency of Interaction')
    plt.tight_layout()
    Viz11 = 'static/New_Interactions.png'
    plt.savefig(Viz11)
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
                           Viz10 = 'static/pressure_present.png',
                           Viz11 = 'static/New_Interactions.png',
                           )

if __name__ == '__main__':
    app.run(debug=True)



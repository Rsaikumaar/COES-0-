import pandas as pd
import sqlite3

# Read the Excel file
def upload():
    df = pd.read_csv('myquestion.csv')
    # Connect to the database
    conn = sqlite3.connect('F:/#project/instance/coes.db')
    cursor = conn.cursor()
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract the data from the row
        column1_data = row['subject']
        column2_data = row['question']
        column3_data = row['opt1']
        column4_data = row['opt2']
        column5_data = row['opt3']
        column6_data = row['opt4']
        column7_data = row['main']
        # Store the data in a temporary list
        temp_list = [column1_data,column2_data,column3_data,column4_data,column5_data,column6_data,column7_data]
        # Store the data in the database
        cursor.execute("INSERT INTO Question (subject,question,opt1,opt2,opt3,opt4,main ) VALUES (?,?,?,?,?,?,?)",(column1_data,column2_data,column3_data,column4_data,column5_data,column6_data,column7_data))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
upload()
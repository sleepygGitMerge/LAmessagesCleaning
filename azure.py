import pyodbc
import pandas as pd
import json

# Load the JSON data
with open('posted_messages.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert JSON to DataFrame
messages = pd.DataFrame(data['messages'])

server = 'larche.database.windows.net'
database = 'larche_search'
username = 'adminlarche'
password = '{F%4mbSQx53iX}'
driver= '{ODBC Driver 18 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        # Create main messages table if not exists
        create_messages_table = '''
            CREATE TABLE IF NOT EXISTS messages (
                id INT PRIMARY KEY,
                subject VARCHAR(255),
                author VARCHAR(255),
                date DATE,
                content TEXT
            );'''
        cursor.execute(create_messages_table)

        # Create categories table if not exists
        create_categories_table = '''
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message_id INT,
                category_name VARCHAR(255),
                FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
            );'''
        cursor.execute(create_categories_table)

        # Insert data into messages table
        for index, row in messages.iterrows():
            insert_message_query = '''
                INSERT INTO messages (id, subject, author, date, content)
                VALUES (%s, %s, %s, STR_TO_DATE(%s, '%d.%m.%Y'), %s)
                ON DUPLICATE KEY UPDATE
                    subject = VALUES(subject),
                    author = VALUES(author),
                    date = VALUES(date),
                    content = VALUES(content);
                '''
            cursor.execute(insert_message_query, (
                row['id'],
                row['subject'],
                row['author'],
                row['date'],
                row['content']
            ))

            # Insert categories into categories table
            for category in row['category']:
                insert_category_query = '''
                    INSERT INTO categories (message_id, category_name)
                    VALUES (%s, %s)
                    '''
                cursor.execute(insert_category_query, (
                    row['id'],
                    category
                ))
    #conn.commit()
    cursor.close()
    conn.close()
    print("MySQL connection is closed.")
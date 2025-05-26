import mysql.connector


try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Mar10ram',
        database='larche'
    )
    ###########
    cursor = connection.cursor(dictionary=True)
    '''query = "select distinct category_name from categories "
    condition = []
    ids = [1,2,3,4]
    if ids:
        ids_conditions = [f"message_id={id}" for id in ids]
    condition.append(f"({' OR '.join(ids_conditions)})")
    if condition:
        query += "WHERE" + " AND ".join(condition)'''
    msg_id = 116
    cursor.execute('select distinct category_name from categories where message_id=%d' % msg_id)
    result = cursor.fetchall()
    #for row in result:

    cursor.close()
    connection.close()
    ###################
except mysql.connector.Error as err:
    print(err)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
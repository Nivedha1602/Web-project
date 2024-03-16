import mysql.connector
dataBase= mysql.connector.connect(
    host='localhost',
    user='root',
    password='Web@123456',
        auth_plugin='mysql_native_password'
)
cursorObject =dataBase.cursor()
cursorObject.execute("CREATE DATABASE websitedb2")
print("All done")
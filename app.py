from flask import Flask, jsonify
import mysql.connector
from mysql.connector import errorcode
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'user': 'admin',
    'password': 'akash123',
    'host': 'api-db.cnica2ouqc9r.eu-north-1.rds.amazonaws.com',
    'port': 3306,
    'database': 'database'
}

# Create a database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/data')
def get_data():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)

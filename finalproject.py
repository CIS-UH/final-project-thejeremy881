# Creating the Flask Application Structure
from flask import Flask, jsonify, request 
import mysql.connector

# Initialize the Flask App

app = Flask(__name__)
app.config["DEBUG"] = True

# Create a function for a connection to the MySQL Database
def database_connection():
    connection = mysql.connector.connect(
        host='cis2368fall.cp0g88ua2h4t.us-east-1.rds.amazonaws.com',
        user='thejeremy881',
        password='jetBlue881!',
        database='cis2368falldb'
    )
    return connection

# GET Endpoint: Get all investors
@app.route('/api/investors', methods=['GET'])
def get_investors():
    try:
        conn = database_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM investor')
        investor = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify (investor)
    except Exception as e:
        return jsonify({"error": str(e)}), 100 #Make the First Commit Here
app.run()
    
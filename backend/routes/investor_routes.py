# Creating the Flask Application Structure
from flask import Flask, jsonify, request 
import mysql.connector

# Initialize the Flask App

app = Flask(__name__)
app.config["DEBUG"] = True

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
    
# POST Endpoint: Create a new investor
@app.route('/api/investors', methods=['POST'])
def add_investor():
    try:
        conn = database_connection()
        cursor = conn.cursor()
        data = request.get_json()
        firstname = data['firstname']
        lastname = data['lastname']
        query = "INSERT INTO investor (firstname, lastname) VALUES (%s, %s)"
        cursor.execute(query, (firstname, lastname))
        conn.commit()
        cursor.close()
        return jsonify({"message": "The investor has been added!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500 #Make the Second Commit Here 
    
# DELETE Endpoint: Delete a investor
@app.route('/api/investors/<int:id>', methods=['DELETE'])
def delete_investor(id):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        query = "DELETE FROM investor WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({"message": "The investor is not found"}), 404
        
        return jsonify({"message": "The investor has been deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT Endpoint: Update an Investor by ID
@app.route('/api/investors/<int:id>', methods=['PUT'])
def update_investor(id):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        data = request.get_json()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        
        #Ensure both of the fields are provided in the request body
        if not firstname or not lastname:
            return jsonify({"error": "Both of the firstname and lastname are required."}), 400
        
        #Update the investor in the database
        query = "UPDATE investor SET firstname = %s, lastname = %s WHERE id = %s"
        cursor.execute(query, (firstname, lastname, id))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"message": "The investor is not found!"}), 404
        
        cursor.close()
        conn.close()
        return jsonify({"message": "The Investor is updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  

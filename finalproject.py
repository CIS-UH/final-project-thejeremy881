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

# Deploy CRUD Operations for investor Table

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

# Deploy CRUD Operations for stock Table

# POST Endpoint: Create a new stock
@app.route('/api/stocks', methods=['POST'])
def add_stock():
    try:
        conn = database_connection()
        cursor = conn.cursor()
        data = request.get_json()
        stockname = data['stockname']
        abbreviation = data['abbreviation']
        currentprice = data['currentprice']

        query = "INSERT INTO stock (stockname, abbreviation, currentprice) VALUES (%s, %s, %s)"
        cursor.execute(query, (stockname, abbreviation, currentprice))
        conn.commit()
        cursor.close()
        return jsonify({"message": "The stock has been added!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT Endpoint: Update a stock by ID
@app.route('/api/stocks/<int:id>', methods=['PUT'])
def update_stock(id):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        data = request.get_json()
        stockname = data.get('stockname', None)
        abbreviation = data.get('abbreviation', None)
        currentprice = data.get('currentprice', None)

        if not stockname or not abbreviation or currentprice is None:
            return jsonify({"error": "All fields (stockname, abbreviation, currentprice) are required!"}), 400

        #Update the stock in the database
        query = "UPDATE stock SET stockname = %s, abbreviation = %s, currentprice = %s WHERE id = %s"
        cursor.execute(query, (stockname, abbreviation, currentprice, id))
        conn.commit()
        cursor.close()
        return jsonify({"message": "The stock has been updated!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE Endpoint: Delete a stock by ID
@app.route('/api/stocks/<int:id>', methods=['DELETE'])
def delete_stock(id):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        query = "DELETE FROM stock WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        cursor.close()
        return jsonify({"message": "The stock has been deleted!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Deploy CRUD Operations for Bond Table

# POST Endpoint: Creating a new bond
@app.route('/api/bond', methods=['POST'])
def bond_create():
    try:
        conn = database_connection()
        cursor = conn.cursor()
        data = request.get_json()
        bondname = data['bondname']
        abbreviation = data['abbreviation']
        currentprice = data['currentprice']
        query = "INSERT INTO bond (bondname, abbreviation, currentprice) VALUES (%s, %s, %s)"
        cursor.execute(query, (bondname, abbreviation, currentprice))
        return jsonify({"message": "A new bond has been added!"})
    except Exception as e :
        return jsonify({"error": str(e)}), 500

# PUT Endpoint: Updating one of the bond records
@app.route('/api/bond/<int:id>', methods=['PUT'])
def update_bond(id):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        data = request.get_json()
        bondname = data.get('bondname')
        abbreviation = data.get('abbreviation')
        currentprice = data.get('currentprice')
        # Updating the bond record by id
        query = "UPDATE bond SET bondname = %s, abbreviation = %s, currentprice = %s WHERE id = %s"
        cursor.execute(query, (bondname, abbreviation, currentprice, id))
        conn.commit()
        # Ensuring that all fields are provided in the query
        if not bondname or not abbreviation or not currentprice:
            return jsonify({"message": "The bondname, abbreviation, and currentprice are required"}), 400
        
        if cursor.rowcount == 0:
            return jsonify({"message": "ERROR: bond was not found"}), 404
        return jsonify({"message": "The Bond has been updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE Endpoint: Deleting one of the bond records
@app.route('/api/bond/<int:id>', methods=['DELETE'])
def delete_bond(id):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        query = "DELETE FROM bond WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        cursor.close()
        return jsonify({"message": "The bond has been deleted!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Deploy CRUD Operations for Stocktransaction table

# POST Endpoint: Create a new stock transaction
@app.route('/api/stocktransaction', methods=['POST'])
def create_stock_transaction():
    try:
        conn = database_connection()
        cursor = conn.cursor()
        data = request.get_json()

        investor_id = data['investorid']
        stock_id = data['stockid']
        quantity = data['quantity']

        if not investor_id or not stock_id or quantity is None:
            return jsonify({"error": "All fields (investorid, stockid, quantity) are required!"}), 400

        query = "INSERT INTO stocktransaction (investorid, stockid, quantity) VALUES (%s, %s, %s)"
        cursor.execute(query, (investor_id, stock_id, quantity))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "The stock transaction has been created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET Endpoint: Get all of the stock transactions
@app.route('/api/stocktransactions', methods=['GET'])
def get_stock_transactions():
    try:
        conn = database_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT 
            st.id, 
            st.date, 
            st.investorid, 
            i.firstname AS investor_firstname,
            i.lastname AS investor_lastname,
            st.stockid, 
            s.stockname AS stock_name,
            s.abbreviation AS stock_abbreviation,
            st.quantity
        FROM 
            stocktransaction st
        JOIN investor i ON st.investorid = i.id
        JOIN stock s ON st.stockid = s.id
        """
        cursor.execute(query)
        stock_transactions = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(stock_transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE Endpoint: Delete a stock transaction by ID
@app.route('/api/stocktransaction/<int:id>', methods=['DELETE'])
def delete_stock_transaction(id):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        query = "DELETE FROM stocktransaction WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "The stock transaction is not found!"}), 404
        cursor.close()
        conn.close()
        return jsonify({"message": "The stock transaction has been deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}, 500)

# Deploy CRUD Operations for BondTransactions Table

# GET Endpoint: Get all of the bondtransactions.
@app.route('/api/bondtransactions', methods=['GET'])
def get_bond_transactions():
    try:
        conn = database_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM bondtransaction"
        cursor.execute(query)
        bond_transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(bond_transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
app.run()

    






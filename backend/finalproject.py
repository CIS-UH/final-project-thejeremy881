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

def get_current_holdings(investor_id, item_id, item_type):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        
        if item_type == 'stock':
            query = """
                SELECT SUM(quantity) AS total_quantity
                FROM stocktransaction
                WHERE investorid = %s AND stockid = %s
            """
        elif item_type == 'bond':
            query = """
                SELECT SUM(quantity) AS total_quantity
                FROM bondtransaction
                WHERE investorid = %s AND bondid = %s
            """
        else:
            return 0
        
        cursor.execute(query, (investor_id, item_id))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return result[0] if result and result[0] else 0
    except Exception as e:
        raise Exception(f"Error calculating current holdings: {str(e)}")

# Deploy CRUD Operations for investor Table

@app.route('/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods),
            "route": str(rule)
        })
    return jsonify(routes)


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
        return jsonify({"error": str(e)}), 500 #Make the First Commit Here
    
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

# GET Endpoint: Get all stocks.
@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    try:
        conn = database_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM stock"
        cursor.execute(query)
        stocks = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(stocks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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

        # Here we will validate the sale to meet the project requirement.
        if quantity < 0:
            current_holdings = get_current_holdings(investor_id, stock_id, 'stock')
            if abs(quantity) > current_holdings:
                return jsonify({"error": "The sale quantity exceeds current holdings!"}), 400

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

@app.route('/api/stocktransaction/<int:id>', methods=['PUT'])
def update_stock_transaction(id):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        data = request.get_json()

        quantity = data.get('quantity')
        if quantity is None:
            return jsonify({"error": "Quantity is required!"}), 400

        query = "UPDATE stocktransaction SET quantity = %s WHERE id = %s"
        cursor.execute(query, (quantity, id))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Transaction not found!"}), 404

        cursor.close()
        conn.close()
        return jsonify({"message": "Transaction updated successfully!"}), 200
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
            return jsonify({"message": "Transaction not found!"}), 404

        cursor.close()
        conn.close()
        return jsonify({"message": "Transaction deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Deploy CRUD Operations for BondTransactions Table

# GET Endpoint: Get all of the bondtransactions.

@app.route('/api/bondtransactions', methods=['GET'])
def get_bond_transactions():
    try:
        conn = database_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Optional filtering by investorid
        investor_id = request.args.get('investorid')
        if investor_id:
            query = "SELECT * FROM bondtransaction WHERE investorid = %s"
            cursor.execute(query, (investor_id,))
        else:
            query = "SELECT * FROM bondtransaction"
            cursor.execute(query)

        bond_transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(bond_transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# DELETE Endpoint: Delete a bondtransaction by ID.

@app.route('/api/bondtransactions/<int:id>', methods=['DELETE'])
def delete_bondtransaction(id):
    try:
        conn = database_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM bondtransaction WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"message": "The bond transaction is not found"}), 404
        
        return jsonify({"message": "The bond transaction has been deleted!"}), 200
    except Exception as e:
        print(f"Error deleting bond transaction: {e}")  # Optional: For debugging purposes
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# POST Endpoint: Create a new bondtransaction.

@app.route('/api/bondtransactions', methods=['POST'])
def create_bondtransaction():
    try:
        conn = database_connection()
        cursor = conn.cursor()
        data = request.get_json()

        investorid = data['investorid']
        bondid = data['bondid']
        quantity = data['quantity']

        # Optional: Let the database auto-generate the date if configured
        date = data.get('date', None)

        if not investorid or not bondid or quantity is None:
            return jsonify({"error": "All fields (investorid, bondid, quantity) are required!"}), 400

        # Validate the sale as part of the project requirement
        if quantity < 0:
            current_holdings = get_current_holdings(investorid, bondid, 'bond')
            if abs(quantity) > current_holdings:
                return jsonify({"error": "Sale quantity exceeds current holdings!"}), 400

        query = "INSERT INTO bondtransaction (date, investorid, bondid, quantity) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (date, investorid, bondid, quantity) if date else (None, investorid, bondid, quantity))
        conn.commit()
        return jsonify({"message": "A new bond transaction has been added!"}), 201
    except Exception as e:
        print(f"Error creating bond transaction: {e}")  # Optional: For debugging purposes
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
    
# GET Endpoint: Retrieve an investor's portfolio

@app.route('/api/investors/<int:id>/portfolio', methods=['GET'])
def get_investor_portfolio(id):
    try:
        conn = database_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get stock transactions for the investor
        stock_query = """
        SELECT 
            st.id AS transaction_id,
            st.date AS transaction_date,
            s.stockname AS stock_name,
            s.abbreviation AS stock_abbreviation,
            s.currentprice AS stock_price,
            st.quantity AS stock_quantity
        FROM 
            stocktransaction st
        JOIN stock s ON st.stockid = s.id
        WHERE st.investorid = %s
        """
        cursor.execute(stock_query, (id,))
        stock_transactions = cursor.fetchall()

        # Get bond transactions for the investor
        bond_query = """
        SELECT 
            bt.id AS transaction_id,
            bt.date AS transaction_date,
            b.bondname AS bond_name,
            b.abbreviation AS bond_abbreviation,
            b.currentprice AS bond_price,
            bt.quantity AS bond_quantity
        FROM 
            bondtransaction bt
        JOIN bond b ON bt.bondid = b.id
        WHERE bt.investorid = %s
        """
        cursor.execute(bond_query, (id,))
        bond_transactions = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "investor_id": id,
            "stock_transactions": stock_transactions,
            "bond_transactions": bond_transactions
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
app.run()



    






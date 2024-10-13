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
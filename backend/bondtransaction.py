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
        cursor.close()
        conn.close()
        return jsonify({"message": "The bond transaction has been deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}, 500)
    
# POST Endpoint: Create a new bondtransaction.

@app.route('/api/bondtransactions', methods=['POST'])
def create_bondtransaction():
    try:
        conn = database_connection()
        cursor = conn.cursor()
        data = request.get_json()
        date = data['date']
        investorid = data['investorid']
        bondid = data['bondid']
        quantity = data['quantity']
        query = "INSERT INTO bondtransaction (date, investorid, bondid, quantity) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (date, investorid, bondid, quantity))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "A new bond transaction has been added!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
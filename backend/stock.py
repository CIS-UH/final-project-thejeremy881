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
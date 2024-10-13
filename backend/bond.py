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
    
    

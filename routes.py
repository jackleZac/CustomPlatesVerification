# This file defines the API endpoints and uses the BK-Tree and database utilities
from flask import request, jsonify
from db import get_db_connection, add_truck_to_db

def init_routes(app, bk_tree):
    @app.route('/api/search_plate', methods=['POST'])
    def search_plate():
        data = request.get_json()
        if not data or 'plate_number' not in data:
            return jsonify({"error": "Missing plate_number in request"}), 400
        
        query_plate = data['plate_number'].strip()
        max_dist = data.get('max_distance', 2)  # Default tolerance of 2
        
        # Search BK-Tree
        matches = bk_tree.search(query_plate, max_dist)
        
        # Fetch details from MySQL for matches
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor(dictionary=True)
        results = []
        for plate, distance in matches:
            cursor.execute("SELECT plate_number, truck_id, owner FROM trucks WHERE plate_number = %s", (plate,))
            truck_data = cursor.fetchone()
            if truck_data:
                truck_data['distance'] = distance
                results.append(truck_data)
        
        cursor.close()
        connection.close()
        
        return jsonify({"matches": results}), 200

    @app.route('/api/add_truck', methods=['POST'])
    def add_truck():
        data = request.get_json()
        if not data or 'plate_number' not in data or 'truck_id' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        plate_number = data['plate_number']
        truck_id = data['truck_id']
        owner = data.get('owner', 'Unknown')
        
        # Add to database
        success = add_truck_to_db(plate_number, truck_id, owner)
        if not success:
            return jsonify({"error": "Failed to add truck to database"}), 500
        
        # Update BK-Tree
        bk_tree.insert(plate_number)
        
        return jsonify({"message": "Truck added successfully"}), 201
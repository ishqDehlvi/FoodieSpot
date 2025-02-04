from flask import Flask, request, jsonify # type: ignore
import json

app = Flask(__name__)

# Load restaurants data from JSON
with open("data/restaurants.json") as f:
    restaurants = json.load(f)

@app.route('/api/check_availability', methods=['POST'])
def check_availability():
    print("Request received:", request.json)

    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON input"}), 400

    date = data.get("date")
    time = data.get("time")
    restaurant_id = data.get("restaurant_id")

    if not date or not time or not restaurant_id:
        return jsonify({"error": "Missing required fields"}), 400

    print(f"Looking for restaurant {restaurant_id}")

    # Find the restaurant in the list
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    print("Found restaurant:", restaurant)

    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    available_seats = restaurant.get("availability", {}).get(date, {}).get(time, 0)
    print("Available seats:", available_seats)

    return jsonify({"available_seats": available_seats})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify # type: ignore
import json
import os

app = Flask(__name__)

with open('data/restaurants.json', 'r') as f:
    restaurants = json.load(f)

if os.path.exists('data/reservations.json'):
    with open('data/reservations.json', 'r') as f:
        try:
            reservations = json.load(f)
        except json.JSONDecodeError:
            reservations = []
else:
    reservations = []

@app.route('/api/check_availability', methods=['POST'])
def check_availability():
    data = request.json
    date = data.get("date")
    time = data.get("time")
    restaurant_id = data.get("restaurant_id")

    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    available_seats = restaurant.get("availability", {}).get(date, {}).get(time, 0)

    return jsonify({"available_seats": available_seats})


@app.route('/api/make_reservation', methods=['POST'])
def make_reservation():
    global reservations  
    data = request.json
    date = data.get("date")
    time = data.get("time")
    restaurant_id = data.get("restaurant_id")
    seats_requested = data.get("seats", 1)
    customer_name = data.get("name")

    if not date or not time or not restaurant_id or not customer_name:
        return jsonify({"error": "Missing required fields"}), 400

    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    available_seats = restaurant.get("availability", {}).get(date, {}).get(time, 0)

    if seats_requested > available_seats:
        return jsonify({"error": "Not enough seats available"}), 400

    restaurant["availability"][date][time] -= seats_requested

    new_reservation = {
        "customer_name": customer_name,
        "date": date,
        "time": time,
        "restaurant_id": restaurant_id,
        "seats": seats_requested
    }
    reservations.append(new_reservation)


    with open('data/reservations.json', 'w') as f:
        json.dump(reservations, f, indent=4)

    return jsonify({"message": "Reservation successful!", "reservation": new_reservation})


if __name__ == '__main__':
    app.run(debug=True)

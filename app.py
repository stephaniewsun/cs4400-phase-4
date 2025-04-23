from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manifesting5s!", 
    database="flight_tracking"
)
cursor = db.cursor(dictionary=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        cursor.callproc("simulation_cycle")
        db.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/add_airplane", methods=["GET", "POST"])
def add_airplane():
    if request.method == "POST":
        data = request.form

        plane_type = data.get("plane_type") or None
        model = data.get("model") or None
        neo = data.get("neo")
        neo_value = True if neo == "on" else None

        if plane_type in ["Airbus", "Boeing"]:
            maintenanced = None
        else:
            maintenanced = True if data.get("maintenanced") == "on" else False

        try:
            cursor.callproc("add_airplane", [
                data["airlineID"],
                data["tail_num"],
                int(data["seat_capacity"]),
                int(data["speed"]),
                data["locationID"],
                plane_type,
                maintenanced,
                model,
                neo_value
            ])
            db.commit()
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("add_airplane.html")
    
@app.route("/add_airport", methods=["GET", "POST"])
def add_airport():
    if request.method == "POST":
        data = request.form
        try:
            cursor.callproc("add_airport", [
                data["airportID"], data["airport_name"], data["city"],
                data["state"], data["country"], data["locationID"]
            ])
            db.commit()
            return jsonify({"status": "airport added"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("add_airport.html")

@app.route("/add_person", methods=["GET", "POST"])
def add_person_form():
    print("📨 DEBUG: add_person_form was hit with method", request.method)

    if request.method == "POST":
        data = request.form
        try:
            cursor.callproc("add_person", [
                data["personID"], data["first_name"], data["last_name"],
                data["locationID"], data.get("taxID") or None,
                int(data["experience"]) if data.get("experience") else None,
                int(data["miles"]) if data.get("miles") else None,
                int(data["funds"]) if data.get("funds") else None
            ])
            db.commit()
            return jsonify({"status": "person added"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("add_person.html")

@app.route("/license", methods=["GET", "POST"])
def license():
    if request.method == "POST":
        data = request.form
        try:
            cursor.callproc("grant_or_revoke_pilot_license", [
                data["personID"],
                data["license"]
            ])
            db.commit()
            return jsonify({"status": "license granted or revoked"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("grant_or_revoke_pilot_license.html")

@app.route("/offer", methods=["GET", "POST"])
def offer():
    if request.method == "POST":
        data = request.form
        try:
            cursor.callproc("offer_flight", [
                data["flightID"],
                data["routeID"],
                data.get("support_airline") or None,
                data.get("support_tail") or None,
                int(data["progress"]),
                data["next_time"],
                int(data["cost"])
            ])
            db.commit()
            return jsonify({"status": "flight offered"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("offer_flight.html")

@app.route("/assign", methods=["GET", "POST"])
def assign():
    if request.method == "POST":
        data = request.form
        try:
            cursor.callproc("assign_pilot", [
                data["flightID"],
                data["personID"]
            ])
            db.commit()
            return jsonify({"status": "pilot assigned"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("assign_pilot.html")

@app.route("/board", methods=["GET", "POST"])
def board():
    if request.method == "POST":
        data = request.form
        try:
            cursor.callproc("passengers_board", [data["flightID"]])
            db.commit()
            return jsonify({"status": "passengers boarded"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("passengers_board.html")
@app.route("/takeoff", methods=["GET", "POST"])
def takeoff():
    if request.method == "POST":
        data = request.form
        try:
            cursor.callproc("flight_takeoff", [data["flightID"]])
            db.commit()
            return jsonify({"status": "flight took off"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("flight_takeoff.html")
@app.route("/land", methods=["GET", "POST"])
def land():
    if request.method == "POST":
        data = request.form
        try:
            cursor.callproc("flight_landing", [data["flightID"]])
            db.commit()
            return jsonify({"status": "flight landed"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("flight_landing.html")
@app.route("/disembark", methods=["GET", "POST"])
def disembark():
    if request.method == "POST":
        data = request.form
        try:
            cursor.callproc("passengers_disembark", [data["flightID"]])
            db.commit()
            return jsonify({"status": "passengers disembarked"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("passengers_disembark.html")
@app.route("/recycle", methods=["GET", "POST"])
def recycle():
    if request.method == "POST":
        data = request.form
        try:
            cursor.callproc("recycle_crew", [data["flightID"]])
            db.commit()
            return jsonify({"status": "crew recycled"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("recycle_crew.html")
@app.route("/retire", methods=["GET", "POST"])
def retire():
    if request.method == "POST":
        data = request.form
        try:
            cursor.callproc("retire_flight", [data["flightID"]])
            db.commit()
            return jsonify({"status": "flight retired"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("retire_flight.html")
@app.route("/simulate_cycle", methods=["GET", "POST"])
def simulate_cycle():
    if request.method == "POST":
        try:
            cursor.callproc("simulation_cycle")
            db.commit()
            return jsonify({"status": "simulation cycle executed"})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template("simulation_cycle.html")
@app.route("/flights_in_air_view")
def flights_in_air_view():
    cursor.execute("SELECT * FROM flights_in_the_air")
    flights = cursor.fetchall()
    return render_template("flights_in_air.html", flights=flights)
@app.route("/flights_on_ground_view")
def flights_on_ground_view():
    cursor.execute("SELECT * FROM flights_on_the_ground")
    flights = cursor.fetchall()
    return render_template("flights_on_ground.html", flights=flights)
@app.route("/people_in_air_view")
def people_in_air_view():
    cursor.execute("SELECT * FROM people_in_the_air")
    people = cursor.fetchall()
    return render_template("people_in_air.html", people=people)
@app.route("/people_on_ground_view")
def people_on_ground_view():
    cursor.execute("SELECT * FROM people_on_the_ground")
    people = cursor.fetchall()
    return render_template("people_on_ground.html", people=people)
@app.route("/route_summary_view")
def route_summary_view():
    cursor.execute("SELECT * FROM route_summary")
    routes = cursor.fetchall()
    return render_template("route_summary.html", routes=routes)
@app.route("/alternative_airports_view")
def alternative_airports_view():
    cursor.execute("SELECT * FROM alternative_airports")
    airports = cursor.fetchall()
    return render_template("alternative_airports.html", airports=airports)


if __name__ == "__main__":
    app.run(debug=True)

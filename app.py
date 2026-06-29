from flask import Flask, render_template, request, redirect, json

app = Flask(__name__)

def load_slots():
    with open("slots.json", "r") as f:
        return json.load(f)

def save_slots(slots):
    with open("slots.json", "w") as f:
        json.dump(slots, f)

@app.route("/")
def home():
    slots = load_slots()
    return render_template("index.html", slots=slots)

@app.route("/admin")
def admin():
    slots = load_slots()
    return render_template("admin.html", slots=slots)

@app.route("/add-slot", methods=["POST"])
def add_slot():
    date = request.form["date"]
    time = request.form["time"]
    slots = load_slots()
    slots.append({"date": date, "time": time, "booked": False})
    save_slots(slots)
    return redirect("/admin")

@app.route("/delete-slot/<int:index>")
def delete_slot(index):
    slots = load_slots()
    slots.pop(index)
    save_slots(slots)
    return redirect("/admin")

@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    phone = request.form["phone"]
    service = request.form["service"]
    slot_index = int(request.form["slot"])
    
    slots = load_slots()
    slots[slot_index]["booked"] = True
    slots[slot_index]["client"] = name
    slots[slot_index]["phone"] = phone
    slots[slot_index]["service"] = service
    save_slots(slots)
    
    return "Booking confirmed! We will see you soon 💅"

if __name__ == "__main__":
    app.run(debug=True)
    
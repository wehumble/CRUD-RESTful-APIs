from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper function to find an event by ID
def find_event(event_id):
    for idx, event in enumerate(events):
        if event.id == event_id:
            return event, idx
    return None, -1

# POST /events - Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    if "title" not in data:
        return jsonify({"error": "Missing 'title' field"}), 400

    new_id = max(event.id for event in events) + 1 if events else 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

# PATCH /events/<id> - Update an event's title
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    if "title" not in data:
        return jsonify({"error": "Missing 'title' field"}), 400

    event, idx = find_event(event_id)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    event.title = data["title"]
    return jsonify(event.to_dict()), 200

# DELETE /events/<id> - Remove an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event, idx = find_event(event_id)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    events.pop(idx)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)

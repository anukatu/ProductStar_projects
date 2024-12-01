from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Event({self.id}, {self.date}, {self.title}, {self.text})"



@app.route("/api/v1/calendar", methods=["POST"])
def create_event():
    data = request.get_json()
    date = datetime.strptime(data["date"], "%Y-%m-%d")
    event = Event(date=date, title=data["title"], text=data["text"])
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201


@app.route("/api/v1/calendar", methods=["GET"])
def get_calendar():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])



@app.route("/api/v1/calendar/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.to_dict())

@app.route("/api/v1/calendar/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    data = request.get_json()
    event.title = data["title"]
    event.text = data["text"]
    db.session.commit()
    return jsonify(event.to_dict())

@app.route("/api/v1/calendar/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"})

if __name__ == "__main__":
    app.run(debug=True)
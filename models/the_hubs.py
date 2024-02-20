from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # You can use a different database URL
db = SQLAlchemy(app)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.name

class Hub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', back_populates='rooms')
    topic = db.relationship('Topic', back_populates='rooms')

    def __repr__(self):
        return self.name

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', back_populates='messages')
    room = db.relationship('Room', back_populates='messages')

    def __repr__(self):
        return self.body[:50]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    rooms = db.relationship('Room', back_populates='user')
    messages = db.relationship('Message', back_populates='user')

    def __repr__(self):
        return self.username

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

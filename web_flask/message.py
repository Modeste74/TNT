#!/usr/bin/python3
"""defines a application for messages"""
from flask import Flask, render_template, request, jsonify
from models import storage
from models.users import Users
from models.messages import Message

app = Flask(__name__)


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    """facilitates the send of message from one user
    to another"""
    if request.method == 'POST':
        messenger = request.form['sender']
        recipient = request.form['recipient']
        message_content = request.form['message']
        users = storage.all(Users).values()
        sender = next((
            user for user in users if user.username == messenger), None)
        receiver = next((
            user for user in users if user.username == recipient), None)
        if sender and receiver:
            if message_content:
                new_message = Message(sender=sender,
                        receiver=receiver,
                        message=message_content)
                storage.new(new_message)
                storage.save()
                return jsonify({"message": "Message sent successfully"})
            else:
                return jsonify({"error": "Message cannot be empty"})
        else:
            return jsonify({"error": "sender or receiver not found"})
    return render_template('message.html')


@app.route('/view_messages', methods=['GET'])
def view_messages():
    """displays the messages between a sender
    and reciever"""
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    messages = storage.all(Message).values()
    direct_messages = [message for message in messages
            if message.sender_id == sender_id and message.receiver_id == receiver_id]
    """users = storage.all(Users).values()
    sender = next((user for user in users
        if user.id == sender_id), None)
    receiver = next((user for user in users
        if user.id == receiver_id), None)"""
    return render_template('view_messages.html', messages=direct_messages)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

#!/usr/bin/python3
"""defines the flask file for chat for hubs"""
from flask import Flask, request, redirect, jsonify, render_template
from models import storage
from models.chat import Chat
from models.hub import Hub
from models.users import Users

app = Flask(__name__)


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        hub_id = request.form['hub_id']
        sender_id = request.form['sender_id']
        message_content = request.form['message']
        
        hub = storage.get(Hub, hub_id)
        sender = storage.get(Users, sender_id)

        if hub and sender:
            new_message = Chat(hub_id=hub.id,
                    sender_id=sender.id,
                    message=message_content)
            storage.new(new_message)
            storage.save()
            return jsonify({"message": "Message sent successfully"})
        else:
            return jsonify({"error": "Hub or sender not found"})
    return render_template('chat.html')


@app.route('/view_messages/<hub_id>', methods=['GET'])
def view_messages(hub_id):
    hub = storage.get(Hub, hub_id)
    
    if hub:
        messages = storage.all(Chat).values()
        hub_messages = [message for message in messages
                if message.hub_id == hub.id]
        return render_template('view_messages.html', messages=hub_messages,
                hub=hub)
    else:
        return jsonify({"error": "Hub not found"})


@app.route('/delete_message/<message_id>', methods=['GET'])
def delete_message(message_id):
    message = storage.get(Chat, message_id)
    
    if message:
        storage.delete(message)
        storage.save()
        return jsonify({"message": "Message deleted successfully"})
    else:
        return jsonify({"error": "Message not found"})


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)

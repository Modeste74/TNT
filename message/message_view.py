#!/usr/bin/python3
"""defines a application for messages"""
from . import message_bp
from flask import Flask, render_template, request, jsonify
from flask_login import current_user, login_required
from models import storage
from models.users import Users
from models.messages import Message


@message_bp.route('/send_message/<sender_id>', methods=['GET', 'POST'])
@login_required
def send_message(sender_id):
    """facilitates the send of message from one user
    to another"""
    if request.method == 'POST':
        recipient = request.form['recipient']
        message_content = request.form['message']
        users = storage.all(Users).values()
        sender = storage.get(Users, sender_id)
        receiver = next((
            user for user in users if user.username == recipient), None)
        if sender and receiver:
            if message_content:
                new_message = Message(sender_id=sender.id,
                        receiver_id=receiver.id,
                        message=message_content)
                storage.new(new_message)
                storage.save()
                return jsonify({"message": "Message sent successfully"})
            else:
                return jsonify({"error": "Message cannot be empty"})
        else:
            return jsonify({"error": "sender or receiver not found"})
    return render_template('message.html', sender_id=sender_id)


@message_bp.route('/user_chat/<receiver_id>', methods=['GET'])
def user_chat(receiver_id):
    messages = storage.all(Message).values()
    received_messages = []
    for message in messages:
        if message.receiver_id == receiver_id:
            received_messages.append(message)
    if received_messages:
        unique_sender_ids = set(msg.sender_id for msg in received_messages)
        direct_messages = []

        for sender_id in unique_sender_ids:
            messages_between_users = [
                message for message in received_messages
                    if (
                        (message.receiver_id == current_user.id and message.sender_id == sender_id) or
                        (message.receiver_id == receiver_id and message.sender_id == current_user.id)
                    )
                ]
            direct_messages.extend(messages_between_users)
        return render_template('view_messages.html', messages=direct_messages,
            recipient_id=receiver_id, current_user=current_user)
    else:
        return render_template('view_messages.html', messages=[],
            recipient_id=receiver_id, current_user=current_user)

#!/usr/bin/python3
"""defines the flask file for chat for hubs"""
from . import chat_bp
from flask import Flask, request, redirect, jsonify
from flask import render_template, url_for
from flask_login import login_required
from models import storage
from models.chat import Chat
from models.hub import Hub
from models.users import Users


@chat_bp.route('/create_chat/<hub_id>/<sender_id>',
        methods=['GET', 'POST'])
@login_required
def create_or_view_chat(hub_id, sender_id):
    if request.method == 'POST':
        message_content = request.form['message']
        
        hub = storage.get(Hub, hub_id)
        sender = storage.get(Users, sender_id)

        if hub and sender:
            new_message = Chat(hub_id=hub.id,
                    sender_id=sender.id,
                    message=message_content)
            storage.new(new_message)
            storage.save()
            return redirect(url_for('chat.create_or_view_chat',
                hub_id=hub_id, sender_id=sender_id))
        else:
            return jsonify({"error":
                "Hub or sender not found"})
    
    hub = storage.get(Hub, hub_id)
    chats = storage.all(Chat).values()
    chats_hub = [chat for chat in chats
            if chat.hub_id == hub_id]
    return render_template('chat.html',
            chats_hub=chats_hub, hub=hub)


@chat_bp.route('/delete_message/<message_id>',
        methods=['GET'])
@login_required
def delete_message(message_id):
    message = storage.get(Chat, message_id)
    
    if message:
        storage.delete(message)
        storage.save()
        return jsonify({"message":
            "Message deleted successfully"})
    else:
        return jsonify({"error":
            "Message not found"})

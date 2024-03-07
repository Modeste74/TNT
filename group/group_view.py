#!/usr/bin/python3
"""defines endpoints for group creation"""
from . import group_bp
from flask import Flask, request, render_template
from flask import flash, url_for, redirect, jsonify
from flask_login import current_user, login_required
from models import storage
from models.users import Users
from models.hub import Hub
from models.group import Group, GroupMessage
from models.group_members import GroupMember
import os


@group_bp.route('/create_group/<hub_id>', methods=['GET', 'POST'])
@login_required
def create_group(hub_id):
    """creates groups for the hubs"""
    hub = storage.get(Hub, hub_id)
    if request.method == 'POST':
        group_name = request.form.get('group_name')

        if not hub:
            flash("Hub not found", "error")
        new_group = Group(hub_id=hub_id, name=group_name)
        storage.new(new_group)
        storage.save()
        groups = storage.all(Group).values()
        group = next((grp for grp in groups
            if grp.name == group_name))
        add_tutor = GroupMember(user_id=current_user.id,
                group_id=group.id)
        storage.new(add_tutor)
        storage.save()
        flash(f"Group '{group_name}' created successfully",
                "success")
        return redirect(url_for('hub.hub_display',
            hub_id=hub.id))
    return render_template('create_group.html', hub=hub)


@group_bp.route('/add_participant_to_group/<group_id>/<hub_id>',
	methods=['GET', 'POST'])
@login_required
def add_participant_to_group(group_id, hub_id):
    """add learners to the groups"""
    if request.method == 'POST':
        username = request.form.get('username')

        users =storage.all(Users).values()
        user = next((usr for usr in users
            if usr.username == username))
        if not user:
            flash("User not found", "error")
            return redirect(url_for(
                'group.add_participant_to_group',
                group_id=group_id, hub_id=hub_id))
        group_member = GroupMember(user_id=user.id,
                group_id=group_id)
        storage.new(group_member)
        storage.save()
        flash("Participant added to the group successfully",
                "success")
        return redirect(url_for(
            'group.add_participant_to_group',
            group_id=group_id, hub_id=hub_id))
    return render_template('add_participant_to_group.html',
            group_id=group_id, hub_id=hub_id)


@group_bp.route('/group_chat/<group_id>/<sender_id>',
        methods=['GET', 'POST'])
@login_required
def group_chat(group_id, sender_id):
    """creates group chats for groups"""
    group = storage.get(Group, group_id)
    sender = storage.get(Users, sender_id)

    if not group or not sender:
        return jsonify({"error": "Group or sender not found"})

    if request.method == 'POST':
        content = request.form.get('content')

        new_message = GroupMessage(
                group_id=group_id,
                sender_id=sender_id, content=content)
        storage.new(new_message)
        storage.save()

    messages = storage.all(GroupMessage).values()
    group_messages = [
            message for message in messages
            if message.group_id == group_id]
    sorted_messages = sorted(group_messages, key=lambda x: x.created_at)

    return render_template('group_chat.html', group=group,
    	sender=sender, group_messages=sorted_messages)


@group_bp.route('/delete_group/<group_id>/<hub_id>',
        methods=['GET', 'POST'])
@login_required
def delete_group(group_id, hub_id):
    """deletes groups in hub"""
    group = storage.get(Group, group_id)
    if group:
        storage.delete(group)
        storage.save()
        flash(f"Group '{group.name}' deleted successfully",
                "success")
    else:
        flash("Group not found", "error")
    return redirect(url_for('group.create_group',
        hub_id=hub_id))

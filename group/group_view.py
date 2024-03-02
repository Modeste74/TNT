#!/usr/bin/python3
"""defines endpoints for group creation"""
from . import group_bp
from flask import Flask, request, render_template, redirect
from flask import flash, url_for
from models import storage
from models.users import Users
from models.hub import Hub
from models.group import Group
from models.group_members import GroupMember
import os


@group_bp.route('/create_group/<hub_id>', methods=['GET', 'POST'])
def create_group(hub_id):
	hub = storage.get(Hub, hub_id)
	if request.method == 'POST':
		group_name = request.form.get('group_name')

		if not hub:
			flash("Hub not found", "error")
		new_group = Group(hub_id=hub_id, name=group_name)
		storage.new(new_group)
		storage.save()
		flash(f"Group '{group_name}' created successfully",
			"success")
		return redirect(url_for('hub.hub_display', hub_id=hub.id))
	return render_template('create_group.html', hub=hub)


@group_bp.route('/add_participant_to_group', methods=['GET', 'POST'])
def add_participant_to_group():
	if request.method == 'POST':
		user_id = request.form.get('user_id')
		group_id = request.form.get('group_id')

		user =storage.get(Users, user_id)
		group = storage.get(Group, group_id)
		if not user or not group:
			flash("User of group not found", "error")
			return redirect(url_for('group.add_participant_to_group'))
		group_member = GroupMember(user_id=user_id, group_id=group_id)
		storage.new(group_member)
		storage.save()
		flash("Participant added to the group successfully",
			"success")
		return redirect(url_for('group.add_participant_to_group'))
	return render_template('add_participant_to_group.html')


@group_bp.route('/delete_group/<group_id>', methods=['GET', 'POST'])
def delete_group(group_id):
	group = storage.get(Group, group_id)
	if group:
		storage.delete(group)
		storage.save()
		flash(f"Group '{group.name}' deleted successfully",
			"success")
	else:
		flash("Group not found", "error")
	return redirect(url_for('group.create_group'))
#!/usr/bin/python3
from . import hub_bp
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user
from models import storage
from models.hub import Hub
from models.users import Users
from models.resource import Resource
from models.chat import Chat
from models.group import Group
import os


@hub_bp.route('/hub_display/<hub_id>')
def hub_display(hub_id):
    hub = storage.get(Hub, hub_id)
    groups = storage.all(Group).values()
    return render_template('hub_display.html', hub=hub, groups=groups)


"""@app.route('/hub_features')
def hub_features():"""

@hub_bp.route('/resources/<hub_id>')
def resources(hub_id):
    hub = storage.get(Hub, hub_id)
    resources = storage.all(Resource).values()
    resource_for_hub = []
    for resource in resources: 
        if resource.hub_id == hub_id:
            resource_for_hub.append(resource)
    return render_template('resources.html',
        resources=resource_for_hub, hub=hub)


@hub_bp.route('/chats/<hub_id>')
def chats(hub_id):
    hub = storage.get(Hub, hub_id)
    chats = storage.all(Chat).values()
    chats_hub = []
    for chat in chats:
        if chat.hub_id == hub_id:
            chats_hub.append(chat)
    return render_template('chats.html', chats_hub=chats_hub, hub=hub)


@hub_bp.route('/groups/<hub_id>')
def groups(hub_id):
    hub = storage.get(Hub, hub_id)
    groups = storage.all(Group).values()
    group_chats = []
    for grp in groups:
        if grp.hub_id == hub_id:
            for member in grp.members:
                if member.user_id == current_user.id:
                    group_chats.append(grp)
    return render_template('group_chat.html',
        group_chats=group_chats, hub=hub)


@hub_bp.route('/add_learner',
    methods=['GET', 'POST'], strict_slashes=False)
def add_learner():
    """Adds a learner to the hub"""
    if request.method == 'POST':
        hub_id = request.form['hub_id']
        learner_id = request.form['learner_id']
        hub = storage.get(Hub, hub_id)
        learner = storage.get(Users, learner_id)
        
        if hub and learner:
            hub.learners.append(learner)
            storage.save()
            flash("Learner added successfully", "success")
        else:
            flash("Hub or learner not found", "error")

    return render_template('add_learner.html')

@hub_bp.route('/create_hub/<tutor_id>',
    methods=['GET', 'POST'], strict_slashes=False)
def create_hub(tutor_id):
    """creates a hub for tutoring"""
    if request.method == 'POST':
        name = request.form.get('name')
        if tutor_id and name:
            new_hub = Hub(tutor_id=tutor_id, name=name)
            storage.new(new_hub)
            storage.save()
            flash('Hub created successfully!', 'success')
            return redirect(url_for('hub.hub_display', hub_id=new_hub.id))
        else:
            flash('Missing required paramters for hub creation',
                    'error')
    return render_template('create_hub.html')


@hub_bp.route('/delete_hub/<hub_id>', methods=['GET'])
def delete_hub(hub_id):
    """deletes a hub"""
    hub = storage.get(Hub, hub_id)
    if hub:
        storage.delete(hub)
        storage.save()
        flash('Hub deleted successfully!', 'success')
    else:
        flash('Hub not found', 'error')
    return redirect(url_for('user.home'))
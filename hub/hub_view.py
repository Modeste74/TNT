#!/usr/bin/python3
from . import hub_bp
from flask import Flask, render_template, request
from flask import flash, redirect, url_for
from flask_login import current_user, login_required
from models import storage
from models.hub import Hub
from models.users import Users
from models.resource import Resource
from models.chat import Chat
from models.group import Group
import os


@hub_bp.route('/hub_display/<hub_id>')
@login_required
def hub_display(hub_id):
    """renders template for specific hubs"""
    hub = storage.get(Hub, hub_id)
    groups = storage.all(Group).values()
    return render_template('hub_display.html',
            hub=hub, groups=groups)


@hub_bp.route('/hub_resources/<hub_id>',
        methods=['GET', 'POST'])
@login_required
def hub_resources(hub_id):
    """creates and displays resource for
    particular hub"""
    hub = storage.get(Hub, hub_id)
    
    if request.method == 'POST':
        content = request.form.get('content')

        if hub:
            new_resource = Resource(hub_id=hub_id,
                    content=content)
            storage.new(new_resource)
            storage.save()
            flash("Resource created successfully", "success")
            return redirect(url_for('hub.hub_resources',
                hub_id=hub_id))

    resources = storage.all(Resource).values()
    resource_for_hub = [
            resource for resource in resources
            if resource.hub_id == hub_id]
    return render_template('hub_resources.html',
            resources=resource_for_hub, hub=hub)


@hub_bp.route('/add_learner/<hub_id>',
    methods=['GET', 'POST'], strict_slashes=False)
@login_required
def add_learner(hub_id):
    """Adds a learner to the hub"""
    if request.method == 'POST':
        learner_name = request.form['learner_name']
        hub = storage.get(Hub, hub_id)
        learners = storage.all(Users).values()
        learner = next((lnr for lnr in learners
            if lnr.username == learner_name))
        
        if hub and learner:
            hub.learners.append(learner)
            storage.save()
            flash("Learner added successfully", "success")
        else:
            flash("Hub or learner not found", "error")

    return render_template('add_learner.html', hub_id=hub_id)


@hub_bp.route('/create_hub/<tutor_id>',
    methods=['GET', 'POST'], strict_slashes=False)
@login_required
def create_hub(tutor_id):
    """creates a hub for tutoring"""
    if request.method == 'POST':
        name = request.form.get('name')
        if tutor_id and name:
            new_hub = Hub(tutor_id=tutor_id, name=name)
            storage.new(new_hub)
            storage.save()
            flash('Hub created successfully!', 'success')
            return redirect(url_for('hub.hub_display',
                hub_id=new_hub.id))
        else:
            flash('Missing required paramters for hub creation',
                    'error')
    return render_template('create_hub.html')


@hub_bp.route('/delete_hub/<hub_id>', methods=['GET'])
@login_required
def delete_hub(hub_id):
    """deletes a hub"""
    hub = storage.get(Hub, hub_id)
    if hub:
        storage.delete(hub)
        storage.save()
        flash('Hub deleted successfully!',
                'success')
    else:
        flash('Hub not found', 'error')
    return redirect(url_for('user.home'))

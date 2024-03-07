#!/usr/bin/python3
"""defines the endpoint for resources in hubs"""
from . import resource_bp
from flask import Flask, request, render_template
from flask import redirect, flash, url_for
from flask_login import login_required
from models import storage
from models.hub import Hub
from models.resource import Resource
import os


@resource_bp.route('/create_resource/<hub_id>',
    methods=['GET', 'POST'], strict_slashes=False)
@login_required
def create_resource(hub_id):
    """defines method for creating resource"""
    hub = storage.get(Hub, hub_id)
    if request.method == 'POST':
        content = request.form.get('content')

        if hub:
            new_resource = Resource(hub_id=hub_id,
                    content=content)
            storage.new(new_resource)
            storage.save()
            flash("Resource created successfully",
                    "success")
            return redirect(url_for('hub.resources',
                hub_id=hub_id))
    elif request.method == 'GET':
        hub = storage.get(Hub, hub_id)
        return render_template('create_resource.html', hub=hub)


@resource_bp.route('/delete_resource/<resource_id>',
        methods=['GET', 'POST'], strict_slashes=False)
@login_required
def delete_resource(resource_id):
    """deletes a resource"""
    resource = storage.get(Resource, resource_id)
    if resource:
        storage.delete(resource)
        storage.save()
        flash("Resource deleted successfully",
                "success")
    else:
        flash("Resource not found", "error")
    return redirect(url_for('resource.create_resource'))

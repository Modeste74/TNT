#!/usr/bin/python3
"""defines the endpoint for resources in hubs"""
from flask import Flask, request, render_template
from flask import redirect, flash, url_for
from models import storage
from models.hub import Hub
from models.resource import Resource
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')


@app.route('/create_resource', methods=['GET', 'POST'])
def create_resource():
    """defines method for creating resource"""
    if request.method == 'POST':
        hub_id = request.form.get('hub_id')
        content = request.form.get('content')

        hub = storage.get(Hub, hub_id)
        if not hub:
            flash("Hub not found", "error")
        new_resource = Resource(hub_id=hub_id, content=content)
        storage.new(new_resource)
        storage.save()
        flash("Resource created successfully", "success")
        return redirect(url_for('create_resource'))
    hubs = storage.all(Hub).values()
    return render_template('create_resource.html', hubs=hubs)


@app.route('/delete_resource/<resource_id>', methods=['GET', 'POST'])
def delete_resource(resource_id):
    """deletes a resource"""
    resource = storage.get(Resource, resource_id)
    if resource:
        storage.delete(resource)
        storage.save()
        flash("Resource deleted successfully", "success")
    else:
        flash("Resource not found", "error")
    return redirect(url_for('create_resource'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

#!/usr/bin/python3
from flask import Flask, render_template, request, flash, redirect, url_for
from models import storage
from models.hub import Hub
from models.users import Users
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

@app.route('/display')
def display():
        return render_template('display.html')


@app.route('/add_learner', methods=['GET', 'POST'])
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

@app.route('/create_hub', methods=['GET', 'POST'])
def create_hub():
    """creates a hub for tutoring"""
    if request.method == 'POST':
        tutor_id = request.form.get('tutor_id')
        name = request.form.get('name')
        if tutor_id and name:
            new_hub = Hub(tutor_id=tutor_id, name=name)
            storage.new(new_hub)
            storage.save()
            flash('Hub created successfully!', 'success')
            return redirect(url_for('display'))
        else:
            flash('Missing required paramters for hub creation',
                    'error')
    return render_template('create_hub.html')


@app.route('/delete_hub/<hub_id>', methods=['GET'])
def delete_hub(hub_id):
    """deletes a hub"""
    hub = storage.get(Hub, hub_id)
    if hub:
        storage.delete(hub)
        storage.save()
        flash('Hub deleted successfully!', 'success')
    else:
        flash('Hub not found', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

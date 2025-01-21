#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        """Handle GET request for all plants"""
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    def post(self):
        """Handle POST request to add a new plant"""
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict()), 201


# Resource for handling single plant by ID
class PlantByID(Resource):
    def get(self, id):
        """Handle GET request for a specific plant by ID"""
        plant = Plant.query.get_or_404(id)
        return jsonify(plant.to_dict())

    def delete(self, id):
        """Handle DELETE request to remove a plant"""
        plant = Plant.query.get_or_404(id)
        db.session.delete(plant)
        db.session.commit()
        return '', 204

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

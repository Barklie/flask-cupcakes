"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, json, jsonify
from models import db, connect_db, Cupcake
from sqlalchemy import text
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# debug = DebugToolbarExtension(app)


connect_db(app)

def serialize_cupcake(cupcake):
    """Serialize a dessert SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }

@app.route('/api/cupcakes', methods=["GET", "POST"])
def all_cupcakes():

    if request.method == 'GET':
        cupcakes = Cupcake.query.all()
        serialized = [serialize_cupcake(c) for c in cupcakes]

        return jsonify(cupcakes=serialized)
    else:
        flavor = request.json["flavor"]
        size = request.json["size"]
        rating = request.json["rating"]
    # image = request.json["image"]

        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating)

        db.session.add(new_cupcake)
        db.session.commit()

        serialized = serialize_cupcake(new_cupcake)

        return (jsonify(cupcake=serialized), 201)





@app.route('/api/cupcakes/<int:id>', methods=["GET", "DELETE", "PATCH"])
def get_cupcake(id):
    if request.method == 'GET':
        cupcake = Cupcake.query.get_or_404(id)
        serialized = serialize_cupcake(cupcake)

        return jsonify(cupcake=serialized)
    
    elif request.method == 'DELETE':
        cupcake = Cupcake.query.get_or_404(id)

        db.session.delete(cupcake)
        db.session.commit()
        
        return jsonify({'Message': "Deleted"}) 
    
    # request.method == 'PATCH':
    else: 
        cupcake = Cupcake.query.get_or_404(id)
        cupcake.flavor = request.json.get("flavor", cupcake.flavor)
        cupcake.size = request.json.get("size", cupcake.size)
        cupcake.rating = request.json.get("rating", cupcake.rating)

        db.session.commit()

        serialized = serialize_cupcake(cupcake)

        return jsonify(cupcake=serialized)

        
    






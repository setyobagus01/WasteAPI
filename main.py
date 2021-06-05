import flask
import flask_restful
import flask_sqlalchemy
import werkzeug
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

from prediction.predict import model_predict


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wastemanagement.db'

db = SQLAlchemy(app)

class WasteModel(db.Model):
    # pylint:disable=invalid-name,used-before-assignment
    id = db.Column(db.Integer, primary_key=True)
    wasteType = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Waste(wasteType={wasteType}, description={description})"

class ContentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer, nullable=False)
    wasteType = db.Column(db.String(50), nullable=False)
    imageUrl = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Content(title={title}, wasteType={wasteType}, imageUrl={imageUrl}, content={content})"

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


# Waste
waste_put_args = reqparse.RequestParser()
waste_put_args.add_argument("wasteType", type=str, help="Name of the waste is required", required=True)
waste_put_args.add_argument("description", type=str, help="Description of the waste",  required=True)

# Content
content_put_args = reqparse.RequestParser()
content_put_args.add_argument("title", type=str, help="title of the content is required", required=True)
content_put_args.add_argument(
    "wasteType", type=str, help="wasteType of the waste is required",  required=True)
content_put_args.add_argument(
    "imageUrl", type=str, help="imageUrl of the waste is required",  required=True)
content_put_args.add_argument(
    "content", type=str, help="content of the waste is required",  required=True)

# Waste Schema
waste_fields = {
    'id': fields.Integer,
    'wasteType': fields.String,
    'description': fields.String
}

# Image Schema
image_fields = {
    'id': fields.Integer,
    'image': fields.String,
    'name': fields.String,
    'mimetype': fields.String
}

# Content Schema
content_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'wasteType': fields.String,
    'imageUrl': fields.String,
    'content': fields.String
}
        
class Waste(Resource):
    @marshal_with(waste_fields)
    def get(self):
        result = WasteModel.query.all()
        return result

    @marshal_with(waste_fields)
    def put(self):
        args = waste_put_args.parse_args()
        waste = WasteModel(wasteType=args['wasteType'], description=args['description'])
        db.session.add(waste)
        db.session.commit()
        return waste, 201

class WasteById(Resource):
    @marshal_with(waste_fields)
    def get(self, wasteId):
        result = WasteModel.query.filter_by(id=wasteId).first()
        if not result:
            abort(404, message="Couldn't find waste id...")
        return result

class Image(Resource):
    @marshal_with(image_fields)
    def get(self):
        return ImageModel.query.all()
    def post(self):

        labels = ['battery', 'biological', 'brown-glass', 'cardboard', 'clothes',
                  'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass']
        
        pic = request.files['pic']

        if not pic:
            abort(400, message="No picture uploaded...")

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(pic.filename))
        pic.save(file_path)


        prediction = model_predict(file_path)

        result = []

        classes = prediction[0]

        predicted_class = zip(labels, classes)

        for (label, p) in predicted_class:
            result.append({label: float(p) * 100})

        return result, 200


class Content(Resource):
    @marshal_with(content_fields)
    def get(self):
        content = ContentModel.query.all()

     
        return content, 200
    @marshal_with(content_fields)
    def put(self):
        args = content_put_args.parse_args()
        content = ContentModel(title=args['title'], wasteType=args['wasteType'], imageUrl=args['imageUrl'], content=args['content'])

        db.session.add(content)
        db.session.commit()
        return content, 201
    

class ContentById(Resource):
    @marshal_with(content_fields)
    def get(self, contentId):
        content = ContentModel.query.filter_by(id=contentId).first()
        if not content:
            abort(404, message="Content with that id is not exist...")

        return content, 200
        

    def delete(self, contentId):
        content = ContentModel.query.get(contentId)
        if not content:
                abort(404, message="Content id is not valid...")
        
        db.session.delete(content)
        db.session.commit()
        return {"message": "Content deleted..."}, 202


api.add_resource(Waste, "/api/waste")
api.add_resource(WasteById, "/api/waste/<int:wasteId>")
api.add_resource(Image, "/api/predict")

api.add_resource(Content, "/api/content")
api.add_resource(ContentById, "/api/content/<int:contentId>")

if __name__ == "__main__":
    app.run(debug=True)

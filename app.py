from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:3003@localhost:3306/iot'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Device(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=True)
    updated_at = db.Column(db.DateTime(), nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class DeviceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Device

    id = ma.auto_field()
    name = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()


@app.route('/', methods=['GET'])
def index():
    return "hello"

#GET
@app.route('/device', methods=['GET'])
def getAllDevice():
    devices = Device.query.all()
    device_schema = DeviceSchema(many=True)
    data = device_schema.dump(devices)
    return jsonify(data)

#POST
@app.route('/device', methods=['POST'])
def createDevice():
    data = request.get_json()
    new_device = Device(
        id = data.get('id'),
        name = data.get('name'),
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow()
    )
    new_device.save()
    device_schema = DeviceSchema()
    data = device_schema.dump(new_device)
    return jsonify(data), 201

#Search
@app.route('/device/<int:id>', methods=['GET'])
def getOneDevice(id):
    device = Device.query.get_or_404(id)
    device_schema = DeviceSchema()
    data = device_schema.dump(device)
    return jsonify(data), 200


#PUT
@app.route('/device/<int:id>', methods=['PUT'])
def updateDevice(id):
    device_to_update = Device.query.get_or_404(id)
    data = request.get_json()
    device_to_update.name = data.get('name')
    device_to_update.updated_at = datetime.utcnow()

    db.session.commit()

    device_schema = DeviceSchema()
    device_data = device_schema.dump(device_to_update)
    return jsonify(device_data), 200

#DELETE
@app.route('/device/<int:id>', methods=['DELETE'])
def deleteDevice(id):
    device_to_delete = Device.query.get_or_404(id)
    device_to_delete.delete()
    return "Delete succesfully", 201

if __name__ == '__main__':
    app.run(debug=True)
import json
import utils
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ash1401043m@localhost/flaskUser'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def save(self):
        db.session.add(self)
        db.session.commit()
        return

    def to_json(self):
        data = {
            "id": self.id,
            "username": self.email
        }
        return data


@app.route("/", methods=["POST"])
def create():
    data = json.loads(request.data)
    obj = User(username=data.get("username"), email=data.get(
        "email"), password=data.get("password"))
    obj.save()
    return obj.to_json(), 201


@app.route("/", methods=["GET"])
def list():
    data = User.query.all()
    return jsonify(utils.to_json_list(data)), 200


# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == '__main__':
    manager.run()

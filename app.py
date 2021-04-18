import json
import utils
import bcrypt
import datetime
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
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
    last_login = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def get_or_404_via_username(cls, params):
        user = User.query.filter_by(username=params["username"]).first()
        if not user:
            return None
        return user

    def save(self):
        db.session.add(self)
        db.session.commit()
        return

    def hash_password(self, password):
        password = bcrypt.hashpw(password.encode(
            "utf-8"), bcrypt.gensalt())
        self.password = password.decode("utf-8")
        return True

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def to_json(self):
        data = {
            "id": self.id,
            "username": self.email
        }
        return data


@app.route("/signup", methods=["POST"])
def signup():
    data = json.loads(request.data)
    obj = User(username=data.get("username"), email=data.get(
        "email"))
    obj.hash_password(data.get("password"))
    obj.save()
    return obj.to_json(), 201


@app.route("/login", methods=["POST"])
def login():
    data = json.loads(request.data)
    obj = User.get_or_404_via_username(data)
    if not obj:
        return {"status": "failed", "msg": "Account with that username not found"}, 401

    verify = obj.verify_password(data["password"])
    if not verify:
        return {"status": "failed", "msg": "Password doesn't match"}, 401

    return {"status": "success", "msg": "Jwt generated", "data": utils.jwt_creator(utils.generate_user_payload(obj))}, 200


if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == '__main__':
#     manager.run()

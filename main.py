from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json
import utils

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://admin:root@localhost:5432/PetRock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Integer, default=0)
    rocks = db.relationship('Rock', backref='owner', lazy=True)
    user_unlocks = db.relationship('UserUnlocks', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Rock(db.Model):
    __tablename__ = 'rock'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    rockshape = db.Column(db.String(50), db.ForeignKey('item.item_path'), nullable=False)
    rockcolor = db.Column(db.String(50), db.ForeignKey('item.item_path'), nullable=False)
    rockmisc = db.Column(db.String(50), db.ForeignKey('item.item_path'), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Rock %r>' % self.name

class UserUnlocks(db.Model):
    __tablename__ = 'userunlocks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    unlock_name = db.Column(db.String(50), nullable=False)
    unlocked_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('user', back_populates='UserUnlocks')
    item = db.relationship('item', back_populates='UserUnlocks')
    def __repr__(self):
        return '<UserUnlocks %r>' % self.unlock_name

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    completion_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.description

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(50), nullable=False)
    item_path = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Item %r>' % self.item_path

@app.route('/')
def index():
    db.drop_all()
    db.create_all()
    hashed_password = generate_password_hash('1234', method='pbkdf2:sha256')
    brady = User(username='Brady', password_hash=hashed_password)

    # Creating items to add to database
    items = [
        {"id": 101 ,"item_type": "eye" ,"item_path": "googlyeyes.png", "price": 25},
        {"id": 102,"item_type": "eye" ,"item_path": "girlface.png" , "price": 20},
        {"id": 103,"item_type": "eye" ,"item_path": "eyelash.png" , "price": 20},
        {"id": 104,"item_type": "eye","item_path": "angryeyes.png" , "price": 15},
        {"id": 105,"item_type": "eye" ,"item_path": "tiredeyes.png" , "price": 15},
        {"id": 201,"item_type": "shape" ,"item_path": "rockshape1.jpg" , "price": 35},
        {"id": 202,"item_type": "shape","item_path": "blackrock.png", "price": 25},
        {"id": 203,"item_type": "shape" ,"item_path": "rockshape2.png", "price": 40},
        {"id":204,"item_type": "shape" ,"item_path": "rockshape3.png" , "price": 35},
        {"id": 301,"item_type": "misc","item_path": "catears.png", "price": 30},
        {"id": 302,"item_type": "misc","item_path": "wizardhat.png", "price": 40},
        {"id": 303,"item_type": "misc","item_path": "piratehat.png" , "price": 50},
        {"id": 304,"item_type": "misc" ,"item_path": "crown.png", "price": 75},
    ]

    for item_data in items:
        item = Item(
            item_type = item_data["item_type"],
            item_path = item_data["item_path"],
            price = item_data["price"]
        )
        db.session.add(item)
    db.session.add(brady)
    db.session.commit()
    print(User.query.all())
    return render_template('index.html', log_html=User.query.all())

# unlocks a new item from the shop, with a user_id and item_id json object as input
@app.route('/shop/unlock', methodd = ['POST'])
def unlock_item():
    data = request.get_json()
    user_id = data['user_id']
    item_id = data['item_id']
    
    user = User.query.get(user_id)
    item = Item.query.get(item_id)
    
    if user.balance >= item.price:
        user.balance -= item.price
    unlock = UserUnlocks(
        user_id=data['user_id'],
        unlock_name=data['unlock_name']
    )
    db.session.add(unlock)
    db.session.commit()
    return {"message": "Item unlocked successfully"}, 201

# gets all items in the shop and returns them
@app.route('/shop', methods= ['GET', 'PUT'])
def shop():

    items = Item.query.all()

    #match item with their type
    grouped_items = defaultdict(list)
    for item in items:
        grouped_items[item.item_type].append(item)

    return render_template('shop.html', grouped_items=grouped_items)


# add a new rock to the database
@app.route('/rock', methods=['POST'])
def create_rock():
    if request.is_json:
        data = request.get_json()
        rock = Rock(
            name=data['name'],
            rockshape=data['rockshape'],
            rockcolor=data['rockcolor'],
            rockmisc=data['rockmisc'],
            owner=data['owner']
        )
        db.session.add(rock)
        db.session.commit()
        return {"message": "Rock added successfully"}, 201
    return {"error": "Invalid input"}, 400
# information for getting, deleting, and updating rocks in the database
@app.route('/rock/<rock_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_rocks(rock_id):
    rock = Rock.query.get_or_404(rock_id)
    if request.method == 'GET':
        return {
            "name": rock.name,
            "rockshape": rock.rockshape,
            "rockcolor": rock.rockcolor,
            "rockmisc": rock.rockmisc,
            "owner": rock.owner
        }, 200
    if request.method == 'PUT':
        data = request.get_json()
        rock.name = data['name']
        rock.rockshape = data['rockshape']
        rock.rockcolor = data['rockcolor']
        rock.rockmisc = data['rockmisc']
        db.session.commit()
        return {"message": f"Rock {rock.name} successfully updated"}
    if request.method == 'DELETE':
        db.session.delete(rock)
        db.session.commit()
        return {"message": f"Rock {rock.name} successfully deleted."}
# add a new user to the database
@app.route('/user', methods=['POST'])
def create_user():
    if request.is_json:
        data = request.get_json()
        user = User(
            username=data['username'],
            password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User added successfully"}, 201
    return {"error": "Invalid input"}, 400

@app.route('/user/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return {
            "username": user.username,
            "password": user.password
        }, 200
    if request.method == 'PUT':
        data = request.get_json()
        user.username = data['username']
        user.password = data['password']
        db.session.commit()
        return {"message": f"User {user.username} successfully updated"}
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User {user.username} successfully deleted."}
    
# takes as input, a user id and an item type (eye, shape, misc) and returns a json object with all the items of that type that the user has unlocked
@app.route('/user/<user_id>/unlocks/<string:item_type>', methods=['GET'])
def get_user_unlocked(user_id, item_type):
    user = User.query.get_or_404(user_id)
    unlocked_items = (
        db.session.query(Item).join(UserUnlocks,Item.id == UserUnlocks.item_id)
        .filter(UserUnlocks.user_id == user.id, Item.item_type == item_type).all()
    )
    item_list = [
        {
            'id':item.id,
            'item_type': item.item_type,
            'item_path': item.item_path,
            'price': item.price
        }
        for item in unlocked_items
    ]
    return jsonify({
                   'user_id': user.id,
                   'item_type': item_type,
                   'unlocked_items': item_list}
    )
# put an item in the database if we need
@app.route('/item', methods=['POST'])
def create_item():
    if request.is_json:
        data = request.get_json()
        item = Item(
            item_type=data['item_type'],
            item_path=data['item_path'],
            price=data['price']
        )
        db.session.add(item)
        db.session.commit()
        return {"message": "Item added successfully"}, 201
    return {"error": "Invalid input"}, 400
# methods for retrieving, deleting, and updating items in the database
@app.route('/item/<item_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_items(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'GET':
        return {
            "item_type": item.item_type,
            "item_path": item.item_path,
            "price": item.price
        }, 200
    if request.method == 'PUT':
        data = request.get_json()
        item.item_type = data['item_type']
        item.item_path = data['item_path']
        item.price = data['price']
        db.session.commit()
        return {"message": f"Item {item.item_path} successfully updated"}
    if request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Item {item.item_path} successfully deleted."}
# adding a new task to the database
@app.route('/task', methods=['POST'])
def create_task():
    if request.is_json:
        data = request.get_json()
        task = Task(
            user_id=data['user_id'],
            description=data['description'],
            completion_date=data['completion_date']
        )
        db.session.add(task)
        db.session.commit()
        return {"message": "Task added successfully"}, 201
    return {"error": "Invalid input"}, 400
# methods for retrieving, deleting, and updating tasks in the database
@app.route('/task/<task_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'GET':
        return {
            "user_id": task.user_id,
            "description": task.description,
            "completion_date": task.completion_date
        }, 200
    if request.method == 'PUT':
        data = request.get_json()
        task.user_id = data['user_id']
        task.description = data['description']
        task.completion_date = data['completion_date']
        db.session.commit()
        return {"message": f"Task {task.description} successfully updated"}
    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return {"message": f"Task {task.description} successfully deleted."}


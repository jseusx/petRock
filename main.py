from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import json
import utils

app = Flask(__name__, template_folder= 'frontend/html', static_folder='frontend/static')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:root@localhost:5432/PetRock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Integer, default=0)
    rocks = db.relationship('Rock', backref='user', lazy=True)
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
    item_path = db.Column(db.String(50), nullable=False, unique = True)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Item %r>' % self.item_path

@app.route('/')
def index():
    db.drop_all()
    db.create_all()
    brady = User(username='Brady', email='bbromaghim@gmail.com', password='1234')

    db.session.add(brady)
    db.session.commit()

    #values cant be null example of what values should be
    # rock = Rock(
    #     name='Rocky',
    #     rockshape='rockshape1', 
    #     rockcolor='gray',    
    #     rockmisc='wizardhat', 
    #     owner=brady.id      
    # )
    # db.session.add(rock)
    # db.session.commit()

    print(User.query.all())
    return render_template('index.html', log_html=User.query.all())

@app.route('/shop', methods= ['GET', 'PUT'])
def shop():

    return render_template('shop.html')



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

@app.route('/user', methods=['POST'])
def create_user():
    if request.is_json:
        data = request.get_json()
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
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
            "email": user.email,
            "password": user.password
        }, 200
    if request.method == 'PUT':
        data = request.get_json()
        user.username = data['username']
        user.email = data['email']
        user.password = data['password']
        db.session.commit()
        return {"message": f"User {user.username} successfully updated"}
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User {user.username} successfully deleted."}

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

if __name__ == "__main__":
    port = 5000  # Default Flask port
    print(f"Server running at: http://127.0.0.1:{port}")
    app.run(debug=True, port=port)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


meals_orders_association = db.Table(
    "meals_orders",
    db.Column("meal_id", db.Integer, db.ForeignKey("meals.id")),
    db.Column("order_id", db.String, db.ForeignKey("orders.id"))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    orders = db.relationship('Order', back_populates='user')


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False, unique=True)
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    picture = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='meals') # запихивать одно блюдо в разные категории не будем, хотя могли бы
    orders = db.relationship("Order", secondary=meals_orders_association, \
                               back_populates="meals")



class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False, unique=True)
    meals = db.relationship('Meal', back_populates='category', order_by=func.random())


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=func.now()) # TODO уточнить
    sum = db.Column(db.Integer)
    status = db.Column(db.String(16))
    name = db.Column(db.String(64), nullable=False)
    mail = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    meals = db.relationship("Meal", secondary=meals_orders_association, \
                               back_populates="orders")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='orders')


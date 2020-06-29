import csv
import os

from flask import Flask

from models import db, Meal, Category
from app import app


db.create_all()


reader = csv.reader(open("mock_data/delivery_categories.csv", "r"))
test_id = db.session.query(Category).get(1)
if test_id:
    print("Похоже, информация о категориях уже есть в базе данных")
else:
    for row in list(reader)[1:]: #id title
        category = db.session.add(Category(id=int(row[0]), title=row[1]))
        print(" ".join(row))
    db.session.commit()
    print("Информация о категориях добавлена в базу данных")


reader = csv.reader(open("mock_data/delivery_items.csv", "r"))
test_id = db.session.query(Meal).get(1)
if test_id:
    print("Похоже, информация о блюдах уже есть в базе данных")
else:
    for row in list(reader)[1:]: #id title price description picture category_id
        meal = db.session.add(Meal(id=int(row[0]), title=row[1], price=int(row[2]), \
                          description=row[3], picture=row[4], category_id=int(row[5])))
        print(" ".join(row))
    db.session.commit()
    print("Информация о блюдах добавлена в базу данных")


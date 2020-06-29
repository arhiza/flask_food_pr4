from flask import Flask, request, render_template, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app import app, db
from models import Category, Meal, User, Order
from forms import OrderForm, RegistrationForm, LoginForm


@app.route("/")
def render_main():
    categories = db.session.query(Category).all()
    return render_template("main.html", categories=categories)


def get_cart_info(cart):
    meals = db.session.query(Meal).filter(Meal.id.in_(cart)).all()
    total_sum = sum([m.price for m in meals])
    return meals, total_sum


@app.route("/addtocart/<int:id>")
def render_add_to_cart(id):
    cart = session.get("cart", [])
    if id not in cart:
        cart.append(id)
        session["cart"] = cart
        meals, total_sum = get_cart_info(cart)
        session["total_sum"] = total_sum
    return(redirect("/cart/"))


@app.route("/removefromcart/<int:id>")
def render_remove_from_cart(id):
    cart = session.get("cart", [])
    if id in cart:
        cart = list(set(cart)-{id})
        session["cart"] = cart
        meals, total_sum = get_cart_info(cart)
        session["total_sum"] = total_sum
        session["remove_from_cart"] = True
    return(redirect("/cart/"))


@app.route("/cart/", methods=["GET", "POST"])
def render_cart():
    form = OrderForm()
    cart = session.get("cart", [])
    meals, total_sum = get_cart_info(cart)
    if request.method == "GET":
        form.mail.data = session.get("mail")
    user_id = session.get("user_id")
    if user_id and form.validate_on_submit():
        user = db.session.query(User).get(user_id)
        order = Order(sum=total_sum, status="новый заказ", name=form.name.data, \
                      mail=form.mail.data, phone=form.phone.data, \
                      address=form.address.data, user_id=user_id) # , meals=meals
        db.session.add(order)
        db.session.commit()
        order.meals = meals
        db.session.commit()
        session.pop("cart")
        session.pop("total_sum")
        return redirect("/ordered/")
    session["to_redirect"] = request.url
    return render_template("cart.html", form=form, meals=meals, total_sum=total_sum)


@app.route("/ordered/")
def render_ordered():
    return render_template("ordered.html")


@app.route("/account/") # кабинет, с историей заказов, только для залогиненных
def render_profile():
    if not session.get("user_id"):
        session["to_redirect"] = request.url
        return redirect("/login/")
    user_id = session.get("user_id")
    user = db.session.query(User).get(user_id)
    orders = user.orders
    return render_template("account.html", orders=orders)


@app.route("/register/", methods=["GET", "POST"])
def render_register():
    if session.get("user_id"):
        url = session.pop("to_redirect", "/")
        return redirect(url)
    form = RegistrationForm()
    if form.validate_on_submit():
        mail = form.mail.data
        password = generate_password_hash(form.password.data)
        user = User(mail=mail, password_hash=password)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        session["mail"] = mail
        url = session.pop("to_redirect", "/")
        return redirect(url)
    return render_template("register.html", form=form)


@app.route("/login/", methods=["GET", "POST"])
def render_login():
    if session.get("user_id"):
        url = session.pop("to_redirect", "/")
        return redirect(url) # "/"
    form = LoginForm()
    if form.validate_on_submit():
        mail = form.mail.data
        password = form.password.data
        user = db.session.query(User).filter_by(mail=mail).first()
        if not user:
            form.mail.errors.append("Пользователь не найден")
            return render_template("login.html", form=form)
        if check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["mail"] = mail
            url = session.pop("to_redirect", "/")
            return redirect(url)
        else:
            form.password.errors.append("Неверный пароль")
    return render_template("login.html", form=form)


@app.route("/logout/")
def render_logout():
    session.pop("user_id")
    session.pop("mail")
    return redirect("/")


class OnlyLookView(ModelView):
    can_create = False  
    can_edit = False
    can_delete = False


admin = Admin(app)
admin.add_view(OnlyLookView(User, db.session))
admin.add_view(OnlyLookView(Category, db.session))
admin.add_view(OnlyLookView(Meal, db.session))
admin.add_view(OnlyLookView(Order, db.session))


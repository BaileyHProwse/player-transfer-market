from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'players.sqlite3')

db = SQLAlchemy(app)

# Player items
class Player(db.Model):
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    short_description = db.Column(db.Text)
    long_description = db.Column(db.Text)
    image = db.Column(db.String(100))
    environmental_impact = db.Column(db.Integer)

# Reviews linked to the players
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    name = db.Column(db.String(100))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    player = db.relationship('Player', backref='reviews')

@app.route('/')
def index():
    # Sorts the players
    sort_by = request.args.get("sort")

    if sort_by == "name":
        players = Player.query.order_by(Player.name.asc()).all()
    elif sort_by == "price_low":
        players = Player.query.order_by(Player.price.asc()).all()
    elif sort_by == "price_high":
        players = Player.query.order_by(Player.price.desc()).all()
    elif sort_by == "impact_low":
        players = Player.query.order_by(Player.environmental_impact.asc()).all()
    elif sort_by == "impact_high":
        players = Player.query.order_by(Player.environmental_impact.desc()).all()
    else:
        players = Player.query.all()

    return render_template("index.html", players=players, sort_by=sort_by)


@app.route('/player/<int:id>')
def single_player(id):
    player = Player.query.get_or_404(id)
    
    # Average rating calculator
    if player.reviews:
        avg_rating = sum(r.rating for r in player.reviews) / len(player.reviews)
    else:
        avg_rating = None
    
    return render_template('single_player.html', player=player, avg_rating=avg_rating)

@app.route('/player_info/<int:id>')
def player_info(id):
    # Used for the long description when hovering
    player = Player.query.get_or_404(id)

    return {
        "name": player.name,
        "long_description": player.long_description
    }


@app.route('/add_player/<int:id>', methods=['POST'])
def add_player(id):
    # Adds item to the basket
    quantity = int(request.form['quantity'])

    if "basket" not in session:
        session["basket"] = {}

    basket = session["basket"]

    id_str = str(id)

    if id_str in basket:
        basket[id_str] += quantity
    else:
        basket[id_str] = quantity

    session["basket"] = basket

    return redirect(url_for('added', id=id, quantity=quantity))


@app.route('/added')
def added():
    # For confirmation page
    id = request.args.get('id')
    quantity = request.args.get('quantity')

    player = Player.query.get(id)

    return render_template('added.html', player=player, quantity=quantity)

@app.route('/basket')
def view_basket():
    # Builds basket list
    basket = session.get("basket", {})

    basket_items = []
    total_price = 0

    for id, quantity in basket.items():
        player = Player.query.get(int(id))
        item_total = player.price * quantity
        total_price += item_total

        basket_items.append({
            "player": player,
            "quantity": quantity,
            "item_total": item_total
        })

    return render_template("basket.html",
                           basket_items=basket_items,
                           total_price=total_price)
    
@app.route('/remove_item/<int:id>')
def remove_item(id):
    basket = session.get("basket", {})

    id = str(id)

    if id in basket:
        basket[id] -= 1
        
        if basket[id] <= 0:
            basket.pop(id)

    session["basket"] = basket

    return redirect(url_for('view_basket'))

@app.route('/remove_all/<int:id>')
def remove_all(id):
    basket = session.get("basket", {})
    id = str(id)

    if id in basket:
        basket.pop(id)

    session["basket"] = basket
    return redirect(url_for('view_basket'))

@app.route('/clear_basket')
def clear_basket():
    session.pop("basket", None)
    return redirect(url_for('view_basket'))

import re

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Calculates total price
    basket = session.get("basket", {})
    
    total_price = 0
    for id, quantity in basket.items():
        player = Player.query.get(int(id))
        total_price += player.price * quantity

    if request.method == 'POST':
        # Payment Validation
        card_number = request.form.get('card_number', '').replace(" ", "").replace("-", "")
        name = request.form.get('name', '')
        expiry = request.form.get('expiry', '')
        cvv = request.form.get('cvv', '')

        errors = []

        if not card_number.isdigit() or len(card_number) != 16:
            errors.append("Card number must be 16 digits")

        if not name or not expiry or not cvv:
            errors.append("All fields are required")

        if not re.match(r"^\d{3}$", cvv):
            errors.append("CVV must be 3 digits")

        if not re.match(r"^\d{2}/\d{2}$", expiry):
            errors.append("Expiry must be in MM/YY format")

        if errors:
            return render_template('checkout.html', errors=errors, total_price=total_price)

        # clear basket after checkout
        session.pop("basket", None)  
        return render_template('success.html', total_price=total_price)

    return render_template('checkout.html', total_price=total_price)

@app.context_processor
def inject_basket_count():
    # Makes basket count available on all pages
    basket = session.get("basket", {})
    total_items = sum(basket.values())
    return dict(basket_count=total_items)

@app.route('/impact_info')
def impact_info():
    return render_template('impact_info.html')

@app.route('/player/<int:player_id>/review', methods=['POST'])
def add_review(player_id):
    # Saves a new review for a player
    name = request.form.get('name')
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')

    review = Review(
        player_id=player_id,
        name=name,
        rating=rating,
        comment=comment
    )

    db.session.add(review)
    db.session.commit()

    return redirect(url_for('single_player', id=player_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

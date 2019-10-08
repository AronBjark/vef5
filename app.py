from os import urandom
from flask import Flask, render_template as rend, session, request, url_for
from ast import literal_eval

app = Flask(__name__)
app.secret_key = urandom(13)

with open('salsa.txt') as file:
	salsa = literal_eval(file.read())

@app.route('/')
def index():
	return rend('store.html', salsa=salsa)

@app.route('/cart')
def cart():
	cart, cartQuantity, price_sum = [], [], .0
	if 'cart' not in session:
		return rend('cart.html', cart="Cart empty", salsa=salsa, cartQuantity=[], price_sum=price_sum)
	for item in session['cart']:
		cart.append(int(item))
	for item in salsa:
		if int(item['id']) in cart:
			cartQuantity.append([item, cart.count(item['id'])])
	for item in cartQuantity:
		item.append(float(item[0]['value']) * item[1])
		price_sum += float(item[0]['value']) * item[1]
	for item in cartQuantity:
		item[2] = round(item[2], 3)
	price_sum = round(price_sum, 3)
	return rend('cart.html', cart=cart, salsa=salsa, cartQuantity=cartQuantity, price_sum=price_sum)
@app.route('/cart/add/<int:ID>')
def add(ID):
	if 'cart' not in session:
		session['cart'] = []
	cart = session['cart']
	cart.append(salsa[ID]['id'])
	session['cart'] = cart
	print(session['cart'])
	return f'<head><meta http-equiv="Refresh" content="0; url=/#book{ID}"></head>'

@app.route('/clear')
def clear_cart():
	session.pop('cart', None)
	return '<head><meta http-equiv="Refresh" content="2; url=/cart"></head>Karfan er losuð'
@app.route('/remove/<int:ID>')
def remove(ID):
	cart = []
	for item in session['cart']:
		cart.append(int(item))
	for item in cart:
		if item == ID:
			cart.remove(item)
			break
	session['cart'] = cart
	if len(session['cart']) == 0: 
		session.pop('cart', None)
	return '<head><meta http-equiv="Refresh" content="2; url=/cart"></head>removed item from list'

@app.route('/secret')
def secret():
	if 'cart' not in session: 
		session['cart'] = []
	cart = session['cart']
	for item in salsa: 
		cart.append(item['id'])
	session['cart'] = cart
	return '<head><meta http-equiv="Refresh" content="0; url=/cart"></head>'

@app.errorhandler(404)
def error404(error):
	return rend('error.html', ERROR=404)
if __name__ == "__main__":
	app.run(debug=True)

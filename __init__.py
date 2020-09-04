import os
import secrets
from flask import Flask, render_template, flash, abort, redirect, url_for, request
from service import InventoryService
from werkzeug.utils import secure_filename
secret = secrets.token_urlsafe(32)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/images'
app.secret_key = secret

def getApp():
    return app

@app.route("/", methods = ['GET', 'POST'])
def home():
    products = InventoryService().get_products()
    profit = InventoryService().get_profit()
    return render_template("index.html", products= products, profit=profit)

@app.route("/purchase/<product_id>")
def purchase(product_id):
    result = InventoryService().purchase(product_id)
    profit = InventoryService().get_profit()
    if result == "SUCCESSFUL":
        return render_template("message.html", message= "Purchase Successfull!", profit=profit)
    else:
        return render_template("message.html", message= result, profit=profit)

@app.route("/cart/<product_id>")
def cart(product_id):
    product = InventoryService().get_info(product_id)
    profit = InventoryService().get_profit()
    if product == 'Invalid product ID!' and product == "Insufficient stock!":
        return render_template("message.html", message= product, profit=profit)
    
    return render_template("cart.html", imgsource=product[0]["src"], name=product[0]["name"], price=product[0]["price"], product_id=product[0]["id"], profit=profit)

@app.route('/upload')
def upload():
    profit = InventoryService().get_profit()
    return render_template('upload.html', profit=profit)
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    profit = InventoryService().get_profit()
    if request.method == 'POST':
        print(request.form)
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        name = request.form['artname']
        price = request.form['price']
        print("price: ", price)
        price_for = float(price)*100
        print("price*100: ", price_for)
        i, d = divmod(price_for, 1)
        price = i
        stock = request.form['stock']
        result = InventoryService().add_peice(name, f.filename, price, stock)
        if result == "SUCCESSFUL":
            return render_template("message.html", message= "Art Peice added Successfully", profit=profit)
        else:
            return render_template("message.html", message= "Could not add Art Peice", profit=profit)

@app.route("/restock")
def restock():
    InventoryService().initialize()
    profit = InventoryService().get_profit()
    return render_template("message.html", message= "Inventory Restocked", profit=profit)

if __name__ == "__main__":
    InventoryService().initialize()
    app.run(debug=True)
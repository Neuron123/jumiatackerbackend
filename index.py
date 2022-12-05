from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo

app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient("mongodb+srv://admin:Passme123@cluster0.zr4a4r4.mongodb.net/?retryWrites=true&w=majority")

#sign up
@app.route('/signup', methods=['POST'])
def signup():
    db = client["test"]
    collection = db["users"]
    data = request.get_json()
    if collection.find_one({"email": data['email']}):
        return jsonify({
            "status": "701",
            "message": "Email already exists"
            })
    else:
        collection.insert_one(data)
        return jsonify({
            "status": "700",
            "message": "User created"
            })

#login
@app.route('/login', methods=['POST'])
def login():
    db = client["test"]
    collection = db["users"]
    data = request.get_json()
    if collection.find_one({"email": data['email'], "password": data['password']}):
        return jsonify({
            "status": "700",
            "message": "Login successful"
            })
    else:
        return jsonify({
            "status": "701",
            "message": "Invalid credentials"
            })

#check if product exists in database
def check_product(product_url):
    db = client["test"]
    collection = db["product"]
    if collection.find_one({"url": product_url}) is None:
        return False
    else:
        return True

#show products
#get all products from database using the user param from url
@app.route('/products/<useremail>', methods=['GET'])
# @app.route('/products/<string:user>/', methods=['GET'])
def get_products(useremail):
    #get email from the url
    user = useremail
    print("get products")
    print("user =",user)
    mydb = client["test"]
    mycol = mydb["product"]
    products = []
    for x in mycol.find({"user": user}):
        #remove the _id field
        x.pop("_id")
        products.append(x)
    print("products",products)
    return jsonify({'products': products})

@app.route('/api', methods=['POST'])
def api():
    try:
        data = request.get_json()
        print(data)
        product_url = data['url']
        if check_product(product_url):
            print("Product already exists")
            return jsonify({'message': 'exists'})
        else:
            data = {
                "user": data['user'],
                "name": data["name"],
                "price": data["price"],
                "url": data["url"]
            }
            #python client to add data to mongodb test database product collection
            mydb = client["test"]
            mycol = mydb["product"]
            mycol.insert_one(data)
            #exclude _id from the response
            data.pop("_id")
            print("Product added")
            return jsonify({'message': 'success', 'product': data})
    except Exception as e:
        print(e)
        return jsonify({'message': 'error'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
import os
import tensorflow as tf
import json
import numpy as np
import pandas as pd
import base64
import matplotlib.pyplot as plt
from datetime import timedelta
from flask import Flask,jsonify,request, session
from util import Preprocessing
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from database import init,getalluser,registerdb,logindb
from flask_cors import CORS
from waitress import serve
from flask_swagger_ui import get_swaggerui_blueprint

#init flask and sql
app = Flask(__name__)
model = tf.keras.models.load_model('model/mymodel.h5')
CORS(app)
mysql = init(app)

#load tensorflow model
# preprocess = Preprocessing("model.h5")
# prediction_results = preprocess.predict()

#JWT
app.config["JWT_SECRET_KEY"] = "capstone-secret-key" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=90)
jwt = JWTManager(app)


# SWAGGER_URL = '/doc'
# API_URL = '/static/swagger.json'
# SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "Leftover app"
#     }
# )
# app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/', methods=['GET'])
def index():
    #current_user = get_jwt_identity()
    #return jsonify(logged_in_as=current_user), 200
    return "Hello Word this is SEESEA-GLOBALE"

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    pwd = request.form['password']
    try:
        user = logindb(mysql,email,pwd)
        if user != "":
            access_token = create_access_token(identity=email)
            data = {"message": "Login Successful" , "user": user, "access_token" : access_token}
            return jsonify(data),200
        return jsonify({"msg": "Wrong Email or Password"}), 401
    except Exception as e:
         err = jsonify(msg=f'{e}'),500
         return err

# 
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    pwd = request.form['password']
    try:
        return registerdb(mysql,username,email, pwd)
    except Exception as e:
         err = jsonify(msg=f'{e}'),500
         return err

@app.route('/users',methods=['GET'])
def userlist():
    try:
        user = getalluser(mysql)
        return jsonify(user)
    except Exception as e:
         err = jsonify(msg=f'{e}'),500
         return err

@app.route("/predict", methods=['POST'])
def predict():
    # file = '../Model/images/laptop.jpg'
        image = generate_image_from_base64(
            request.form["title"], request.form["body"])
        img = tf.keras.preprocessing.image.load_img(image, target_size=(150, 150))
        x = tf.keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        history = model.predict(images)
        print(history)
        os.remove(get_filename(request.form["title"]))
        predict = ""
        if history[0]>0.5:
            predict = "is a Trash" 
        else:
            predict = "is a Coral"

        return {
            "title": request.form["title"],
            "body": predict
        }
    
def generate_image_from_base64(filename, string):
        file = open('./{filename}.jpg'.format(filename=filename), 'wb')
        file.write(base64.b64decode((string)))
        file.close()
        return './{filename}.jpg'.format(filename=filename)

def get_filename(filename):
        return './{filename}.jpg'.format(filename=filename)

# Logout user endpoint
@app.route("/logout", methods=['GET'])
def logout():
    return {"massage": "Logout successful"}, 200

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=int(os.environ.get('PORT', 80)))
    #app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    #$Env:PORT=4000

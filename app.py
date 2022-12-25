from re import A
from flask import flash
from flask import Flask
from flask import jsonify, make_response

app = Flask (__name__)
@app.route("/")
def welcome():
  return jsonify({"error":"true"})


#try:
 #import controller.userController as userontroller
from controller import *
#except Exception as e:
  #print(e)



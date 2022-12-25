
from datetime import datetime
from typing import final
from flask import request
from app import app
from auth.authModel import authModel
from model.userModel import userModel

obj = userModel()
auth = authModel()



@app.route("/api/user/allusers")
#@auth.token_auth("/api/user/allusers")
def allusers():
    return obj.allusers()

@app.route("/api/user/signup",methods=["POST"])
def signup():
    
    return obj.signup(request.json)

@app.route("/api/user/update",methods=["PUT"])
def update():
    print(request.form)
    return obj.update(request.form)

@app.route("/api/user/delete/<id>",methods=["DELETE"])
def delete(id):
    print(id)
    return obj.delete(id)
@app.route("/api/user/login",methods=["POST"])
def login():
    print(request.json)
    return obj.login(request.json)


@app.route("/api/user/forgetpassword",methods=["POST"])   
def forgetUserpassword(): 
    print(request.json)
    return obj.forgetUserpassword(request.json)

@app.route("/api/user/passwordChange/<id>",methods=["POST"])
def changePassword(id):
 
    return obj.changePassword(request.json,id)
    
     










@app.route("/api/user/<user_id>/upload",methods=["PUT"])
def upload(user_id):
    file=request.files['avater']
    #file.save(f"upload/{file.filename}")

   
    uniqueFileName = str(datetime.now().timestamp()).replace(".","")
    fileNameSplit = file.filename.split(".")
    ext =fileNameSplit[len(fileNameSplit)-1]
    finalFilePath = f"upload/{uniqueFileName}.{ext}"
    file.save(finalFilePath)
    return obj.upload(user_id,finalFilePath)


@app.route("/ap/user/update/<user_id>", methods=['PATCH'])
def profile_update(user_id):
   
    return obj.profile_update(request.form,user_id)

@app.route("/api/user/countries")
def country():
    return obj.countries()

@app.route("/api/user/states/<id>", methods=["POST"])
def state(id):
    return obj.state(id)


@app.route("/api/user/cities/<id>", methods=["POST"])
def city(id):
    return obj.city(id)

@app.route("/api/user/userDetails/<id>")
def userProfile(id):
    return obj.userDetails(id)

@app.route("/api/user/comment",methods=['POST'])
def usercomment():
    return obj.comment(request.form)

@app.route("/api/user/passwordUpdate/<id>",methods=['PUT'])
def  passwordUpdate(id):
    return obj.passwordUpdate(request.form,id)
    

@app.route("/api/user/pagination/<limit>/page/<page>",methods=['GET'])
def  pagination(limit, page):
    print(limit,page)
    return obj.userPagination(limit, page)


    



    



    

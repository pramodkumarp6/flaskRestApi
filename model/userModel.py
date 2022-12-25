from pickle import OBJ
from random import randint
import re
from sys import api_version
from tkinter.tix import Select
from unittest import result
from datetime import datetime,timedelta
from flask import jsonify, make_response, request
import jwt
import mysql.connector
from app import app 
import json
from configs.config import dbconfig
import bcrypt
from flask import *  



class userModel(): 
    def __init__(self):
        try:
           self.con=mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
           self.con.autocommit=True
           self.cur = self.con.cursor(dictionary=True   )
           print("sucessfully")
        except:
            print("some error")
    def allusers(self):
        self.cur.execute("SELECT user_id,name,email,gender,country,state,city,address,created_at FROM users ORDER BY user_id DESC")
        result = self.cur.fetchall()
        if len(result)>0:
             return make_response({"users":result},200)
        else:
             return make_response( {"message":"No Data found"},204)

    def signup(self,data):
       name = data['name']

       if len(name) <3:
           return jsonify({'message':'Name is mandatery'})
       lastname = data['lastname']
       
       if len(lastname) <3:
          return jsonify({'message':'lastname is mandatery '})
       gender = data['gender']

       if len(gender) <1:
         return jsonify({'message':'Gender is mandatery '})

       email = data['email']
       if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
         return jsonify({'massage': 'Invalid email address !'})

       password = data['password']
        
       if len(password) <8:
              return jsonify({'message':'length should be at least 8'})



       country = data['country']
       if len(country) <2:
              return jsonify({'message':'Country is mandatery '})
     




       state = data['state']
       if len(state) <1:
              return jsonify({'message':'state is mandatery '})
     

       city = data['city']
       if len(city) <1:
              return jsonify({'message':'city is mandatery '})



       mobile = data['mobile']
       if len(mobile) <10:
          return jsonify({'message':'Mobile is mandatery '})
      
       address = data['address']

       if len(address) <5:
         return jsonify({'message':'Address is mandatery '})

       
      # hashpassword  = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
     
       self.cur.execute(f"SELECT * from users WHERE email='{data['email']}'")
       result = self.cur.fetchone()
       if self.cur.rowcount>0:
           return jsonify({"error":"true","message":"User Exists!!.."}) 
       else:
        self.cur.execute(f"INSERT INTO users(name, lastname,gender,email,password,country,state,city, mobile, address) VALUES('{data['name']}','{data['lastname']}','{data['gender']}','{data['email']}','{data['password']}','{data['country']}','{data['state']}','{data['city']}','{data['mobile']}','{data['address']}' )")
        self.cur.execute(f"SELECT user_id, email,name,gender,mobile,country,state,city,address,created_at from Users WHERE email='{data['email']}'")
        res = self.cur.fetchone()
        return jsonify({"error":"false","message" :"User Created Successfully!!.."})
      
             


    
    def update(self,data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}',lastname='{data['lastname']}',gender='{data['gender']}',email='{data['email']}',password='{data['password']}',mobile='{data['mobile']}',address='{data['address']}' WHERE user_id={data['id']} ")
        if self.cur.rowcount>0:
            return {"message":"update users sucessfully!!!"}
        else:
            return {"message":"nothing update !!!"}

     
    def delete(self,id):
        self.cur.execute(f" DELETE FROM users where user_id ={id} ")
        if self.cur.rowcount>0:
            return {"message":"users Deleted sucessfully!!!"}
        else:
            return {"message":"nothing to Delete !!!"}


    def login(self,data):
        self.cur.execute(f"SELECT email from  users WHERE email='{data['email']}'")
        result = self.cur.fetchone()
        if self.cur.rowcount>0:
               self.cur.execute(f"SELECT user_id,usertype, email,name,gender,mobile,country,state,city,address FROM users where email='{data['email']}' and password='{data['password']}'")
               result = self.cur.fetchall()
 
               if self.cur.rowcount>0:
                   userData = result[0]
                   print(userData)
                   exptime = datetime.now() + timedelta(minutes=30)
                   exp_epoc_time = exptime.timestamp()
                   payload = {
                              "payload":userData,
                              "exp":int(exp_epoc_time)
                              }
                   print(int(exp_epoc_time))
                   jwtoken = jwt.encode(payload, "Pandey@123", algorithm="HS256")

                   return make_response({"error":"false","message":"login Successfully","users":userData},200)
               else:
                  return make_response({"error":"true","message":"Email & Password Invalid"},200)

        else:
             resp = jsonify({"error":"true","message":"User doesnot exist"})
            
            
             resp.status_code = 200
             return resp

    def forgetUserpassword(self,data):
        email = data['email']
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
             return jsonify({'massage': 'Invalid email address !'})

        self.cur.execute(f"SELECT * from users WHERE email='{data['email']}'")
        result = self.cur.fetchone()
        if self.cur.rowcount>0:
           return jsonify({"error":"true","message":"User Exists!!.."})     

        else:
            return jsonify({"error":"true","message":"email id Is not Exist"})
        
                


    def changePassword(self,data,id):
        

        oldpass =  data['oldPassword']
        



        if len(oldpass) <8:
              return jsonify({'message':'length should be at least 8'})
        newpass =  data['newPassword']
        if len(newpass) <8:
              return jsonify({'message':'length should be at least 8'})

        if(oldpass ==newpass):
         return jsonify({'message':'OldPassword & NewPassword Same'})


       

       

       

       
       
        self.cur.execute(f"SELECT  password from users WHERE user_id='{data['id']}'and password='{data['oldPassword']}'")
        result = self.cur.fetchone()
        
        if self.cur.rowcount>0:
            self.cur.execute(f"UPDATE users SET password='{data['newPassword']}'")
            if self.cur.rowcount>0:
                return make_response({"error":"false","message":"Password Update Successfully"},201)
            else:
                return make_response({"error":"true","message":"old password match"},200)

             
        else:
             return make_response({"error":"true","message":"oldpassword does Not Match"},200)
             
       
    

   
     

             

    def upload(self,user_id,filepath):
        self.cur.execute(f"UPDATE users SET avatar='{filepath}' WHERE user_id={user_id}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Profile upload sucessfully!!!"},200)
        else:
            return make_response({"message":"nothing upload !!!"},304)

    

    def profile_update(self, data, user_id):

        qry ="UPDATE users SET "
        for key in data:

            qry +=  f"{key}='{data[key]}'," 

        qry =qry[:-1] +f" WHERE user_id={user_id}"
        print(qry)
        #UPDATE users SET name='tata', lastname='tata' WHERE user_id=55
        self.cur.execute(qry)
        if self.cur.rowcount>0:
                return {"message":" Users Profile Update sucessfully!!!"}
        else:
            return {"message":"nothing update !!!"}

    def countries(self):
        self.cur.execute("SELECT * FROM countries")
        result = self.cur.fetchall()
        if len(result)>0:
             return make_response({"countries":result},200) 
        else:
             return make_response( {"message":"No Data found"},204)


    def state(self,id):
        self.cur.execute(f"SELECT * FROM states WHERE country_id={id}")
        result = self.cur.fetchall()
        if len(result)>0:
             return make_response({"states":result},200)
        else:
             return make_response( {"message":"No Data found"},204)

    def city(self,id):
        self.cur.execute(f"SELECT * FROM cities WHERE state_id={id}")
        result = self.cur.fetchall()
        if len(result)>0:
             return make_response({"states":result},200)
        else:
             return make_response( {"message":"No Data found"},204)

    def userDetails(self,id):
        self.cur.execute(f"SELECT user_id, name , lastname,email,gender,country,state,city,address FROM users WHERE user_id= {id}")
        result = self.cur.fetchall()
        if len(result)>0:
             return make_response({"usersDetails":result},200)
        else:
             return make_response( {"message":"No Data found"},200) 

    def comment(self,data):
        print(data)
        self.cur.execute(f"INSERT INTO comment(user_id,title, message) VALUES('{data['id']}','{data['title']}','{data['message']}' )")
        return make_response({"message":"comment Created sucessfully !!!"},201)


    def passwordUpdate(self, data,id):


       # self.cur.execute(f"SELECT password FROM users WHERE user_id={id}")
       # result = self.cur.fetchone()
       
        self.cur.execute(f"UPDATE users SET password='{data['newPassword']}'  WHERE user_id={id}")
        #self.cur.execute(f"UPDATE users SET password='{data['newPassword']}'  WHERE user_id={id}")
        if self.cur.rowcount>0:
            #return {"message":"User PasswordChange sucessfully!!!"}

            resp = jsonify({'message' :' User PasswordChange sucessfully!!!'})
            resp.status_code = 200
            return resp
        else:
             resp = jsonify({'message' :' Nothing Update!!!'})
             resp.status_code = 200
             return resp

    def userPagination(self,limit, page):
        limit = int(limit)
        page = int(page)
        start = (page*limit)-limit
        qry = f"SELECT * FROM users Limit {start},{limit}"
      
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
             return make_response({"users":result},200)
        else:
            return make_response( {"message":"No Data found"},204)
           
            


    
     
        

   
        

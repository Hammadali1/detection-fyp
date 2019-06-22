from flask_pymongo import PyMongo
from flask import Flask, jsonify,json,request,render_template
from wtforms import Form, StringField, SubmitField

app = Flask(__name__)


app.config['MONGO_DBNAME']=''
app.config['MONGO_URI']='mongodb://hammad:hammad123@ds351455.mlab.com:51455/data'
mongo = PyMongo(app)


@app.route("/Admin",methods=['POST'])
def AddAdmin():
    if request.method=='POST':
       Uname=request.form['Uname']
       Email=request.form['Email']
       Password=request.form['Password']
       NIC=request.form['NIC']
       mongo.db.admin.insert({'_id':NIC,'uname':Uname,'email':Email,'password':Password})
       return "Successfully add"
                  

@app.route("/Admin",methods=['GET'])
def ShowAdmin():
    if request.method=='GET':
       data=mongo.db.admin.find({}).count()
       if(data==0):
           return "data not found"
       else:
            d = []
            data=mongo.db.admin.find({})
            for i in data:
                d.append({"id":i["_id"] ,"name": i["uname"],"email":i["email"]})
            return (jsonify(d))
                  

@app.route("/Admin/<string:param>",methods=['GET','POST'])
def UpdateAdmin(param):
        
      if request.method=='GET':
        print("enter")
        if (mongo.db.admin.find({'_id': param})):
             d = []
             data=mongo.db.admin.find({'_id':param})
             for i in data:
                 d.append({"id":i["_id"] ,"name": i["uname"],"email":i["email"]})
             return jsonify(d)
        return ('not find')           

      
      if request.method=='POST':
        Uname=request.form['name']
        Id=param
        Message=request.form['email']
        Oldpassword=request.form['oldPassword']
        Newpassword=request.form['newPassword']
        d={}
        data=mongo.db.admin.find({'_id': param})
        for i in data:
          dd={"id":i["_id"] ,"name": i["uname"],"email":i["email"],'password':i["password"]}  
        password=dd['password']
        if (Oldpassword==password):
            if (mongo.db.admin.find({'_id': param})):
              update_query=mongo.db.admin.update_one({"_id": Id},{'$set':{"name":Uname,"email": Message,"password":Newpassword}})
            return jsonify({'msg':"successfull Add"})   
        else:
           return ("wrong password")           
    


if __name__ == "__main__":
    app.run(debug=True)
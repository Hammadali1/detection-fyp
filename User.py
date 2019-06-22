from flask_pymongo import PyMongo
from flask import Flask, jsonify,json,request,render_template
from wtforms import Form, StringField, SubmitField

app = Flask(__name__)


app.config['MONGO_DBNAME']=''
app.config['MONGO_URI']='mongodb://hammad:hammad123@ds351455.mlab.com:51455/data'
mongo = PyMongo(app)


@app.route("/User",methods=['POST'])
def AddUser():
    if request.method=='POST':
       Uname=request.form['Uname']
       Email=request.form['Email']
       Password=request.form['Password']
       NIC=request.form['NIC']

       mongo.db.user.insert({'_id':NIC,'uname':Uname,'email':Email,'password':Password})
       return "Successfully add"
                  
    return render_template('signupUser.html')


@app.route("/User",methods=['GET'])
def ShowUser():
    if request.method=='GET':
       data=mongo.db.user.find({}).count()
       if(data==0):
           return "data not found"
       else:
            d = []
            data=mongo.db.user.find({})
            for i in data:
                d.append({"id":i["_id"] ,"name": i["uname"],"email":i["email"],"password":i["password"]})
            return (jsonify(d))
              
@app.route("/User/<string:param>",methods=['GET','POST'])
def UpdateUser(param):
        
      if request.method=='GET':
        if (mongo.db.user.find({'_id': param})):
             d = []
             data=mongo.db.user.find({'_id':param})
             for i in data:
                 d.append({"id":i["_id"] ,"name": i["uname"],"email":i["email"],"password":i["password"]})
             return jsonify(d)
        return ('not find')           

      
      if request.method=='POST':
        Uname=request.form['name']
        Id=param
        Message=request.form['email']
        password=request.form['password']
        
        if (mongo.db.user.find({'_id': param})):
        
              update_query=mongo.db.user.update_one({"_id": Id},{'$set':{"name":Uname,"email": Message,"password":password}})
              return jsonify({'msg':"successfull Add"})   
                   


@app.route("/User/<string:param>", methods=['DELETE'])
def DeleteUser(param):
    if request.method=='DELETE':
        
        data=mongo.db.user.find({'_id': param})
        ddd={}
        mongo.db.user.delete_one({'_id': param})
        return "deleted"


if __name__ == "__main__":
    app.run(debug=True)
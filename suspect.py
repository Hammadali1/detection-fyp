from flask_pymongo import PyMongo
from wtforms import Form, StringField, SubmitField
from flask import Flask, jsonify,json,request,render_template

app = Flask(__name__)


app.config['MONGO_DBNAME']=''
app.config['MONGO_URI']='mongodb://hammad:hammad123@ds351455.mlab.com:51455/data'
mongo = PyMongo(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/suspect", methods=['POST'])
def upload():
    if request.method=='POST':
        Uname=request.form['name']
        Id=request.form['id']
        Message=request.form['message']#s='img/'+Id
        target = os.path.join(APP_ROOT, 'img/')
        if not os.path.isdir(target):
            os.mkdir(target)
                
        for file in request.files.getlist("img"):
            print(file)
            filename=Id+'.jpg'
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
        
        mongo.db.suspect.insert({"_id": Id,"name":Uname,"message": Message,"Path":destination})
        return jsonify({'msg':"successfull Add"})   
      

@app.route("/suspect", methods=['GET'])
def retrieve():
    if request.method=='GET':
        data = mongo.db.suspect.find({}).count()
        if (data == 0):
            return "data not found"
        else:
            d = []
            data=mongo.db.suspect.find({})
            for i in data:
                image="/".join([target2, i['_id']])
                print(image)
                d.append({"id":i["_id"] ,"name": i["name"],"message":i["message"],'image':i["Path"]})
        
            return jsonify(d)
            

@app.route("/suspect/<string:param>", methods=['DELETE'])
def delete(param):
    if request.method=='DELETE':
        
        data=mongo.db.suspect.find({'_id': param})
        ddd={}
        data=mongo.db.suspect.find({'_id': param})
        for i in data:
          ddd={"id":i["_id"] ,"name": i["name"],"message":i["message"],'Path':i["Path"]}  
        addrr=ddd['Path']
        mongo.db.suspect.delete_one({'_id': param})
        os.remove(addrr)
        return "deleted"
        
@app.route("/suspect/<string:param>", methods=['POST','GET'])
def Update(param):
    if request.method=='GET':
        if (mongo.db.suspect.find({'_id': param})):
             d = []
             data=mongo.db.suspect.find({'_id':param})
             for i in data:
                 d.append({"id":param ,"name": i["name"],"message":i["message"],'Path':i['Path']})
             return jsonify(d)
        return ('not find')                
    if request.method=='POST':
        Uname=request.form['name']
        Id=param
        Message=request.form['message']
        
        d={}
        data=mongo.db.suspect.find({'_id': param})
        for i in data:
          dd={"id":i["_id"] ,"name": i["name"],"message":i["message"],'Path':i["Path"]}  
        addrr=dd['Path']
        target = os.path.join(APP_ROOT, 'img/')

        if not os.path.isdir(target):
            os.mkdir(target)
                
        for file in request.files.getlist("img"):
            os.remove(addrr)
            filename=Id+'.jpg'
            destination = "/".join([target, filename])
            file.save(destination)
        if (mongo.db.suspect.find({'_id': param})):
        
           update_query=mongo.db.suspect.update_one({"_id": Id},{'$set':{"name":Uname,"message": Message,"Path":destination}})
        return jsonify({'msg':"successfull Add"})   
                   

if __name__ == "__main__":
    app.run(debug=True)
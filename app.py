
from flask import Flask

app = Flask(__name__)

@app.route("/suspect", methods=['GET'])
def retrieve():
    if request.method=='GET':
        return ("yahoo")
         
if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask

app = Flask(__name__)

@app.route("/")
def retrieve():
        return "yahoo"
         
if __name__ == "__main__":
    app.run()

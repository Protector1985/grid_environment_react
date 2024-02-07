from flask import Flask, request

from flask_cors import CORS

from lib.Resnet import Resnet

resnet = Resnet()


app = Flask(__name__)

#allow all origins for simplicity
CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/data", methods=["POST"])
def processor():
    if request.method == "POST":
        data = request.json
        data = data['imageURL']
        move = resnet.resnet_processor(data)
        return move
    else:
        return "Can't process GET"
    

if __name__ == "__main__":
    app.run(port=5001, debug=True)
from flask import Flask, request

from flask_cors import CORS

from lib.RL_processor import RL_PROCESSOR

RL = RL_PROCESSOR()


app = Flask(__name__)

#allow all origins for simplicity
CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/data", methods=["POST"])
def processor():
    if request.method == "POST":
        data = request.json
        incoming_move_data = data['data']['data']
        b64_img = data['data']['dataURL']
        move = RL.rl_processor(b64_img, incoming_move_data)
        return move
    else:
        return "Can't process GET"
    

if __name__ == "__main__":
    app.run(port=5001, debug=True)
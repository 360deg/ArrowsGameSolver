from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from core import run_the_hell_machine

app = Flask(__name__)
CORS(app)


@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        new_game_value = request.args.get('newGame', default=None)
        binary_data = request.get_data()
        with open(os.path.join('image.png'), 'wb') as file:
            file.write(binary_data)
        res = run_the_hell_machine(new_game_value)

        return jsonify({'result': res}), 200


if __name__ == '__main__':
    app.run(port=5000)

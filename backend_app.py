import flask
from flask import request, jsonify
import re

app = flask.Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'Backend is ready.'})

@app.route('/get-path', methods=['GET'])
def calculate_path():
    input = request.args.get('input')
    headings = [(0,1), (-1,0), (0,-1), (1,0)]
    index = 0
    # This is record largest absolute value of any coordinate
    # To be used for canvas size optimization
    largest_coord = 0
    cur_position = (0,0)
    # 'S' for starting point
    path = { '0,0': 'S' }
    for char in input:
        if char == 'L':
            index = index + 1 if index < 3 else 0
        elif char == 'R':
            index = index - 1 if index > 0 else 3
        elif char == 'F':
            cur_position = (cur_position[0] + headings[index][0], cur_position[1] + headings[index][1])
            cur_position_key = f'{cur_position[0]},{cur_position[1]}'
            if cur_position_key in path:
                # Duplicate points
                path[cur_position_key] = 'D'
            else:
                # Non-duplicate points
                path[cur_position_key] = 'R'
            bigger_coord = max(abs(cur_position[0]), abs(cur_position[1]))
            if bigger_coord > largest_coord:
                largest_coord = bigger_coord
        else:
            return jsonify({'message': 'invalid text'})

    # 'E' for end point
    path[cur_position_key] = 'E'
    return jsonify({'path': path, 'largest_coord': largest_coord})

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      data = request.files['file'].read()
      str = data.decode('UTF-8')
      # Ensure the file only contains L, R or F
      if re.compile("^[LRF]+$").match(str):
          return str.rstrip()
      else:
          return jsonify({'message': 'File contains invalid text'}), 500

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

app.run()

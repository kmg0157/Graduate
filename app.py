# app.py
from flask import Flask, request, render_template
from show_gps import Map

app = Flask(__name__)
map_generator = Map()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map', methods=['POST'])
def update_map():
    data = request.json
    if data:
        map_generator.read_data(data)
        map_html = map_generator.generate_map_html()
        return map_html
    else:
        return 'No data received', 400

if __name__ == '__main__':
    app.run(debug=True)

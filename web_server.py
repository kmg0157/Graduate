from flask import Flask, request
from show_gps import Map  # 위에서 제공한 Map 클래스 코드를 map_generator.py 파일로 저장하고 임포트합니다.

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        data = request.json
        if data:
            map_instance = Map()
            map_instance.read_data(data)
            map_instance.show_map()
            return 'Map generated and displayed successfully!'
        else:
            return 'No data received', 400
    else:
        return 'Invalid request method', 405

if __name__ == '__main__':
    app.run(debug=True)

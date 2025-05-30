from flask import Flask, jsonify
from datetime import datetime
import pytz
import threading
import time

app = Flask(__name__)

# Biến trạng thái HUD giả lập
hud_state = {
    "speed": 0,
    "distance": 0,
}

def update_hud():
    speed = 50
    distance = 0
    increasing = True
    while True:
        # Tăng giảm tốc độ giả lập từ 0 đến 100 rồi giảm lại
        if increasing:
            speed += 5
            if speed >= 100:
                increasing = False
        else:
            speed -= 5
            if speed <= 0:
                increasing = True
        
        distance += speed * 0.1  # khoảng cách giả lập tăng theo speed
        hud_state["speed"] = int(speed)
        hud_state["distance"] = int(distance)
        time.sleep(1)

@app.route('/hud')
def hud():
    tz = pytz.timezone('Asia/Shanghai')  # múi giờ Trung Quốc
    now = datetime.now(tz)
    return jsonify({
        "speed": hud_state["speed"],
        "clock": now.strftime("%H:%M:%S"),
        "distance": hud_state["distance"]
    })

if __name__ == '__main__':
    # Khởi chạy thread cập nhật HUD động
    thread = threading.Thread(target=update_hud)
    thread.daemon = True
    thread.start()

    # Chạy Flask server
    app.run(host='127.0.0.1', port=80)

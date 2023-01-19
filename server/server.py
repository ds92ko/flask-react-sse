from flask import Flask,jsonify
from flask_sse import sse
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS

# import logging
import datetime

# helper.py에서 가라 데이터 & 업뎃 예정된 시간 가져옴
from helper import get_data, get_schd_time

app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = "redis://localhost:6379"
app.register_blueprint(sse, url_prefix='/events')

# 로깅
# log = logging.getLogger('apscheduler.executors.default')
# log.setLevel(logging.INFO)
# fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
# h = logging.StreamHandler()
# h.setFormatter(fmt)
# log.addHandler(h)

def server_side_event():
  """ Function to publish server side event """
  with app.app_context():
    sse.publish(get_data(), type='dataUpdate') 
                # get_data() => Fake data 리턴해주는 함수
                # type       => event type, 알아서 명명하되 리액트에서 EventSource의 EventListener에 type 파라미터 값이랑 통일시켜줘야 됨
    print("Event Scheduled at ", datetime.datetime.now())

sched = BackgroundScheduler(daemon=True)
sched.add_job(server_side_event,'interval',seconds=get_schd_time())
                                                  # get_schd_time() => interval 시간초
sched.start()

# 리액트에서 처음에 페이지 진입했을 때 한번은 여기로 axios 요청 날림
@app.route('/')
def index():
  return jsonify(get_data())

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)
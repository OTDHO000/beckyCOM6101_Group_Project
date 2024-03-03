from flask import Flask
from flask_cors import CORS
from controller.QueryInfoController import queryinfo


'''
邏輯：用戶在前端發出要求：租金比例，想要開的店，還有想要的產業，還有所屬地區
後端接收到這些資料後，會去資料庫找到符合的空置店鋪（比如：如果店鋪的經緯度在地區範圍以内，而且租金數據在範圍以内，就會被篩選出來）
然後訓練模型會把這些符合資格的空店，各個項目評分
然後把結果回傳回前端
前端會把這些後端分析出來的結果，用地圖的方式呈現出來
'''

app = Flask(__name__) 

app.register_blueprint(queryinfo, url_prefix="/search")

CORS(app)
 
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
    

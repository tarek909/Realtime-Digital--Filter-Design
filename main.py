from flask import Flask , render_template
import numpy as np
import scipy, scipy.signal
import json
from flask_sock import Sock
import cmath

# InputData = np.tan(np.linspace(-np.pi, np.pi, 10))
# xaxis = np.linspace(0, 1, len(InputData))

global poles
poles=[]
global zeros
zeros=[]

global RereceivedData
RereceivedData=[]

DataForRealImag = {
  "Real":[] ,
  "imaginary":[]
}

DataR_I=DataForRealImag

YData = {
  "Value":[]
}
YFiltered=YData

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def index():
    return render_template('index.html')

@sock.route('/echo')
def echo(sock):
    while True:
        YFiltered["Value"].clear()
        data = sock.receive()
        data = json.loads(data)
        if data["type"] == "poles":
            global poles
            poles.clear()
            for i in range(len(data['value'])):
                poles.append(complex(data['value'][i][0],data['value'][i][1]))

        elif data["type"] == "zeros":
            global zeros
            zeros.clear()
            for i in range(len(data['value'])):
                zeros.append(complex(data['value'][i][0],data['value'][i][1]))

        elif data["type"] == "data":
            global RereceivedData
            RereceivedData.clear()
            RereceivedData = list(data["value"])

        b, a = scipy.signal.zpk2tf(zeros, poles, 1)
        YFiltered["Value"] = scipy.signal.lfilter(b, a,RereceivedData).tolist()


        if len(YFiltered["Value"])>0:
            DataR_I["imaginary"].clear()
            DataR_I["Real"].clear()
            for i in range(len(YFiltered["Value"])):
                DataR_I["imaginary"].append(((YFiltered["Value"][i].imag)))
                DataR_I["Real"].append(((YFiltered["Value"][i].real)))
        try:
            FinalYData = json.dumps(DataR_I)
            sock.send(FinalYData)
        except:
            print("error")





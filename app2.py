from flask import Flask,render_template, Response, request, redirect, url_for
from pyfirmata import Arduino
from pyfirmata.util import Iterator
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
app = Flask(__name__)

board = Arduino('COM3')

iterator = Iterator(board)
iterator.start()

pin_a0 = board.get_pin('a:0:i')
pin_a1 = board.get_pin('a:1:i')
pin_a2 = board.get_pin('a:2:i')
pin_a3 = board.get_pin('a:3:i')
pin_a4 = board.get_pin('a:4:i')
pin_a5 = board.get_pin('a:5:i')
led_13 = board.get_pin('d:13:o')

@app.route("/")
@app.route("/home")
def home():
    return render_template("index2.html")

@app.route("/status",methods = ['POST',"GET"])
def status():
    color = "ff0000";
    if __name__ == '__main__':
        color = "66ff00"
        version = str(board.get_firmata_version())
        analogs = []
        analogs.append(str(pin_a0.mode))
        analogs.append(str(pin_a1.mode))
        analogs.append(str(pin_a2.mode))
        analogs.append(str(pin_a3.mode))
        analogs.append(str(pin_a4.mode))
        analogs.append(str(pin_a5.mode))
        analogs = np.array(analogs)
        analogs=["INPUT" if x=="0" else x for x in analogs]
        analogs=["OUTPUT" if x=="1" else x for x in analogs]
        analogs=["ANALOG" if x=="2" else x for x in analogs]
        analogs=["PWM" if x=="3" else x for x in analogs]
        pin_a0_r = analogs[0]
        pin_a1_r = analogs[1]
        pin_a2_r = analogs[2]
        pin_a3_r = analogs[3]
        pin_a4_r = analogs[4]
        pin_a5_r = analogs[5]
    return render_template("index2.html",color=color,
                           version=version,
                           pin_a0_r=pin_a0_r,
                           pin_a1_r=pin_a1_r,
                           pin_a2_r=pin_a2_r,
                           pin_a3_r=pin_a3_r,
                           pin_a4_r=pin_a4_r,
                           pin_a5_r=pin_a5_r)


@app.route("/result",methods = ['POST',"GET"])
def result():
    time.sleep(1)
    t = pin_a0.read()
    t1 = t*(5000/1024)*1000
    temp = np.round((t1 - 500)/10,2)
    Temp_unit = "degrees Celcius"
    return render_template("index2.html",name=temp,Temp_unit=Temp_unit)

@app.route("/resultF",methods = ['POST',"GET"])
def resultF():
    time.sleep(1)
    t = pin_a0.read()
    t1 = t*(5000/1024)*1000
    temp = np.round((t1 - 500)/10,2) 
    temp = temp*(9/5) + 32
    Temp_unit = "degrees Farenheit"
    return render_template("index2.html",name=temp,Temp_unit=Temp_unit)

@app.route("/resultK",methods = ['POST',"GET"])
def resultK():
    time.sleep(1)
    t = pin_a0.read()
    t1 = t*(5000/1024)*1000
    temp = np.round((t1 - 500)/10,2) + 273.15
    Temp_unit = "Kelvin"
    return render_template("index2.html",name=temp,Temp_unit=Temp_unit)

@app.route("/magnet2s",methods = ['POST',"GET"])
def magnet2s():
    time.sleep(1)
    t = []
    for i in range(0,20):
        t.append(pin_a1.read())
        time.sleep(0.1)
    t = np.min(t)
    if t<0.2:
        mag_result = "Magnetic Field Detected!"
    else:
        mag_result = "No Magnetic Field Detected"
    return render_template("index2.html",mag=mag_result,mag_result=mag_result)


@app.route("/magnet4s",methods = ['POST',"GET"])
def magnet4s():
    time.sleep(1)
    t = []
    for i in range(0,40):
        t.append(pin_a1.read())
        time.sleep(0.1)
    t = np.min(t)
    if t<0.2:
        mag_result = "Magnetic Field Detected!"
    else:
        mag_result = "No Magnet Detected"
    return render_template("index2.html",mag=mag_result,mag_result=mag_result)

@app.route("/Tplot",methods = ['POST',"GET"])
def Tplot():
    time.sleep(1)
    s = []
    for i in range(0,30):
        t = pin_a0.read()
        temp = (((t*(5000/1024)*1000)- 500)/10)
        s.append(temp)
        time.sleep(1)

    s = pd.Series(s)
    fig, ax = plt.subplots()
    s.plot()
    ax.legend(['Temperature reading'])
    ax.set_xlabel('seconds')
    ax.set_ylabel('Centigrade')
    count = np.random.randint(1,100000)
    fig.savefig('static/my_plot'+str(count)+'.png') 
    time.sleep(3)
    image = "Temperature as a function of time"
    return render_template("index2.html",image=image,count=count)


@app.route("/Mplot",methods = ['POST',"GET"])
def Mplot():
    time.sleep(1)
    t = []
    for i in range(0,100):
        t.append(pin_a1.read())
        time.sleep(0.2)
    s = np.array(t)
    s=[1 if x<0.1 else 0 for x in s]
    s = pd.Series(s)
    print(s)
    fig, ax = plt.subplots()
    s.plot()
    ax.legend([0, 1], ['No Magnet Detected', 'Magnet Detected'])
    ax.set_xlabel('seconds')
    ax.set_ylabel('Magnetic Field (Boolean)')
    count = np.random.randint(1,100000)
    fig.savefig('static/my_plotM'+str(count)+'.png') 
    time.sleep(3)
    imageM = "Magnetic Field (Boolean)"
    return render_template("index2.html",imageM=imageM,count=count)

@app.route("/LED",methods = ['POST',"GET"])
def LED():
    for x in range(0,200):
        led_13.write(1)
        print('Led ON')
        time.sleep(0.02)
        led_13.write(0)
        print('Led OFF')
        time.sleep(0.02)
    image = "LED On"
    return render_template("index2.html",image=image)

@app.route("/LED2",methods = ['POST',"GET"])
def LED2():
    for x in range(0,20):
        led_13.write(1)
        print('Led ON')
        time.sleep(0.2)
        led_13.write(0)
        print('Led OFF')
        time.sleep(0.2)
        time.sleep(0.3)
    image = "LED Off"
    return render_template("index2.html",image=image)

@app.route("/LED3",methods = ['POST',"GET"])
def LED3():
    for x in range(0,10):
        led_13.write(1)
        time.sleep(1)
        led_13.write(0)
        time.sleep(0.5)
        led_13.write(1)
        time.sleep(0.5)
        led_13.write(0)
        time.sleep(1)
    image = "LED Just blinked 10 times"
    return render_template("index2.html",image=image)



@app.route("/stats1",methods = ['POST',"GET"])
def stats1():
    time.sleep(1)
    s = []
    for t in range(1,31):
        t = pin_a0.read()
        temp = (((t*(5000/1024)*1000)- 500)/10)
        s.append(temp)
        time.sleep(1)
    mean = np.mean(s)
    std = np.std(s)
    var = std**2
    range1 = max(s)-min(s)
    
    row_headers = ['Mean','Std','var','Range']
    column_headers = ['STATS']
    cell_text = [[str(mean)],[str(std)],[str(var)],[str(range1)]]
    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    fig, ax = plt.subplots()
    plt.axis("off")
    the_table = plt.table(cellText=cell_text,
                      rowLabels=row_headers,
                      rowColours=rcolors,
                      rowLoc='right',
                      colColours=ccolors,
                      colLabels=column_headers,
                      loc='center')
    count = np.random.randint(1,100000)
    fig.savefig('static/my_plot'+str(count)+'.png') 
    time.sleep(3)
    image = "Temperature statistics below over the last 30 seconds"
    return render_template("index2.html",image=image,count=count)

@app.route("/stats2",methods = ['POST',"GET"])
def stats2():
    time.sleep(1)
    s = []
    for t in range(1,61):
        t = pin_a0.read()
        temp = (((t*(5000/1024)*1000)- 500)/10)
        s.append(temp)
        time.sleep(1)
    mean = np.mean(s)
    std = np.std(s)
    var = std**2
    range1 = max(s)-min(s)
    
    row_headers = ['Mean','Std','var','Range']
    column_headers = ['STATS']
    cell_text = [[str(mean)],[str(std)],[str(var)],[str(range1)]]
    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    fig, ax = plt.subplots()
    plt.axis("off")
    the_table = plt.table(cellText=cell_text,
                      rowLabels=row_headers,
                      rowColours=rcolors,
                      rowLoc='right',
                      colColours=ccolors,
                      colLabels=column_headers,
                      loc='center')
    count = np.random.randint(1,100000)
    fig.savefig('static/my_plot'+str(count)+'.png') 
    time.sleep(3)
    image = "Temperature statistics below over the last 1 minutes"
    return render_template("index2.html",image=image,count=count)

@app.route("/stats3",methods = ['POST',"GET"])
def stats3():
    time.sleep(1)
    s = []
    for t in range(1,301):
        t = pin_a0.read()
        temp = (((t*(5000/1024)*1000)- 500)/10)
        s.append(temp)
        time.sleep(1)
    mean = np.mean(s)
    std = np.std(s)
    var = std**2
    range1 = max(s)-min(s)
    
    row_headers = ['Mean','Std','var','Range']
    column_headers = ['STATS']
    cell_text = [[str(mean)],[str(std)],[str(var)],[str(range1)]]
    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    fig, ax = plt.subplots()
    plt.axis("off")
    the_table = plt.table(cellText=cell_text,
                      rowLabels=row_headers,
                      rowColours=rcolors,
                      rowLoc='right',
                      colColours=ccolors,
                      colLabels=column_headers,
                      loc='center')
    count = np.random.randint(1,100000)
    fig.savefig('static/my_plot'+str(count)+'.png') 
    time.sleep(3)
    image = "Temperature statistics below over the last 5 minutes"
    return render_template("index2.html",image=image,count=count)

@app.route("/stats4",methods = ['POST',"GET"])
def stats4():
    time.sleep(1)
    s = []
    for t in range(1,601):
        t = pin_a0.read()
        temp = (((t*(5000/1024)*1000)- 500)/10)
        s.append(temp)
        time.sleep(1)
    mean = np.mean(s)
    std = np.std(s)
    var = std**2
    range1 = max(s)-min(s)
    
    row_headers = ['Mean','Std','var','Range']
    column_headers = ['STATS']
    cell_text = [[str(mean)],[str(std)],[str(var)],[str(range1)]]
    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    fig, ax = plt.subplots()
    plt.axis("off")
    the_table = plt.table(cellText=cell_text,
                      rowLabels=row_headers,
                      rowColours=rcolors,
                      rowLoc='right',
                      colColours=ccolors,
                      colLabels=column_headers,
                      loc='center')
    count = np.random.randint(1,100000)
    fig.savefig('static/my_plot'+str(count)+'.png') 
    time.sleep(5)
    image = "Temperature statistics below over the last 10 minutes"
    return render_template("index2.html",image=image,count=count)



@app.route("/pinread",methods = ['POST',"GET"])
def pinread():
    s = []
    for x in range(0,10):
        time.sleep(1)
        x = pin_a0.read()
        s.append(x)
    s = pd.Series(s)
    fig, ax = plt.subplots()
    s.plot()
    ax.legend(['pin A0'])
    ax.set_ylabel('Raw Pin Data')
    ax.set_xlabel('seconds')
    count = np.random.randint(1,100000)
    fig.savefig('static/my_plot'+str(count)+'.png') 
    df = pd.DataFrame(s)
    df.to_csv('ArduinoPinData.csv')
    image = "A CSV of this data can now be found in the route folder named ArduinoPinData.csv"
    return render_template("index2.html",image=image,count=count)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5100)
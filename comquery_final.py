import json
import tkinter as tk
import serial
import time
import threading
import mysql.connector
import calendar
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import requests
from requests.structures import CaseInsensitiveDict
from tkcalendar import Calendar
from datetime import datetime, timedelta
from datetime import time as taim
from tktimepicker import SpinTimePickerModern, AnalogThemes
from tktimepicker import constants
from tkinter import *
from tkinter import ttk
from random import uniform
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#### Descomentar si se quiere recibir los datos en tiempo real

#sport = serial.Serial("COM3",9600, timeout=1.0)
#time.sleep(2)

dbtable = 'datas'

mysqlcon = {
        'host':'localhost',
        'port':'3306',
        'user':'myshs',
        'password':'dla.2002/mysqli',
        'database':'jsondata'
    }

global tablilla, grafica
tablif = False
realtt = False
isReceiving = False
isRun = False
value = 0.0


def plotData(self, Samples, lines):
    global value
    data.append(value)
    lines.set_data(range(Samples), data)

def showdata():
    conn,cursor = conex()
    ress = select(cursor)
    print(ress)
    global tablif, tablilla
    if(tablif==True):
        tablilla.destroy()
        tablif=False
    else:
        tablilla = showtabla()
        tables(cursor,tablilla)
        tablilla.place(x=10,y=220)
        tablif=True
    cursor.close()

def togles():
    global continues
    if togle.config('text')[-1]=='Insert Activo':
        togle.config(text='Insert Inactivo')
        print("No")
        continues=False
    else:
        togle.config(text='Insert Activo')
        continues=True
        print("Si")

continues = True

def dorequst():
    url = "http://localhost:3000/api/saci"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    while True:
        if(continues):
            data = {"temp":str(uniform(5,15)),"dist":str(uniform(5,15))}
            resp = requests.post(url, json=data)
            print(resp)
        time.sleep(1)

def insertest():
    while True:
        conn,cursor = conex()
        query = 'INSERT INTO '+dbtable+' (peso,distancia) VALUES ('+str(uniform(5,15))+','+str(uniform(0,15))+')'
        if(continues==True):
            cursor.execute(query)
            conn.commit()
            print('Insertado')
        else:
            print('No válido para insertar')
        cursor.close()
        time.sleep(1)

def insertor():
    global continues, gram, cent
    print(continues)
    conn,cursor = conex()
    if (confirme==True & continues==True):
        query = 'INSERT INTO '+dbtable+' (peso,distancia) VALUES ('+gram+','+cent+')'
        cursor.execute(query)
        conn.commit()
        print('Insertado')
    else:
        print('No válido para inserción')
    cursor.close()

def conex():
    try:
        conn = mysql.connector.connect(**mysqlcon)
        print('Conexion exitosa')
        curs = conn.cursor()
        return conn, curs
    except mysql.connector.Error as error:
        print('Fallo la conexion a mysql: '.format(error))
        return

def select(cursor):
    regs = ''
    cursor.execute(getparams())
    for x in cursor:
        regs += "peso: "+str(x[1])+" distancia: "+str(x[2])+"\n"
    return regs

def tables(cursor,tabl):
    cursor.execute(getparams())
    tabl
    for x in cursor:
        tabl.insert(parent="",index='end',values=(str(x[1]),str(x[2])))

def showtabla():
    tabla = ttk.Treeview(root)
    tabla["columns"] = ("peso","distancia")
    tabla.column("#0",width=0,stretch=NO)
    tabla.column("peso",width=80)
    tabla.column("distancia",width=80)
    tabla.heading("#0",anchor=CENTER)
    tabla.heading("peso",text="PESO",anchor=CENTER)
    tabla.heading("distancia",text="DISTANCIA",anchor=CENTER)
    return tabla

def multidates():
    horafin = taim(Hora_fin.time()[0],Hora_fin.time()[1])
    horaini = taim(Hora_ini.time()[0],Hora_ini.time()[1])
    initihour = str(cal.selection_get())+ " " + str(horaini)
    finalhour = str(cal.selection_get())+ " " + str(horafin)
    fechaini = datetime.strptime(initihour, '%Y-%m-%d %H:%M:%S')
    fechafin = datetime.strptime(finalhour, '%Y-%m-%d %H:%M:%S')
    return str(fechaini),str(fechafin)

def getparams():
    fechaini,fechafin = multidates()
    selector = "SELECT * FROM "+dbtable+" WHERE fechareg BETWEEN '"+fechaini+"' AND '"+fechafin+"'"
    print(selector)
    return selector

global anim, data

def showreal():
    global value, anim, data
    samples = 100
    data = collections.deque([0] * samples, maxlen=samples)
    sampleTime = 100
    xmin = 0
    xmax = samples
    ymin = 0
    ymax = 20
    fig = plt.figure(facecolor='0.94')
    ax = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))
    plt.title("Grafica en tiempo real")
    ax.set_xlabel("Muestras")
    ax.set_ylabel("Distancia")
    lines = ax.plot([], [])[0]
    canvas = FigureCanvasTkAgg(fig, master=root)
    anim = animation.FuncAnimation(fig, plotData, fargs=(samples,lines), interval=sampleTime,cache_frame_data=False)
    return canvas._tkcanvas

def realtime():
    global realtt, grafica, isRun, continues
    if(realtt==True & continues==True):
        grafica.destroy()
        isRun = False
        realtt=False
    else:
        grafica = showreal()
        grafica.place(x=180,y=240)
        realtt=True
        isRun = True

def obten():
    while True:
        arduinoo = sport.readline().decode('utf-8')        
        try:
            global confirme, cent, gram
            confirme = True
            datos = json.loads(arduinoo)
            cent = datos["cent"]
            pul = datos["inch"]
            libr = datos["lbr"]
            gram = datos["grs"]
            
            if(isRun):
                value = cent
                isReceiving = True
            
            if opt1.get() == 1:
                dato0.set(cent)
            else:
                dato0.set(pul)
            
            if opt2.get() == 1:
                dato1.set(gram)
            else:
                dato1.set(libr)
        except json.JSONDecodeError as e:
            datos = e
            confirme = False
        confirme = True
        #insertor()
        print(datos)
        time.sleep(1)

#### descomentar si se quiere recibir las mediciones en tiempo real

thread = threading.Thread(target = dorequst,daemon = True)
thread.start()

def close():
    thread.join()
    root.quit()
    root.destroy()

global dato0, dato1

root=tk.Tk()
root.wm_protocol('WM_DELETE_WIMDOW',close)
root.geometry("800x800")
root.title("Lectura de datos")

initialdate = tk.StringVar()
finaldate = tk.StringVar()
dato0 = tk.StringVar()
dato1 = tk.StringVar()
infos = tk.StringVar()
opt1 = IntVar()
opt2 = IntVar()

ttk.Label(root,text = "Distancia: ").place(x=10,y=10)
ttk.Label(root,text = "Peso: ").place(x=10,y=70)

centim = ttk.Entry(root,width=25,textvariable = dato0,state='readonly').place(x=10,y=40)
pulgad = ttk.Entry(root,width=25,textvariable = dato1,state='readonly').place(x=10,y=100)

selce = ttk.Button(root,width=25, text='Mostrar / Ocultar', command=showdata)
togle = ttk.Button(root,width=25, text='Activar / Desactivar', command=togles)
realt = ttk.Button(root,width=25, text='Tiempo real', command=realtime)
selce.place(x=10,y=130)
togle.place(x=10,y=160)
realt.place(x=10,y=190)

bot1 = ttk.Radiobutton(root, text='cm',value=1,variable = opt1)
bot2 = ttk.Radiobutton(root, text='Pul',value=2,variable = opt1)
bot3 = ttk.Radiobutton(root, text='Grs',value=1,variable = opt2)
bot4 = ttk.Radiobutton(root, text='Lbr',value=2,variable = opt2)
bot1.grid(column=0,row=5, columnspan=3)
bot2.grid(column=1,row=5, columnspan=3)
bot3.grid(column=0,row=5, columnspan=3)
bot4.grid(column=1,row=5, columnspan=3)
bot1.place(x=180,y=40)
bot2.place(x=240,y=40)
bot3.place(x=180,y=100)
bot4.place(x=240,y=100)

cal = Calendar(root, selectmode = 'day',year = 2023, month = 2, day = 22)
cal.place(x=300,y=40)

picker_conf = {
    "bg":"#ffffff",
    "height":1,
    "fg":"#000000",
    "font":("Microsoft Tai Le", 12),
    "hoverbg":"#ffffff",
    "hovercolor":"#000000",
    "clickedbg":"#ffffff",
    "clickedcolor":"#000000"
    }
picker_cf = {
    "bg":"#404040",
    "height":1,
    "fg":"#ffffff",
    "font":("Times", 16),
    "hoverbg":"#404040",
    "hovercolor":"#d73333",
    "clickedbg":"#2e2d2d",
    "clickedcolor":"#d73333"
    }

Hora_ini = SpinTimePickerModern(root)
Hora_ini.addAll(constants.HOURS24)
Hora_ini.configureAll(**picker_conf)
Hora_ini.configure_separator(bg="#ffffff", fg="#000000")
Hora_ini.place(x=580,y=40)

Hora_fin = SpinTimePickerModern(root)
Hora_fin.addAll(constants.HOURS24)
Hora_fin.configureAll(**picker_conf)
Hora_fin.configure_separator(bg="#ffffff", fg="#000000")
Hora_fin.place(x=580,y=100)

ttk.Label(root,text = "Inicio: ").place(x=580,y=10)
ttk.Label(root,text = "Fin: ").place(x=580,y=70)

root.mainloop()

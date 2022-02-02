#Name of the module: AB2_programming
#Date of module creation: 2022/01/18
#Author of the module: Amador Fernández Carrión
#Modification history: 2022/02/01
#Synopsis of the module about what the module does: to do list supported by a database 
#Different functions supported in the module along with their input output parameters:no 
#Global variables accessed or modified by the module: none

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os.path
import sqlite3
import datetime


########################################################### BASE DEL PROYECTO ###########################################################
#sobre estas especificaciones son las que determinan las características del interfaz creado por el tkinter,como su tamaño, fondo y capacidad de ser aumentado.
root = Tk()
root.geometry("550x405")
root.resizable(width=TRUE,height=TRUE)
root.config(bg="#312738")


############################################################ PROCESOS ###########################################################

#linkbase es la funcion principal que conecta a la base de datos con la información aportada en la interfaz para realizar una creación y adición a la base (para esto se emplea la biblioteca de os.path)
def LinkBase():
    if not os.path.exists("tareas"):      
        link=sqlite3.connect('tareas')
        cursor=link.cursor()
        cursor.execute("""
                CREATE TABLE "lastareas"(
                    "Orden" INTEGER ,
                    "Tarea" VARCHAR ,
                    "Descripción" VARCHAR,
                    "Fecha de inclusión" VARCHAR,
                    "Deadline/Último día" VARCHAR,
                    PRIMARY KEY ("Orden"AUTOINCREMENT))
                 """)
        messagebox.showinfo("tarea nueva"," lista comenzada")
    else:
        messagebox.showwarning("Base ya creada","Conectando con la base")

    link=sqlite3.connect("tareas")
    cursor=link.cursor()
    cursor.execute('SELECT * FROM lastareas ')
    tareas=cursor.fetchall()
    cursor.close()
    link.close()
    if tareas !=[]:
        base = Toplevel(root)
        List= ttk.Treeview (base, columns=("1","2","3","4","5"))
        List.heading("1", text="Orden")
        List.heading("2", text="Tareas")
        List.heading("3", text="Descripción")
        List.heading("4", text="Fecha de adición")
        List.heading("5", text="Deadline/Último día")
        List.column('#0', stretch=YES, minwidth=100, )
        for tarea in tareas:
            List.insert('','end',values=tarea)
        List.pack()
        Button(base, text="OK", command=base.destroy).pack()
#además, el uso de la biblioteca de ttk.treeview nos permite realizar una ventana de visualización de la base de datos     


#esta función se encarga de eitar los datos recopilados en el interfaz principal, para su modificación en la base de datos (mediante una tupla)
def editar_tarea():         
    tupla=(tarea.get(),
            Descripción.get("1.0",END),
            fecha.get(),
            Deadline.get(),
            Orden.get())
    link=sqlite3.connect("tareas")
    cursor=link.cursor()
    cursor.execute("""UPDATE lastareas SET Tarea=?,
                             Descripción=?,
                             Fecha de adición=?,
                             Deadline/Último día=?,
                             WHERE Orden=?""",tupla )
                             
    link.commit()
    cursor.close()
    link.close()
    messagebox.showinfo("lista","Tarea editada exitosamente")


#eliminar_tarea se encarga de, como dice el nombre, eliminar la tarea seleccionada mediante la interfaz. esta queda determinada por el número del orden que se le ha asignado
def eliminar_tarea_de_lista():  
    tupla=(Orden.get())
    link=sqlite3.connect("tareas")
    cursor=link.cursor()
    cursor.execute("""DELETE FROM lastareas WHERE "Orden"=?""", tupla)
    link.commit()
    cursor.close()
    link.close()
    messagebox.showinfo("tarea completada", "La tarea se ha retirado de tu lista, bien hecho.")


#esta función se encarga de transferir los datos recopilados en el interfaz principal, para su inserción en la base de datos
def Añadir_tarea():
    splitdate= fecha.get()
    esunafecha = True
    splitdeadline= Deadline.get()
    esunadeadline = True

    try:
      año,mes,día,  = splitdate.split('/') # formato AAAA-MM-DD
    except ValueError:
        esunafecha = False

    if esunafecha:
        try:
            datetime.datetime(int(año), int(mes), int(día)) 
        except ValueError:
            esunafecha = False
    else:
        messagebox.showwarning("Error", "Esto no es una fecha")

    try:
      día,mes,día,  = splitdeadline.split('/') #formato AAAA-MM-DD
    except ValueError:
        esunadeadline = False

    if esunadeadline:
        try:
            datetime.datetime(int(año), int(mes), int(día)) 
        except ValueError:
            esunadeadline = False
    else:
        messagebox.showwarning("Error", "Esto no es una fecha")

    tupla = ()
    if esunafecha is True and esunadeadline is True:

        tupla=(tarea.get(),
         Descripción.get("1.0",END),
            fecha.get(),
            Deadline.get(),)
        link=sqlite3.connect("tareas")
        cursor=link.cursor()
        cursor.execute("""INSERT INTO lastareas
                VALUES(NULL,?,?,?,?)""",tupla)
        link.commit()
        messagebox.showinfo("Lista","Tarea insertada en la lista")
    else: 
        pass

#esta es simple, cierra el programa con un aviso por si este es cerrado por error
def CerrarTODOLIST():
    if messagebox.askquestion("Cerrar programa","¿Quiere salir de la aplicación? Las tareas no guardadas se perderán.")=="yes":
        root.destroy()



########################################################### ENTRADAS DE INFORMACIÓN ###########################################################

#skyline es un marco sobre el que se colocan los diferentes entrys de datos, junto a sus etiquetas que determinan el tipo de dato a introducir
skyline =Frame(root)
skyline.pack()
skyline.config(bg="#044687")


Orden=StringVar()
tarea=StringVar()
fecha=StringVar()
Deadline=StringVar()


#aquí se introduce el orden de la variable (según se vallan añadiendo)
Orden =Entry(skyline, textvariable=Orden)
Orden.grid(row=0, column=1)
Orden.config(font="arial",bg="#69fac5")

#aquí se introduce el nombre de la tarea a anotar
tarea =Entry(skyline, textvariable=tarea)
tarea.grid(row=1, column=1)
tarea.config(font="arial",bg="#69fac5")

#aquí se introduce la descripción de la tarea 
Descripción= Text(skyline, width = 30, height=8)
Descripción.grid(row=2, column=1)
Descripción.config(font="sans",bg="#69fac5")

#aquí se introduce la fecha de creación
fecha =Entry(skyline,width=10, textvariable=fecha)
fecha.grid(row=3, column=1)
fecha.config(font="sans",bg="#69fac5")

#aquí se introduce el último día para completar la tarea
Deadline =Entry(skyline,width=10, textvariable=Deadline)
Deadline.grid(row=4, column=1)
Deadline.config(font="sans",bg="#69fac5")


############################################################ ETIQUETAS DE LAS ENTRADAS ###########################################################


#la etiqueta muestra el tipo de dato a introducir en el entry al que acompaña
etiqueta=Label(skyline, text="Orden:")
etiqueta.grid(row=0, column=0, sticky="e", padx=10, pady=10)


etiqueta=Label(skyline, text="Nombre de la tarea:")
etiqueta.grid(row=1, column=0, sticky="e", padx=10, pady=10)


etiqueta=Label(skyline, text="Fecha de introducción:")
etiqueta.grid(row=3, column=0, sticky="e", padx=10, pady=10)


etiqueta=Label(skyline, text="Deadline/último día:")
etiqueta.grid(row=4, column=0, sticky="e", padx=10, pady=10)


etiqueta=Label(skyline, text="Descripción:")
etiqueta.grid(row=2, column=0, sticky="e", padx=10, pady=10)



############################################################ BOTONES ###########################################################
#downtown es otro marco sobre el que se colocan los diferentes botones,este se encuentra en el inferior de la interfaz, para la distinción entre entradas de datos y procesos a realizar
downtown=Frame(root)
downtown.pack()
downtown.config(bg="#a87f27")

#este botón ejecuta la función antes mencionada
añadir=Button(downtown, text="Añadir tarea",command=Añadir_tarea)
añadir.grid(row=1, column=0, sticky="e", padx=10, pady=10)

#este botón ejecuta la función antes mencionada
actualiza_base=Button(downtown, text="Actualizar la lista",command=editar_tarea)
actualiza_base.grid(row=1, column=2, sticky="e", padx=10, pady=10)

#este botón ejecuta la función antes mencionada
Completar=Button(downtown, text="Completar tarea",command=eliminar_tarea_de_lista)
Completar.grid(row=1, column=3, sticky="e", padx=10, pady=10)

#este botón ejecuta la función antes mencionada
conectar=Button(downtown, text="conectar a la base",command=LinkBase)
conectar.grid(row=1, column=4, sticky="e", padx=10, pady=10)

#este botón ejecuta la función antes mencionada
Salir=Button(downtown, text="SALIR",command=CerrarTODOLIST)
Salir.grid(row=1, column=5, sticky="e", padx=10, pady=10)


root.mainloop()   
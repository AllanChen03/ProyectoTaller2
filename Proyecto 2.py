from tkinter import *
import tkinter as tk
import os
import threading
import random
import time

about ="""
-------------------------------------------------------
Instituto Tecnológico de Costa Rica
Taller a la programación
Semestre 1
Grupo 4
-------------------------------------------------------

Profesor: Luis Barboza Artavia
Estudiantes:
Marianna Méndez Solano
Li Hao Allan Chen Liang
Carné:
2021142221
2019049482
Fecha de entrega: 23 de Junio del 2021
Versión de Python: 3.9.2
Pais de elaboracion: Costa Rica
-------------------------------------------------------
"""
def load_image(nombre):
    path = os.path.join('/Users/chain03/Documents/Cursos/Taller/Proyecto 2',nombre)  #Path 
    image = PhotoImage(file = path)
    return image

class Ventana_Principal:
    def __init__(self,master):

        self.canvas = Canvas(master, width = 500, height = 500, highlightthickness = 0, bg = 'black')
        self.canvas.place(x=0,y=0)

        self.fondo = load_image('Fondo.png')
        self.label_fondo = Label(self.canvas,bg = 'black', image = self.fondo)
        self.label_fondo.place(x = 0, y = 0)

        self.logo = load_image('logo.png')
        self.label_logo = Label(self.canvas,bg = 'black', image = self.logo)
        self.label_logo.place(x = 150, y = 50)
        
        
        self.name_entry = Entry(self.canvas)
        self.name_entry.place(x=230,y=240, width = 120, height = 30)

        #Label "Digite su nombre"
        self.label_name = Label(self.canvas, text = "Digite su nombre:", bg = 'black', fg = 'white', font = ("Arial",14))
        self.label_name.place(x= 100, y = 245)

        self.button_play = Button(self.canvas, text = "Play",bg="#38EB5C",fg = 'black', command = self.verificacion)
        self.button_play.place(x = 230, y = 360)
        
        #Select the level 1 for default
        selection.set(1)
        self.best_score = Best_Score

        #Radio Buttons
        self.Radio_level1 = Radiobutton(self.canvas, text = "Level 1",bg = 'black', fg = 'white',variable=selection,value=1) 
        self.Radio_level1.place(x=120, y = 300)

        self.Radio_level2 = Radiobutton(self.canvas, text = "Level 2",bg = 'black', fg = 'white',variable=selection,value=2)
        self.Radio_level2.place(x=200, y = 300)

        self.Radio_level3 = Radiobutton(self.canvas, text = "Level 3",bg = 'black', fg = 'white',variable=selection,value=3)
        self.Radio_level3.place(x=280, y = 300)

        self.button_about = Button(self.canvas, text = "About",bg="#38EB5C",fg = 'black', command = self.about)
        self.button_about.place(x=20, y= 460)

        self.button_exit = Button(self.canvas, text = "Exit", bg = "black", command = self.exit_ventana)
        self.button_exit.place(x=450, y=460)

        self.button_best_score = Button(self.canvas, text = "Score", bg = "black", command = self.best_score)
        self.button_best_score.place(x=80, y = 460)
        

    def about(self):

        self.about = Toplevel()
        self.about.title("Creditos")
        self.about.minsize(500,500)
        self.about.resizable(width = NO, height = NO)
        self.canvas_about = Canvas(self.about, width = 500, height = 500, highlightthickness = 0, bg = 'black')
        self.canvas_about.place(x=0,y=0)

        self.label_about = Label(self.about, text = about, font= ("Arial",14), bg = 'black', fg = 'white')
        self.label_about.place(x=100,y=80)

        self.button_about_exit = Button(self.about, text = "Exit", bg = 'black', command = self.exit_about)
        self.button_about_exit.place(x=450, y= 470)

    def verificacion(self):
        self.label_error = Label(self.canvas, text = "Debe ingresar su nombre", font = ("Arial",14), bg = 'black', fg = 'white')
         #Get the name ot the text entry
        self.name = self.name_entry.get()

        self.rango = selection.get()
        
        if self.name != "":
            self.new_game_screen = Game(self.name,self.rango)
            self.new_game_screen.iniciar_game()
        else:
            return self.label_error.place(x=150, y=330)

    
    def exit_about(self):
        self.about.destroy()
        
    def exit_ventana(self):
        window.destroy()
        
        
class Game:
    def __init__(self,name,rango):
        self.game = Toplevel()
        
        self.game.minsize(500,500)
        self.game.resizable(width=NO,height=NO)
        
        self.canvas_game = Canvas(self.game, width = 500,height = 500,bg = 'black',highlightthickness = 0)
        self.canvas_game.place(x=0,y=0)

        self.label_player = Label(self.game, text = "Player:",font = ("Arial",14), bg = 'black', fg = 'yellow')
        self.label_player.place(x=5,y=5)
        self.label_name = Label(self.game, text = name ,font = ("Arial",14), bg = 'black', fg = 'yellow')
        self.label_name.place(x=53, y = 5)

        self.lista_enemigos = []
        
        #Player Life
        self.player_life = 3
        self.label_player_life = Label(self.game, text = self.player_life ,font = ("Arial",14), bg = 'black', fg = 'yellow')
        self.label_player_life.place(x= 225,y= 5)
        self.label_player = Label(self.game, text = "Life:" ,font = ("Arial",14), bg = 'black', fg = 'yellow')
        self.label_player.place(x= 190,y= 5)

        #Exit Button
        self.button_exit = Button(self.game, text = "Exit",font = ("Arial",16),background = 'black', command = self.exit)
        self.button_exit.place(x=430, y= 5)

        self.rango = rango

        self.timer = Timer(self.canvas_game)

    def exit(self):
        self.game.destroy()

    def iniciar_game(self):
        self.nave = Nave(self.canvas_game)
        for x in range(3*self.rango):
            self.lista_enemigos += [Enemigo(self.canvas_game,x, 50+(x*30), 100)]
            self.lista_enemigos[x].start_enemy()
            
        self.score = Score(self.canvas_game,self.rango)
        
class Nave:
    def __init__(self,canvas_game):
        self.ship = load_image('player.png')
        self.ship_posx = 220
        self.ship_posy = 300
        self.label_ship = Label(canvas_game,bg = 'black', image = self.ship)
        self.label_ship.place(x = self.ship_posx,y = self.ship_posy)
        self.label_ship.focus_set()
        self.label_ship.bind("<Right>",self.right)
        self.label_ship.bind("<Left>", self.left)
        self.label_ship.bind("<Up>",self.up)
        self.label_ship.bind("<Down>",self.down)

    def right(self,event):
        print("Hola")
        if (self.ship_posx < 440):
            self.ship_right = load_image('player_right.png')
            self.label_ship.configure(image=self.ship_right)
            self.label_ship.image = self.ship_right
            self.ship_posx += 20
            self.ship_posy += 0
            self.label_ship.place(x= self.ship_posx, y = self.ship_posy)
    #SpaceShip Direction Left
    def left(self,event):
        if (self.ship_posx > 8):
            self.ship_left = load_image('player_left.png')
            self.label_ship.configure(image=self.ship_left)
            self.label_ship.image = self.ship_left
            self.ship_posx -= 20
            self.ship_posy -= 0
            self.label_ship.place(x= self.ship_posx, y = self.ship_posy)
    #SpaceShip Direction Up
    def up(self,event):
        print(self.ship_posy)
        if (self.ship_posy > 40):
            self.ship_up = load_image('player.png')
            self.label_ship.configure(image = self.ship_up)
            self.label_ship.image = self.ship_up
            self.ship_posx += 0
            self.ship_posy -= 20
            self.label_ship.place(x= self.ship_posx, y = self.ship_posy)
    #SpaceShip Direction Down
    def down(self,event):
        if (self.ship_posy < 430):
            self.ship_down = load_image('player_down.png')
            self.label_ship.configure(image = self.ship_down)
            self.label_ship.image = self.ship_down
            self.ship_posx += 0
            self.ship_posy += 20
            self.label_ship.place(x= self.ship_posx, y = self.ship_posy)

class Enemigo:
    def __init__(self,canvas_game,x, pos_x,pos_y):
        self.id = x
        self.enemy_x = pos_x
        self.enemy_y = pos_y
        self.enemy_image = load_image('playerAlien.png')
        self.label_enemy = Label(canvas_game, bg = 'black', image = self.enemy_image)
        self.label_enemy.place(x = self.enemy_x,y = self.enemy_y)
        self.thread_movement = threading.Thread(target=(self.move()))

    def start_enemy(self):
        self.thread.start()

    def move(self):
        while (True):
            print("Hola, soy el thread del enemy =", str(self.id))
            time.sleep(1)

        
class Timer:
    def __init__(self,canvas_game):
        self.label_time = Label(canvas_game, text = "Time:",font = ("Arial",14), bg = 'black', fg = 'yellow')
        self.label_time.place(x=125, y = 5)
        self.meter = 0
        self.label_meter = Label(canvas_game, text = self.meter, font = ("Arial",14), bg = 'black', fg = 'yellow')
        self.label_meter.place(x= 165, y=5)
        self.label_meter.after(1000, self.refresh_timer)
        
    #Refresh the timer 
    def refresh_timer(self):
        self.meter += 1
        self.label_meter.configure(text=self.meter)
        self.label_meter.after(1000,self.refresh_timer)

class Score:
    def __init__(self,canvas_game,rango):
        self.rango = rango
        self.score = 0
        self.label_player_score= Label(canvas_game, text = "Score:" ,font = ("Arial",14), bg = 'black', fg = 'yellow')
        self.label_player_score.place(x = 340, y = 5)
        self.label_score = Label(canvas_game, text = self.score ,font = ("Arial",14), bg = 'black', fg = 'yellow')
        self.label_score.place(x = 390, y = 5)
        self.label_score.after(1000, self.refresh_score)

    def refresh_score(self):
        if self.rango == 1:
            self.score += 1
            self.label_score.configure(text=self.score)
            self.label_score.after(1000,self.refresh_score)
        elif self.rango == 2:
            self.score += 3
            self.label_score.configure(text=self.score)
            self.label_score.after(1000,self.refresh_score)
        else:
            self.score += 5
            self.label_score.configure(text=self.score)
            self.label_score.after(1000,self.refresh_score)
            

class Best_Score:
    def __init__(self):
        self.score_window = Toplevel()
        self.score_window.title("Best Scores")

        #Set the dimensions of the TopLevel
        self.score_window.minsize(500,500)

        #The Screen can't resizable
        self.score_window.resizable(width = NO, height = NO)
        
        self.canvas_score = Canvas(self.score_window,width = 500, height = 500,highlightthickness = 0, bg = 'black')
        self.canvas_score.place(x=0,y=0)

        #Add the image to the background
        self.bg = load_image('Fondo.png')
        self.label_bg = Label(self.canvas_score,bg = 'black', image = self.bg)
        self.label_bg.place(x = 0,y = 0)

        self.button_score_exit = Button(self.canvas_score, text = "Exit",background = 'black', command = self.exit_score)
        self.file = open('Best_Scores.txt','r')
        self.text = self.file.read()
        print(self.file.read())

        self.label_score = Label(self.score_window, text = self.text, font= ("Arial",14), bg = 'black', fg = 'white')
        self.label_score.place(x=100,y=80)

    def exit_score(self):
        self.score_window.destroy() 

        
        
    
    
        
        

window = Tk()
selection = IntVar()
enemy_x = random.randint(0,500)
enemy_y = random.randint(0,500)
window.minsize(500,500)
window.resizable(width = NO, height = NO)
ventana_principal = Ventana_Principal(window)
window.title("SpaceRush")
window.mainloop()



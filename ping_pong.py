"""  Project "Ping-pong"(tkinter)
Nikitina N.V.
"""

from tkinter import *
import random
import time

#-----------------(глобальные переменные)---------------


#  поле
WIDTH = 900
HEIGHT = 300

# мяч
BALL_SPEED_UP = 1.05 #увеличение скорости мяча
BALL_SPEED_STOP = 40
RADIUS_OF_BALL = 35
START_SPEED, BALL_SPEED_X, BALL_SPEED_Y = 20, 20, 20



BALL_X_CHANGE = 20
BALL_Y_CHANGE = 0


# ракетка
WIDTH_RACKET = 15 
HEIGHT_RACKET = 100
# их скорость
RACKET_SPEED = 20
LEFT_RACKET_SPEED = 0
RIGHT_RACKET_SPEED = 0

# счет
SCORE_1 = 0
SCORE_2 = 0


DISTANCE = WIDTH - WIDTH_RACKET #S до правого край



#------------------------(функции)------------------------

def main():
    movement_of_ball()
    move_rackets()
    root.after(30, main)

def update_score(player):
    """Обновление счета"""
    global SCORE_1, SCORE_2
    if player == "right":
        SCORE_1 += 1
        if SCORE_1 >= 20:
            label['text'] = 'Победа второго игрока!'
            c.delete(ALL)
            c.create_text(300,150,text="Нажмите кнопку 'ВЫЙТИ'",anchor="w", font="Verdana 18")
        c.itemconfig(score1_text, text=SCORE_1)
    else:
        SCORE_2 += 1
        if SCORE_2 >= 20:
            label['text'] = 'Победа первого игрока!'
            c.delete(ALL)
            c.create_text(300,150,text="Нажмите кнопку 'ВЫЙТИ'",anchor="w", font="Verdana 18")
        c.itemconfig(score2_text, text=SCORE_2)
 
def ball_to_center():
    """Изменение направления"""
    global BALL_SPEED_X
    # мяч по центру
    c.coords(BALL, WIDTH/2-RADIUS_OF_BALL/2,
             HEIGHT/2-RADIUS_OF_BALL/2,
             WIDTH/2+RADIUS_OF_BALL/2,
             HEIGHT/2+RADIUS_OF_BALL/2)
    # меняем направление и скорость
    BALL_SPEED_X = -(BALL_SPEED_X * -START_SPEED) / abs(BALL_SPEED_X)


def bounce(action):
    """Отскок мяча"""
    global BALL_SPEED_X, BALL_SPEED_Y
    if action == "отскок":
        BALL_SPEED_Y = random.randrange(-10, 10)
        if abs(BALL_SPEED_X) < BALL_SPEED_STOP:
            BALL_SPEED_X *= -BALL_SPEED_UP
        else:
            BALL_SPEED_Y = -BALL_SPEED_X
    else:
        BALL_SPEED_Y = -BALL_SPEED_Y


def movement_of_ball():
    """Движение шара"""
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL) # координаты границ сторон
    ball_center = (ball_top + ball_bot) / 2
 
    # вертикальный отскок
    # при остуствуии касания
    if ball_right + BALL_SPEED_X < DISTANCE and ball_left + BALL_SPEED_X > WIDTH_RACKET:
        c.move(BALL, BALL_SPEED_X, BALL_SPEED_Y)
        
    # при касании
    elif ball_right == DISTANCE or ball_left == WIDTH_RACKET:
        # проверка стороны
        if ball_right > WIDTH / 2:
            if c.coords(RIGHT_RACKET)[1] < ball_center < c.coords(RIGHT_RACKET)[3]:
                bounce("отскок")
            else:
                update_score("left")
                ball_to_center()
        else:
            # То же самое для левого игрока
            if c.coords(LEFT_RACKET)[1] < ball_center < c.coords(LEFT_RACKET)[3]:
                bounce("отскок")
            else:
                update_score("right")
                ball_to_center()
                
    # при вылете за границы поля
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, DISTANCE - ball_right, BALL_SPEED_Y)
        else:
            c.move(BALL, -ball_left + WIDTH_RACKET, BALL_SPEED_Y)
            
    # горизонтальный отскок
    if ball_top + BALL_SPEED_Y < 0 or ball_bot + BALL_SPEED_Y > HEIGHT:
        bounce("рикошет")


def move_rackets():
    """Движение ракеток"""
    # словарь = {ракетка : скорость}
    RACKETS = {LEFT_RACKET: LEFT_RACKET_SPEED, 
            RIGHT_RACKET: RIGHT_RACKET_SPEED}
    for racket in RACKETS:
        # двигаем ракетку с заданной скоростью
        c.move(racket, 0, RACKETS[racket])
        # если ракетка за полем - возвращаем ее наместо
        if c.coords(racket)[1] < 0:
            c.move(racket, 0, -c.coords(racket)[1])
        elif c.coords(racket)[3] > HEIGHT:
            c.move(racket, 0, HEIGHT - c.coords(racket)[3])

 

def handle(event):
    """Функция обработки нажатия кравиш"""
    global LEFT_RACKET_SPEED, RIGHT_RACKET_SPEED
    if event.keysym == "w":
        LEFT_RACKET_SPEED = -RACKET_SPEED
    elif event.keysym == "s":
        LEFT_RACKET_SPEED = RACKET_SPEED
    elif event.keysym == "Up":
        RIGHT_RACKET_SPEED = -RACKET_SPEED
    elif event.keysym == "Down":
        RIGHT_RACKET_SPEED = RACKET_SPEED


def racket_stop(event):
    """Реакция на отпускание клавиши"""
    global LEFT_RACKET_SPEED, RIGHT_RACKET_SPEED
    if event.keysym in "ws":
        LEFT_RACKET_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_RACKET_SPEED = 0
def f():
    btn.configure(text = 'ВЫЙТИ', command = f2)
    main()
    
def f2():
    root.destroy()


    
#----------------------------(работа с tkinter)------------------------

root = Tk()
root.title("Ping Pong")
root.configure(background='white')

c = Canvas(root, width=WIDTH, height=HEIGHT, background="#c3ff87")
c.pack()

btn = Button(root, text="НАЧАТЬ", width=30, height=5, bg="#c3ff87", fg="#631010s", command = f)
label = Label(root, text="Добро пожаловать в игру! \n Игра закончиться, когда счет одного из игроков достигнет 20 очков!",
              font="Arial 18",  bg="white", fg="#283b15")

label.pack()
btn.pack()

# поле
c.create_line(WIDTH_RACKET, 0, WIDTH_RACKET, HEIGHT, width=3, fill="#283b15")
c.create_line(WIDTH - WIDTH_RACKET, 0, WIDTH - WIDTH_RACKET, HEIGHT, width=3,
                  fill="#283b15")
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, width=3, fill="#283b15")
     
# мяч
BALL = c.create_oval(WIDTH/2-RADIUS_OF_BALL/2, HEIGHT/2-RADIUS_OF_BALL/2,
                         WIDTH/2+RADIUS_OF_BALL/2, HEIGHT/2+RADIUS_OF_BALL/2,
                         fill="white")

# левая ракетка
LEFT_RACKET = c.create_line(WIDTH_RACKET/2, 0, WIDTH_RACKET/2, HEIGHT_RACKET,
                             width=WIDTH_RACKET, fill="#631010s")
     
# правая ракетка
RIGHT_RACKET = c.create_line(WIDTH-WIDTH_RACKET/2, 0, WIDTH-WIDTH_RACKET/2, 
                              HEIGHT_RACKET, width=WIDTH_RACKET, fill="#631010")

# счет
score1_text = c.create_text(WIDTH-WIDTH/3, HEIGHT_RACKET/4,
                             text=SCORE_1, font="Arial 24",
                             fill="#631010")
     
score2_text = c.create_text(WIDTH/3, HEIGHT_RACKET/4,
                              text=SCORE_2, font="Arial 24",
                              fill="#631010")

c.focus_set()
c.bind("<KeyPress>", handle)
c.bind("<KeyRelease>", racket_stop)


root.mainloop()

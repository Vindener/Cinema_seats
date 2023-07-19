from turtle import Turtle, Screen

import os

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 720
HALL_HEADER = 150
FONT_SIZE = 20

ROW = 5
COLUMN = 5

main_screen = Screen()
main_screen.setup(SCREEN_WIDTH,SCREEN_HEIGHT)
main_screen.setworldcoordinates(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
main_screen.title("Cinema")

#Main Turtle
main_turtle = Turtle()
main_turtle.hideturtle()
main_turtle.speed(0)
main_turtle.penup()

cell_width = SCREEN_WIDTH / COLUMN
cell_height = (SCREEN_HEIGHT - HALL_HEADER) / ROW

seat_radius = (cell_height *0.8)/ 2

x = cell_width / 2
y = (cell_height / 2) - seat_radius

seats = {}

for r in range(ROW):
    for c in range(COLUMN):
        seats[(x,y)] = False
        x += cell_width 
    x = cell_width / 2
    y += cell_height
        # pass and ... - countine

def draw_seat(x,y,color="blue"):
    main_turtle.setposition(x,y)
    main_turtle.pendown()
    main_turtle.begin_fill()
    main_turtle.circle(seat_radius)
    main_turtle.fillcolor(color)
    main_turtle.end_fill()
    main_turtle.penup()

# Second Turtle
main_writer = Turtle()
main_writer.hideturtle()
main_writer.speed(0)
main_writer.penup()

def get_seat(x,y):
    for seat in seats:
        distance = ((x-seat[0])**2+(y - (seat[1]+seat_radius))**2)**0.5
        if distance<=seat_radius:
            return seat

# Бронювання місць
def book_seat(x,y):
   seat_coord = get_seat(x,y)
   if seat_coord:
       seats[seat_coord] = True
       draw_seat(*seat_coord,color="tomato")
       write_free_seats(3)

# Повернення місць
def unbook_seat(x,y):
   seat_coord = get_seat(x,y)
   if seat_coord:
       seats[seat_coord] = False
       draw_seat(*seat_coord,color="blue")
       write_free_seats(3)
       
def write_free_seats(position):
    main_screen.tracer(False)
    main_writer.clear()
    main_writer.setposition(10, SCREEN_HEIGHT-(FONT_SIZE * position))
    
    main_writer.pendown()
    free_seats = len(seats.values()) - sum(seats.values())
    main_writer.write(f"Free: {free_seats}",font=("TimesNewRoman",FONT_SIZE,"bold"))
    main_writer.penup()

    main_writer.setposition(10, SCREEN_HEIGHT-(FONT_SIZE * (position+2)))
    main_writer.pendown()
    sold_seats = sum(seats.values())
    main_writer.write(f"Sold: {sold_seats}",font=("TimesNewRoman",FONT_SIZE,"bold"))
    main_writer.penup()

    main_writer.setposition((SCREEN_WIDTH/2)-40, SCREEN_HEIGHT-(FONT_SIZE * 5))

    main_writer.pendown()
    free_seats = len(seats.values()) - sum(seats.values())
    main_writer.write("Screen", font=(
        "TimesNewRoman", FONT_SIZE, "bold"))
    main_writer.penup()

    main_writer.setposition((SCREEN_WIDTH/1.25)-40, SCREEN_HEIGHT-(FONT_SIZE * 3))

    main_writer.pendown()
    free_seats = len(seats.values()) - sum(seats.values())
    main_writer.write("After exit info about seats \n saves in file seats.txt", font=(
        "TimesNewRoman", 14, "bold"))
    main_writer.penup()

    main_screen.tracer(True) 

#Виключити екран щоб не блимало
main_screen.tracer(False)
for seat in seats:
    draw_seat(*seat)
main_screen.tracer(True) 

write_free_seats(3)
# write_free_seats(4)

main_screen.onclick(book_seat)
main_screen.onclick(unbook_seat,3)
main_screen.mainloop()


seats_to_save = []

for seat,status in seats.items():
    row_number = ROW - int(seat[1] // cell_height)
    seat_number = int(seat[0] // cell_width)+1
    result = f"Row {row_number:02d}, seat {seat_number:02d} - {status}"
    seats_to_save.append(result)
seats_to_save.sort()


# Отримати поточний каталог, де знаходиться файл Python та створити файл
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'seats.txt')

file = open(file_path, "w")
file.write("\n".join(seats_to_save))
file.close()

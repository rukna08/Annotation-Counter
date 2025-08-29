import tkinter as tk
import keyboard
from pynput import mouse
import winsound
import json
import os
from pynput.mouse import Controller, Button
import time

image_count = 0
money = 0

SAVE_FILE = "progress.json"

def click_on_roboflow_polygon_tool_button():
	time.sleep(0.15)
	mouse_controller = Controller()
	mouse_controller.position = (1885, 355 + 110)
	time.sleep(0.05)
	mouse_controller.click(Button.left, 1)
	time.sleep(0.05)
	mouse_controller.position = (1076, 518 + 110)


def save_progress():
	data = {
		"image_count": image_count,
		"money": money
	}
	with open(SAVE_FILE, "w") as f:
		json.dump(data, f)

def load_progress():
	if os.path.exists(SAVE_FILE):
		with open(SAVE_FILE, "r") as file:
			data = json.load(file)
			return data.get("image_count", 0), data.get("money", 0)
	return 0, 0

def increment_image_count():
	global image_count, money
	image_count += 1
	money += 3
	canvas.itemconfig(image_count_text, text=str(image_count))
	canvas.itemconfig(money_text, text=str(money))

def listen_for_keys():
	keyboard.add_hotkey('w', increment_image_count)

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
    	if 996 <= x <= 1020:
    		if 138 <= y <= 158:
    			increment_image_count()
    			winsound.PlaySound("coin_sfx.x-wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    			save_progress()
    			click_on_roboflow_polygon_tool_button()

def reset_progress():
	global image_count, money
	image_count = 0
	money = 0
	canvas.itemconfig(image_count_text, text=str(image_count))
	canvas.itemconfig(money_text, text=str(money))
	save_progress()

def create_window():
	global canvas, image_count_text, image_count, money_text, money
	image_count, money = load_progress()
	root = tk.Tk()
	root.geometry("350x200")
	root.title("Annotation Counter")
	root.call('wm', 'attributes', '.', '-topmost', '1')
	root.resizable(False, False)
	root.attributes('-toolwindow', True)  # On Windows removes maximize
	root.configure(bg="black")
	canvas = tk.Canvas(root, width=350, height=200, bg="black", highlightthickness=0, bd=0)
	canvas.pack()
	image_count_text = canvas.create_text(300, 48, text=str(image_count), font="Arial 40 bold", fill="yellow")
	image_meta_text  = canvas.create_text(130, 45, text="images: ",       font="Arial 40", 		fill="yellow")
	money_text 	     = canvas.create_text(300, 98, text=str(money),       font="Arial 40 bold", fill="green")
	money_meta_text  = canvas.create_text(130, 95, text="money: ",  	  font="Arial 40",		fill="green")

	reset_button = tk.Button(root, text="Reset", font="Arial 14 bold", bg="blue", fg="white", command=reset_progress)
	reset_button.place(x=10, y=150, width=100, height=40)
	#listen_for_keys()
	listener = mouse.Listener(on_click=on_click)
	listener.start()

	root.mainloop()

def main():
	create_window()

main()
import tkinter
import PIL
from PIL import Image
from tkinter import ImageTk

root = tkinter.Tk()
root.title("Image Viewer")
root.geometry("500x500")
label = tkinter.Label(root)
label.pack()

def display(image):



    global label
    img = ImageTk.PhotoImage(image)



    label.configure(image=img)
    label.image = img
    root.update()

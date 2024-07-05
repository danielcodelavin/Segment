import tkinter
import PIL
from PIL import Image
from tkinter import ImageTk

def display(image):
    import tkinter
    from PIL import Image
    from tkinter import ImageTk

    def startdisp():
        root = tkinter.Tk()
        root.title("Image Viewer")
        root.geometry("500x500")
        label = tkinter.Label(root)
        label.pack()

    def update(image):
        global label
        img = ImageTk.PhotoImage(image)
        label.configure(image=img)
        label.image = img
        root.update()    root.title("Image Viewer")
        root.geometry("500x500")
        label = tkinter.Label(root)
        label.pack()



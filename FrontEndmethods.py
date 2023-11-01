# file name is FrontEndmethods.py (pythonGUIWithMethods.py)
import tkinter as tk
import cv2
from tkinter import filedialog, messagebox, Button
from PIL import Image, ImageTk
from BackEndmethods import ImageToText
import numpy as np


class DesktopApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Photo Uploader")
        self.tall = 300
        self.stretched = 300
        self.image_contour_processing = None
        self.image_rotate_processing = None
        self.image_text_processing = None
        self.file_path = None
        self.current_button = 1

        # Create a label widget to display the image
        # self.image_label = Label(self.master)
        self.image_label = tk.Label(self.master)
        self.image_label.pack()

        self.create_widgets()

    # call defined methods inside create_widgets method(create_canvas, create_frame, create_label, create_button)
    def create_widgets(self):
        self.create_canvas()
        self.create_frame()
        self.create_label()
        self.create_button1()
        self.create_button2()
        self.create_button3()
        self.create_button4()

    def next_button(self):
        if self.current_button == 1:
            self.button.config(text="Next")
            self.current_button += 1
            self.create_button2()
        elif self.current_button == 2:
            self.current_button += 1
            self.create_button3()
        elif self.current_button == 3:
            self.current_button += 1
            self.create_button4()


    # Create a canvas
    # def create_canvas(self, tall, stretched):
    def create_canvas(self):
        self.canvas = tk.Canvas(height=self.tall, width=self.stretched)
        self.canvas.pack()

    # Create a frame
    def create_frame(self):
        self.frame = tk.Frame(self.master, height=150, bg="green", bd=5)
        self.frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    # Create a label
    def create_label(self):
        self.label = tk.Label(self.frame, text="Image to Text converter Desktop app", font=("Arial", 10))
        self.label.place(relx=0.5, rely=0.5, anchor="center")

    # Create the Upload Photo button
    def create_button1(self):
        self.button = tk.Button(self.frame, text="Upload Photo", bg="gray", fg="red", height=2, width=20,
                                command=self.upload_photo)
        self.button.pack(side="bottom")

    def create_button2(self):
        self.button = Button(self.frame, text="Next", bg="gray", fg="red", height=2, width=20,
                             command=self.display_contour)
        self.button.pack(side="bottom")

    def create_button3(self):
        self.button = Button(self.frame, text="Next", bg="gray", fg="red", height=2, width=20,
                             command=self.display_rotated_or_not)
        self.button.pack(side="bottom")

    def create_button4(self):
        self.button = Button(self.frame, text="Next", bg="gray", fg="red", height=2, width=20,
                             command=self.display_text)
        self.button.pack(side="bottom")

    def upload_photo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpeg"), ("JPG Files", "*.jpg"), ("GIF Files", "*.gif"),
                       ("TIFF Files", "*.tiff"), ("WEBP Files", "*.webp"), ("BMP Files", "*.bmp"),
                       ("HEIF Files", "*.heif"), ("SVG Files", "*.svg"), ("CR Files", "*.cr"), ("CRW Files", "*.crw"),
                       ("AVIF Files", "*.avif")])

        if file_path.endswith(".png") or file_path.endswith(".jpg") or file_path.endswith(".jpeg") or \
                file_path.endswith(".gif") or file_path.endswith(".tiff") or file_path.endswith(
            ".webp") or file_path.endswith(".bmp") or file_path.endswith(".heif") or file_path.endswith(".svg") \
                or file_path.endswith(".cr") or file_path.endswith(".crw") or file_path.endswith(".avif"):

            # Saving the file path
            self.file_path = file_path
            print("# " * 100)
            print(self.file_path)
            print(self.file_path)
            print(self.file_path)

            # Open the selected image file
            image = Image.open(file_path)

            # Resize the image to fit the label
            image = image.resize((300, 300), Image.LANCZOS)

            # Create a photoimage object of the image
            photo = ImageTk.PhotoImage(image)

            # Create a new window to display the image
            top = tk.Toplevel()
            label = tk.Label(top, image=photo)
            label.image = photo
            label.pack()

        else:
            error_msg = "Please select a correct image format, for example PNG or JPG format file."
            messagebox.showerror("Error", error_msg, parent=self.master)

    def display_contour(self):
        self.image_contour_processing = ImageToText(self.file_path, "C:\\Users\\User\\PycharmProjects\\ProjectFinal\\ABC.txt")
        contour_image = self.image_contour_processing.contours_img(self.file_path)
        print(contour_image)
        # if self.image_contour_processing:
        top = tk.Toplevel()
        contour_image = ImageTk.PhotoImage(Image.fromarray(contour_image))
        label = tk.Label(top, image=contour_image)
        label.image = contour_image
        label.pack()

    def display_rotated_or_not(self):
        self.image_rotate_processing = ImageToText(self.file_path, "C:\\Users\\User\\PycharmProjects\\ProjectFinal\\ABC.txt")
        rotated_image = self.image_rotate_processing.rotate_if_necessary()
        # cv2.imshow("rotated", rotated_image)
        print("####" * 100)
        print(rotated_image)
        print(rotated_image)

        # Create a new window to display the rotated or not rotated image, keeping the same
        top = tk.Toplevel()
        rotated_image = ImageTk.PhotoImage(Image.fromarray(rotated_image))
        label = tk.Label(top, image=rotated_image)
        label.image = rotated_image
        label.pack()

    def display_text(self):
        self.image_text_processing = ImageToText(self.file_path, "C:\\Users\\User\\PycharmProjects\\ProjectFinal\\ABC.txt")
        text_image = self.image_text_processing.extract_text()

        top = tk.Toplevel()
        if text_image is not None:
            text_image = ImageTk.PhotoImage(Image.fromarray(text_image))
            label = tk.Label(top, image=text_image)
            label.image = self.image_text_processing.read_text
            label.pack()

        # top = tk.Toplevel()
        # label = tk.Label(top, text=text_image)
        # label.pack()


root = tk.Tk()
app = DesktopApp(root)
root.mainloop()

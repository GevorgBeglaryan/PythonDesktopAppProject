# file name is BackEndmethods.py
from PIL import Image
import cv2
import pytesseract

class ImageToText:
    def __init__(self, image_path, text_path):
        self.image_path = image_path
        self.text_path = text_path
        self.img_with_contours = None
        self.contour_path = "contoured.jpg"

    def contours_img(self, image_path):
        image = cv2.imread(self.image_path)

        if image is None:
            print("Error: Failed to load image")
            return None

        # Check if the image is empty
        if image.size == 0:
            print("Error: Image is empty")
            return None

        # grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # threshold
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

        # dilate
        dilated = cv2.dilate(thresh, kernel, iterations=13)

        # get contours
        contours, hierarchy = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # for each contour found, draw a rectangle around it on original image
        for contour in contours:
            # get rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(contour)

            # discard areas that are too large
            if h > image.shape[0] or w > image.shape[1]:
                continue

            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 4) #crop

        # Convert the image to grayscale
        gray_img_rectangle = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)       # gray crop

        # write original image with added contours to disk
        cv2.imwrite(self.contour_path, image)
        return image

    def extract_text(self):
        # path pytesseract
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        img_with_contours = self.contours_img(self.image_path)

        if img_with_contours is None:
            print("Error: Failed to load image")
            return None

            # Check if the image is empty
        if img_with_contours.size == 0:
            print("Error: Image is empty")
            return None

        text = pytesseract.image_to_string(Image.fromarray(img_with_contours))
        return text

    def rotate_if_necessary(self):

        self.img_with_contours = self.contours_img(self.image_path)
        text = self.extract_text()
        # write all text with pytesseract and if file does not exist, create file
        with open(self.image_path, "w") as f:
            # Check if the text is horizontal or vertical
            horizontal = all(c.isalnum() and c.isspace() for c in text)

            if not horizontal:
                print("if not horizontal")
                # Rotate the cropped image by 90 degrees counterclockwise
                crop_img = cv2.rotate(self.img_with_contours, cv2.ROTATE_90_COUNTERCLOCKWISE)
                text = pytesseract.image_to_string(Image.fromarray(crop_img), lang="eng")
                # print(text)
                f.write(text)
                return crop_img

            elif horizontal:
                text = pytesseract.image_to_string(Image.fromarray(self.img_with_contours), lang="eng")
                # print(text)
                f.write(text)
                return self.img_with_contours
            else:
                # Rotate the cropped image by 180 degrees counterclockwise
                crop_img = cv2.rotate(self.img_with_contours, cv2.ROTATE_180_COUNTERCLOCKWISE)
                text = pytesseract.image_to_string(Image.fromarray(crop_img), lang="eng")
                # print(text)
                f.write(text)
                return crop_img

    def read_text(self):
        with open(self.text_path, "r") as f:
            content = f.readlines()

        i = 0
        while i < len(content):
            if not content[i].strip():
                del content[i]
            i += 1

        for line in range(len(content)):
            count_line = input("Enter line_number --> ")
            try:
                count_line = int(count_line)
                if count_line < 1 or count_line > len(content):
                    print(f"Please enter a number in the range 1 to {len(content)}")
                else:
                    line_text = content[count_line - 1].strip()
                    # line_text = linecache.getline(self.text_path, count_line)
                    print(line_text)
            except ValueError:
                print("Please enter a valid number")

    # def read_text(self):
    #     with open(self.text_path, "r") as f:
    #         content = f.read()
    #
    #     # Create a new window to display the text
    #     top = tk.Toplevel()
    #     label = tk.Label(top, text=content)
    #     label.pack()





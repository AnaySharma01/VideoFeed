#Imports necessary packages
import cv2 as cv
from tkinter import *
from PIL import Image, ImageTk
import numpy as np

# Creates a Tkinter window
root = Tk()

# Create a label and displays it on the window
label = Label(root)
label.grid()

#Starts the video
video = cv.VideoCapture(0)

#Creates the video dimensions
width, height = 800, 600

#Sets the video dimensions
video.set(cv.CAP_PROP_FRAME_WIDTH, width)
video.set(cv.CAP_PROP_FRAME_HEIGHT, height)


#Creates a mask around the frame
def crop_image(image, vertices):
    #Defines the mask using numpy
    mask = np.zeros_like(image)
    #Fills the mask
    mask_color = 255
    cv.fillPoly(mask, vertices, mask_color)
    masked_image = cv.bitwise_and(image, mask)
    #Returns the mask when called
    return masked_image
#Creates the video overlay
def display_lines(image, lines):
    #Creates numpy array for the frame
    image = np.copy(image)
    blank_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    try:
        #Creates lines if the camera detects a lane
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv.line(blank_image, (x1,y1), (x2,y2), (0, 255, 0), thickness=10)
        image = cv.addWeighted(image, 0.8, blank_image, 1, 0.0)
        return image
    #If it does not detect, return the video feed without the lines
    except: return image
    #Creates and displays the center line
    finally: cv.line(image, pt1=(400, 400), pt2=(400, 800), color=(0, 255, 0), thickness=10)

#Displays the frame overlay
def process_image(image):
    #Sets the dimensions of the overlay lines and mask
    height = image.shape[0]
    width = image.shape[1]
    masked_image_vertices = [
        (0, height),
        (width/2, height/2),
        (width, height)
    ]
    #Image processes the frame using gaussian blur and canny edge detection
    gray_image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    gaussian_image = cv.GaussianBlur(gray_image, (7, 7),1)
    canny_image = cv.Canny(gaussian_image, 100, 120)
    cropped_image = crop_image(canny_image,
    np.array([masked_image_vertices], np.int32))
    #Processes the lines and displays them when called
    lines = cv.HoughLinesP(cropped_image, rho=3, theta=np.pi/180, threshold=200, lines=np.array([]), minLineLength=75, maxLineGap=200)
    image_with_lines = display_lines(image, lines)
    return image_with_lines

#Captures the frames and processes them
def show_overlay():
    #Captures the frame
    _, frame = video.read()
    #Processes the frame
    frame = process_image(frame)
    #Displays the frame
    cv.imshow('frame', frame)

    #Every 10 milliseconds, captures the frame
    label.after(10, show_overlay)

show_overlay()

#Displays the app in Tkinter
root.mainloop()


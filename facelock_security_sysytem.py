import imutils
import time
import cv2
import csv
import os

# Path to the Haarcascade XML file (ensure the file path is correct)
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
detector = cv2.CascadeClassifier(cascade_path)

# Check if the cascade file loaded correctly
if detector.empty():
    print("Error loading Haarcascade XML file. Ensure the file path is correct.")
    exit()

Name = str(input("Enter your Name: "))
Roll_Number = int(input("Enter your Roll Number: "))
dataset = 'dataset'
sub_data = Name
path = os.path.join(dataset, sub_data)

# Create dataset directory if it doesn't exist
if not os.path.isdir(path):
    os.makedirs(path)
    print(f"Directory created for {sub_data}")

# Save the student's info into a CSV file
info = [str(Name), str(Roll_Number)]
with open('student.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(info)

print("Starting video stream...")
cam = cv2.VideoCapture(0)
time.sleep(2.0)
total = 0

while total < 50:
    _, frame = cam.read()
    if frame is None:
        print("Failed to capture frame from camera.")
        break

    img = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    rects = detector.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Save the image
        p = os.path.sep.join([path, "{}.png".format(str(total).zfill(5))])
        cv2.imwrite(p, img)
        total += 1

    # Display the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Cleanup
cam.release()
cv2.destroyAllWindows()

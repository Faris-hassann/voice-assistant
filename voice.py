import speech_recognition as sr
import pyaudio
import pyttsx3
import wikipedia
import pywhatkit
import datetime
import wikipedia
import pyjokes
import cv2
import cmake
import dlib
import face_recognition
import numpy as np
import os
import time

# main variables
path = 'D:/python/images/'
images = []

my_list = os.listdir(path)
print(my_list)

#list for the names
classnames = []

#append the last word from the list
for cl in my_list:
    current_image = cv2.imread(f'{path}/{cl}')
    images.append(current_image)
    classnames.append(os.path.splitext(cl)[0])

# print the names in the class
print(classnames)

# find encoding functions
def find_encoding(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def get_command():
    try:
        with sr.Microphone() as main_source:
            print('listening...')
            voice = listener.listen(main_source)
            command = listener.recognize_google(voice)
            command = command.lower()
            # if 'alexa' in command:
            #     command = command.replace('alexa', '')
            #     print(command)

    except:
        pass

    return command

def run_robot():
    command = get_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%H:%M')
        talk('current time is ' + time)
    elif 'date' in command:
        today = datetime.datetime().today().strftime('%d:%m:%y')
        talk('today is ' + today)
    elif 'search for' in command:
        search = command.replace('search for', '')
        info = wikipedia.summary(search)
        talk('i found' + info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    else:
        talk('sorry, i did not get it')
        run_robot()

print("Encoding...")
encode_list_known = find_encoding(images)
print("encoding is complete...")

#open camera
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    image_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    image_small = cv2.cvtColor(image_small, cv2.COLOR_BGR2RGB)

    #find the location of the face
    face_current_frame = face_recognition.face_locations(image_small)
    encodes_current_frame = face_recognition.face_encodings(image_small, face_current_frame)

    #compare the faces in the program with the videos
    for encode_face, face_location in zip(encodes_current_frame, face_current_frame):
        matches = face_recognition.compare_faces(encode_list_known, encode_face)
        face_distance = face_recognition.face_distance(encode_list_known, encode_face)
        match_index = np.argmin(face_distance)

        if matches[match_index]:
            name = classnames[match_index].upper()
            print(name)
            y1, y2, x1, x2 = face_location
            y1, y2, x1, x2 = y1*4, y2*4, x1*4, x2*4
            #cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            #cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            #cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255,255), 2)
            talk('hi' + name)
            run_robot()
            sleep(40)
            
    cv2.imshow('TEST', img)
    cv2.waitKey(1)
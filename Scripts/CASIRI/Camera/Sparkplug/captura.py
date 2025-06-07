import requests
import json
import getOculusimage
import time
import threading
import os
import cv2
from datetime import datetime, timedelta

def clean():
    os.system("rm -r imagenes/jpgs/*.jpg")
    os.system("rm -r imagenes/fits/*.fit")
    print("Archivos previos borrados")

def get_frames(interval_minutes):
    try:
        while True:
            os.system("python getOculusimage.py")
            time.sleep(interval_minutes * 60)  # Convertir minutos a segundos
    except KeyboardInterrupt:
        print("Captura de frames detenida por el usuario")

def time_lapse():
    """Extrae los archivos de la carpeta frames y los organiza por
    fecha de adquisicion """
    frames = os.listdir("imagenes/jpgs")
    frames = list(map(lambda dates: datetime.strptime(dates.replace('.jpg',''), '%Y-%m-%d %H:%M:%S.%f'), frames))
    frames = sorted(frames)
    frames = list(map(lambda files: str(files)+".jpg", frames))

    img_array = []
    for f in frames:
        img = cv2.imread("imagenes/jpgs/"+f)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
    path_file = datetime.now()
    writer = cv2.VideoWriter("timelapses/"+str(path_file)+".mp4",cv2.VideoWriter_fourcc(*'X264'), 10, size)
    for i in range(len(img_array)):
        writer.write(img_array[i])
    writer.release()
    print("timelapse creado")
    return "timelapses/"+str(path_file)+".mp4"

try:
    clean()

    # Captura de frames cada 5 minutos
    interval_minutes = 1
    frame_thread = threading.Thread(target=get_frames, args=(interval_minutes,))
    frame_thread.start()

    # Espera a que el usuario interrumpa el programa
    frame_thread.join()

    t = time_lapse()

except KeyboardInterrupt:
    print("An error occurred")

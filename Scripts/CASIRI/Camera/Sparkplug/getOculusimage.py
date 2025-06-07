import io
import PyIndi
import time
from datetime import datetime
import sys
import threading
from astropy.io import fits
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from threading import Timer


    
class IndiClient(PyIndi.BaseClient):
    def __init__(self):
        super(IndiClient, self).__init__()
    def newDevice(self, d):
        pass
    def newProperty(self, p):
        pass
    def removeProperty(self, p):
        pass
    def newBLOB(self, bp):
        print("new BLOB ", bp.name)
        # global blobEvent
        blobEvent.set()
        pass
    def newSwitch(self, svp):
        pass
    def newNumber(self, nvp):
        pass
    def newText(self, tvp):
        pass
    def newLight(self, lvp):
        pass
    def newMessage(self, d, m):
        pass
    def serverConnected(self):
        pass
    def serverDisconnected(self, code):
        pass

def getImage(exposure):
    """
    inputs:
    exposure: es el tiempo de exposicion del sensor en segundos"""
    # connect the server

    indiclient=IndiClient()
    indiclient.setServer("localhost",7624)
    if (not(indiclient.connectServer())):
        print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")
        print("  indiserver indi_simulator_telescope indi_simulator_ccd")
        sys.exit(1)
    # Let's take some pictures
    ccd="SX CCD SuperStar"
    device_ccd = indiclient.getDevice(ccd)

    while not(device_ccd):
        time.sleep(0.5)
        device_ccd = indiclient.getDevice(ccd)    
    ccd_connect = device_ccd.getSwitch("CONNECTION")
    while not(ccd_connect):
        time.sleep(0.5)
        ccd_connect = device_ccd.getSwitch("CONNECTION")
    if not(device_ccd.isConnected()):
        ccd_connect[0].s = PyIndi.ISS_ON  # the "CONNECT" switch
        ccd_connect[1].s = PyIndi.ISS_OFF # the "DISCONNECT" switch
        indiclient.sendNewSwitch(ccd_connect)

    ccd_exposure = device_ccd.getNumber("CCD_EXPOSURE")
    while not(ccd_exposure):
        time.sleep(0.5)
        ccd_exposure=device_ccd.getNumber("CCD_EXPOSURE")
    print(ccd_exposure, "EXPOSURE......")


    # Ensure the CCD simulator snoops the telescope simulator
    # otherwise you may not have a picture of vega
    ccd_active_devices = device_ccd.getText("ACTIVE_DEVICES")
    while not(ccd_active_devices):
        time.sleep(0.5)
        ccd_active_devices = device_ccd.getText("ACTIVE_DEVICES")


    # we should inform the indi server that we want to receive the
    # "CCD1" blob from this device
    indiclient.setBLOBMode(PyIndi.B_ALSO, ccd, "CCD1")
    global ccd_ccd1
    ccd_ccd1 = device_ccd.getBLOB("CCD1")
    while not(ccd_ccd1):
        time.sleep(0.5)
        ccd_ccd1 = device_ccd.getBLOB("CCD1")

    # we use here the threading.Event facility of Python
    # we define an event for newBlob event
    # blobEvent = threading.Event()
    blobEvent.clear()
    ccd_exposure[0].value = exposure
    indiclient.sendNewNumber(ccd_exposure)
    blobEvent.wait()
    blobEvent.clear()

    fits1 = ccd_ccd1[0].getblobdata()
    blobfile = io.BytesIO(fits1)
    filename= "oculus.fit"
    date = str(datetime.now())
    path_file = "imagenes/fits/"+date+filename
    with open(path_file, "wb") as f:
        f.write(blobfile.getvalue())
    return date




if __name__ == "__main__":
    global blobEvent
    blobEvent = threading.Event()
    date = getImage(0.5)
    path_file = "imagenes/fits/"+date+"oculus.fit"

    hdulist = fits.open(path_file)
    plt.imshow(hdulist[0].data, cmap = 'gray')
    plt.title(date)
    path_frames = "imagenes/jpgs/"+date+".jpg"
    plt.savefig(path_frames)
    #plt.show()


#/********************************************************************************
# * Module for taking and adjusting data from the Davis VantagePro2 console
# *
# * Contributors:
# *   CEMOS - initial implementation
# *   Felipe Rubio - final development
# ********************************************************************************/

from pyvantagepro import VantagePro2

def get_vantagepro2_data():
    """
    Take data from vantagePro2 and return a dictionary type variable with the data
    """
    device = VantagePro2.from_url('serial:/dev/ttyUSB0:19200:8N1')
    data = device.get_current_data()
    dateNow = str(data['Datetime'])
    fecha = dateNow[:10]
    hora = dateNow[11:19]

    # Units change

    tempOutC = "{:.2f}".format((data['TempOut'] - 32) / 1.8)
    Velms = "{:.2f}".format(data['WindSpeed'] * 0.44704)
    BarmmHg = "{:.2f}".format(data['Barometer'] * 25.4)

    datos = {
        'Date': fecha,
        'Hour': hora,
        'Temp': tempOutC,
        'Wind_Speed': Velms,
        'Wind_Dir': data['WindDir'], 
        'Hum': data['HumOut'],
        'Pres': BarmmHg
        }
    return datos
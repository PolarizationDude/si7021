"""
Driver for the Si7021 humidity and temperature sensor
requires SMBus
"""
from smbus import SMBus
from time import sleep

class RHTS:
    """ Driver for Si7021 temperatuer and humidity sensor
    """
    meas_RH = 0xf5
    read_temp = 0xe0
    reset = 0xfe
    def __init__(self, i2cbus, addr):
        self.i2cbus = i2cbus
        self.bus = SMBus(self.i2cbus)
        self.addr = addr
    def measure(self):
        self.bus.write_byte(self.addr, self.meas_RH)
        sleep(0.3)
    def readall(self):
        """Units of temperature in  deg C """
        self.measure()
        # Pull the MSB of the RH data
        data0 = self.bus.read_byte(self.addr)
        # Pull the LSB from the RH data
        data1 = self.bus.read_byte(self.addr)
        # Calculate the RH from user manual section 5.1.1
        RH = ((data0*256 + data1)*125 / 65535.0)-6
        self.RH = max(0, min(100, RH)) 
        # Pull the two byte temperature dats - needs byte shifting
        data3 = self.bus.read_word_data(self.addr, self.read_temp)
        # Shift the bytes
        data4 = ((data3 & 0xff) << 8) | (data3 >> 8)
        # Calculate the temperature in deg C from manual section 5.1.1
        self.tempC = 175.72 * data4 / 65536. - 46.85
        # return the RH and Temperature data
        return [self.tempC, self.RH]

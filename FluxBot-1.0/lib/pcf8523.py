

class PCF8523:
    ADDRESS = 0x68

    def __init__(self, i2c):
        self.i2c = i2c

    def now(self):
        now = [0, 0, 0, 0, 0, 0]#year, month, day, hour, minute, second
        self.i2c.writeto(PCF8523.ADDRESS, 0x03)
        buffer = self.i2c.readfrom(PCF8523.ADDRESS, 7)
        #set the year
        now[0] = 2000 + PCF8523.bcd2bin(buffer[6])
        #set the month
        now[1] = PCF8523.bcd2bin(buffer[5])
        #set the day
        now[2] = PCF8523.bcd2bin(buffer[3] & 0x3F)
        #set the hour (24 sys)
        now[3] = PCF8523.bcd2bin(buffer[2])
        #set the minute
        now[4] = PCF8523.bcd2bin(buffer[1])
        #set the second
        now[5] = PCF8523.bcd2bin(buffer[0] & 0x7F)
        return now


    @staticmethod
    def bcd2bin(value):
        """Convert binary coded decimal to Binary
        :param value: the BCD value to convert to binary (required, no default)
        """
        return value - 6 * (value >> 4)
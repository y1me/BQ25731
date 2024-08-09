




import EasyMCP2221
import time

class BQ25731(EasyMCP2221.Device):
    # Default I2C address for BQ25731
    BQ25731_ADDR = 0x6B
    BQ25731_ADDR = 0x6B

    # BQ25731 Register Map addresses
    CHARGER_OPTION_0_ADDR       =  0x00
    CHARGE_CURRENT_ADDR         =  0x02
    CHARGE_VOLTAGE_ADDR         =  0x04
    OTG_VOLTAGE_ADDR            =  0x06
    OTG_CURRENT_ADDR            =  0x08
    INPUT_VOLTAGE_ADDR          =  0x0A
    IIN_HOST_ADDR               =  0x0E
    CHARGER_STATUS_ADDR         =  0x20
    PROCHOT_STATUS_ADDR         =  0x22
    IIN_DPM_ADDR                =  0x24
    ADC_VBUS_ADDR               =  0x26
    ADC_IBAT_ADDR               =  0x28
    ADC_IIN_ADDR                =  0x2A
    ADC_VSYS_ADDR               =  0x2C
    MANUFACTURER_ID_ADDR        =  0x2E
    DEVICE_ID_ADDR              =  0x2F
    CHARGER_OPTION_1_ADDR       =  0x30
    CHARGER_OPTION_2_ADDR       =  0x32
    CHARGER_OPTION_3_ADDR       =  0x34
    PROCHOT_OPTION_0_ADDR       =  0x36
    PROCHOT_OPTION_1_ADDR       =  0x38
    ADC_OPTION_ADDR             =  0x3A
    CHARGER_OPTION_4_ADDR       =  0x3C
    VMIN_ACTIVE_PROT_ADDR       =  0x3E

    WORD_SIZE                   = 2

    def __init__(self):
        # Initialize the parent class (EasyMCP2221.Device)
        super().__init__()

    def bq25731_write(self,payload):
        self.I2C_write(addr=self.BQ25731_ADDR, data=bytes(payload))
    def bq25731_read(self, start_address,size):
        self.I2C_write(self.BQ25731_ADDR, [start_address], kind='nonstop')

        # Read max 100 bytes
        dataraw = self.I2C_read(addr=self.BQ25731_ADDR, size=size, kind='restart', timeout_ms=200)
        return dataraw

    def read_ID(self):
        id_raw =  self.bq25731_read(self.MANUFACTURER_ID_ADDR,self.WORD_SIZE)
        if id_raw [0] == 0x40 and id_raw[1] == 0xD6 :
            print("Find TI BQ25731 chip")
            Find = True
        else :
            print("Cannot find TI BQ25731 chip")
            print("MANUFACTURE_ID read: " + hex(id_raw [0]))
            print("DEVICE_ID read: " + hex(id_raw [1]))
            Find = False
        return Find

    def read_regmap(self):

        sectorData = bytearray()
        sectorMap = [[self.CHARGER_OPTION_0_ADDR,12],[self.IIN_HOST_ADDR,2],[self.CHARGER_STATUS_ADDR,16],[self.CHARGER_OPTION_1_ADDR,16]]
        address = []
        for sector in sectorMap:
            sectorData = b''.join([sectorData,self.bq25731_read(sector[0], sector[1])])
            address.append(list(range(sector[0], sector[0] + sector[1])))
        address = sum(address, [])
        regMap = []
        for idx, data in enumerate(sectorData):
            regMap.append([address[idx], data])
        return regMap

        # Read NVM data from BQ25731

        #nvm_data = []
        #for i in range(self.NVM_SIZE):
            # Read each byte from the NVM
         #   data = self.i2c.read_byte_data(self.BQ25731_ADDR, self.NVM_START_ADDR + i)
         #   nvm_data.append(data)
          #  time.sleep(0.01)  # Small delay to ensure stable communication

        return sectorData

    def reset_Chip(self):
        self.bq25731_write([self.CHARGER_OPTION_3_ADDR,0x30,0x44])
        print("Reset TI bq25731 chip")


    def print_regMap(self):
        # Read the NVM data
        nvm_data = self.read_regmap()

        # Print the NVM data
        print("BQ25731 Regmap")
        for data in nvm_data:
            print("reg address " + hex(data[0]) + " : " + hex(data[1]))

def main():
    bq25731 = BQ25731()


    if bq25731.read_ID() :
        bq25731.reset_Chip()
    bq25731.print_regMap()

if __name__ == "__main__":
    main()





"""


# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mcp = EasyMCP2221.Device()
    MEM_ADDR = 0x28
    MEM_POS = 6

    mcp.I2C_write(
        addr=MEM_ADDR,
        data=b'\x26\x00'
        )
    # Seek EEPROM to position

    mcp.I2C_write(
        addr=MEM_ADDR,
        data=MEM_POS.to_bytes(1, byteorder='little'),
        kind='nonstop')

    # Read max 100 bytes
    dataraw = mcp.I2C_read(
        addr=MEM_ADDR,
        size=143,
        kind='restart',
        timeout_ms=200)

    #data = data.split(b'\0')
    listo = dataraw.hex()
    n = 2
    datalist = [listo[i:i + n] for i in range(0, len(listo), n)]
    print(datalist)
    Offset = 6
    for val in datalist :
        print("Address " + hex(Offset) + " = 0x" + val)
        Offset +=1


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
"""
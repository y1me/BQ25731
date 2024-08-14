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


    MANUFACTURER_ID             =  0x40
    DEVICE_ID                   =  0xD6
    CLEAR_FAULT                 =  0x18

    CHARGER_OPTION_0_RESET      =  0xE70E
    EN_LWPWR_DIS_BIT            =  0x7FFF
    WDTMR_ADJ_DIS_BIT           =  0x9FFF
    PWM_FREQ_800K_BIT           =  0xFDFF
    #050A

    CHARGER_OPTION_1_RESET      =  0x3F00
    EN_IBAT_BIT                 =  0x8000
    RSNS_RAC_10mO_BIT           =  0xF7FF
    RSNS_RSR_10mO_BIT           =  0xFBFF
    EN_FAST_5MOHM_OFF_BIT       =  0xFEFF
    #B200

    CHARGER_OPTION_3_RESET      =  0x0434
   # 0430 ?? Rsense??
    ADC_OPTION_RESET            =  0x2000

    EN_ADC_CONV_CONT_BIT        =  0x8000
    EN_ADC_CMPIN_BIT            =  0x0080
    EN_ADC_VBUS_BIT             =  0x0040
    EN_ADC_PSYS_BIT             =  0x0020
    EN_ADC_IIN_BIT              =  0x0010
    EN_ADC_IDCHG_BIT            =  0x0008
    EN_ADC_ICHG_BIT             =  0x0004
    EN_ADC_VSYS_BIT             =  0x0002
    EN_ADC_VBAT_BIT             =  0x0001

    #A0FF
    #Charge voltage 0x1388
    IIN_HOST_RESET              =  0x2000
    IIN_HOST_7A                 =  0x4600
    #0x4600
    CHARGE_VOLTAGE_MASK         =  0x7FF8
    CHARGE_CURRENT_MASK         =  0x1FC0
    CHARGE_CURRENT_RESET        =  0x0080
    #set 1.5A



    CHARGER_OPTION_3_RESET_BIT  =  0x4000

    WORD_SIZE                   = 2

    def __init__(self):
        # Initialize the parent class (EasyMCP2221.Device)
        super().__init__()

    def getMSByte(self,word) :
        return (word >> 8) & 0xFF
    def getLSByte(self,word) :
        return word & 0xFF
    def bq25731_write(self,payload):
        self.I2C_write(addr=self.BQ25731_ADDR, data=bytes(payload))
    def bq25731_read(self, start_address,size=1):
        self.I2C_write(self.BQ25731_ADDR, [start_address], kind='nonstop')

        # Read max 100 bytes
        dataraw = self.I2C_read(addr=self.BQ25731_ADDR, size=size, kind='restart', timeout_ms=200)
        return dataraw

    def word_write(self, address, payload):
        self.bq25731_write([address, self.getLSByte(payload), self.getMSByte(payload)])

    def word_read(self, address):
        return self.bq25731_read(address,self.WORD_SIZE)

    def read_ID(self):
        id_raw =  self.word_read(self.MANUFACTURER_ID_ADDR)
        if id_raw [0] == self.MANUFACTURER_ID  and id_raw[1] == self.DEVICE_ID :
            print("Find TI BQ25731 chip")
            Find = True
        else :
            print("Cannot find TI BQ25731 chip")
            print("MANUFACTURE_ID read: " + hex(id_raw [0]))
            print("DEVICE_ID read: " + hex(id_raw [1]))
            Find = False
        return Find

    def get_Status(self):
        status = self.word_read(self.CHARGER_STATUS_ADDR)
        return status[1]

    def get_fault(self):
        fault = self.word_read(self.CHARGER_STATUS_ADDR)
        return fault[0]

    def get_IIN_DPM(self):
        value = self.word_read(self.IIN_DPM_ADDR)
        value = value[1]
        if value == 0 :
            value = 0.15
        else :
            value = 0.05 + (value*0.05)
        return value

    def get_ADCVBUS(self):
        value = self.word_read(self.ADC_VBUS_ADDR)
        value = value[1]
        return value*0.096

    def get_ADCPSYS(self):
        value = self.word_read(self.ADC_VBUS_ADDR)
        value = value[0]
        return value*0.012

    def get_ADCICHG(self):
        value = self.word_read(self.ADC_IBAT_ADDR)
        value = value[1]
        return value*0.064

    def get_ADCVSYS(self):
        value = self.word_read(self.ADC_VSYS_ADDR)
        value = value[1]
        return ( 2.88 + (value*0.064) )

    def get_ADCVBAT(self):
        value = self.word_read(self.ADC_VSYS_ADDR)
        value = value[0]
        return ( 2.88 + (value*0.064) )

    def get_ADCIIN(self):
        value = self.word_read(self.ADC_IIN_ADDR)
        value = value[1]
        return value*0.05

    def get_ChargeVoltage(self):
        value = self.word_read(self.CHARGE_VOLTAGE_ADDR)
        # Comment to return value in mV
        value = (((value[1] & 0x7F) << 8) + value[0]) #>> 3
        return value #*0.008

    def get_ChargeCurrent(self):
        value = self.word_read(self.CHARGE_CURRENT_ADDR)
        value = (((value[1] & 0x1F) << 8) + value[0]) >> 6
        return value * 0.064

    def set_ChargeVoltage(self,value_mV):
        if value_mV > 23000 or value_mV < 1024 :
            print("Error : Charge voltage value is invalid, provide charge voltage range from 1024 mV to 23000 mV")
        else :
            value_mV = value_mV & self.CHARGE_VOLTAGE_MASK
            self.word_write(self.CHARGE_VOLTAGE_ADDR,value_mV)
            print("Set charge voltage to " + str(value_mV) + " mV")

    def set_ChargeCurrent(self,value_A):
        if value_A > 8.128 or value_A < 0 :
            print("Error : Charge voltage value is invalid, provide charge voltage range from 0 A to 8.128 A")
        else :
            value_A = int(value_A/0.064)
            value_A = ((value_A << 6) & self.CHARGE_CURRENT_MASK)
            self.word_write(self.CHARGE_CURRENT_ADDR,value_A)
            print("Set charge current to " + str((value_A >> 6)*0.064) + " A")


    def clear_fault(self):
        self.bq25731_write(self.CHARGER_STATUS_ADDR,self.CLEAR_FAULT)

    def print_Fault(self):
        status = self.word_read(self.CHARGER_STATUS_ADDR)
        if (status[0] & 0x80) :
            print("Fault ACOV")
        if (status[0] & 0x40) :
            print("Fault BATOC")
        if (status[0] & 0x20) :
            print("Fault ACOC")
        if (status[0] & 0x10) :
            print("Fault SYSOVP")
        if (status[0] & 0x08) :
            print("Fault VSYS_UVP")
        if (status[0] & 0x04) :
            print("Fault Force_Converter_Off")
        if (status[0] & 0x02) :
            print("Fault_OTG_OVP")
        if (status[0] & 0x01) :
            print("Fault_OTG_UVP")

    def print_Status(self):
        status = self.word_read(self.CHARGER_STATUS_ADDR)
        if (status[1] & 0x80) :
            print("STAT_AC : Input is present")
        if (status[1] & 0x40) :
            print("ICO_DONE : ICO is complete")
        if (status[1] & 0x20) :
            print("IN_VAP : Charger is operated in VAP mode")
        if (status[1] & 0x10) :
            print("IN_VINDPM : Charger is in VINDPM during forward mode, or voltage regulation during OTG mode")
        if (status[1] & 0x08) :
            print("IN_IIN_DPM : Charger is not in IIN_DPM during forward mode")
        if (status[1] & 0x04) :
            print("IN_FCHRG : Charger is in fast charger")
        if (status[1] & 0x02) :
            print("Reserved : Reserved")
        if (status[1] & 0x01) :
            print("IN_OTG : Charge is in OTG")

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

    def reset_Chip(self):
        self.word_write(self.CHARGER_OPTION_3_ADDR,self.CHARGER_OPTION_3_RESET | self.CHARGER_OPTION_3_RESET_BIT)
        print("Reset TI bq25731 chip")

    def initial_config_Chip(self):
        #ChargeOption0 Register : disable low power mode, disable watchdog, set pwm frequency to 800 kHz
        self.word_write(self.CHARGER_OPTION_0_ADDR,self.CHARGER_OPTION_0_RESET & self.EN_LWPWR_DIS_BIT & self.WDTMR_ADJ_DIS_BIT & self.PWM_FREQ_800K_BIT)
        #ChargeOption1 Register : Enable the IBAT output buffer,
        self.word_write(self.CHARGER_OPTION_1_ADDR,(self.CHARGER_OPTION_1_RESET | self.EN_IBAT_BIT) & self.RSNS_RAC_10mO_BIT & self.RSNS_RSR_10mO_BIT & self.EN_FAST_5MOHM_OFF_BIT )
        #ADCOption Register : Enable conversion every seconds and all adc
        self.word_write(self.ADC_OPTION_ADDR,self.ADC_OPTION_RESET | self.EN_ADC_CONV_CONT_BIT | self.EN_ADC_CMPIN_BIT | self.EN_ADC_VBUS_BIT | self.EN_ADC_PSYS_BIT | self.EN_ADC_IIN_BIT | self.EN_ADC_IDCHG_BIT | self.EN_ADC_ICHG_BIT | self.EN_ADC_VSYS_BIT | self.EN_ADC_VBAT_BIT )
        #IIN_HOST Register : Set Input current limit to 7A (3.5A with 10 mOhms sense)
        self.word_write( self.IIN_HOST_ADDR, self.IIN_HOST_7A )

        print("Config TI bq25731 chip done")

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
    bq25731.initial_config_Chip()
    print(bq25731.set_ChargeVoltage(4800))
    print(bq25731.set_ChargeCurrent(1.500))
    bq25731.print_Status()
    if bq25731.get_fault() :
        bq25731.print_Fault()
    print(bq25731.get_IIN_DPM())
    print(bq25731.get_ADCVBUS())
    print(bq25731.get_ADCIIN())
    print(bq25731.get_ADCVSYS())
    print(bq25731.get_ADCICHG())
    print(bq25731.get_ADCVBAT())
    print(bq25731.get_ChargeVoltage())
    print(bq25731.get_ChargeCurrent())
    while 1 :
        print(bq25731.get_IIN_DPM())
        print(bq25731.get_ADCVBUS())
        print(bq25731.get_ADCIIN())
        print(bq25731.get_ADCVSYS())
        print(bq25731.get_ADCICHG())
        print(bq25731.get_ADCVBAT())
        time.sleep(2)

if __name__ == "__main__":
    main()





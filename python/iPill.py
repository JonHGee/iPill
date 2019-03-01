from servosix import ServoSix
import time

ss = ServoSix()

period = 2

def dispensePill():
    ss.set_servo(1, 0)
    time.sleep(period)
    ss.set_servo(1, 180)

class pillInfo():
    pname = "NaN"
    pinfo = "NaN"
    dinfo = "NaN"
    pills = 0
    def setinfo(self,pname,pinfo,dinfo,pills):
        self.pname = pname
        self.pinfo = pinfo
        self.dinfo = dinfo
        self.pills = int(pills)
    def getpills(self):
        return str(self.pills)
    def dispense(self):
        self.pills -= 1
             

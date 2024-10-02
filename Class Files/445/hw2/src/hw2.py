import os
import sys
import random
from queue import SimpleQueue

class SSES():
    def __init__(self, fileLoc):
        self.fileLoc = fileLoc
        self.iaRand = random.Random(1)
        self.uniRand = random.Random(2)
        self.sim_clock = 0.0
        self.SERVER_IDLE = 0
        self.SERVER_BUSY = 1

        self.simStopTime = 0
        self.triageServers = 0
        self.triageIAMean = 0.0
        self.triageServiceMean = 0.0
        self.triageDischargeChance = 0.0
        self.traumaServers = 0
        self.traumaServiceMean = 0.0
        self.traumaDischargeChance = 0.0
        self.acuteServers = 0
        self.acuteServiceMean = 0.0
        self.acuteDischargeChance = 0.0
        self.promptServers = 0
        self.promptServiceMean = 0.0
        self.promptDischargeChance = 0.0

        self.time_last_event = 0.0
        self.arrival_times = list()
        self.event_list = list()
        self.parseFile()
        print(self.triageIAMean)
        self.event_list.append(self.iaRandom(self.triageIAMean))
        self.event_list.append(float('inf'))
        self.event_list.append(self.simStopTime)
        self.EVENT_ARRIVAL = 0
        self.EVENT_DEPARTURE = 1
        self.EVENT_END = 2
        

    def arrivalTriage(self):
        self.event_list[self.EVENT_ARRIVAL] = self.sim_clock + self.iaRandom(self.triageIAMean)
    
    def iaRandom(self, mean):
        return self.iaRand.expovariate(1/mean)
    
    def start(self):
        print("Thinking...")
        
    def moveProb(self, prob):
        if (self.uniRand.uniform(0,1) <= prob):
            return True
        else:
            return False

    def parseFile(self):
        try:
            input = self.fileLoc
            file = open(input, 'r')
            row = 0
            for line in file:
                line = line.strip()
                split = line.split(" ")

                if (row == 0):
                    self.simStopTime = int(split[0])
                elif (row == 1):
                    self.triageServers = int(split[0])
                    self.triageIAMean = float(split[1])
                    self.triageServiceMean = float(split[2])
                    self.triageDischargeChance = float(split[3])
                elif (row == 2):
                    self.traumaServers = int(split[0])
                    self.traumaServiceMean = float(split[1])
                    self.traumaDischargeChance = float(split[2])
                elif (row == 3):
                    self.acuteServers = int(split[0])
                    self.acuteServiceMean = float(split[1])
                    self.acuteDischargeChance = float(split[2])
                elif (row == 4):
                    self.promptServers = int(split[0])
                    self.promptServiceMean = float(split[1])
                    self.promptDischargeChance = float(split[2])

                row += 1
            
            file.close()
            

        except FileNotFoundError:
            print("whoops")
            sys.exit(1)

debugmode = 0
if (debugmode == 0):
    if len(sys.argv) != 1:
        print("Command Line Error, 2 arguements required")
        sys.exit(1)
    fileLoc = sys.argv[0]
else:
    fileLoc = os.path.join(os.path.dirname(__file__), "../ed.txt")
sses = SSES(fileLoc)
sses.parseFile()

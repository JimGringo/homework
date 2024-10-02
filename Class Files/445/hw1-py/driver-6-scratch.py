'''
Cody Nelson
driver-6-scratch.py
replaces the old list system with a random number generator
'''
import random
import sys

class SSES():
    def __init__(self, iaMean, service_mean, end_sim):
        # predefined inter-arrival and service times
        iaseed = 1
        serviceseed = 2
        self.iaRand = random.Random(iaseed)
        self.serviceRand = random.Random(serviceseed)
        self.iaMean = iaMean
        self.serviceMean = service_mean

        #self.inter_arrival = [0.4, 1.2, 0.5, 1.7, 0.2, 1.6, 0.2, 1.4, 1.9]
        #self.service = [2.0, 0.7, 0.2, 1.1, 3.7, 0.6]
        #self.ia_index = 0
        #self.service_index = 0

        self.sim_clock = 0.0
        self.SERVER_IDLE = 0
        self.SERVER_BUSY = 1
        self.server_state = self.SERVER_IDLE
        self.time_active = 0.0

        self.time_last_event = 0.0
        self.arrival_times = list()

        # the event list holds times for next arrival and departure events
        # the event list should only have as many entries as there are events
        self.event_list = list()
        # index in event_list for arrival events
        self.EVENT_ARRIVAL = 0
        # index in event list for departure events
        self.EVENT_DEPARTURE = 1
        # set time for initial arrival event
        self.event_list.append(self.iaRandom())
        
        # set the departure time so that arrival occurs before departure
        self.event_list.append(float('inf'))

        self.number_delayed = 0
        self.total_delay_time = 0.0
        self.q_size_area = 0.0

    def iaRandom(self):
        return self.iaRand.expovariate(1/self.iaMean)
    
    def serviceRandom(self):
        return self.serviceRand.expovariate(1/self.serviceMean)
    
    def __str__():
        f"Single Server Event Simulation"

    def interim_report(self):
        """prints variables of interest"""
        print("server state: " + str(self.server_state))
        print("sim clock: " + str(self.sim_clock))
        print("event_list[EVENT_ARRIVAL]: "
              + str(self.event_list[self.EVENT_ARRIVAL]))
        print("event_list[EVENT_DEPARTURE]: "
              + str(self.event_list[self.EVENT_DEPARTURE]))
        print("arrival_times[]: ", end="")
        print(self.arrival_times)
        print("number delayed: " + str(self.number_delayed))
        print("total delay time: " + str(self.total_delay_time))
        avg_delay = 0.0
        if self.number_delayed != 0:
            avg_delay = self.total_delay_time / self.number_delayed
        print("expected avg delay in queue: " + str(avg_delay))
        print("q size area: " + str(self.q_size_area))
        avg_queue_size = 0.0
        total_active = 0.0
        if self.sim_clock != 0:
            avg_queue_size = self.q_size_area / self.sim_clock
            total_active = self.time_active / self.sim_clock
            

        print("expected avg queue size: " + str(avg_queue_size))
        print(f"server utilization: {total_active:.2%}")
        print("------------------------------------")

    def timing(self):
        """sets sim clock to time of next event. returns event type"""
        if (self.event_list[self.EVENT_ARRIVAL]
                < self.event_list[self.EVENT_DEPARTURE]):
            self.sim_clock = self.event_list[self.EVENT_ARRIVAL]
            retval = self.EVENT_ARRIVAL
        else:
            self.sim_clock = self.event_list[self.EVENT_DEPARTURE]
            retval = self.EVENT_DEPARTURE

        if self.server_state == self.SERVER_BUSY:
            self.time_active += self.sim_clock - self.time_last_event
        return retval

    def arrival(self):
        """processes an arrival event based on server status"""
        self.event_list[self.EVENT_ARRIVAL] = (
                self.sim_clock + self.iaRandom())
        queue_size = len(self.arrival_times)
        time_interval = self.sim_clock - self.time_last_event

        if self.server_state == self.SERVER_IDLE:
            self.server_state = self.SERVER_BUSY
            self.event_list[self.EVENT_DEPARTURE] = (
                    self.sim_clock + self.serviceRandom())
            self.number_delayed += 1
        else:
            self.arrival_times.append(self.sim_clock)

        self.q_size_area += queue_size * time_interval
        self.time_last_event = self.sim_clock

    def departure(self):
        """processes a departure event based on queue size"""
        queue_size = len(self.arrival_times)
        time_interval = self.sim_clock - self.time_last_event

        if len(self.arrival_times) > 0:
            cust_arrival_time = self.arrival_times.pop(0)
            self.event_list[self.EVENT_DEPARTURE] = (
                    self.sim_clock + self.serviceRandom())
            self.number_delayed += 1
            delayI = self.sim_clock - cust_arrival_time
            self.total_delay_time += delayI
        else:
            self.server_state = self.SERVER_IDLE
            self.event_list[self.EVENT_DEPARTURE] = float('inf')

        self.q_size_area += queue_size * time_interval
        self.time_last_event = self.sim_clock

if len(sys.argv) != 4:
    print("Command Line Error")
    sys.exit(1)
iaArrivalMean = float(sys.argv[1])
serviceMean = float(sys.argv[2])
endTime = float(sys.argv[3])

#iaArrivalMean = 6
#serviceMean = 2
#endTime = 100

sses = SSES(iaArrivalMean, serviceMean, endTime)
sses.interim_report()

while sses.number_delayed < 6:
    event_type = sses.timing()
    if sses.EVENT_ARRIVAL == event_type:
        print("^^^^^ ARRIVAL")
        sses.arrival()
    else:
        print("^^^^^ DEPART")
        sses.departure()

    sses.interim_report()
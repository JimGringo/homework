class SSES():
    def __init__(self):
        # predefined inter-arrival and service times
        self.inter_arrival = [0.4, 1.2, 0.5, 1.7, 0.2, 1.6, 0.2, 1.4, 1.9]
        self.service = [2.0, 0.7, 0.2, 1.1, 3.7, 0.6]
        self.ia_index = 0
        self.service_index = 0

        self.sim_clock = 0.0
        self.SERVER_IDLE = 0
        self.SERVER_BUSY = 1
        self.server_state = self.SERVER_IDLE

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
        self.event_list.append(self.inter_arrival[self.ia_index])
        self.ia_index += 1
        # set the departure time so that arrival occurs before departure
        self.event_list.append(float('inf'))

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
        return retval

    def arrival(self):
        """processes an arrival event based on server status"""
        self.event_list[self.EVENT_ARRIVAL] = (
                self.sim_clock + self.inter_arrival[self.ia_index])
        self.ia_index += 1

        if self.server_state == self.SERVER_IDLE:
            self.server_state = self.SERVER_BUSY
            self.event_list[self.EVENT_DEPARTURE] = (
                    self.sim_clock + self.service[self.service_index])
            self.service_index += 1
        else:
            self.arrival_times.append(self.sim_clock)

    def departure(self):
        """processes a departure event based on queue size"""
        if len(self.arrival_times) > 0:
            self.arrival_times.pop(0)
            self.event_list[self.EVENT_DEPARTURE] = (
                    self.sim_clock + self.service[self.service_index])
            self.service_index += 1
        else:
            self.server_state = self.SERVER_IDLE
            self.event_list[self.EVENT_DEPARTURE] = float('inf')

sses = SSES()
sses.interim_report()
event_count = 0
while event_count <= 12:
    event_type = sses.timing()
    if sses.EVENT_ARRIVAL == event_type:
        print("^^^^^ ARRIVAL")
        sses.arrival()
    else:
        print("^^^^^ DEPART")
        sses.departure()

    sses.interim_report()
    event_count += 1

import sys
import random
import math
import heapq
from collections import deque, defaultdict

# Generate exponential random variable
def exponential(mean):
    return -mean * math.log(random.random())

# Event class to represent different events
class Event:
    def __init__(self, time, event_type, patient_id):
        self.time = time
        self.event_type = event_type
        self.patient_id = patient_id

    def __lt__(self, other):
        return self.time < other.time

# Simulation class to manage the simulation process
class EmergencyDepartmentSimulation:
    def __init__(self, config_file):
        self.load_config(config_file)
        self.current_time = 0
        self.event_queue = []
        self.patient_counter = 0
        self.triage_queue = deque()
        self.trauma_queue = deque()
        self.acute_queue = deque()
        self.prompt_queue = deque()

        # Track patient waiting times in each queue
        self.waiting_times = {
            'triage': defaultdict(float),
            'trauma': defaultdict(float),
            'acute': defaultdict(float),
            'prompt': defaultdict(float)
        }

        # To compute average delay and queue length over time
        self.queue_lengths = {'triage': 0, 'trauma': 0, 'acute': 0, 'prompt': 0}
        self.queue_length_area = {'triage': 0, 'trauma': 0, 'acute': 0, 'prompt': 0}

        # Track the time servers are busy in each area for utilization calculations
        self.server_busy_time = {'triage': 0, 'trauma': 0, 'acute': 0, 'prompt': 0}

        # Track start of server busy times
        self.server_start_times = {'triage': None, 'trauma': None, 'acute': None, 'prompt': None}

        # Patient discharges
        self.triage_patients_discharged = 0
        self.trauma_patients_discharged = 0
        self.acute_patients_discharged = 0
        self.prompt_patients_discharged = 0

    # Load simulation configuration from a file
    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                lines = f.readlines()

            self.simulation_end_time = int(lines[0].strip())

            triage_config = self.parse_config_line(lines[1], 4)
            trauma_config = self.parse_config_line(lines[2], 3)
            acute_config = self.parse_config_line(lines[3], 3)
            prompt_config = self.parse_config_line(lines[4], 3)

            # Triage area configuration
            self.triage_servers = triage_config[0]
            self.triage_inter_arrival_mean = triage_config[1]
            self.triage_service_mean = triage_config[2]
            self.triage_discharge_prob = triage_config[3]

            # Trauma area configuration
            self.trauma_servers = trauma_config[0]
            self.trauma_service_mean = trauma_config[1]
            self.trauma_prob = trauma_config[2]

            # Acute care area configuration
            self.acute_servers = acute_config[0]
            self.acute_service_mean = acute_config[1]
            self.acute_prob = acute_config[2]

            # Prompt care area configuration
            self.prompt_servers = prompt_config[0]
            self.prompt_service_mean = prompt_config[1]
            self.prompt_prob = prompt_config[2]

        except ValueError as ve:
            print(f"Error loading configuration: {ve}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    def parse_config_line(self, line, expected_length):
        values = list(map(float, line.split()))
        if len(values) != expected_length:
            raise ValueError(f"Expected {expected_length} values but got {len(values)} in line: {line}")
        return values

    # Schedule an event
    def schedule_event(self, event):
        heapq.heappush(self.event_queue, event)

    # Start the simulation
    def run(self):
        self.schedule_event(Event(exponential(self.triage_inter_arrival_mean), 'ARRIVAL', self.patient_counter))

        while self.event_queue and self.current_time < self.simulation_end_time:
            event = heapq.heappop(self.event_queue)
            self.update_statistics()
            self.current_time = event.time
            self.handle_event(event)

        # Output the final report
        self.report()

    # Update queue lengths and other statistics at each time step
    def update_statistics(self):
        # Update queue length areas (for average length over time)
        for queue_name, length in self.queue_lengths.items():
            self.queue_length_area[queue_name] += length * (self.current_time - self.server_start_times[queue_name] if self.server_start_times[queue_name] else 0)
            self.server_start_times[queue_name] = self.current_time

    # Handle an event
    def handle_event(self, event):
        if event.event_type == 'ARRIVAL':
            self.handle_arrival(event)
        elif event.event_type == 'TRIAGE_COMPLETE':
            self.handle_triage_complete(event)
        elif event.event_type == 'TRAUMA_COMPLETE':
            self.handle_trauma_complete(event)
        elif event.event_type == 'ACUTE_COMPLETE':
            self.handle_acute_complete(event)
        elif event.event_type == 'PROMPT_COMPLETE':
            self.handle_prompt_complete(event)

    # Handle patient arrival
    def handle_arrival(self, event):
        self.patient_counter += 1
        if self.current_time + exponential(self.triage_inter_arrival_mean) < self.simulation_end_time:
            self.schedule_event(Event(self.current_time + exponential(self.triage_inter_arrival_mean), 'ARRIVAL', self.patient_counter))

        self.triage_queue.append((event.patient_id, self.current_time))
        self.queue_lengths['triage'] += 1
        self.schedule_event(Event(self.current_time + exponential(self.triage_service_mean), 'TRIAGE_COMPLETE', event.patient_id))

    # Handle completion of triage
    def handle_triage_complete(self, event):
        patient_id, arrival_time = self.triage_queue.popleft()
        self.queue_lengths['triage'] -= 1
        wait_time = self.current_time - arrival_time
        self.waiting_times['triage'][patient_id] = wait_time
        if random.random() < self.triage_discharge_prob:
            self.triage_patients_discharged += 1
        else:
            r = random.random()
            if r < self.trauma_prob:
                self.trauma_queue.append((patient_id, self.current_time))
                self.queue_lengths['trauma'] += 1
                self.schedule_event(Event(self.current_time + exponential(self.trauma_service_mean), 'TRAUMA_COMPLETE', patient_id))
            elif r < self.trauma_prob + self.acute_prob:
                self.acute_queue.append((patient_id, self.current_time))
                self.queue_lengths['acute'] += 1
                self.schedule_event(Event(self.current_time + exponential(self.acute_service_mean), 'ACUTE_COMPLETE', patient_id))
            else:
                self.prompt_queue.append((patient_id, self.current_time))
                self.queue_lengths['prompt'] += 1
                self.schedule_event(Event(self.current_time + exponential(self.prompt_service_mean), 'PROMPT_COMPLETE', patient_id))

    # Handle completion of trauma care
    def handle_trauma_complete(self, event):
        patient_id, arrival_time = self.trauma_queue.popleft()
        self.queue_lengths['trauma'] -= 1
        self.waiting_times['trauma'][patient_id] = self.current_time - arrival_time
        self.trauma_patients_discharged += 1

    # Handle completion of acute care
    def handle_acute_complete(self, event):
        patient_id, arrival_time = self.acute_queue.popleft()
        self.queue_lengths['acute'] -= 1
        self.waiting_times['acute'][patient_id] = self.current_time - arrival_time
        self.acute_patients_discharged += 1

    # Handle completion of prompt care
    def handle_prompt_complete(self, event):
        patient_id, arrival_time = self.prompt_queue.popleft()
        self.queue_lengths['prompt'] -= 1
        self.waiting_times['prompt'][patient_id] = self.current_time - arrival_time
        self.prompt_patients_discharged += 1

    # Final report
    def report(self):
        print("=== Final Report ===")
        
        # Calculate average waiting times (delays) in each queue
        for area in ['triage', 'trauma', 'acute', 'prompt']:
            total_wait_time = sum(self.waiting_times[area].values())
            num_patients = len(self.waiting_times[area])
            average_wait_time = total_wait_time / num_patients if num_patients > 0 else 0
            print(f"Average delay in {area.capitalize()} Queue: {average_wait_time:.2f} time units")

        # Calculate average queue lengths
        for area in ['triage', 'trauma', 'acute', 'prompt']:
            average_queue_length = self.queue_length_area[area] / self.current_time
            print(f"Average number of patients in {area.capitalize()} Queue: {average_queue_length:.2f}")

        # Server utilization for each care area
        for area in ['triage', 'trauma', 'acute', 'prompt']:
            utilization = self.server_busy_time[area] / self.current_time
            print(f"Server utilization in {area.capitalize()}: {utilization:.2f}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python emergency_simulation.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    simulation = EmergencyDepartmentSimulation(config_file)
    simulation.run()

/*
 * David Apostal
 * Fall 2020, CSci 445
 *
 * Due: 11:59pm, Saturday, Sept 12, 2020
 *
 * This is a partial implementation of the single server queueing
 * system presented in Section 1.4 of the textbook, Simulation
 * Modeling and Analysis, 5th edition, by Averill M. Law.
 *
 * This example uses predefined interarrival and service times.
 * Using this data the simulation is intended to run for no more than
 * six delays in the queue. In other words, the simulation should
 * stop when the sixth customer enters service.
 *
 * This implementation is meant to show one approach to
 * developing a simulation by focusing on how the event list and
 * event types advance the simulation.
 */

#include <cfloat>
#include <iostream>
#include <queue>

float interarrival[] = {0.4, 1.2, 0.5, 1.7, 0.2, 1.6, 0.2, 1.4, 1.9};
float service[] = {2.0, 0.7, 0.2, 1.1, 3.7, 0.6};
int ia_index = 0;
int service_index = 0;

const int EVENT_ARRIVAL = 0;
const int EVENT_DEPARTURE = 1;
float event_list[2];

float sim_clock;
int server_state;
const int SERVER_IDLE = 0;
const int SERVER_BUSY = 1;

float time_last_event;
std::queue<float> arrival_times;

int number_delayed;
float total_delay_time;
float qtArea;

/*
 * initializes certain variables. this function is called once prior
 * to the start of the simulation.
 */
void init() {
    server_state = SERVER_IDLE;
    sim_clock = 0.0f;
    time_last_event = 0.0f;

    event_list[EVENT_ARRIVAL] = interarrival[ia_index];
    ia_index++;
    event_list[EVENT_DEPARTURE] = FLT_MAX;

    number_delayed = 0;
    total_delay_time = 0.0f;
    qtArea = 0.0f;
}

/*
 * prints to standard out variables of interest. this is used for
 * development and debugging.
 */
void interim_report() {
    using namespace std;
    cout << "server_state: " << server_state << endl;
    cout << "sim_clock: " << sim_clock << endl;
    cout << "event_list[EVENT_ARRIVAL]: "
        << event_list[EVENT_ARRIVAL] << endl;
    cout << "event_list[EVENT_DEPARTURE]: "
        << event_list[EVENT_DEPARTURE] << endl;

    cout << "arrival_times[]: ";
    std::queue<float>temp(arrival_times);     // make a temp copy
    while (!temp.empty()) {
        float time = temp.front();
        cout << time << " ";
        temp.pop();
    }
    cout << endl;
    cout << "number_delayed: " << number_delayed << endl;
    cout << "total_delay_time: " << total_delay_time << endl;
    cout << "avg customers in queue: " << qtArea << endl;
    cout << "------------------------------------" << endl;
}

/*
 * sets the simulation clock to the time of the next (most imminent)
 * event. returns the event type of the next event.
 */
int timing() {
    int ret_val = EVENT_ARRIVAL;
    if (event_list[EVENT_ARRIVAL] < event_list[EVENT_DEPARTURE]) {
        sim_clock = event_list[EVENT_ARRIVAL];
        ret_val = EVENT_ARRIVAL;
    } else {
        sim_clock = event_list[EVENT_DEPARTURE];
        ret_val = EVENT_DEPARTURE;
    }
    return ret_val;
}

/*
 * processes an arrival event based on the server status.
 */
void arrival() {
    event_list[EVENT_ARRIVAL] = sim_clock + interarrival[ia_index];
    ia_index++;
    int queue_size = arrival_times.size();
    float time_interval = sim_clock - time_last_event;

    if (server_state == SERVER_IDLE) {
        server_state = SERVER_BUSY;
        event_list[EVENT_DEPARTURE] = sim_clock + service[service_index];
        service_index++;
        number_delayed++;
        //total_delay_time += 0;
    } else {
        arrival_times.push(sim_clock);
    }

    qtArea += queue_size * time_interval;

    time_last_event = sim_clock;
}

/*
 * processes a departure event based on whether or not there are any
 * customers in the queue.
 */
void departure() {
    int queue_size = arrival_times.size();
    float time_interval = sim_clock - time_last_event;

    if (!arrival_times.empty()) {
        // customer in queue moves to server
        // auto it = arrival_times.begin();
        // float cust_arrival_time = *it;
        // arrival_times.erase(it);
        float cust_arrival_time = arrival_times.front();
        arrival_times.pop();
        event_list[EVENT_DEPARTURE] =
            sim_clock + service[service_index];
        service_index++;
        number_delayed++;
        float dI = sim_clock - cust_arrival_time;
        total_delay_time += dI;
    } else {
        server_state = SERVER_IDLE;
        event_list[EVENT_DEPARTURE] = FLT_MAX;
    }

    qtArea += queue_size * time_interval;

    time_last_event = sim_clock;
}

int main(int argc, char *argv[]) {
    using std::cout;
    using std::endl;

    init();
    interim_report();

    while (number_delayed < 6) {
        int event_type = timing();
        if (EVENT_ARRIVAL == event_type) {
            cout << "^^^^^ ARRIVAL " << endl;
            arrival();
        } else {
            cout << "^^^^^ DEPART " << endl;
            departure();
        }

        interim_report();
        // cout << ""
    }
}

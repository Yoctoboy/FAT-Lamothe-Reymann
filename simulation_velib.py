import numpy as np
import matplotlib.pyplot as plt
import heapq as hp
import sys
#il faut verifier ce que prend np.random.exponential en parametre

class Station:
    
    def __init__(self, _id, _nb_places, _client_intensity, _initial_fullness, _probabilities_of_target_station):
        self.id = _id
        self.nb_places = _nb_places
        self.client_intensity = _client_intensity
        self.nb_used_places = _initial_fullness
        self.probabilities_of_target_station = _probabilities_of_target_station
        

class Event:
    
    def __init__(self, _name, _time, _station, _target_station = None):
        self.name = _name
        self.time = _time
        self.station = _station
        self.target_station = _target_station
    
    def __lt__(self,other):
        return (self.time < other.time)
	
    def __str__(self): #Overload print(Event e)
        if self.name == "Pedestrian arrival":
            return "Event Pedestrian : Time={0:.3f} - At S{1}".format(self.time, self.station.id)
        elif self.name == "Bike arrival":
            return "Event Bike       : Time={0:.3f} - From S{1} to S{2}".format(self.time, self.station.id, self.target_station.id)
			
    
    def handle(self, list_stations, mean_travel_times):
        new_events = []
        if self.name == "Pedestrian arrival":
            if self.station.nb_used_places > 0 :
                destination = np.random.choice(list_stations, p = self.station.probabilities_of_target_station)
                mtt = mean_travel_times[list_stations.index(self.station)][list_stations.index(destination)]
                new_events.append(Event("Bike arrival", self.time +  np.random.exponential(mtt), self.station, destination))
                self.station.nb_used_places -= 1
            else:
                print("-->station vide")
            new_events.append(Event("Pedestrian arrival", self.time +  np.random.exponential(self.station.client_intensity), self.station))
            
        
        if self.name == "Bike arrival":
            if self.station.nb_places > self.station.nb_used_places:
                self.target_station.nb_used_places += 1
            else:
                print("-->station pleine")
                destination = np.random.choice(list_stations, p = self.target_station.probabilities_of_target_station)
                mtt = mean_travel_times[list_stations.index(self.target_station)][list_stations.index(destination)]
                new_events.append(Event("Bike arrival", self.time +  np.random.exponential(mtt), self.target_station, destination))
        
        return new_events
                
                
                
    

def simulation(nb_places, client_intensities, mean_travel_times, initial_fullness, ending_time, list_probabilities_of_target_station):
    list_events = []
    current_time = 0
    list_stations = []  
    for i in range(len(nb_places)):
        list_stations.append(Station(i+3, nb_places[i], client_intensities[i], initial_fullness[i], list_probabilities_of_target_station[i]))
    
    time_of_next_arrival_to_station = np.random.exponential(client_intensities)
    list_events = [Event("Pedestrian arrival", current_time + time_of_next_arrival_to_station[i], list_stations[i]) for i in range(len(list_stations))]
    hp.heapify(list_events)
    
    while not current_time > ending_time:
        event = hp.heappop(list_events)
        print(event)
        current_time = event.time
        list_new_events = event.handle(list_stations, mean_travel_times)
        for new_event in list_new_events:
            hp.heappush(list_events, new_event)
        
    
nb_places = [24, 20, 20, 15, 20]
initial_fullness = [20, 15, 17, 13, 18]
client_intensities = [1/2.8, 1/3.7, 1/5.5, 1/3.5, 1/4.6]
list_probabilities_of_target_station = [[0,    0.2,  0.3,  0.2,  0.3 ],
                                        [0.2,  0,    0.3,  0.2,  0.3 ],
                                        [0.2,  0.25, 0,    0.25, 0.3 ],
                                        [0.15, 0.2,  0.3,  0,    0.35],
                                        [0.2,  0.25, 0.35, 0.2,  0   ]]
mean_travel_times = [[0, 3, 5, 7, 7],
                     [2, 0, 2, 5, 5],
                     [4, 2, 0, 3, 3],
                     [8, 6, 4, 0, 2],
                     [7, 7, 5, 2, 0]]
ending_time = 100
simulation(nb_places, client_intensities, mean_travel_times, initial_fullness, ending_time, list_probabilities_of_target_station)
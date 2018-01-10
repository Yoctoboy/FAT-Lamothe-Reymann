import numpy as np
import matplotlib.pyplot as plt
import heapq as hp
#il faut verifier ce que prend np.random.exponential en parametre

class Station:
    
    def __init__(self, nb_places, client_intensity, probabilities_of_target_station):
        self.nb_places = nb_places
        self.client_intensity = client_intensity
        self.nb_used_places = 0
        self.probabilities_of_target_station = probabilities_of_target_station
        

class Event:
    
    def __init__(self, name, time, station, target_station = None):
        self.name = name
        self.time = time
        self.station = station
        self.target_station = target_station
    
    def __lt__(self,other):
        return (self.time < other.time)
    
    def handle(self, list_stations, mean_travel_times):
        new_events = []
        if self.name == "Arrival to station":
            if self.station.nb_used_places > 0 :
                destination = np.random.choice(list_stations, p = self.station.probabilities_of_target_station)
                mtt = mean_travel_times[list_stations.index(self.station)][list_stations.index(destination)]
                new_events.append(Event("Bike arrival", self.time +  np.random.exponential(mtt), self.station, destination))
                self.station.nb_used_places -= 1
            else:
                print("station vide")
            new_events.append(Event("Arrival to station", self.time +  np.random.exponential(self.station.client_intensity), self.station))
            
        
        if self.name == "Bike arrival":
            if self.station.nb_places > self.station.nb_used_places:
                self.target_station.nb_used_places += 1
            else:
                print("station pleine")
                destination = np.random.choice(list_stations, p = self.target_station.probabilities_of_target_station)
                mtt = mean_travel_times[list_stations.index(self.target_station)][list_stations.index(destination)]
                new_events.append(Event("Bike arrival", self.time +  np.random.exponential(mtt), self.target_station, destination))
        
        return new_events
                
                
                
    

def simulation(nb_places, client_intensities, mean_travel_times, initial_fullness, ending_time, list_probabilities_of_target_station):
    list_events = []
    time = 0
    list_stations = []
    for i in range(len(nb_places)):
        list_stations.append(Station(nb_places[i], client_intensities[i], list_probabilities_of_target_station[i]))
    
    for i in range(len(list_stations)):
        list_stations[i].nb_used_places = initial_fullness[i]
    
    time_of_next_arrival_to_station = np.random.exponential(client_intensities)
    list_events = [Event("Arrival to station", time + time_of_next_arrival_to_station[i], list_stations[i]) for i in range(len(list_stations))]
    hp.heapify(list_events)
    
    while not time > ending_time:
        event = hp.heappop(list_events)
        time = event.time
        list_new_events = event.handle(list_stations, mean_travel_times)
        for new_event in list_new_events:
            hp.heappush(list_events, new_event)
        
    
nb_places = [10,20,30]
client_intensities = [1,2,3]
mean_travel_times = [[1,2,2],[2,1,2],[2,2,1]]
initial_fullness = [8,15,22]
list_probabilities_of_target_station = [[0,0.5,0.5],[0.5,0,0.5],[0.5,0.5,0]]
ending_time = 100
simulation(nb_places, client_intensities, mean_travel_times, initial_fullness, ending_time, list_probabilities_of_target_station)
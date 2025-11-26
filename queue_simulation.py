#Human generated with AI debugging

import random
import heapq
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class Packet:
    # Represents a packet in the system
    arrival_time: float
    packet_id: int
    queue_assigned: int = -1  # -1 means not assigned yet
    service_start_time: float = -1
    departure_time: float = -1


@dataclass
class Event:
    #Represents an event in the simulation
    time: float
    event_type: str  # 'arrival' or 'departure'
    queue_id: int = -1  # Which queue for departure events
    packet: Packet = None
    
    def __lt__(self, other):
        """For heap comparison"""
        return self.time < other.time


class Queue:
    #Represents a single queue with server
    def __init__(self, capacity=10, queue_id=0):
        self.capacity = capacity  # Including packet in server
        self.queue_id = queue_id
        self.packets = []  # Waiting packets (not including the one being served)
        self.server_busy = False
        self.packet_in_service = None
        
    def length(self):
        #Returns current queue length including packet in server
        return len(self.packets) + (1 if self.server_busy else 0)
    
    def is_full(self):
        #Check if queue is at capacity 
        return self.length() >= self.capacity
    
    def enqueue(self, packet):
        #Add packet to queue
        if self.is_full():
            return False
        self.packets.append(packet)
        return True
    
    def start_service(self, current_time):
        #Move next packet from queue to server
        if self.packets and not self.server_busy:
            self.packet_in_service = self.packets.pop(0)
            self.packet_in_service.service_start_time = current_time
            self.server_busy = True
            return self.packet_in_service
        return None
    
    def finish_service(self, current_time):
        #Complete service of current packet
        if self.server_busy:
            packet = self.packet_in_service
            packet.departure_time = current_time
            self.packet_in_service = None
            self.server_busy = False
            return packet
        return None


class TwoQueueSimulation:
    #Main simulation class for two-queue system
    
    def __init__(self, arrival_rate, service_rate, strategy='random', seed=None):
        
        # Initialize simulation
        
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.strategy = strategy
        self.queue_capacity = 10
        
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # Initialize queues
        self.queue1 = Queue(capacity=self.queue_capacity, queue_id=0)
        self.queue2 = Queue(capacity=self.queue_capacity, queue_id=1)
        
        # Event queue (priority queue)
        self.event_queue = []
        
        # Statistics
        self.current_time = 0.0
        self.packets_offered = 0
        self.packets_dropped = 0
        self.packets_admitted = 0
        self.packets_departed = 0
        
        self.total_queue_length_samples = 0
        self.queue_length_sum = 0
        
        self.total_sojourn_time = 0.0
        self.sojourn_time_samples = 0
        
    def generate_arrival_time(self):
        # Generate next arrival time using exponential distribution
        return self.current_time + random.expovariate(self.arrival_rate)
    
    def generate_service_time(self):
    # Generate service time using exponential distribution
        return random.expovariate(self.service_rate)
    
    def select_queue(self, packet):
        
        # Select which queue to assign packet to based on strategy
        if self.strategy == 'random':
            # Random selection
            selected_queue = random.choice([self.queue1, self.queue2])
            if not selected_queue.is_full():
                return selected_queue
            # Try the other queue
            other_queue = self.queue2 if selected_queue == self.queue1 else self.queue1
            if not other_queue.is_full():
                return other_queue
            return None  # Both full
            
        elif self.strategy == 'min_queue':
            # Min-queue strategy
            len1 = self.queue1.length()
            len2 = self.queue2.length()
            
            if len1 < self.queue_capacity and len2 < self.queue_capacity:
                # Both have space, choose shorter one
                return self.queue1 if len1 <= len2 else self.queue2
            elif len1 < self.queue_capacity:
                return self.queue1
            elif len2 < self.queue_capacity:
                return self.queue2
            else:
                return None  # Both full
    
    def schedule_event(self, event):
        """Add event to event queue"""
        heapq.heappush(self.event_queue, event)
    
    def handle_arrival(self, packet):
        """Handle packet arrival event"""
        self.packets_offered += 1
        
        # Sample queue lengths at arrival time
        avg_length = (self.queue1.length() + self.queue2.length()) / 2.0
        self.queue_length_sum += avg_length
        self.total_queue_length_samples += 1
        
        # Select queue based on strategy
        selected_queue = self.select_queue(packet)
        
        if selected_queue is None:
            # Packet dropped
            self.packets_dropped += 1
        else:
            # Packet admitted
            self.packets_admitted += 1
            packet.queue_assigned = selected_queue.queue_id
            selected_queue.enqueue(packet)
            
            # Try to start service if server is idle
            if not selected_queue.server_busy:
                served_packet = selected_queue.start_service(self.current_time)
                if served_packet:
                    # Schedule departure event
                    service_time = self.generate_service_time()
                    departure_time = self.current_time + service_time
                    departure_event = Event(
                        time=departure_time,
                        event_type='departure',
                        queue_id=selected_queue.queue_id,
                        packet=served_packet
                    )
                    self.schedule_event(departure_event)
    
    def handle_departure(self, event):
        # Handle packet departure event
        queue = self.queue1 if event.queue_id == 0 else self.queue2
        
        # Finish service
        departed_packet = queue.finish_service(self.current_time)
        
        if departed_packet:
            self.packets_departed += 1
            
            # Calculate sojourn time
            sojourn_time = departed_packet.departure_time - departed_packet.arrival_time
            self.total_sojourn_time += sojourn_time
            self.sojourn_time_samples += 1
            
            # Start service for next packet in queue if any
            next_packet = queue.start_service(self.current_time)
            if next_packet:
                service_time = self.generate_service_time()
                departure_time = self.current_time + service_time
                departure_event = Event(
                    time=departure_time,
                    event_type='departure',
                    queue_id=queue.queue_id,
                    packet=next_packet
                )
                self.schedule_event(departure_event)
    
    def run(self, num_packets=10000):
        #Run simulation for specified number of offered packets
        # Schedule initial arrival
        next_arrival_time = self.generate_arrival_time()
        first_packet = Packet(arrival_time=next_arrival_time, packet_id=0)
        self.schedule_event(Event(
            time=next_arrival_time,
            event_type='arrival',
            packet=first_packet
        ))
        
        packet_id = 1
        
        # Main event loop
        while self.event_queue:
            # Get next event
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time
            
            if event.event_type == 'arrival':
                self.handle_arrival(event.packet)
                
                # Schedule next arrival if we haven't generated enough packets
                if self.packets_offered < num_packets:
                    next_arrival_time = self.generate_arrival_time()
                    next_packet = Packet(arrival_time=next_arrival_time, packet_id=packet_id)
                    packet_id += 1
                    self.schedule_event(Event(
                        time=next_arrival_time,
                        event_type='arrival',
                        packet=next_packet
                    ))
            
            elif event.event_type == 'departure':
                self.handle_departure(event)
            
            # Stop if we've offered enough packets and all admitted packets have departed
            if self.packets_offered >= num_packets and self.packets_departed >= self.packets_admitted:
                break
        
        # Calculate final metrics
        return self.get_metrics()
    
    def get_metrics(self):
        #Calculate and return performance metrics
        blocking_prob = self.packets_dropped / self.packets_offered if self.packets_offered > 0 else 0
        avg_queue_length = self.queue_length_sum / self.total_queue_length_samples if self.total_queue_length_samples > 0 else 0
        avg_sojourn_time = self.total_sojourn_time / self.sojourn_time_samples if self.sojourn_time_samples > 0 else 0
        
        return {
            'blocking_probability': blocking_prob,
            'average_queue_length': avg_queue_length,
            'average_sojourn_time': avg_sojourn_time,
            'packets_offered': self.packets_offered,
            'packets_dropped': self.packets_dropped,
            'packets_admitted': self.packets_admitted,
            'packets_departed': self.packets_departed
        }


def run_multiple_simulations(arrival_rate, service_rate, strategy, num_runs=10, num_packets=10000):
    
    # Run multiple independent simulations and average results
    
    blocking_probs = []
    avg_queue_lengths = []
    avg_sojourn_times = []
    
    for run in range(num_runs):
        sim = TwoQueueSimulation(
            arrival_rate=arrival_rate,
            service_rate=service_rate,
            strategy=strategy,
            seed=run  # Different seed for each run
        )
        metrics = sim.run(num_packets=num_packets)
        
        blocking_probs.append(metrics['blocking_probability'])
        avg_queue_lengths.append(metrics['average_queue_length'])
        avg_sojourn_times.append(metrics['average_sojourn_time'])
    
    return {
        'blocking_probability': np.mean(blocking_probs),
        'average_queue_length': np.mean(avg_queue_lengths),
        'average_sojourn_time': np.mean(avg_sojourn_times),
        'blocking_probability_std': np.std(blocking_probs),
        'average_queue_length_std': np.std(avg_queue_lengths),
        'average_sojourn_time_std': np.std(avg_sojourn_times)
    }

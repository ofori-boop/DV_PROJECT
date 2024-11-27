import socket
import threading
import time
import ast


class Router:
    def __init__(self, router_id):
        """Initialize the Router with a unique ID."""
        self.router_id = router_id
        self.interfaces = {}  # Interface ID → Port
        self.neighbors = {}  # Neighbor ID → {interface_id, cost}
        self.routing_table = {}  # Destination ID → (Next Hop, Cost)
        self.running = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('127.0.0.1', 10000 + router_id))  # Use a unique port for each router

    def configure_interface(self, interface_id, port):
        """Configure a virtual interface with a specific port."""
        self.interfaces[interface_id] = port
        print(f"Interface {interface_id} configured on port {port}")

    def set_link(self, interface_id, neighbor_id, cost):
        """Set a link to a neighbor via an interface with a specific cost."""
        if interface_id not in self.interfaces:
            print(f"Interface {interface_id} not found.")
            return
        self.neighbors[neighbor_id] = {"interface": interface_id, "cost": cost}
        self.routing_table[neighbor_id] = (neighbor_id, cost)  # Direct connection
        print(f"Link to router {neighbor_id} set with cost {cost}")

    def start_routing(self):
        """Start the DV routing protocol."""
        if self.running:
            print("Routing protocol is already running.")
            return
        self.running = True
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        threading.Thread(target=self.send_routing_updates, daemon=True).start()
        print("Routing protocol started.")

    def stop_routing(self):
        """Stop the DV routing protocol."""
        self.running = False
        print("Routing protocol stopped.")

    def send_routing_updates(self):
        """Periodically send routing table updates to neighbors."""
        while self.running:
            for neighbor_id, details in self.neighbors.items():
                interface_id = details["interface"]
                message = f"{self.router_id} {str(self.routing_table)}"
                self.send_message(interface_id, message)
            time.sleep(30)  # Send updates every 30 seconds

    def send_message(self, interface_id, message):
        """Send a message via a specific interface."""
        port = self.interfaces[interface_id]
        self.socket.sendto(message.encode(), ('127.0.0.1', port))

    def listen_for_messages(self):
        """Listen for incoming messages and process them."""
        while self.running:
            data, addr = self.socket.recvfrom(1024)
            message = data.decode()
            self.process_message(message)

    def process_message(self, message):
        """Process incoming routing updates."""
        sender_id, received_table = message.split(' ', 1)
        sender_id = int(sender_id)
        received_table = ast.literal_eval(received_table)  # Convert string back to dict
        self.process_routing_update(sender_id, received_table)

    def process_routing_update(self, sender_id, received_table):
        """Update routing table based on received advertisements."""
        updated = False
        for dest_id, (next_hop, cost) in received_table.items():
            new_cost = self.neighbors[sender_id]['cost'] + cost
            if dest_id not in self.routing_table or new_cost < self.routing_table[dest_id][1]:
                self.routing_table[dest_id] = (sender_id, new_cost)
                updated = True
        if updated:
            print(f"Routing table updated for Router {self.router_id}")
            self.show_routing_table()

    def show_routing_table(self):
        """Print the current routing table."""
        print(f"Routing Table for Router {self.router_id}:")
        for dest, (next_hop, cost) in self.routing_table.items():
            print(f"Destination: {dest}, Next Hop: {next_hop}, Cost: {cost}")

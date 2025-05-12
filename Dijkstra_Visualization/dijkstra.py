import heapq

class DijkstraAlgorithm:
    def __init__(self, graph):
        """Initialize Dijkstra's algorithm with a graph instance"""
        self.graph = graph
        
        # Algorithm state
        self.distances = {}
        self.predecessors = {}
        self.visited = set()
        self.priority_queue = []  # Min heap priority queue
        self.current_node = None
        self.current_neighbors = []
        self.path = []  # Final shortest path
        
        # Algorithm logs for explanation display
        self.step_count = 0
        self.logs = []
        self.testing_edges = []  # Store edges currently being tested
        
        # State flags
        self.initialized = False
        self.finished = False
        
    def initialize(self, start_node, end_node):
        """Initialize the algorithm with start and end nodes"""
        self.start_node = start_node
        self.end_node = end_node
        
        # Reset state
        self.distances = {}
        self.predecessors = {}
        self.visited = set()
        self.priority_queue = []
        self.current_node = None
        self.current_neighbors = []
        self.path = []
        
        self.step_count = 0
        self.logs = []
        self.testing_edges = []
        
        # Set initial distances
        for node in self.graph.get_nodes():
            if node == start_node:
                self.distances[node] = 0
            else:
                self.distances[node] = float('inf')
            self.predecessors[node] = None
            
        # Add start node to priority queue
        heapq.heappush(self.priority_queue, (0, start_node))
        
        self.initialized = True
        self.finished = False
        
        # Add initial log
        self.logs.append(f"Initialized Dijkstra's algorithm from {start_node} to {end_node}")
        self.logs.append(f"Set distance to {start_node} as 0 and all other nodes as infinity")
        
    def step(self):
        """Execute one step of the algorithm and return state information"""
        if not self.initialized or self.finished:
            return None
            
        self.step_count += 1
        self.testing_edges = []  # Reset testing edges
        
        # If the priority queue is empty, we're done
        if not self.priority_queue:
            self.logs.append("Priority queue is empty. Algorithm complete.")
            self.finished = True
            self._reconstruct_path()
            return {
                'finished': True,
                'path': self.path
            }
            
        # Get the node with the smallest distance from the priority queue
        current_distance, self.current_node = heapq.heappop(self.priority_queue)
        
        # If we've reached the end node, we're done
        if self.current_node == self.end_node:
            self.logs.append(f"Reached destination node {self.end_node}")
            self.finished = True
            self._reconstruct_path()
            return {
                'finished': True,
                'path': self.path
            }
            
        # Skip if the node has already been visited
        if self.current_node in self.visited:
            self.logs.append(f"Node {self.current_node} has already been visited. Skipping.")
            return self.step()
            
        # Mark the node as visited
        self.visited.add(self.current_node)
        
        self.logs.append(f"Step {self.step_count}: Processing node {self.current_node} with distance {current_distance}")
        
        # Get the neighbors of the current node
        self.current_neighbors = self.graph.get_neighbors(self.current_node)
        
        # Process neighbors
        for neighbor, weight in self.current_neighbors:
            self.testing_edges.append((self.current_node, neighbor))
            
            # Calculate new distance
            new_distance = self.distances[self.current_node] + weight
            
            # If we have a shorter path to the neighbor
            if new_distance < self.distances[neighbor]:
                self.logs.append(f"Found shorter path to {neighbor} via {self.current_node}: {new_distance}")
                self.distances[neighbor] = new_distance
                self.predecessors[neighbor] = self.current_node
                
                # Add to the priority queue
                heapq.heappush(self.priority_queue, (new_distance, neighbor))
            else:
                self.logs.append(f"Path to {neighbor} via {self.current_node} is not shorter: {new_distance} >= {self.distances[neighbor]}")
                
        # Return the current state
        return {
            'current_node': self.current_node,
            'visited': list(self.visited),
            'testing_edges': self.testing_edges,
            'distances': self.distances.copy(),
            'predecessors': self.predecessors.copy(),
            'priority_queue': sorted(self.priority_queue.copy()),
            'finished': False
        }
        
    def run_to_completion(self):
        """Run the algorithm to completion and return the final state"""
        while not self.finished:
            state = self.step()
            if state and state.get('finished', False):
                break
                
        return {
            'path': self.path,
            'distances': self.distances,
            'predecessors': self.predecessors,
            'visited': list(self.visited),
            'finished': True
        }
        
    def _reconstruct_path(self):
        """Reconstruct the shortest path from start to end"""
        if self.end_node not in self.distances or self.distances[self.end_node] == float('inf'):
            self.logs.append(f"No path exists from {self.start_node} to {self.end_node}")
            return
            
        current = self.end_node
        path = []
        
        while current:
            path.append(current)
            current = self.predecessors.get(current)
            
        self.path = list(reversed(path))
        self.logs.append(f"Shortest path: {' -> '.join(self.path)}")
        self.logs.append(f"Total distance: {self.distances[self.end_node]}")
        
    def get_current_logs(self, max_logs=5):
        """Get the most recent log entries for display"""
        if not self.logs:
            return ["No steps executed yet."]
        
        return self.logs[-max_logs:]
        
    def get_heap_items(self):
        """Get items in the priority queue (heap) for display"""
        return sorted(self.priority_queue.copy())
        
    def get_distances_table(self):
        """Get current distances as a formatted table for display"""
        table = []
        for node in sorted(self.distances.keys()):
            distance = self.distances[node]
            if distance == float('inf'):
                distance_str = "∞"
            else:
                distance_str = str(distance)
            table.append((node, distance_str))
        return table
        
    def get_predecessors_table(self):
        """Get current predecessors as a formatted table for display"""
        table = []
        for node in sorted(self.predecessors.keys()):
            predecessor = self.predecessors[node]
            if predecessor is None:
                predecessor_str = "-"
            else:
                predecessor_str = predecessor
            table.append((node, predecessor_str))
        return table 
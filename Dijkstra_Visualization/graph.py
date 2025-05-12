import pygame
import math

class Graph:
    def __init__(self):
        # Dictionary to store the graph as an adjacency list
        # Format: {node: [(neighbor, weight), ...]}
        self.graph = {}
        
        # Node positions for rendering
        self.node_positions = {}
        
        # Colors for visualization
        self.colors = {
            'node': (200, 200, 200),           # Regular node color (gray)
            'edge': (0, 0, 0),                 # Regular edge color (black)
            'text': (0, 0, 0),                 # Text color (black)
            'current': (0, 120, 255),          # Current node being processed (blue)
            'visited': (100, 100, 255),        # Visited nodes (light blue)
            'testing': (255, 165, 0),          # Testing edge (orange)
            'shortest': (0, 200, 0),           # Shortest path (green)
            'start': (0, 255, 0),              # Start node (green)
            'end': (255, 0, 0),                # End node (red)
            'background': (255, 255, 255)      # Background color (white)
        }
        
        # Node size
        self.node_radius = 20
        
        # Arrow properties
        self.arrow_size = 10
        
    def add_node(self, node, position):
        """Add a node to the graph with position (x, y)"""
        if node not in self.graph:
            self.graph[node] = []
        self.node_positions[node] = position
        
    def add_edge(self, start, end, weight):
        """Add a directed edge from start to end with given weight"""
        if start in self.graph:
            # Check if edge already exists
            for i, (neighbor, _) in enumerate(self.graph[start]):
                if neighbor == end:
                    # Update weight if edge exists
                    self.graph[start][i] = (end, weight)
                    return
            # Add new edge
            self.graph[start].append((end, weight))
        else:
            # Create node with this edge
            self.graph[start] = [(end, weight)]
            
    def get_neighbors(self, node):
        """Return list of (neighbor, weight) tuples for a node"""
        if node in self.graph:
            return self.graph[node]
        return []
        
    def get_nodes(self):
        """Return list of all nodes in the graph"""
        return list(self.graph.keys())
        
    def load_example_graph(self):
        """Load the example graph shown in the provided image"""
        # Clear any existing graph
        self.graph = {}
        self.node_positions = {}
        
        # Define node positions based on a circle layout
        center_x, center_y = 400, 300
        radius = 200
        
        # Define nodes and their positions
        nodes = ['s', '2', '3', '6', '5', '4', '7', 't']
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * (i / len(nodes))
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.add_node(node, (x, y))
            
        # Add edges based on the diagram
        self.add_edge('s', '2', 9)
        self.add_edge('s', '6', 14)
        self.add_edge('s', '7', 15)
        self.add_edge('2', '3', 23)
        self.add_edge('3', 't', 19)
        self.add_edge('6', '5', 30)
        self.add_edge('6', '7', 5)
        self.add_edge('7', '5', 20)
        self.add_edge('7', 't', 44)
        self.add_edge('5', '4', 11)
        self.add_edge('5', 't', 16)
        self.add_edge('4', 't', 6)
        self.add_edge('5', '3', 2)
        self.add_edge('3', '4', 6)
        self.add_edge('6', '3', 18)
        
    def draw(self, screen, current_node=None, visited_nodes=None, 
             testing_edges=None, shortest_path=None, start_node=None, end_node=None):
        """Draw the graph on the screen with visualization of algorithm state"""
        if visited_nodes is None:
            visited_nodes = []
        if testing_edges is None:
            testing_edges = []
        if shortest_path is None:
            shortest_path = []
            
        # Draw edges first (so they appear behind the nodes)
        for start in self.graph:
            start_pos = self.node_positions[start]
            for end, weight in self.graph[start]:
                end_pos = self.node_positions[end]
                
                # Determine edge color based on algorithm state
                edge_color = self.colors['edge']
                
                # Check if this edge is part of the shortest path
                if shortest_path and len(shortest_path) > 1:
                    for i in range(len(shortest_path) - 1):
                        if shortest_path[i] == start and shortest_path[i + 1] == end:
                            edge_color = self.colors['shortest']
                            break
                
                # Check if this edge is being tested
                if (start, end) in testing_edges:
                    edge_color = self.colors['testing']
                
                # Draw the edge line
                self._draw_edge(screen, start_pos, end_pos, weight, edge_color)
        
        # Draw nodes
        for node in self.graph:
            # Determine node color based on algorithm state
            node_color = self.colors['node']
            
            if node == current_node:
                node_color = self.colors['current']
            elif node in visited_nodes:
                node_color = self.colors['visited']
            
            if node == start_node:
                node_color = self.colors['start']
            elif node == end_node:
                node_color = self.colors['end']
                
            # Draw the node
            pos = self.node_positions[node]
            pygame.draw.circle(screen, node_color, pos, self.node_radius)
            pygame.draw.circle(screen, self.colors['edge'], pos, self.node_radius, 2)
            
            # Draw node label
            font = pygame.font.SysFont('Arial', 20)
            text = font.render(str(node), True, self.colors['text'])
            text_rect = text.get_rect(center=pos)
            screen.blit(text, text_rect)
    
    def _draw_edge(self, screen, start_pos, end_pos, weight, color):
        """Draw a directed edge with weight and arrow"""
        # Calculate direction vector
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = max(1, math.sqrt(dx * dx + dy * dy))
        
        # Normalize direction
        dx, dy = dx / distance, dy / distance
        
        # Adjust start and end positions to account for node radius
        adjusted_start_x = start_pos[0] + dx * self.node_radius
        adjusted_start_y = start_pos[1] + dy * self.node_radius
        adjusted_end_x = end_pos[0] - dx * self.node_radius
        adjusted_end_y = end_pos[1] - dy * self.node_radius
        
        # Draw the line
        pygame.draw.line(screen, color, 
                         (adjusted_start_x, adjusted_start_y), 
                         (adjusted_end_x, adjusted_end_y), 2)
        
        # Draw arrow at the end
        self._draw_arrow(screen, (adjusted_end_x, adjusted_end_y), (dx, dy), color)
        
        # Draw weight
        # Position the weight text in the middle of the edge
        mid_x = (adjusted_start_x + adjusted_end_x) / 2
        mid_y = (adjusted_start_y + adjusted_end_y) / 2
        
        # Offset the text slightly to the side of the edge
        normal_x, normal_y = -dy, dx  # Normal vector to the edge
        offset_x = mid_x + normal_x * 15
        offset_y = mid_y + normal_y * 15
        
        font = pygame.font.SysFont('Arial', 16)
        text = font.render(str(weight), True, color)
        text_rect = text.get_rect(center=(offset_x, offset_y))
        screen.blit(text, text_rect)
    
    def _draw_arrow(self, screen, pos, direction, color):
        """Draw an arrow head at pos pointing in direction"""
        dx, dy = direction
        
        # Calculate perpendicular vector
        perp_dx, perp_dy = -dy, dx
        
        # Calculate arrow points
        x, y = pos
        point1 = (x - dx * self.arrow_size - perp_dx * self.arrow_size/2, 
                  y - dy * self.arrow_size - perp_dy * self.arrow_size/2)
        point2 = (x - dx * self.arrow_size + perp_dx * self.arrow_size/2, 
                  y - dy * self.arrow_size + perp_dy * self.arrow_size/2)
        
        # Draw arrow head
        pygame.draw.polygon(screen, color, [pos, point1, point2]) 
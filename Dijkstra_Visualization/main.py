import pygame
import sys
import time

from graph import Graph
from dijkstra import DijkstraAlgorithm
from heap_visual import HeapVisualizer
from info_panel import InfoPanel
from button import Button

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

class DijkstraVisualization:
    def __init__(self):
        # Create the main window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dijkstra Algorithm Visualization")
        
        # Create a clock for controlling FPS
        self.clock = pygame.time.Clock()
        
        # Create graph
        self.graph = Graph()
        self.graph.load_example_graph()
        
        # Create Dijkstra algorithm
        self.dijkstra = DijkstraAlgorithm(self.graph)
        
        # Create visualization components
        # Panel sizes and positions
        self.graph_rect = pygame.Rect(0, 0, 800, 600)
        self.info_panel_rect = pygame.Rect(0, 600, 800, 200)
        self.heap_panel_rect = pygame.Rect(800, 0, 400, 300)
        self.controls_rect = pygame.Rect(800, 300, 400, 500)
        
        # Create heap visualizer
        self.heap_visualizer = HeapVisualizer(self.heap_panel_rect)
        
        # Create info panel
        self.info_panel = InfoPanel(self.info_panel_rect)
        
        # Create buttons
        button_width = 180
        button_height = 40
        button_margin = 20
        button_x = 800 + (400 - button_width) // 2
        button_y = 320
        
        self.buttons = {
            'init': Button(
                (button_x, button_y, button_width, button_height),
                "Initialize Algorithm"
            ),
            'step': Button(
                (button_x, button_y + (button_height + button_margin), button_width, button_height),
                "Next Step"
            ),
            'run': Button(
                (button_x, button_y + 2 * (button_height + button_margin), button_width, button_height),
                "Run All Steps"
            ),
            'reset': Button(
                (button_x, button_y + 3 * (button_height + button_margin), button_width, button_height),
                "Reset"
            )
        }
        
        # Disable step and run buttons initially
        self.buttons['step'].disable()
        self.buttons['run'].disable()
        
        # Algorithm state
        self.algorithm_state = None
        self.last_extracted = None
        self.auto_run = False
        self.auto_run_delay = 0.5  # seconds between steps
        self.last_step_time = 0
        
    def handle_events(self):
        """Handle pygame events"""
        # Get mouse state
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # Left button
        
        # Update buttons
        for name, button in self.buttons.items():
            if button.update(mouse_pos, mouse_pressed):
                self.handle_button_click(name)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def handle_button_click(self, button_name):
        """Handle button clicks"""
        if button_name == 'init':
            # Initialize the algorithm
            self.dijkstra.initialize('s', 't')
            self.algorithm_state = None
            self.last_extracted = None
            self.auto_run = False
            
            # Enable step and run buttons
            self.buttons['step'].enable()
            self.buttons['run'].enable()
            
        elif button_name == 'step':
            # Execute one step of the algorithm
            state = self.dijkstra.step()
            if state:
                self.algorithm_state = state
                
                # Track the last extracted item for the heap visualization
                if state.get('current_node') and state.get('priority_queue'):
                    if hasattr(self.dijkstra, 'current_node') and self.dijkstra.current_node:
                        distance = self.dijkstra.distances.get(self.dijkstra.current_node, float('inf'))
                        self.last_extracted = (distance, self.dijkstra.current_node)
                
                # If algorithm is finished, disable step and run buttons
                if state.get('finished', False):
                    self.buttons['step'].disable()
                    self.buttons['run'].disable()
            
        elif button_name == 'run':
            # Auto-run the algorithm
            self.auto_run = True
            self.last_step_time = time.time()
            
        elif button_name == 'reset':
            # Reset everything
            self.dijkstra = DijkstraAlgorithm(self.graph)
            self.algorithm_state = None
            self.last_extracted = None
            self.auto_run = False
            
            # Disable step and run buttons
            self.buttons['step'].disable()
            self.buttons['run'].disable()
            
    def update(self):
        """Update game state"""
        # Handle auto-run
        if self.auto_run:
            current_time = time.time()
            if current_time - self.last_step_time >= self.auto_run_delay:
                self.handle_button_click('step')
                self.last_step_time = current_time
                
                # Stop auto-run if algorithm finished
                if self.algorithm_state and self.algorithm_state.get('finished', False):
                    self.auto_run = False
    
    def draw(self):
        """Draw everything on the screen"""
        # Fill the background
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw graph
        current_node = None
        visited_nodes = []
        testing_edges = []
        shortest_path = []
        
        if self.algorithm_state:
            current_node = self.algorithm_state.get('current_node')
            visited_nodes = self.algorithm_state.get('visited', [])
            testing_edges = self.algorithm_state.get('testing_edges', [])
            
            if self.algorithm_state.get('finished', False) and 'path' in self.algorithm_state:
                shortest_path = self.algorithm_state.get('path', [])
        
        self.graph.draw(
            self.screen, 
            current_node=current_node,
            visited_nodes=visited_nodes,
            testing_edges=testing_edges,
            shortest_path=shortest_path,
            start_node='s',
            end_node='t'
        )
        
        # Draw heap visualization
        heap_items = []
        if self.dijkstra.initialized:
            heap_items = self.dijkstra.get_heap_items()
            
        self.heap_visualizer.draw(
            self.screen,
            heap_items,
            self.last_extracted
        )
        
        # Draw info panel
        distances_table = []
        predecessors_table = []
        logs = ["Click 'Initialize Algorithm' to start."]
        
        if self.dijkstra.initialized:
            distances_table = self.dijkstra.get_distances_table()
            predecessors_table = self.dijkstra.get_predecessors_table()
            logs = self.dijkstra.get_current_logs()
            
        self.info_panel.draw(
            self.screen,
            distances_table,
            predecessors_table,
            logs
        )
        
        # Draw buttons
        for button in self.buttons.values():
            button.draw(self.screen)
            
        # If algorithm is finished, display the result
        if self.algorithm_state and self.algorithm_state.get('finished', False):
            if 'path' in self.algorithm_state and self.algorithm_state['path']:
                path_str = " → ".join(self.algorithm_state['path'])
                distance = self.dijkstra.distances.get('t', float('inf'))
                
                if distance == float('inf'):
                    distance_str = "∞ (no path)"
                else:
                    distance_str = str(distance)
                
                # Draw result text
                font = pygame.font.SysFont('Arial', 24, bold=True)
                result_text = font.render(f"Shortest Path: {path_str}", True, (0, 100, 0))
                distance_text = font.render(f"Total Distance: {distance_str}", True, (0, 100, 0))
                
                result_rect = result_text.get_rect(center=(self.graph_rect.width//2, 30))
                distance_rect = distance_text.get_rect(center=(self.graph_rect.width//2, 60))
                
                self.screen.blit(result_text, result_rect)
                self.screen.blit(distance_text, distance_rect)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

# Run the application
if __name__ == "__main__":
    app = DijkstraVisualization()
    app.run() 
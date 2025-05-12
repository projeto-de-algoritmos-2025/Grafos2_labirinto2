import pygame

class HeapVisualizer:
    def __init__(self, rect, font_size=16):
        """Initialize heap visualizer in a specified rectangle
        
        Args:
            rect: A rectangle (x, y, width, height) to contain the heap visualization
            font_size: Size of the font for text
        """
        self.rect = rect
        self.font_size = font_size
        self.font = pygame.font.SysFont('Arial', font_size)
        
        # Colors
        self.colors = {
            'background': (240, 240, 240),
            'text': (0, 0, 0),
            'node': (200, 200, 255),
            'node_outline': (100, 100, 200),
            'title': (0, 0, 0),
            'extracted': (255, 200, 200)
        }
        
        # Node properties
        self.node_radius = 25
        self.last_extracted = None
        
    def draw(self, screen, heap_items, extracted_item=None):
        """Draw the heap visualization
        
        Args:
            screen: Pygame screen to draw on
            heap_items: List of (priority, node) tuples to visualize
            extracted_item: Last extracted (priority, node) from the heap
        """
        # Draw background rectangle
        pygame.draw.rect(screen, self.colors['background'], self.rect)
        pygame.draw.rect(screen, self.colors['node_outline'], self.rect, 2)
        
        # Draw title
        title_font = pygame.font.SysFont('Arial', self.font_size + 4, bold=True)
        title_text = title_font.render("Priority Queue (Min Heap)", True, self.colors['title'])
        title_rect = title_text.get_rect(centerx=self.rect[0]+self.rect[2]//2, y=self.rect[1]+10)
        screen.blit(title_text, title_rect)
        
        # Keep track of the last extracted item
        if extracted_item:
            self.last_extracted = extracted_item
        
        # Draw the extracted item if available
        if self.last_extracted:
            y_pos = title_rect.bottom + 30
            extracted_text = self.font.render(f"Last extracted: ({self.last_extracted[0]}, {self.last_extracted[1]})", 
                                           True, self.colors['text'])
            extracted_rect = extracted_text.get_rect(centerx=self.rect[0]+self.rect[2]//2, y=y_pos)
            screen.blit(extracted_text, extracted_rect)
            
            # Draw red box around extracted
            pygame.draw.rect(screen, self.colors['extracted'], 
                            (extracted_rect.x - 5, extracted_rect.y - 5, 
                             extracted_rect.width + 10, extracted_rect.height + 10), 2)
            
            start_y = extracted_rect.bottom + 20
        else:
            start_y = title_rect.bottom + 20
        
        # Draw the heap as a list
        if not heap_items:
            empty_text = self.font.render("Queue is empty", True, self.colors['text'])
            empty_rect = empty_text.get_rect(centerx=self.rect[0]+self.rect[2]//2, y=start_y+20)
            screen.blit(empty_text, empty_rect)
            return
        
        # Draw heap nodes
        self._draw_heap_as_list(screen, heap_items, start_y)
        
    def _draw_heap_as_list(self, screen, heap_items, start_y):
        """Draw the heap as a vertical list
        
        Args:
            screen: Pygame screen to draw on
            heap_items: List of (priority, node) tuples to visualize
            start_y: Y coordinate to start drawing from
        """
        # Calculate maximum items that can fit
        max_items = min(len(heap_items), (self.rect[3] - start_y - 20) // 40)
        
        for i in range(min(len(heap_items), max_items)):
            priority, node = heap_items[i]
            
            # Y position for each node
            y_pos = start_y + i * 40
            
            # Center of node
            center_x = self.rect[0] + self.rect[2] // 2
            center_y = y_pos + 20
            
            # Draw circle for node
            pygame.draw.circle(screen, self.colors['node'], (center_x, center_y), self.node_radius)
            pygame.draw.circle(screen, self.colors['node_outline'], (center_x, center_y), self.node_radius, 2)
            
            # Text for the node
            if isinstance(priority, float) and priority == float('inf'):
                priority_str = '∞'
            else:
                priority_str = str(priority)
                
            text = self.font.render(f"({priority_str}, {node})", True, self.colors['text'])
            text_rect = text.get_rect(center=(center_x, center_y))
            screen.blit(text, text_rect)
            
            # Add index label
            index_text = self.font.render(f"{i}", True, self.colors['text'])
            index_rect = index_text.get_rect(x=center_x - 40 - self.node_radius, centery=center_y)
            screen.blit(index_text, index_rect)
        
        # Show count of remaining items if not all shown
        if len(heap_items) > max_items:
            more_text = self.font.render(f"... {len(heap_items) - max_items} more items", True, self.colors['text'])
            more_rect = more_text.get_rect(centerx=self.rect[0]+self.rect[2]//2, y=start_y + max_items * 40 + 10)
            screen.blit(more_text, more_rect)
    
    def _draw_heap_as_tree(self, screen, heap_items, start_y):
        """Draw the heap as a binary tree (more advanced visualization)
        
        Note: This is more complex and may not always render well for larger heaps,
        so we're using the list representation as the default.
        
        Args:
            screen: Pygame screen to draw on
            heap_items: List of (priority, node) tuples to visualize
            start_y: Y coordinate to start drawing from
        """
        if not heap_items:
            return
            
        level_height = 70
        max_levels = 4  # Limit levels to prevent overflow
        
        # Calculate the number of levels in the heap
        levels = 0
        total_nodes = 0
        while total_nodes < len(heap_items) and levels < max_levels:
            levels += 1
            total_nodes += 2 ** (levels - 1)
        
        # Width of the tree visualization
        tree_width = self.rect[2] - 40
        
        # Draw nodes level by level
        for level in range(levels):
            # Number of nodes at this level and previous levels
            nodes_in_level = 2 ** level
            start_index = 2 ** level - 1
            
            # Level spacing
            level_width = tree_width
            node_spacing = level_width / nodes_in_level
            
            for i in range(nodes_in_level):
                node_index = start_index + i
                if node_index >= len(heap_items):
                    break
                    
                priority, node = heap_items[node_index]
                
                # Node position (centered)
                x = self.rect[0] + 20 + i * node_spacing + node_spacing / 2
                y = start_y + level * level_height
                
                # Draw circle for node
                pygame.draw.circle(screen, self.colors['node'], (x, y), self.node_radius)
                pygame.draw.circle(screen, self.colors['node_outline'], (x, y), self.node_radius, 2)
                
                # Text for the node
                if isinstance(priority, float) and priority == float('inf'):
                    priority_str = '∞'
                else:
                    priority_str = str(priority)
                    
                text = self.font.render(f"({priority_str}, {node})", True, self.colors['text'])
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)
                
                # Draw lines to children
                left_child = 2 * node_index + 1
                right_child = 2 * node_index + 2
                
                if left_child < len(heap_items):
                    left_x = self.rect[0] + 20 + (2 * i) * (node_spacing / 2) + node_spacing / 4
                    left_y = start_y + (level + 1) * level_height
                    pygame.draw.line(screen, self.colors['node_outline'], (x, y + self.node_radius), 
                                   (left_x, left_y - self.node_radius), 2)
                    
                if right_child < len(heap_items):
                    right_x = self.rect[0] + 20 + (2 * i + 1) * (node_spacing / 2) + node_spacing / 4
                    right_y = start_y + (level + 1) * level_height
                    pygame.draw.line(screen, self.colors['node_outline'], (x, y + self.node_radius), 
                                   (right_x, right_y - self.node_radius), 2) 
import pygame

class InfoPanel:
    def __init__(self, rect, font_size=16):
        """Initialize the information panel
        
        Args:
            rect: A rectangle (x, y, width, height) to contain the panel
            font_size: Size of the font for text
        """
        self.rect = rect
        self.font_size = font_size
        self.font = pygame.font.SysFont('Arial', font_size)
        self.title_font = pygame.font.SysFont('Arial', font_size + 4, bold=True)
        
        # Colors
        self.colors = {
            'background': (240, 240, 240),
            'text': (0, 0, 0),
            'title': (0, 0, 0),
            'table_header': (220, 220, 220),
            'table_row_even': (255, 255, 255),
            'table_row_odd': (245, 245, 245),
            'border': (100, 100, 200)
        }
        
    def draw(self, screen, distances_table, predecessors_table, logs):
        """Draw the information panel with all data
        
        Args:
            screen: Pygame screen to draw on
            distances_table: List of (node, distance) tuples
            predecessors_table: List of (node, predecessor) tuples
            logs: List of log strings to display
        """
        # Draw background rectangle
        pygame.draw.rect(screen, self.colors['background'], self.rect)
        pygame.draw.rect(screen, self.colors['border'], self.rect, 2)
        
        # Panel margin
        margin = 10
        content_width = self.rect[2] - margin * 2
        
        # Current y position to draw content
        y_pos = self.rect[1] + margin
        
        # Draw title
        title_text = self.title_font.render("Algorithm Information", True, self.colors['title'])
        title_rect = title_text.get_rect(centerx=self.rect[0]+self.rect[2]//2, y=y_pos)
        screen.blit(title_text, title_rect)
        y_pos = title_rect.bottom + margin
        
        # Draw tables side by side
        table_width = (content_width - margin) // 2
        
        # Draw distances table
        distances_height = self._draw_table(screen, 
                                           (self.rect[0] + margin, y_pos, table_width, 0), 
                                           "Distances", 
                                           [("Node", "Dist")] + distances_table)
        
        # Draw predecessors table
        predecessors_height = self._draw_table(screen, 
                                              (self.rect[0] + margin + table_width + margin, y_pos, table_width, 0), 
                                              "Predecessors", 
                                              [("Node", "Prev")] + predecessors_table)
        
        # Update y position to after the tables
        y_pos += max(distances_height, predecessors_height) + margin * 2
        
        # Draw logs
        logs_title = self.title_font.render("Algorithm Steps", True, self.colors['title'])
        logs_title_rect = logs_title.get_rect(x=self.rect[0] + margin, y=y_pos)
        screen.blit(logs_title, logs_title_rect)
        y_pos = logs_title_rect.bottom + margin
        
        # Draw log entries
        for log in logs:
            # Word wrap long logs
            words = log.split(' ')
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_width = self.font.size(test_line)[0]
                
                if test_width <= content_width:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw each line
            for line in lines:
                log_text = self.font.render(line, True, self.colors['text'])
                log_rect = log_text.get_rect(x=self.rect[0] + margin, y=y_pos)
                screen.blit(log_text, log_rect)
                y_pos = log_rect.bottom + 5
                
                # Check if we're out of the panel bounds
                if y_pos > self.rect[1] + self.rect[3] - margin:
                    more_text = self.font.render("...", True, self.colors['text'])
                    more_rect = more_text.get_rect(x=self.rect[0] + margin, y=y_pos - 20)
                    screen.blit(more_text, more_rect)
                    break
            
            # Check if we're out of the panel bounds
            if y_pos > self.rect[1] + self.rect[3] - margin:
                break
    
    def _draw_table(self, screen, rect, title, data):
        """Draw a table with a title and data
        
        Args:
            screen: Pygame screen to draw on
            rect: Rectangle to draw the table in (x, y, width, height)
            title: Title of the table
            data: List of row tuples, first row is the header
            
        Returns:
            The height of the table
        """
        x, y, width, _ = rect
        
        # Draw title
        title_text = self.title_font.render(title, True, self.colors['title'])
        title_rect = title_text.get_rect(x=x, y=y)
        screen.blit(title_text, title_rect)
        
        # Current y position after title
        y_pos = title_rect.bottom + 5
        
        # Row height
        row_height = self.font_size + 10
        
        # Calculate column widths (even distribution)
        if data and len(data[0]) > 0:
            col_width = width // len(data[0])
            
            # Draw header
            header_rect = pygame.Rect(x, y_pos, width, row_height)
            pygame.draw.rect(screen, self.colors['table_header'], header_rect)
            pygame.draw.rect(screen, self.colors['border'], header_rect, 1)
            
            for i, cell in enumerate(data[0]):
                cell_text = self.font.render(str(cell), True, self.colors['text'])
                cell_rect = cell_text.get_rect(
                    centerx=x + i*col_width + col_width//2,
                    centery=y_pos + row_height//2
                )
                screen.blit(cell_text, cell_rect)
            
            y_pos += row_height
            
            # Draw data rows
            for row_idx, row in enumerate(data[1:]):
                row_rect = pygame.Rect(x, y_pos, width, row_height)
                
                # Alternate row colors
                if row_idx % 2 == 0:
                    pygame.draw.rect(screen, self.colors['table_row_even'], row_rect)
                else:
                    pygame.draw.rect(screen, self.colors['table_row_odd'], row_rect)
                    
                pygame.draw.rect(screen, self.colors['border'], row_rect, 1)
                
                for i, cell in enumerate(row):
                    cell_text = self.font.render(str(cell), True, self.colors['text'])
                    cell_rect = cell_text.get_rect(
                        centerx=x + i*col_width + col_width//2,
                        centery=y_pos + row_height//2
                    )
                    screen.blit(cell_text, cell_rect)
                
                y_pos += row_height
                
                # Check if we're out of the panel bounds
                if y_pos > self.rect[1] + self.rect[3] - 10:
                    more_rect = pygame.Rect(x, y_pos - row_height, width, row_height)
                    pygame.draw.rect(screen, self.colors['table_row_odd'], more_rect)
                    pygame.draw.rect(screen, self.colors['border'], more_rect, 1)
                    
                    more_text = self.font.render("...", True, self.colors['text'])
                    more_rect = more_text.get_rect(centerx=x + width//2, centery=y_pos - row_height//2)
                    screen.blit(more_text, more_rect)
                    
                    y_pos = y_pos - row_height + row_height
                    break
        
        # Return the height of the table
        return y_pos - y 
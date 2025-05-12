import pygame

class Button:
    def __init__(self, rect, text, font_size=18, color_scheme=None):
        """Initialize a button with text
        
        Args:
            rect: A rectangle (x, y, width, height) for the button
            text: Text to display on the button
            font_size: Size of the font for the button text
            color_scheme: Optional custom color scheme
        """
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = pygame.font.SysFont('Arial', font_size)
        
        # Default colors
        self.colors = {
            'normal': {
                'bg': (100, 100, 200),
                'border': (50, 50, 150),
                'text': (255, 255, 255)
            },
            'hover': {
                'bg': (120, 120, 220),
                'border': (70, 70, 170),
                'text': (255, 255, 255)
            },
            'pressed': {
                'bg': (80, 80, 180),
                'border': (30, 30, 130),
                'text': (230, 230, 230)
            },
            'disabled': {
                'bg': (150, 150, 150),
                'border': (100, 100, 100),
                'text': (200, 200, 200)
            }
        }
        
        # Override with custom colors if provided
        if color_scheme:
            for state, colors in color_scheme.items():
                if state in self.colors:
                    for color_key, color_val in colors.items():
                        if color_key in self.colors[state]:
                            self.colors[state][color_key] = color_val
        
        # Button state
        self.state = 'normal'  # 'normal', 'hover', 'pressed', 'disabled'
        self.is_hovered = False
        self.is_pressed = False
        self.is_enabled = True
        
    def enable(self):
        """Enable the button"""
        self.is_enabled = True
        self.state = 'normal'
        
    def disable(self):
        """Disable the button"""
        self.is_enabled = False
        self.state = 'disabled'
        
    def update(self, mouse_pos, mouse_pressed):
        """Update button state based on mouse position and button state
        
        Args:
            mouse_pos: Current mouse position (x, y)
            mouse_pressed: Boolean indicating if mouse button is pressed
            
        Returns:
            Boolean indicating if the button was clicked (released while hovering)
        """
        if not self.is_enabled:
            return False
            
        was_pressed = self.is_pressed
        clicked = False
        
        # Check if mouse is over the button
        hover = self.rect.collidepoint(mouse_pos)
        self.is_hovered = hover
        
        # Update press state
        if hover and mouse_pressed:
            self.is_pressed = True
            self.state = 'pressed'
        else:
            # Check for click (release while hovering)
            if was_pressed and hover and not mouse_pressed:
                clicked = True
                
            self.is_pressed = False
            
            if hover:
                self.state = 'hover'
            else:
                self.state = 'normal'
                
        return clicked
        
    def draw(self, screen):
        """Draw the button on the screen
        
        Args:
            screen: Pygame screen to draw on
        """
        # Get the right colors based on state
        colors = self.colors[self.state]
        
        # Draw button background
        pygame.draw.rect(screen, colors['bg'], self.rect, border_radius=5)
        pygame.draw.rect(screen, colors['border'], self.rect, width=2, border_radius=5)
        
        # Draw text centered on button
        text_surf = self.font.render(self.text, True, colors['text'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect) 
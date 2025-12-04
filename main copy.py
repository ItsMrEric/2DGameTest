import pygame
import time

class InputHandler:
    def __init__(self):
        # Track key states
        self.keys_pressed = {}
        self.keys_down = {}  # Keys pressed this frame
        self.keys_up = {}    # Keys released this frame
        
        # Customizable key bindings
        self.bindings = {
            'move_left': [pygame.K_a, pygame.K_LEFT],
            'move_right': [pygame.K_d, pygame.K_RIGHT],
            'jump': [pygame.K_SPACE, pygame.K_w, pygame.K_UP],
            'attack': [pygame.K_x],
            'special': [pygame.K_z],
            'pause': [pygame.K_ESCAPE, pygame.K_p]
        }
    
    def update(self):
        """Call this once per frame before checking input"""
        # Reset one-frame states
        self.keys_down.clear()
        self.keys_up.clear()
        
        # Get all currently pressed keys
        current_keys = pygame.key.get_pressed()
        
        # Process events for key down/up
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.keys_down[event.key] = True
                self.keys_pressed[event.key] = True
                
            elif event.type == pygame.KEYUP:
                self.keys_up[event.key] = True
                if event.key in self.keys_pressed:
                    del self.keys_pressed[event.key]
        
        # Update continuous pressed state from get_pressed()
        for key_code in range(len(current_keys)):
            if current_keys[key_code]:
                self.keys_pressed[key_code] = True
    
    def is_pressed(self, action_name):
        """Check if an action key is currently held"""
        if action_name in self.bindings:
            for key in self.bindings[action_name]:
                if key in self.keys_pressed:
                    return True
        return False
    
    def is_just_pressed(self, action_name):
        """Check if an action key was pressed THIS FRAME"""
        if action_name in self.bindings:
            for key in self.bindings[action_name]:
                if key in self.keys_down:
                    return True
        return False
    
    def is_just_released(self, action_name):
        """Check if an action key was released THIS FRAME"""
        if action_name in self.bindings:
            for key in self.bindings[action_name]:
                if key in self.keys_up:
                    return True
        return False

# Usage in your game
class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.speed = 300  # pixels/second
        self.jump_force = 500
        self.velocity_y = 0
        self.on_ground = False
    
    def update(self, dt, input_handler):
        # Continuous movement
        if input_handler.is_pressed('move_left'):
            self.x -= self.speed * dt
        if input_handler.is_pressed('move_right'):
            self.x += self.speed * dt
        
        # One-time jump (only when first pressed)
        if input_handler.is_just_pressed('jump') and self.on_ground:
            self.velocity_y = -self.jump_force
            self.on_ground = False
        
        # Attack combo
        if input_handler.is_just_pressed('attack'):
            self.start_attack()
        
        # Apply gravity
        self.velocity_y += 980 * dt  # 980 pixels/sec² gravity
        self.y += self.velocity_y * dt
        
        # Ground collision
        if self.y >= 500:  # Ground level
            self.y = 500
            self.velocity_y = 0
            self.on_ground = True

# Main game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    input_handler = InputHandler()
    player = Player()
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        # Update input
        input_handler.update()
        
        # Check for quit (escape or window close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Check pause (using the new input handler)
        if input_handler.is_just_pressed('pause'):
            paused = not paused
        
        # Update player with input
        player.update(dt, input_handler)
        
        # Drawing code...
        screen.fill((30, 30, 50))
        pygame.draw.rect(screen, (255, 100, 100), 
                        (player.x - 25, player.y - 25, 50, 50))
        
        # Display input state
        font = pygame.font.Font(None, 24)
        text = font.render(f"Left: {input_handler.is_pressed('move_left')} "
                          f"Right: {input_handler.is_pressed('move_right')} "
                          f"Jump: {input_handler.is_just_pressed('jump')}",
                          True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
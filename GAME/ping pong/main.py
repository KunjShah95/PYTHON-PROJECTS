import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
FPS = 60
FONT_SIZE = 74
SCORE_LIMIT = 20  # Increased score limit to 20
PADDLE_SPEED = 10
BALL_SPEED_INITIAL = 7
POWER_UP_DURATION = 5000  # 5 seconds in milliseconds
POWER_UP_SPAWN_TIME = 10000  # 10 seconds in milliseconds

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Ping Pong Game")

# Load sound effects
try:
    paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
    wall_hit_sound = pygame.mixer.Sound("wall_hit.wav")
    score_sound = pygame.mixer.Sound("score.wav")
    power_up_sound = pygame.mixer.Sound("power_up.wav")
except:
    # If sound files don't exist, create dummy functions
    class DummySound:
        def play(self): pass
    paddle_hit_sound = wall_hit_sound = score_sound = power_up_sound = DummySound()

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, 
                               BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.speed_x = BALL_SPEED_INITIAL * (-1) ** (pygame.time.get_ticks() % 2)
        self.speed_y = BALL_SPEED_INITIAL * (-1) ** (pygame.time.get_ticks() % 2)
        self.color = WHITE
        self.is_power_ball = False

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
            wall_hit_sound.play()

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = BALL_SPEED_INITIAL * (-1) ** (pygame.time.get_ticks() % 2)
        self.speed_y = BALL_SPEED_INITIAL * (-1) ** (pygame.time.get_ticks() % 2)
        self.color = WHITE
        self.is_power_ball = False

    def increase_speed(self, factor=1.1):
        # Increase ball speed but cap it at a maximum value
        max_speed = 15
        self.speed_x *= factor
        self.speed_y *= factor
        
        # Cap the speed
        if abs(self.speed_x) > max_speed:
            self.speed_x = max_speed * (1 if self.speed_x > 0 else -1)
        if abs(self.speed_y) > max_speed:
            self.speed_y = max_speed * (1 if self.speed_y > 0 else -1)

    def activate_power_ball(self):
        self.is_power_ball = True
        self.color = RED

    def deactivate_power_ball(self):
        self.is_power_ball = False
        self.color = WHITE

# Paddle class
class Paddle:
    def __init__(self, x, control_type="player"):
        self.rect = pygame.Rect(x, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score = 0
        self.color = WHITE
        self.original_height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.control_type = control_type  # "player" or "ai"
        self.ai_reaction_time = 2  # Lower is faster
        self.power_up_active = None
        self.power_up_end_time = 0

    def move(self, dy):
        self.rect.y += dy * self.speed
        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def ai_move(self, ball):
        # Basic AI: follow the ball with some delay and occasional mistakes
        if pygame.time.get_ticks() % self.ai_reaction_time == 0:
            target_y = ball.rect.centery - self.rect.height // 2
            current_y = self.rect.y
            
            # Add some randomness to make AI imperfect
            if random.random() < 0.2:  # 20% chance to make a mistake
                target_y += random.randint(-50, 50)
            
            if target_y > current_y:
                self.move(1)
            elif target_y < current_y:
                self.move(-1)

    def reset_position(self):
        self.rect.y = HEIGHT // 2 - self.rect.height // 2

    def activate_power_up(self, power_up_type):
        self.power_up_active = power_up_type
        self.power_up_end_time = pygame.time.get_ticks() + POWER_UP_DURATION
        
        if power_up_type == "bigger_paddle":
            self.rect.height = int(self.original_height * 1.5)
            self.color = GREEN
        elif power_up_type == "smaller_paddle":
            self.rect.height = int(self.original_height * 0.7)
            self.color = RED
        elif power_up_type == "faster_paddle":
            self.speed = PADDLE_SPEED * 1.5
            self.color = BLUE
        elif power_up_type == "slower_paddle":
            self.speed = PADDLE_SPEED * 0.7
            self.color = YELLOW

    def deactivate_power_up(self):
        self.power_up_active = None
        self.rect.height = self.original_height
        self.speed = PADDLE_SPEED
        self.color = WHITE

    def update_power_up(self):
        if self.power_up_active and pygame.time.get_ticks() > self.power_up_end_time:
            self.deactivate_power_up()

# PowerUp class
class PowerUp:
    def __init__(self):
        size = 30
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (random.randint(size, WIDTH - size), 
                           random.randint(size, HEIGHT - size))
        self.type = random.choice([
            "bigger_paddle", "smaller_paddle", "faster_paddle", "slower_paddle", "power_ball"
        ])
        
        # Color based on type
        if self.type == "bigger_paddle":
            self.color = GREEN
        elif self.type == "smaller_paddle":
            self.color = RED
        elif self.type == "faster_paddle":
            self.color = BLUE
        elif self.type == "slower_paddle":
            self.color = YELLOW
        elif self.type == "power_ball":
            self.color = MAGENTA
        
        self.active = True

    def draw(self):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 2)  # Border

# Particle class for visual effects
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.life = random.randint(10, 30)
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.size = max(0, self.size - 0.1)
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Game state management
class GameState:
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

# Main game function
def main():
    clock = pygame.time.Clock()
    ball = Ball()
    player1 = Paddle(30, "player")
    
    # Ask for game mode at startup
    game_mode = get_game_mode()
    
    if game_mode == "2 PLAYER":
        player2 = Paddle(WIDTH - 40, "player")
    else:  # AI opponent
        player2 = Paddle(WIDTH - 40, "ai")
        # Set AI difficulty based on mode
        if game_mode == "EASY AI":
            player2.ai_reaction_time = 5
        elif game_mode == "MEDIUM AI":
            player2.ai_reaction_time = 3
        elif game_mode == "HARD AI":
            player2.ai_reaction_time = 1
    
    game_state = GameState.PLAYING
    power_ups = []
    particles = []
    last_power_up_time = pygame.time.get_ticks()
    
    # For ball trail effect
    ball_positions = []
    
    # For power ball effect
    power_ball_end_time = 0
    
    # Main game loop
    while True:
        current_time = pygame.time.get_ticks()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == GameState.PLAYING:
                        game_state = GameState.PAUSED
                    elif game_state == GameState.PAUSED:
                        game_state = GameState.PLAYING
                if event.key == pygame.K_r and game_state == GameState.GAME_OVER:
                    # Reset the game
                    ball.reset()
                    player1.score = player2.score = 0
                    player1.reset_position()
                    player2.reset_position()
                    game_state = GameState.PLAYING
        
        if game_state == GameState.PLAYING:
            # Player 1 controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player1.move(-1)
            if keys[pygame.K_s]:
                player1.move(1)
            
            # Player 2 or AI controls
            if player2.control_type == "player":
                if keys[pygame.K_UP]:
                    player2.move(-1)
                if keys[pygame.K_DOWN]:
                    player2.move(1)
            else:  # AI
                player2.ai_move(ball)
            
            # Update power-ups status
            player1.update_power_up()
            player2.update_power_up()
            
            # Check if power ball effect ended
            if ball.is_power_ball and current_time > power_ball_end_time:
                ball.deactivate_power_ball()
            
            # Store ball position for trail effect
            ball_positions.append((ball.rect.centerx, ball.rect.centery))
            if len(ball_positions) > 10:  # Keep only last 10 positions
                ball_positions.pop(0)
            
            # Move ball
            ball.move()
            
            # Check for collision with paddles
            if ball.rect.colliderect(player1.rect):
                # Adjust angle based on where ball hits the paddle
                relative_intersect_y = (player1.rect.centery - ball.rect.centery) / (player1.rect.height / 2)
                angle = relative_intersect_y * (math.pi / 4)  # Max 45 degrees
                ball.speed_x = abs(ball.speed_x) * math.cos(angle)
                ball.speed_y = -math.sin(angle) * abs(ball.speed_x)
                
                # Reverse x direction and slightly increase speed
                ball.speed_x *= -1.05
                
                # Create particles on hit
                for _ in range(10):
                    particles.append(Particle(ball.rect.left, ball.rect.centery, WHITE))
                
                paddle_hit_sound.play()
            
            if ball.rect.colliderect(player2.rect):
                # Adjust angle based on where ball hits the paddle
                relative_intersect_y = (player2.rect.centery - ball.rect.centery) / (player2.rect.height / 2)
                angle = relative_intersect_y * (math.pi / 4)  # Max 45 degrees
                ball.speed_x = -abs(ball.speed_x) * math.cos(angle)
                ball.speed_y = -math.sin(angle) * abs(ball.speed_x)
                
                # Slightly increase speed
                ball.speed_x *= -1.05
                
                # Create particles on hit
                for _ in range(10):
                    particles.append(Particle(ball.rect.right, ball.rect.centery, WHITE))
                
                paddle_hit_sound.play()
            
            # Check for scoring
            if ball.rect.left <= 0:
                player2.score += 1
                score_sound.play()
                # Create particles for scoring effect
                for _ in range(20):
                    particles.append(Particle(0, ball.rect.centery, RED))
                ball.reset()
            elif ball.rect.right >= WIDTH:
                player1.score += 1
                score_sound.play()
                # Create particles for scoring effect
                for _ in range(20):
                    particles.append(Particle(WIDTH, ball.rect.centery, RED))
                ball.reset()
            
            # Check for winner
            if player1.score >= SCORE_LIMIT:
                game_state = GameState.GAME_OVER
                winner_text = "Player 1 Wins!"
            elif player2.score >= SCORE_LIMIT:
                game_state = GameState.GAME_OVER
                winner_text = "Player 2 Wins!"
            
            # Spawn power-ups occasionally
            if current_time - last_power_up_time > POWER_UP_SPAWN_TIME:
                power_ups.append(PowerUp())
                last_power_up_time = current_time
            
            # Check for collision with power-ups
            for power_up in power_ups[:]:
                if power_up.active:
                    if ball.rect.colliderect(power_up.rect):
                        power_up_sound.play()
                        
                        # Apply power-up effect based on which player is about to receive the ball
                        if ball.speed_x > 0:  # Ball moving toward player2
                            if power_up.type == "power_ball":
                                ball.activate_power_ball()
                                power_ball_end_time = current_time + POWER_UP_DURATION
                            else:
                                if power_up.type in ["bigger_paddle", "faster_paddle"]:
                                    player2.activate_power_up(power_up.type)
                                else:  # Negative effects applied to opponent
                                    player1.activate_power_up(power_up.type)
                        else:  # Ball moving toward player1
                            if power_up.type == "power_ball":
                                ball.activate_power_ball()
                                power_ball_end_time = current_time + POWER_UP_DURATION
                            else:
                                if power_up.type in ["bigger_paddle", "faster_paddle"]:
                                    player1.activate_power_up(power_up.type)
                                else:  # Negative effects applied to opponent
                                    player2.activate_power_up(power_up.type)
                        
                        power_up.active = False
                        power_ups.remove(power_up)
            
            # Update particles
            for particle in particles[:]:
                particle.update()
                if particle.life <= 0:
                    particles.remove(particle)
        
        # Drawing
        screen.fill(BLACK)
        
        # Draw center line
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        
        # Draw ball trail
        for i, pos in enumerate(ball_positions):
            # Make the trail fade out
            alpha = int(i * (255 / len(ball_positions)))
            trail_color = (min(ball.color[0], alpha), min(ball.color[1], alpha), min(ball.color[2], alpha))
            size = int(BALL_RADIUS * (i / len(ball_positions)) * 0.8)
            pygame.draw.circle(screen, trail_color, pos, size)
        
        # Draw ball
        pygame.draw.circle(screen, ball.color, ball.rect.center, BALL_RADIUS)
        
        # Draw paddles
        pygame.draw.rect(screen, player1.color, player1.rect)
        pygame.draw.rect(screen, player2.color, player2.rect)
        
        # Draw power-ups
        for power_up in power_ups:
            power_up.draw()
        
        # Draw particles
        for particle in particles:
            particle.draw()
        
        # Draw scores
        font = pygame.font.Font(None, FONT_SIZE)
        score_text = font.render(f"{player1.score} : {player2.score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        
        # Draw UI based on game state
        if game_state == GameState.PAUSED:
            draw_text("PAUSED", WIDTH // 2, HEIGHT // 2, font)
            draw_text("Press ESC to continue", WIDTH // 2, HEIGHT // 2 + 60, pygame.font.Font(None, 30))
        
        elif game_state == GameState.GAME_OVER:
            draw_text(winner_text, WIDTH // 2, HEIGHT // 2, font)
            draw_text("Press R to restart", WIDTH // 2, HEIGHT // 2 + 60, pygame.font.Font(None, 30))
        
        pygame.display.flip()
        clock.tick(FPS)

def get_game_mode():
    """Display a menu to select game mode"""
    menu_options = ["2 PLAYER", "EASY AI", "MEDIUM AI", "HARD AI"]
    selected_option = 0
    
    font_large = pygame.font.Font(None, 50)
    font_small = pygame.font.Font(None, 30)
    
    while True:
        screen.fill(BLACK)
        
        # Title
        title = font_large.render("PING PONG", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        
        # Draw instructions
        instructions = font_small.render("Use UP/DOWN to select, ENTER to confirm", True, WHITE)
        screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 4 + 60))
        
        # Draw options
        for i, option in enumerate(menu_options):
            color = RED if i == selected_option else WHITE
            option_text = font_large.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 60))
        
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    return menu_options[selected_option]
        
        pygame.time.Clock().tick(10)

def draw_text(text, x, y, font, color=WHITE):
    """Helper function to draw text"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    main()
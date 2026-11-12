import math
import pygame

# Screen and colors
WIDTH = 900
HEIGHT = 600
FPS = 60
BALL_RADIUS = 12

WHITE = (245, 245, 245)
RED = (220, 55, 55)
BLUE = (60, 120, 230)
YELLOW = (245, 200, 50)
GREEN = (35, 125, 75)
BROWN = (105, 60, 30)
BLACK = (15, 20, 18)


class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = BALL_RADIUS
        self.vx = 0
        self.vy = 0
        self.active = True

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, self.color,
                               (int(self.x), int(self.y)), self.radius)

    def move(self):
        if not self.active:
            return

        self.x += self.vx
        self.y += self.vy

        # Friction slows the ball down.
        self.vx *= 0.985
        self.vy *= 0.985

        if abs(self.vx) < 0.05:
            self.vx = 0
        if abs(self.vy) < 0.05:
            self.vy = 0

    def is_moving(self):
        return self.vx != 0 or self.vy != 0

    def collide(self, other):
        if not self.active or not other.active:
            return

        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.hypot(dx, dy)
        min_distance = self.radius + other.radius

        if distance == 0 or distance >= min_distance:
            return

        nx = dx / distance
        ny = dy / distance

        # Separate balls that overlap.
        overlap = min_distance - distance
        self.x -= nx * overlap / 2
        self.y -= ny * overlap / 2
        other.x += nx * overlap / 2
        other.y += ny * overlap / 2

        # Exchange velocity along the collision direction.
        speed = (self.vx - other.vx) * nx + (self.vy - other.vy) * ny
        if speed > 0:
            self.vx -= speed * nx
            self.vy -= speed * ny
            other.vx += speed * nx
            other.vy += speed * ny


class Table:
    def __init__(self):
        self.x = 70
        self.y = 100
        self.width = 760
        self.height = 400
        self.pockets = [
            (self.x, self.y),
            (self.x + self.width / 2, self.y),
            (self.x + self.width, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width / 2, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN,
                         (self.x - 25, self.y - 25,
                          self.width + 50, self.height + 50),
                         border_radius=12)
        pygame.draw.rect(screen, GREEN,
                         (self.x, self.y, self.width, self.height))

        for x, y in self.pockets:
            pygame.draw.circle(screen, BLACK, (int(x), int(y)), 23)

    def check_ball(self, ball):
        if not ball.active:
            return

        # A ball disappears when it enters a pocket.
        for x, y in self.pockets:
            if math.hypot(ball.x - x, ball.y - y) < 23:
                ball.vx = 0
                ball.vy = 0
                if ball.color == WHITE:
                    # Put the cue ball back on the table.
                    ball.x = 250
                    ball.y = 300
                else:
                    ball.active = False
                return

        # Bounce off the four sides.
        if ball.x - ball.radius < self.x:
            ball.x = self.x + ball.radius
            ball.vx = abs(ball.vx)
        if ball.x + ball.radius > self.x + self.width:
            ball.x = self.x + self.width - ball.radius
            ball.vx = -abs(ball.vx)
        if ball.y - ball.radius < self.y:
            ball.y = self.y + ball.radius
            ball.vy = abs(ball.vy)
        if ball.y + ball.radius > self.y + self.height:
            ball.y = self.y + self.height - ball.radius
            ball.vy = -abs(ball.vy)


class Cue:
    def draw(self, screen, white_ball, mouse_pos):
        dx = mouse_pos[0] - white_ball.x
        dy = mouse_pos[1] - white_ball.y
        distance = math.hypot(dx, dy)
        if distance < 10:
            return

        nx = dx / distance
        ny = dy / distance
        start = (int(white_ball.x - nx * 24),
                 int(white_ball.y - ny * 24))
        end = (int(white_ball.x - nx * 155),
               int(white_ball.y - ny * 155))
        pygame.draw.line(screen, BROWN, end, start, 8)
        pygame.draw.line(screen, YELLOW, start,
                         (int(white_ball.x - nx * 35),
                          int(white_ball.y - ny * 35)), 4)

    def hit(self, white_ball, mouse_pos):
        dx = mouse_pos[0] - white_ball.x
        dy = mouse_pos[1] - white_ball.y
        distance = math.hypot(dx, dy)
        if distance < 10:
            return

        white_ball.vx = dx / distance * 12
        white_ball.vy = dy / distance * 12


def create_balls():
    return [
        Ball(250, 300, WHITE),
        Ball(600, 300, RED),
        Ball(628, 284, BLUE),
        Ball(628, 316, YELLOW)
    ]


def balls_are_moving(balls):
    for ball in balls:
        if ball.active and ball.is_moving():
            return True
    return False


def all_colored_balls_pocketed(balls):
    for i in range(1, len(balls)):
        if balls[i].active:
            return False
    return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Billiards - Python OOP Basics")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22)

    table = Table()
    cue = Cue()
    balls = create_balls()
    running = True

    while running:
        moving = balls_are_moving(balls)
        won = all_colored_balls_pocketed(balls)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    balls = create_balls()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not moving and not won:
                    cue.hit(balls[0], event.pos)

        for ball in balls:
            ball.move()
            table.check_ball(ball)

        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                balls[i].collide(balls[j])

        screen.fill((30, 35, 38))
        table.draw(screen)
        for ball in balls:
            ball.draw(screen)

        if not balls_are_moving(balls):
            if not all_colored_balls_pocketed(balls):
                cue.draw(screen, balls[0], pygame.mouse.get_pos())

        message = "Click to shoot  |  R: restart  |  Esc: exit"
        if all_colored_balls_pocketed(balls):
            message = "You win! Press R to play again."
        text = font.render(message, True, WHITE)
        screen.blit(text, (70, 540))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

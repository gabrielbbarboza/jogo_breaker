import pygame
import threading
import time

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

fullscreen = True
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Breakar")

WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
RED = (255, 0, 0)
GRAY = (150, 150, 150)
BLUE = (50, 150, 255)
NEON_GREEN = (57, 255, 20)
NEON_PINK = (255, 20, 147)

font_size = int(HEIGHT * 0.035)
big_font_size = int(HEIGHT * 0.07)
font = pygame.font.SysFont("Arial", font_size)
big_font = pygame.font.SysFont("Arial", big_font_size)

paddle_width = WIDTH // 10
paddle_height = HEIGHT // 60
paddle_y = HEIGHT - HEIGHT // 12
paddle_speed = WIDTH // 100

ball_radius = HEIGHT // 80
ball_x_speed = WIDTH // 200
ball_y_speed = -HEIGHT // 200
ball_attached = True

brick_width = WIDTH // 12
brick_height = HEIGHT // 30
brick_gap = brick_height // 3

semaforo = threading.Semaphore()

running = True
jogo_ativo = False
vidas = 3
pontuacao = 0
fase = 1

paddle_x = (WIDTH - paddle_width) // 2
ball_x = paddle_x + paddle_width // 2
ball_y = paddle_y - ball_radius

width, height = WIDTH, HEIGHT

# Carregar a imagem do coração (coloque heart.png na mesma pasta do script)
heart_img = pygame.image.load("heart.png")
heart_img = pygame.transform.scale(heart_img, (30, 30))  # Ajuste o tamanho como quiser

def desenhar_texto(texto, fonte, cor, x, y, centralizado=True):
    render = fonte.render(texto, True, cor)
    rect = render.get_rect(center=(x, y)) if centralizado else render.get_rect(topleft=(x, y))
    window.blit(render, rect)

def desenhar_coracoes(vidas):
    x_inicial = 20
    y_inicial = 10  # Distante dos blocos
    espacamento = 40  # Espaço entre os corações
    for i in range(vidas):
        x = x_inicial + i * espacamento
        window.blit(heart_img, (x, y_inicial))

def criar_tijolos():
    bricks = []
    for row in range(5):
        for col in range(10):
            brick_x = col * (brick_width + 10) + 35
            brick_y = row * (brick_height + 10) + 50
            bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))
    return bricks

def iniciar_jogo():
    global paddle_x, ball_x, ball_y, ball_attached, bricks, vidas, jogo_ativo, pontuacao, ball_x_speed, ball_y_speed, fase
    paddle_x = (width - paddle_width) // 2
    ball_x = paddle_x + paddle_width // 2
    ball_y = paddle_y - ball_radius
    ball_attached = True
    bricks = criar_tijolos()
    vidas = 3
    pontuacao = 0
    fase = 1
    ball_x_speed = 4
    ball_y_speed = -4
    jogo_ativo = True

def mostrar_tela_inicial():
    window.fill(BLACK)
    desenhar_texto("BREAKER", big_font, NEON_GREEN, width // 2, height // 3)
    desenhar_texto("Pressione ENTER para começar", font, GRAY, width // 2, height // 2)
    pygame.display.update()

def mostrar_game_over():
    window.fill(BLACK)
    desenhar_texto("GAME OVER", big_font, NEON_PINK, width // 2, height // 3)
    desenhar_texto(f"Pontuação final: {pontuacao}", font, WHITE, width // 2, height // 2)
    desenhar_texto("Pressione ENTER para jogar novamente", font, GRAY, width // 2, height // 2 + 50)
    pygame.display.update()

def mover_bola():
    global ball_x, ball_y, ball_x_speed, ball_y_speed, bricks, vidas, jogo_ativo, ball_attached, pontuacao, fase
    clock = pygame.time.Clock()
    while running:
        if jogo_ativo and not ball_attached:
            with semaforo:
                ball_x += ball_x_speed
                ball_y += ball_y_speed

                if ball_x <= ball_radius or ball_x >= width - ball_radius:
                    ball_x_speed *= -1
                if ball_y <= ball_radius:
                    ball_y_speed *= -1

                if paddle_y - ball_radius <= ball_y <= paddle_y + paddle_height:
                    if paddle_x <= ball_x <= paddle_x + paddle_width:
                        ball_y_speed = -abs(ball_y_speed)
                        offset = (ball_x - (paddle_x + paddle_width // 2)) / (paddle_width // 2)
                        ball_x_speed = offset * 5

                for brick in bricks:
                    if brick.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius*2, ball_radius*2)):
                        bricks.remove(brick)
                        ball_y_speed *= -1
                        pontuacao += 10
                        break

                if ball_y >= height:
                    vidas -= 1
                    if vidas > 0:
                        ball_attached = True
                        ball_x = paddle_x + paddle_width // 2
                        ball_y = paddle_y - ball_radius
                    else:
                        jogo_ativo = False

                if len(bricks) == 0:
                    fase += 1
                    bricks = criar_tijolos()
                    ball_attached = True
                    ball_x = paddle_x + paddle_width // 2
                    ball_y = paddle_y - ball_radius
                    ball_x_speed *= 1.1
                    ball_y_speed *= -1.1
        time.sleep(0.01)
        clock.tick(60)

def mover_paddle():
    global paddle_x, ball_x, ball_y
    while running:
        if jogo_ativo:
            keys = pygame.key.get_pressed()
            with semaforo:
                if keys[pygame.K_LEFT] and paddle_x > 0:
                    paddle_x -= paddle_speed
                if keys[pygame.K_RIGHT] and paddle_x < width - paddle_width:
                    paddle_x += paddle_speed

                if ball_attached:
                    ball_x = paddle_x + paddle_width // 2
                    ball_y = paddle_y - ball_radius
        time.sleep(0.01)

threading.Thread(target=mover_bola, daemon=True).start()
threading.Thread(target=mover_paddle, daemon=True).start()

while running:
    if not jogo_ativo and vidas == 3:
        mostrar_tela_inicial()
    elif not jogo_ativo and vidas == 0:
        mostrar_game_over()
    else:
        window.fill((10, 10, 30))
        with semaforo:
            pygame.draw.rect(window, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height), border_radius=8)
            pygame.draw.circle(window, BLUE, (int(ball_x), int(ball_y)), ball_radius)
            for brick in bricks:
                pygame.draw.rect(window, (255, 60, 60), brick, border_radius=4)
            desenhar_coracoes(vidas)  # Aqui o coração em imagem
            desenhar_texto(f"Pontuação: {pontuacao}", font, WHITE, width - 200, 20, centralizado=False)
            desenhar_texto(f"Fase {fase}", font, NEON_GREEN, width // 2, 20)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not jogo_ativo:
                iniciar_jogo()
            elif event.key == pygame.K_SPACE and jogo_ativo and ball_attached:
                ball_attached = False
            elif event.key == pygame.K_ESCAPE:
                fullscreen = not fullscreen
                if fullscreen:
                    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                    width, height = WIDTH, HEIGHT
                else:
                    window = pygame.display.set_mode((1280, 720))
                    width, height = 1280, 720

    pygame.time.Clock().tick(60)

pygame.quit()

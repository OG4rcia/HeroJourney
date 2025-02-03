import pgzrun
import random

# Configuração da tela
WIDTH, HEIGHT = 800, 400
GRAVITY = 0.5
JUMP_STRENGTH = -10
DOUBLE_JUMP_STRENGTH = -8

# Fundo e chão
background = "background.png"
chao = Actor("chao.png", (WIDTH // 2, 470))

# Plataformas
platforms = [
    Actor("platform.png", (150, 350)),
    Actor("platform.png", (400, 270)),
    Actor("platform.png", (650, 190)),
    Actor("platform.png", (300, 100)),
    Actor("platform.png", (600, 50)),
]

# Itens colecionáveis
items = [
    Actor("collect.png", (150, 320)),
    Actor("collect.png", (400, 240)),
    Actor("collect.png", (650, 160)),
    Actor("collect.png", (300, 70)),
    Actor("collect.png", (600, 30)),
]

# Criar personagem
player = Actor("idle1.png", (10, HEIGHT - 150))
player.vel_y = 0
player.can_double_jump = False
player.direction = 1  # 1 para direita, -1 para esquerda
player.idle_frames = ["idle1.png", "idle2.png", "idle3.png", "idle4.png", "idle5.png", "idle6.png", "idle7.png", "idle8.png"]
player.idle_index = 0
player.idle_timer = 0

# Projéteis
projectiles = []
projectile_speed = 5
projectile_fired = False

# Inimigos
enemies = []

# Sistema de vidas e respawn
lives = 3
collected_items = 0
player_alive = True
respawn_time = 2
time_since_death = 0
respawn_position = (10, HEIGHT - 10)

# Criar inimigos
for platform in platforms:
    enemy = Actor(random.choice(["enemy1.png", "enemy2.png", "enemy3.png"]))
    enemy.pos = (platform.x, platform.y - platform.height // 2 - enemy.height // 2)
    enemy.speed = random.randint(2, 5)
    enemy.direction = random.choice([1, -1])
    enemy.platform = platform
    enemies.append(enemy)

def on_ground():
    """Verifica se o jogador está no chão ou em uma plataforma."""
    if player.colliderect(chao) and player.vel_y > 0:
        return True
    for platform in platforms:
        if player.colliderect(platform) and player.vel_y > 0:
            return True
    return False

def create_projectile():
    """Cria um projétil na direção do jogador."""
    global projectile_fired
    if not projectile_fired:
        proj = Actor("projetil.png")
        proj.pos = (player.x + (20 * player.direction), player.y)
        proj.direction = player.direction
        projectiles.append(proj)
        projectile_fired = True

def update():
    global projectile_fired, collected_items, time_since_death, player_alive, lives
    
    # Verifica se o jogador perdeu
    if not player_alive:
        time_since_death += 1 / 60
        if time_since_death >= respawn_time:
            respawn_player()
        return

    # Verifica se o jogador ganhou
    if collected_items >= 5:
        # Aqui estamos parando o jogo e desenhando a tela de vitória
        global game_won
        game_won = True  # Marcamos que o jogo foi vencido
        return  # Paralisa o jogo quando ganha

    # O restante do código do jogo continua normalmente se o jogador não venceu ainda

    # Gravidade
    player.vel_y += GRAVITY
    player.y += player.vel_y

    moving = False

    # Movimentação
    if keyboard.left:
        player.x -= 3
        player.direction = -1
        player.image = "default-teste-left.png"
        moving = True
    elif keyboard.right:
        player.x += 3
        player.direction = 1
        player.image = "default-teste.png"
        moving = True
    
    # Pulo
    if keyboard.up:
        if on_ground():
            player.vel_y = JUMP_STRENGTH
            player.can_double_jump = True
        elif player.can_double_jump:
            player.vel_y = DOUBLE_JUMP_STRENGTH
            player.can_double_jump = False
    
    # Animação de idle
    if not moving:
        player.idle_timer += 1
        if player.idle_timer >= 30:
            player.idle_index = (player.idle_index + 1) % len(player.idle_frames)
            player.image = player.idle_frames[player.idle_index]
            player.idle_timer = 0
    else:
        player.idle_timer = 0
    
    # Colisão com plataformas
    for platform in platforms:
        if player.colliderect(platform) and player.vel_y > 0:
            player.y = platform.y - platform.height // 2 - player.height // 2
            player.vel_y = 0
            player.can_double_jump = False

    # Colisão com o chão
    if player.colliderect(chao) and player.vel_y > 0:
        player.y = chao.y - chao.height // 2 - player.height // 2
        player.vel_y = 0
        player.can_double_jump = False

    # Movimento dos inimigos
    for enemy in enemies:
        enemy.x += enemy.speed * enemy.direction
        if enemy.x <= enemy.platform.x - enemy.platform.width // 2 or enemy.x >= enemy.platform.x + enemy.platform.width // 2:
            enemy.direction *= -1

        # Verificação de colisão inimigo-jogador
        if player.colliderect(enemy):
            # Perde vida e reposiciona o jogador
            lives -= 1
            if lives > 0:
                respawn_player()  # Reposiciona o jogador após a colisão
            else:
                player_alive = False
                screen.clear()
                screen.draw.text("Fim de jogo! Você perdeu todas as suas vidas!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")
                return  # Paralisa o jogo

    # Disparo de projétil
    if keyboard.space:
        create_projectile()

    # Movimentação dos projéteis
    for proj in projectiles[:]:
        proj.x += projectile_speed * proj.direction
        if proj.x > WIDTH or proj.x < 0:
            projectiles.remove(proj)
            projectile_fired = False
        
        # Colisão projétil-inimigo
        for enemy in enemies[:]:
            if proj.colliderect(enemy):
                enemies.remove(enemy)
                projectiles.remove(proj)
                projectile_fired = False

    # Coleta de itens
    for item in items[:]:
        if player.colliderect(item):
            items.remove(item)
            collected_items += 1

def respawn_player():
    global player_alive, time_since_death, lives
    if lives > 0:
        player.pos = respawn_position
        player.vel_y = 0
        player_alive = True
        time_since_death = 0
    else:
        print("Fim de jogo! Você perdeu todas as suas vidas!")

def draw():
    # Se o jogo foi vencido
    if game_won:
        screen.clear()
        screen.draw.text("Você ganhou!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")
        return  # Paralisa o jogo

    if player_alive:
        screen.clear()
        screen.blit(background, (0, 0))
        chao.draw()
        for platform in platforms:
            platform.draw()
        for item in items:
            item.draw()
        for proj in projectiles:
            proj.draw()
        for enemy in enemies:
            enemy.draw()
        player.draw()
        screen.draw.text(f"Itens coletados: {collected_items}/5", (10, 10), fontsize=30, color="white")
        screen.draw.text(f"Vidas: {lives}", (WIDTH - 100, 10), fontsize=30, color="white")
    else:
        # Caso o jogador tenha perdido, já mostra a tela de derrota.
        screen.draw.text("Fim de jogo! Você perdeu todas as suas vidas!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")

# Variável global para indicar se o jogo foi vencido
game_won = False

pgzrun.go()
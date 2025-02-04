import random
from pgzero.builtins import *
import pgzrun

# Toca a música de fundo ao iniciar o jogo
music.play('night1.wav')
music.set_volume(0.3)  # Define o volume da música para 30%

# Configuração da tela e propriedades físicas do jogo
WIDTH, HEIGHT = 800, 400
GRAVITY = 0.5  # Gravidade que afeta o jogador
JUMP_STRENGTH = -10  # Força do pulo
DOUBLE_JUMP_STRENGTH = -8  # Força do segundo pulo (duplo)

# Fundo e chão do jogo
background = "background.png"
chao = Actor("chao.png", (WIDTH // 2, 470))  # Criação do chão do jogo

# Definindo as plataformas onde o jogador pode andar
platforms = [
    Actor("platform.png", (150, 350)),
    Actor("platform.png", (400, 270)),
    Actor("platform.png", (650, 190)),
    Actor("platform.png", (300, 100)),
    Actor("platform.png", (600, 50)),
]

# Itens colecionáveis espalhados pelas plataformas
items = [
    Actor("collect.png", (150, 320)),
    Actor("collect.png", (400, 240)),
    Actor("collect.png", (650, 160)),
    Actor("collect.png", (300, 70)),
    Actor("collect.png", (600, 30)),
]

# Criar o personagem principal (jogador)
player = Actor("idle1.png", (10, HEIGHT - 150))  # Imagem inicial do jogador
player.vel_y = 0  # Velocidade inicial no eixo Y (vertical)
player.can_double_jump = False  # Controla o pulo duplo
player.direction = 1  # Direção inicial (1 = direita, -1 = esquerda)

# Animações do jogador
player.idle_frames = ["idle1.png", "idle2.png", "idle3.png", "idle4.png", "idle5.png", "idle6.png", "idle7.png", "idle8.png"]
player.idle_index = 0  # Índice da animação de idle (quando o jogador não está se movendo)
player.idle_timer = 0  # Timer para trocar as imagens da animação de idle

player.walk_frames_right = ["walk1.png", "walk2.png", "walk3.png", "walk4.png", "walk5.png", "walk6.png", "walk7.png", "walk8.png"]
player.walk_frames_left = ["walk1-reverse.png", "walk2-reverse.png", "walk3-reverse.png", "walk4-reverse.png", "walk5-reverse.png", "walk6-reverse.png", "walk7-reverse.png", "walk8-reverse.png"]
player.walk_index = 0
player.walk_timer = 0

# Projéteis disparados pelo jogador
projectiles = []
projectile_speed = 5  # Velocidade do projétil
projectile_fired = False  # Controla se um projétil foi disparado

# Inimigos
enemies = []

# Sistema de vidas e respawn
lives = 3  # O jogador começa com 3 vidas
collected_items = 0  # Contagem de itens coletados
player_alive = True  # Controle de estado do jogador (vivo ou morto)
respawn_time = 2  # Tempo de respawn após a morte
time_since_death = 0  # Tempo que passou desde a morte do jogador
respawn_position = (10, HEIGHT - 10)  # Posição de respawn do jogador

# Criando inimigos aleatórios nas plataformas
for platform in platforms:
    enemy = Actor(random.choice(["enemy1.png", "enemy2.png", "enemy3.png"]))  # Escolhe uma imagem aleatória para o inimigo
    enemy.pos = (platform.x, platform.y - platform.height // 2 - enemy.height // 2)  # Posiciona o inimigo acima da plataforma
    enemy.speed = random.randint(2, 5)  # Velocidade aleatória do inimigo
    enemy.direction = random.choice([1, -1])  # Direção aleatória do inimigo
    enemy.platform = platform  # Associa o inimigo à plataforma
    enemies.append(enemy)

# Função que verifica se o jogador está no chão ou em uma plataforma
def on_ground():
    if player.colliderect(chao) and player.vel_y > 0:
        return True
    for platform in platforms:
        if player.colliderect(platform) and player.vel_y > 0:
            return True
    return False

# Função que cria um projétil
def create_projectile():
    global projectile_fired
    if not projectile_fired:
        proj = Actor("projetil.png")
        proj.pos = (player.x + (20 * player.direction), player.y)  # Posiciona o projétil
        proj.direction = player.direction  # Direção do projétil
        projectiles.append(proj)
        projectile_fired = True
        sounds.arrow.play()  # Toca o som do disparo

# Função de respawn do jogador
def respawn_player():
    global player_alive, time_since_death, lives
    if lives > 0:
        player.pos = respawn_position
        player.vel_y = 0
        player_alive = True
        time_since_death = 0
    else:
        print("Fim de jogo! Você perdeu todas as suas vidas!")  # Exibe a mensagem de fim de jogo

# Função que atualiza o estado do jogo a cada quadro
def update():
    global projectile_fired, collected_items, time_since_death, player_alive, lives
    
    if not player_alive:
        time_since_death += 1 / 60  # Contagem do tempo após a morte do jogador
        if time_since_death >= respawn_time:
            respawn_player()  # Respawn após a morte
        return

    if collected_items >= 5:  # Se o jogador coletou todos os itens, o jogo foi vencido
        global game_won
        game_won = True
        return

    # Gravidade e movimento vertical do jogador
    player.vel_y += GRAVITY
    player.y += player.vel_y

    moving = False

    # Movimentação do jogador
    if keyboard.left:
        player.x -= 3
        player.direction = -1
        moving = True
    elif keyboard.right:
        player.x += 3
        player.direction = 1
        moving = True

    # Animação de caminhada
    if moving:
        player.walk_timer += 1
        if player.walk_timer >= 5:  # Controla a velocidade da animação de caminhada
            player.walk_index = (player.walk_index + 1) % len(player.walk_frames_right)
            if player.direction == 1:
                player.image = player.walk_frames_right[player.walk_index]
            else:
                player.image = player.walk_frames_left[player.walk_index]
            player.walk_timer = 0

    # Controle do pulo
    if keyboard.up:
        if on_ground():
            player.vel_y = JUMP_STRENGTH
            sounds.jump.play()  # Toca o som do pulo
            player.can_double_jump = True  # Permite o pulo duplo
        elif player.can_double_jump:
            player.vel_y = DOUBLE_JUMP_STRENGTH
            player.can_double_jump = False
    
    # Animação de idle (quando o jogador não está se movendo)
    if not moving:
        player.idle_timer += 1
        if player.idle_timer >= 30:
            player.idle_index = (player.idle_index + 1) % len(player.idle_frames)
            player.image = player.idle_frames[player.idle_index]
            player.idle_timer = 0

    # Verificação de colisão com plataformas e chão
    for platform in platforms:
        if player.colliderect(platform) and player.vel_y > 0:
            player.y = platform.y - platform.height // 2 - player.height // 2
            player.vel_y = 0
            player.can_double_jump = False

    if player.colliderect(chao) and player.vel_y > 0:
        player.y = chao.y - chao.height // 2 - player.height // 2
        player.vel_y = 0
        player.can_double_jump = False

    # Movimentação e colisão dos inimigos
    for enemy in enemies:
        enemy.x += enemy.speed * enemy.direction
        if enemy.x <= enemy.platform.x - enemy.platform.width // 2 or enemy.x >= enemy.platform.x + enemy.platform.width // 2:
            enemy.direction *= -1

        if player.colliderect(enemy):  # Se o jogador colidir com um inimigo
            sounds.hero_hurt.play()  # Toca o som de dano
            lives -= 1  # Perde uma vida
            if lives > 0:
                respawn_player()  # Respawn do jogador
            else:
                player_alive = False  # O jogador morreu
                return

    # Verifica se o jogador pressionou a tecla espaço para disparar um projétil
    if keyboard.space:
        create_projectile()

    # Atualiza a posição dos projéteis e verifica colisões com os inimigos
    for proj in projectiles[:]:
        proj.x += projectile_speed * proj.direction
        if proj.x > WIDTH or proj.x < 0:  # Remove o projétil se sair da tela
            projectiles.remove(proj)
            projectile_fired = False
        
        for enemy in enemies[:]:
            if proj.colliderect(enemy):  # Se o projétil acertar um inimigo
                sounds.enemy_dies.play()  # Toca o som do inimigo morrendo
                enemies.remove(enemy)  # Remove o inimigo da lista
                projectiles.remove(proj)  # Remove o projétil
                projectile_fired = False

    # Verifica se o jogador coletou algum item
    for item in items[:]:
        if player.colliderect(item):
            sounds.find_money.play()  # Toca o som de item coletado
            items.remove(item)  # Remove o item da tela
            collected_items += 1  # Incrementa o número de itens coletados

# Função que desenha os elementos na tela
def draw():
    if game_won:  # Se o jogador ganhou
        screen.clear()
        screen.draw.text("Você ganhou!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")
        return

    if not player_alive:  # Se o jogador perdeu todas as vidas
        screen.clear()
        screen.draw.text("Você perdeu todas as suas vidas!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")
        return

    # Desenha o cenário, o personagem, inimigos e itens
    if player_alive:
        screen.clear()
        screen.blit(background, (0, 0))  # Fundo
        chao.draw()  # Chão
        for platform in platforms:
            platform.draw()  # Desenha as plataformas
        for item in items:
            item.draw()  # Desenha os itens colecionáveis
        for proj in projectiles:
            proj.draw()  # Desenha os projéteis
        for enemy in enemies:
            enemy.draw()  # Desenha os inimigos
        player.draw()  # Desenha o jogador
        screen.draw.text(f"Itens coletados: {collected_items}/5", (10, 10), fontsize=30, color="white")  # Exibe a quantidade de itens coletados
        screen.draw.text(f"Vidas: {lives}", (WIDTH - 100, 10), fontsize=30, color="white")  # Exibe o número de vidas restantes

game_won = False  # Variável que indica se o jogador venceu

pgzrun.go()  # Inicia o jogo

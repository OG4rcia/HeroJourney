import pgzrun
import subprocess

# Toca a música de fundo ao iniciar o menu
music.play('night2.wav')
music.set_volume(0.3)  # Define o volume da música para 30%

# Função que inicia o jogo ao pressionar "Start"
def start_game():
    subprocess.Popen(["python", "game.py"])  # Inicia o jogo chamando o arquivo game.py
    exit()  # Fecha o menu ao iniciar o jogo

# Função para alternar entre mutar e desmutar a música de fundo
def toggle_mute():
    global muted  # Usamos a variável 'muted' para controlar o estado (mutado ou não)
    muted = not muted  # Troca o estado de 'muted' (se estava mutado, agora será desmutado e vice-versa)
    
    # Se estiver mutado, o volume da música é zerado
    if muted:
        music.set_volume(0)  # Muta a música
    else:
        music.set_volume(0.3)  # Restaura o volume da música (30%)

# Função que encerra o jogo e fecha o menu
def exit_game():
    exit()  # Encerra o programa

# Configuração da tela
WIDTH, HEIGHT = 800, 400

# Definindo os botões do menu
buttons = [
    {"text": "Start", "pos": (WIDTH // 2, 150), "action": start_game},  # Botão "Start" para iniciar o jogo
    {"text": "Mute Volume", "pos": (WIDTH // 2, 220), "action": toggle_mute},  # Botão para mutar/desmutar a música
    {"text": "Exit", "pos": (WIDTH // 2, 290), "action": exit_game}  # Botão "Exit" para sair do menu
]

muted = False  # Inicializa o estado da música como não mutado

# Fundo do menu
background = "background.png"
button_bg = "platform.png"  # Fundo dos botões

# Função que desenha os elementos na tela
def draw():
    screen.clear()  # Limpa a tela antes de desenhar os novos elementos
    screen.blit(background, (0, 0))  # Exibe o fundo do menu
    
    # Desenha os botões na tela
    for button in buttons:
        screen.blit(button_bg, (button["pos"][0] - 80, button["pos"][1] - 20))  # Fundo do botão
        screen.draw.text(button["text"], center=button["pos"], fontsize=30, color="white")  # Texto do botão

# Função chamada quando um botão é pressionado
def on_mouse_down(pos):
    # Verifica se a posição do clique está dentro da área de um dos botões
    for button in buttons:
        bx, by = button["pos"]
        # Verifica se o clique está dentro dos limites do botão
        if bx - 80 <= pos[0] <= bx + 80 and by - 20 <= pos[1] <= by + 20:
            button["action"]()  # Executa a ação associada ao botão pressionado

# Inicia o jogo
pgzrun.go()

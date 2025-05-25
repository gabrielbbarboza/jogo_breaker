O Jogo Breaker 2 é uma implementação moderna do clássico jogo Breakout, desenvolvida com Python e Pygame, incorporando conceitos avançados de programação concorrente com threads e semáforos.

🛠️ Tecnologias e Recursos
Pygame (SDL): Biblioteca gráfica para jogos em Python, utilizada para renderização em tela cheia, detecção de colisões e controle de entrada do usuário.

* Threads e Semáforos (threading, Semaphore): Controle concorrente para execução simultânea da lógica da bola e da raquete sem travar o loop principal.

* Escalabilidade dinâmica: Interface e elementos do jogo ajustados dinamicamente ao tamanho da tela do dispositivo.

* Sistema de fases: Dificuldade progressiva com aumento de velocidade da bola a cada nível completado.

* Sistema de vidas com ícones gráficos: Corações visuais atualizados em tempo real representam as tentativas restantes.

* Design modular e limpo: Código separado em funções para melhor organização, legibilidade e manutenção.

🔍 Funcionalidades
Tela inicial e tela de "Game Over"

*Detecção precisa de colisão entre a bola, raquete e tijolos

* Reposicionamento da bola após perda de vida

* Animações suaves com atualização baseada em clock.tick

* Pontuação dinâmica e indicador de fase centralizado na interface

* Alternância entre modo janela e modo tela cheia

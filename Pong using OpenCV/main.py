from GameSettings import GameSettings
from PongGame import PongGame
from Menu import Menu

def main():
    gameSettings = GameSettings()
    pongGame = PongGame(gameSettings)
    menu = Menu(gameSettings, pongGame)
    menu.title()

if __name__ == "__main__":
    main()

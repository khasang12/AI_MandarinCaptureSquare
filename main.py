from game import Game
import pygame
import sys
if __name__ == "__main__":
    print("+----- O AN QUAN -----+\n\n")

    game = Game()
    while True:        
        game.run()
        reset = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                        reset = True
                        break
            if reset:
                break

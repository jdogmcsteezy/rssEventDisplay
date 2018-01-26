# ---- TESTING -----
import pygame
import rssEventDisplay
def main():
    pygame.init()
    clock = pygame.time.Clock()
    testScreen = pygame.display.set_mode((1200, 75))
    testScreen.fill((200, 255, 230))
    ticker = rssEventDisplay.AcademicCalanderDisplay(1200, 75)
    testScreen.blit(ticker, (0, 0))
    pygame.display.update()
    run = True
    while(run):
        clock.tick(26)
        testScreen.blit(ticker.Update(), (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    run = False
            elif event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == "__main__":
    main()

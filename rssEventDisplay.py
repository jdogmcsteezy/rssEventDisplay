import pygame
from pygame import Surface, time
import urllib.request
import xml.etree.ElementTree as ET
import os


class AcademicCalanderDisplay(pygame.Surface):
    def __init__(self, width, height):
        pygame.Surface.__init__(self, (width, height))
        pygame.font.init()
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.rssTree = ET.parse(urllib.request.urlopen('http://calendar.butte.edu/RSSSyndicator.aspx?type=N&number=5&category=4-0&rssid=7&rsstitle=Academic+Calendar&sortorder=ASC'))
        self.width = width
        self.height = height
        self.fill((255, 255, 255))
        self.titleBar_textOffset = (0, -2)
        self.titleBar_heightRatio = .4
        self.titleBar_bgColor = (0, 0, 0)
        self.titleBar_textColor = (158, 0, 49)
        self.titleBar_font = ('Instruction.otf', 25)
        self.titleBar_text = 'Butte College Academic Deadlines'
        self.RenderTitleBar()
        self.scrollBarSpeed = 3
        self.scrollBar_heightRatio = 1.0 - self.titleBar_heightRatio
        self.scrollBar_bgColor = (255, 255, 255)
        self.scrollBar_textColor = (0, 0, 0)
        self.scrollBar_textOffset = (0, -2)
        self.scrollBar_font = ('Instruction Bold.otf', 25)
        self.scrollBar_textSeperator = '           '
        self.scrollBar = pygame.Surface((self.width, self.height * (1.0 - self.titleBar_heightRatio)))
        self.scrollBar.fill(self.scrollBar_bgColor)
        self.scrollX1 = 0
        self.scrollX2 = 0
        self.UpdateContents()
        self.scrollBar.convert()

    def UpdateContents(self):
        root = self.rssTree.getroot()
        font = pygame.font.Font(self.dir_path + '/Fonts/' + self.scrollBar_font[0], self.scrollBar_font[1])
        contentList = [title.text for title in root.iter('title')]
        contentList.pop(0)
        self.scrollBar_text = self.scrollBar_textSeperator + self.scrollBar_textSeperator.join(contentList)
        self.scrollBar_text = self.scrollBar_text.upper()
        self.scrollBar_content = font.render(self.scrollBar_text, False, self.scrollBar_textColor)
        self.scrollBar_contentRect = self.scrollBar_content.get_rect()
        self.scrollBar_Rect = self.scrollBar.get_rect()
        self.scrollBar.blit(self.scrollBar_content, (0, self.scrollBar_Rect.centery - self.scrollBar_contentRect.centery))
        self.blit(self.scrollBar, (0, self.height * self.titleBar_heightRatio))
        self.scrollX2 = self.scrollBar_contentRect.right
        self.scrollBar_content.convert()

    def RenderTitleBar(self):
        font = pygame.font.Font(self.dir_path + '/Fonts/' + self.titleBar_font[0], self.titleBar_font[1])
        titleBarHeading = font.render(self.titleBar_text, False, self.titleBar_textColor)
        self.titleBar = pygame.Surface((self.width, self.height * self.titleBar_heightRatio))
        self.titleBar.fill(self.titleBar_bgColor)
        titleBarRect = self.titleBar.get_rect()
        headingRect = titleBarHeading.get_rect()
        pygame.draw.line(self.titleBar, (198, 225, 234), (0, titleBarRect.centery), (60, titleBarRect.centery), 2)
        pygame.draw.line(self.titleBar, (198, 225, 234), (titleBarRect.right, titleBarRect.centery), (titleBarRect.right - 63, titleBarRect.centery), 2)
        self.titleBar.blit(titleBarHeading, (titleBarRect.centerx - headingRect.centerx + self.titleBar_textOffset[0],
                                             titleBarRect.centery - headingRect.centery + self.titleBar_textOffset[1]))
        self.titleBar.convert()
        self.blit(self.titleBar, (0, 0))

    def Update(self):
        self.scrollX1 -= self.scrollBarSpeed
        self.scrollX2 -= self.scrollBarSpeed
        self.scrollBar.fill(self.scrollBar_bgColor)
        if self.scrollX1 < self.scrollX2 and abs(self.scrollX1) > self.scrollBar_contentRect.right:
            self.scrollX1 = self.scrollBar_contentRect.right
        elif self.scrollX1 > self.scrollX2 and abs(self.scrollX2) > self.scrollBar_contentRect.right:
            self.scrollX2 = self.scrollBar_contentRect.right
        if self.scrollX1 < self.scrollBar_Rect.right:
            self.scrollBar.blit(self.scrollBar_content, (self.scrollX1 + self.scrollBar_textOffset[0],
                                                         self.scrollBar_Rect.centery - self.scrollBar_contentRect.centery + self.scrollBar_textOffset[1]))
        if self.scrollX2 < self.scrollBar_Rect.right:
            self.scrollBar.blit(self.scrollBar_content, (self.scrollX2 + self.scrollBar_textOffset[0],
                                                         self.scrollBar_Rect.centery - self.scrollBar_contentRect.centery + self.scrollBar_textOffset[1]))
        self.blit(self.scrollBar, (0, self.height * self.titleBar_heightRatio))
        return self


def main():
    pygame.init()
    clock = pygame.time.Clock()
    testScreen = pygame.display.set_mode((1200, 75))
    testScreen.fill((200, 255, 230))
    ticker = AcademicCalanderDisplay(1200, 75)
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

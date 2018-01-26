from pygame import Surface, time, font, draw
import urllib.request
import xml.etree.ElementTree as ET
import os


class AcademicCalanderDisplay(Surface):
    def __init__(self, width, height):
        Surface.__init__(self, (width, height))
        font.init()
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.rssTree = ET.parse(urllib.request.urlopen('http://calendar.butte.edu/RSSSyndicator.aspx?type=N&number=5&category=4-0&rssid=7&rsstitle=Academic+Calendar&sortorder=ASC'))
        self.width = width
        self.height = height
        self.fill((255, 255, 255))
        self.titleBar_textOffset = (0, -2)
        self.titleBar_heightRatio = .4
        self.titleBar_bgColor = (198, 225, 234)
        self.titleBar_textColor = (0, 0, 0)
        self.titleBar_font = ('Instruction Bold.otf', 25)
        self.titleBar_text = 'Butte College Academic Deadlines'
        self.RenderTitleBar()
        self.scrollBarSpeed = 3
        self.scrollBar_heightRatio = 1.0 - self.titleBar_heightRatio
        self.scrollBar_bgColor = (0, 0, 0)
        self.scrollBar_textColor = (158, 0, 49)
        self.scrollBar_textOffset = (0, -2)
        self.scrollBar_font = ('Instruction.otf', 25)
        self.scrollBar_textSeperator = '           '
        self.scrollBar = Surface((self.width, self.height * (1.0 - self.titleBar_heightRatio)))
        self.scrollBar.fill(self.scrollBar_bgColor)
        self.scrollX1 = 0
        self.scrollX2 = 0
        self.UpdateContents()
        self.scrollBar.convert()

    def UpdateContents(self):
        root = self.rssTree.getroot()
        contentFont = font.Font(self.dir_path + '/Fonts/' + self.scrollBar_font[0], self.scrollBar_font[1])
        contentList = [title.text for title in root.iter('title')]
        contentList.pop(0)
        self.scrollBar_text = self.scrollBar_textSeperator + self.scrollBar_textSeperator.join(contentList)
        #self.scrollBar_text = self.scrollBar_text.upper()
        self.scrollBar_content = contentFont.render(self.scrollBar_text, True, self.scrollBar_textColor)
        self.scrollBar_contentRect = self.scrollBar_content.get_rect()
        self.scrollBar_Rect = self.scrollBar.get_rect()
        self.scrollBar.blit(self.scrollBar_content, (0, self.scrollBar_Rect.centery - self.scrollBar_contentRect.centery))
        self.blit(self.scrollBar, (0, self.height * self.titleBar_heightRatio))
        self.scrollX2 = self.scrollBar_contentRect.right
        self.scrollBar_content.convert()

    def RenderTitleBar(self):
        # This should probably be changed to os.path.join() and have 'Fonts as class variable'
        titleFont = font.Font(self.dir_path + '/Fonts/' + self.titleBar_font[0], self.titleBar_font[1])
        titleBarHeading = titleFont.render(self.titleBar_text, True, self.titleBar_textColor)
        self.titleBar = Surface((self.width, self.height * self.titleBar_heightRatio))
        self.titleBar.fill(self.titleBar_bgColor)
        titleBarRect = self.titleBar.get_rect()
        headingRect = titleBarHeading.get_rect()
        draw.line(self.titleBar, (0, 0, 0), (0, titleBarRect.centery), (300, titleBarRect.centery), 2)
        draw.line(self.titleBar, (0, 0, 0), (titleBarRect.right, titleBarRect.centery), (titleBarRect.right - 300, titleBarRect.centery), 2)
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



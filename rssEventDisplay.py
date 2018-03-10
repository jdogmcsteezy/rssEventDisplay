from pygame import Surface, time, font, draw
import urllib.request
import xml.etree.ElementTree as ET
import os
from datetime import datetime


class AcademicCalanderDisplay(Surface):
    def __init__(self, width, height):
        Surface.__init__(self, (width, height))
        font.init()
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.rssTree = None
        self.width = width
        self.height = height
        self.today = None
        self.fill((255, 255, 255))
        self.titleBar_textOffset = (0, -2)
        self.titleBar_heightRatio = .4
        self.titleBar_bgColor = (39,40,34)
        self.titleBar_textColor = (186, 111, 23)
        self.titleBar_font = ('OpenSans-Bold.ttf', int(height * .3067))
        self.titleBar_text = 'Butte College Academic Deadlines'
        self.RenderTitleBar()
        self.scrollBarSpeed = 3
        self.scrollBar_heightRatio = 1.0 - self.titleBar_heightRatio
        self.scrollBar_bgColor = (242,242,242)
        self.scrollBar_textColor = (0,0,0)
        self.scrollBar_textOffset = (0, 0)
        self.scrollBar_font = ('OpenSans-Regular.ttf', int(height * .33333))
        self.scrollBar_textSeperator = '      |      '
        self.scrollBar = Surface((self.width, self.height * (1.0 - self.titleBar_heightRatio)))
        self.scrollBar.fill(self.scrollBar_bgColor)
        self.scrollX1 = 0
        self.scrollX2 = 0
        self.UpdateContents()
        self.scrollBar.convert()

    def UpdateContents(self):
        self.rssTree = ET.parse(urllib.request.urlopen('http://calendar.butte.edu/RSSSyndicator.aspx?type=N&number=5&category=4-0&rssid=7&rsstitle=Academic+Calendar&sortorder=ASC'))
        root = self.rssTree.getroot()
        contentFont = font.Font(self.dir_path + '/Fonts/' + self.scrollBar_font[0], self.scrollBar_font[1])
        contentList = [title.text for title in root.iter('title')]
        contentList.pop(0)
        self.scrollBar_text = self.scrollBar_textSeperator + self.scrollBar_textSeperator.join(contentList)
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
        draw.line(self.titleBar, (0, 0, 0), (0, titleBarRect.centery), (int(self.width * .25), titleBarRect.centery), 2)
        draw.line(self.titleBar, (0, 0, 0), (titleBarRect.right, titleBarRect.centery), (titleBarRect.right - int(self.width * .25), titleBarRect.centery), 2)
        self.titleBar.blit(titleBarHeading, (titleBarRect.centerx - headingRect.centerx,
                                             titleBarRect.centery - headingRect.centery))
        self.titleBar.convert()
        self.blit(self.titleBar, (0, 0))

    def Update(self):
        if self.today != datetime.today().day:
            self.today = datetime.today().day
            self.UpdateContents()
        self.scrollX1 -= self.scrollBarSpeed
        self.scrollX2 -= self.scrollBarSpeed
        self.scrollBar.fill(self.scrollBar_bgColor)
        if self.scrollX1 < self.scrollX2 and abs(self.scrollX1) > self.scrollBar_contentRect.right:
            self.scrollX1 = self.scrollBar_contentRect.right
        elif self.scrollX1 > self.scrollX2 and abs(self.scrollX2) > self.scrollBar_contentRect.right:
            self.scrollX2 = self.scrollBar_contentRect.right
        if self.scrollX1 < self.scrollBar_Rect.right:
            self.scrollBar.blit(self.scrollBar_content, (self.scrollX1,
                                                         self.scrollBar_Rect.centery - self.scrollBar_contentRect.centery))
        if self.scrollX2 < self.scrollBar_Rect.right:
            self.scrollBar.blit(self.scrollBar_content, (self.scrollX2,
                                                         self.scrollBar_Rect.centery - self.scrollBar_contentRect.centery))
        self.blit(self.scrollBar, (0, self.height * self.titleBar_heightRatio))
        return self



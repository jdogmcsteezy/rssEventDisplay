import pygame
from pygame import Surface, time
import urllib.request
import xml.etree.ElementTree as ET

class AcademicCalanderDisplay(pygame.Surface):
	def __init__(self, width, height):
		pygame.Surface.__init__(self,(width,height))
		pygame.font.init()
		self.rssTree = ET.parse(urllib.request.urlopen('http://calendar.butte.edu/RSSSyndicator.aspx?type=N&number=5&category=4-0&rssid=7&rsstitle=Academic+Calendar&sortorder=ASC'))
		self.width = width
		self.height = height
		self.fill((255,255,255))
		self.titleBar_heightRatio = .3
		self.titleBar_bgColor = (0,0,0)
		self.titleBar_textColor = (255,255,255)
		self.titleBar_font = ('Arial', 25)
		self.titleBar_text = 'Butte College Academic Deadlines'
		self.RenderTitleBar()
		self.scrollBar_heightRatio = 1.0 - self.titleBar_heightRatio
		self.scrollBar_bgColor = (255,255,255)
		self.scrollBar_textColor = (0,0,0)
		self.scrollBar_font = ('Arial', 25)
		self.scrollBar_textSeperator = '           '
		self.scrollBar = pygame.Surface((self.width, self.height * (1.0 - self.titleBar_heightRatio)))
		self.scrollBar.fill(self.scrollBar_bgColor)
		self.UpdateContents()
		

	def UpdateContents(self):
		root = self.rssTree.getroot()
		font = pygame.font.SysFont(*self.scrollBar_font)
		self.scrollBar_text = self.scrollBar_textSeperator.join([title.text for title in root.iter('title')])
		self.scrollBar_content = font.render(self.scrollBar_text, False, self.scrollBar_textColor)
		self.scrollBar_contentRect = self.scrollBar_content.get_rect()
		self.scrollBar_Rect = self.scrollBar.get_rect()
		contentRect = self.scrollBar_content.get_rect()
		self.scrollBar.blit(self.scrollBar_content,(0, self.scrollBar_Rect.centery - self.scrollBar_contentRect.centery))
		self.blit(self.scrollBar, (0, self.height * self.titleBar_heightRatio))

	def RenderTitleBar(self):
		font = pygame.font.SysFont(*self.titleBar_font)
		titleBarHeading = font.render(self.titleBar_text, False, self.titleBar_textColor)
		self.titleBar = pygame.Surface((self.width, self.height * self.titleBar_heightRatio))
		self.titleBar.fill(self.titleBar_bgColor)
		titleBarRect = self.titleBar.get_rect()
		headingRect = titleBarHeading.get_rect()
		self.titleBar.blit(titleBarHeading, (titleBarRect.centerx - headingRect.centerx,titleBarRect.centery - headingRect.centery))
		self.blit(self.titleBar, (0,0))

	def Update(self):
		self.scrollBar_content.scroll(-2,0)
		self.scrollBar.fill(self.scrollBar_bgColor)
		self.scrollBar.blit(self.scrollBar_content,(0, self.scrollBar_Rect.centery - self.scrollBar_contentRect.centery))
		self.blit(self.scrollBar, (0, self.height * self.titleBar_heightRatio))
		return self

def main():
	pygame.init()
	clock = pygame.time.Clock()
	testScreen = pygame.display.set_mode((600,600))
	testScreen.fill((200,255,230))
	ticker = AcademicCalanderDisplay(600, 75)
	testScreen.blit(ticker, (0,0))
	pygame.display.update()
	run = True
	while(run):
		clock.tick(26)
		testScreen.blit(ticker.Update(),(0,0))
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
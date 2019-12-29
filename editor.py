import pygame,sys

pygame.init()

clock = pygame.time.Clock()

cursor_font = pygame.font.SysFont('algerian',27)

window_size = window_width, window_height = 1700, 1000

border_left = window_width / 4 + window_width / 16

border_top = window_height / 6

input_width, input_height  = window_width / 2, window_height

gray_background = (192,192,192)

alpha = 255  # The current alpha value of the surface.
timer = 20  # To get a 20 frame delay.

window = pygame.display.set_mode(window_size , pygame.RESIZABLE)

window.fill(gray_background)

white = (255,255,255)

black = (0,0,0)


class Input_Page:
	def __init__(self):
		self.input_part = pygame.draw.rect(window,white,(window_width/4,0,input_width, input_height))
		pygame.display.flip()
		self.list_of_strings = [[]]
		self.num_of_rows = len(self.list_of_strings)
		self.app_font = pygame.font.SysFont('timesnewroman',25)
		self.current_letter_position = 'default'
		self.current_row = self.num_of_rows-1
		self.orig_surf = cursor_font.render('|', True, pygame.Color('royalblue'))
		self.txt_surf = self.orig_surf.copy()

	def text_rendering(self):
		text = ''.join(self.list_of_strings[self.num_of_rows-1])
		rendered_text = self.app_font.render(text,True,black)
		window.blit(rendered_text, (border_left,border_top))
		pygame.display.flip()

	def row_checker(self):
		text = ''.join(self.list_of_strings[self.num_of_rows-1])
		word_width = (self.app_font.size(text))[0]
		word_heigth = self.app_font.size(text)[1]
		print(word_width)
		if word_width + 2 * (window_width/16) + cursor_font.size('|')[0] + 5 >= input_width :
			print('yikes')
			self.list_of_strings.append([])
			self.num_of_rows += 1
			self.current_row += 1
			#self.text_rendering()


	def event_checker(self):
		for event in pygame.event.get():
			if len(self.list_of_strings[self.num_of_rows-1])!=0 and self.current_letter_position == 'default':
				self.current_letter_position = len(self.list_of_strings[self.num_of_rows-1]) - 1
			if len(self.list_of_strings[self.num_of_rows-1]) == 0:
				self.current_letter_position = 0
			if len(self.list_of_strings) == 0:
				self.current_row = 0

			if event.type == pygame.KEYDOWN:
				if(event.key == pygame.K_BACKSPACE):
					self.list_of_strings[self.current_row] = self.list_of_strings[self.current_row][0:self.current_letter_position] + self.list_of_strings[self.current_row][self.current_letter_position + 1:]
					self.current_letter_position -= 1
					pygame.draw.rect(window,white,(window_width/4,0,input_width, input_height))
					#self.text_rendering()

				elif event.key == pygame.K_LEFT:
					if(self.current_letter_position != 0):
						self.current_letter_position -= 1 
				elif event.key == pygame.K_RIGHT:
					if(self.current_letter_position != len(self.list_of_strings[0])):
						self.current_letter_position += 1
				elif event.key == pygame.K_UP:
					if self.current_row != 0:
						self.current_row -= 1
				elif event.key == pygame.K_DOWN:
					if self.current_row != self.num_of_rows - 1:
						self.current_row += 1
				elif event.key == pygame.K_RETURN:
					self.list_of_strings.append([])
					self.num_of_rows += 1
					self.current_row += 1

				else:
					self.list_of_strings[self.current_row].insert(self.current_letter_position,event.unicode)	
					self.current_letter_position += 1

			elif event.type==pygame.QUIT:
				sys.exit()

	def rows_iterator(self):
		for row in self.list_of_strings:
			text = ''.join(row)
			#print('aye')
			global border_top
			border_top += self.app_font.size(text)[1]
			rendered_text = self.app_font.render(text,True,black)
			window.blit(rendered_text, (border_left, border_top))
			pygame.display.flip()

	def blinking_cursor(self):
		global alpha,timer
		if timer > 0:
			timer -= 1
		else:
			if alpha > 0:
			# Reduce alpha each frame, but make sure it doesn't get below 0.
				alpha = max(0 , alpha - 4)
				# Create a copy so that the original surface doesn't get modified.                
				self.txt_surf = self.orig_surf.copy()
				self.txt_surf.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
			else:
				timer = 20
				alpha = 255

		text = self.app_font.size(''.join(self.list_of_strings[self.current_row][0:self.current_letter_position]))
		window.fill(white,((border_left + text[0], window_height / 6 + (self.current_row + 1)*text[1]),(cursor_font.size('|')[0],cursor_font.size('|')[1])))
		#print(cursor_font.size('|')[0])
		window.blit(self.txt_surf, (border_left + text[0] , window_height / 6 + (self.current_row + 1)*text[1]))
		pygame.display.flip()
		clock.tick(50)


	def typing(self):
		while 1:
			global border_top, border_left
			border_left = window_width / 4 + window_width / 16
			border_top = window_height / 6
			self.event_checker()
			self.rows_iterator()
			self.blinking_cursor()
			self.row_checker()
			self.text_rendering()


input_page = Input_Page()
input_page.typing()
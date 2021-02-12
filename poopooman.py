import random, sys, time, pygame
from pygame.locals import*

fps = 30
windows_width = 640
window_height = 480
#in milliseconds
flash_speed = 500
#in milliseconds
flash_delay = 200
button_size = 200
button_gapsize = 20
#seconds before game over if no button is pushed
time_out = 4
#colors
WHITE = (255, 255, 255)
DARK = (66, 45, 45)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = ( 0, 255, 0)
GREEN = ( 0, 155, 0)
BRIGHTBLUE = ( 0, 0, 255)
BLUE = ( 0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
DARKGRAY = ( 40, 40, 40)
BLACK = (0, 0 , 0)

bgColor = DARK
xmargin = int((windows_width - (2 * button_size) - button_gapsize) / 2)
ymargin = int((window_height - (2 * button_size) - button_gapsize) / 2)

#rect object for each of the four buttons
YELLOWRECT = pygame.Rect(
	xmargin, 
	ymargin,
	button_size,
	button_size
	)
BLUERECT = pygame.Rect(
	xmargin + button_size + button_gapsize,
	ymargin,
	button_size, 
	button_size
	)
REDRECT = pygame.Rect(
	xmargin, 
	ymargin + button_size + button_gapsize,
	button_size,
	button_size
	)
GREENRECT = pygame.Rect(
	xmargin + button_size + button_gapsize,
	ymargin + button_size + button_gapsize,
	button_size,
	button_size
	)

def main():
	global fpsclock, display_surf, basic_font, beep1, beep2, beep3, beep4
	pygame.init()
	fpsclock = pygame.time.Clock()
	display_surf = pygame.display.set_mode(
		(
		windows_width, 
		window_height
		)
	)
	pygame.display.set_caption('POO POO man')
	basic_font = pygame.font.SysFont(
		'timesnewroman',
		18
		)
	infoSurf = basic_font.render(
		'--Q is Yellow, W is Blue, A is Red, S is Green--',
		1,
		BLACK
		)
	infoRect = infoSurf.get_rect()
	infoRect.topleft = (
		145,
		window_height - 253
		)
	#load the sound files
	beep1 = pygame.mixer.Sound('Sounds/beep1.ogg')
	beep2 = pygame.mixer.Sound('Sounds/beep2.ogg')
	beep3 = pygame.mixer.Sound('Sounds/beep3.ogg')
	beep4 = pygame.mixer.Sound('Sounds/beep4.ogg')
	#initialize some variables for a new game
	pattern = [] #stores the pattern of colors
	current_step = 0 #the color of the player must push next
	last_click_time = 0 #timestamp of the players last button push
	score = 0
	"""
	when False, the pattern is playing.
	when True, waiting for the player to click
	a colored button:  
	"""
	waiting_for_input = False
	#main game loop
	while True:
		'''
		buton that was clicked
		(set to YELLOW, RED, GREEN, or BLUE)
		'''
		clicked_button = None
		display_surf.fill(bgColor)
		drawButtons()
		score_surf = basic_font.render(
			'Score: ' + str(score),
			1,
			WHITE
			)
		score_rect = score_surf.get_rect()
		score_rect.topleft = (
			windows_width - 100,
			10
			)
		display_surf.blit(infoSurf, infoRect)
		check_for_quit()
		#event handling loop
		for event in pygame.event.get(): 
			if event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				clicked_button = getButtonClicked(mousex, mousey)
			elif event.type == KEYDOWN:
					if event.key == K_q:
						clicked_button = YELLOW
					elif event.key == K_w:
						clicked_button = BLUE
					elif event.key == K_a:
						clicked_button = RED
					elif event.key == K_s:
						clicked_button = GREEN

		if not waiting_for_input:
			#play the pattern
			pygame.display.update()
			pygame.time.wait(1000)
			pattern.append(
				random.choice(
					(
						YELLOW,
						BLUE,
						RED,
						GREEN
						)
					)
				)
			for button in pattern:
				flashButtonAnimation(button)
				pygame.time.wait(flash_delay)
			waiting_for_input = True
		else:
			#wait for the player to enter buttons
			if clicked_button and clicked_button == pattern[current_step]:
				#pushed the correct button
				flashButtonAnimation(clicked_button)
				current_step += 1
				last_click_time = time.time()
				if current_step == len(pattern):
					#pushed the last button in the pattern
					changeBackgroundAnimation()
					score += 1
					waiting_for_input = False
					current_step = 0 #reset back to first step
			elif(
				clicked_button and clicked_button != pattern[current_step]
				) or (
				current_step != 0 and time.time() - time_out > last_click_time
				):
				#pushed the incorrect button, or has timed out
				gameOverAnimation()
				#reset the variables for a new game:
				pattern = []
				current_step = 0
				waiting_for_input = False
				score = 0
				pygame.time.wait(1000)
				changeBackgroundAnimation()
		pygame.display.update()
		fpsclock.tick(fps)

def terminate():
	pygame.quit()
	sys.exit()

def check_for_quit():
	for event in pygame.event.get(QUIT): #get all the QUIT events
		terminate() #terminate if any QUIT events are present
	for event in pygame.event.get(KEYUP): #get all the KEYUP events
		if event.key == K_ESCAPE:
			terminate() #terminate if the KEYUP event was for the Esc key
		pygame.event.post(event) #put the other KEYUP events objects back

def flashButtonAnimation(color, animation_speed = 50):
	if color == YELLOW:
		sound = beep1
		flashColor = BRIGHTYELLOW
		rectangle = YELLOWRECT
	elif color == BLUE:
		sound = beep2
		flashColor = BRIGHTBLUE
		rectangle = BLUERECT
	elif color == RED:
		sound = beep3
		flashColor = BRIGHTRED
		rectangle = REDRECT
	elif color == GREEN:
		sound = beep4
		flashColor = BRIGHTGREEN
		rectangle = GREENRECT
	origSurf = display_surf.copy()
	flashSurf = pygame.Surface(
		(
			button_size,
			button_size
			)
		)
	flashSurf = flashSurf.convert_alpha()
	r, g, b = flashColor
	sound.play()
	for start, end, step in ((0, 255, 1), (255, 0, -1)): #animation loop
		for alpha in range(start, end, animation_speed * step):
			check_for_quit()
			display_surf.blit(origSurf, (0, 0))
			flashSurf.fill((r, g, b, alpha))
			display_surf.blit(flashSurf, rectangle.topleft)
			pygame.display.update()
			fpsclock.tick(fps)
	display_surf.blit(origSurf, (0, 0))

def drawButtons():
	pygame.draw.rect(display_surf, YELLOW, YELLOWRECT)
	pygame.draw.rect(display_surf, BLUE, BLUERECT)
	pygame.draw.rect(display_surf, RED, REDRECT)
	pygame.draw.rect(display_surf, GREEN, GREENRECT)

def changeBackgroundAnimation(animation_speed = 40):
	global bgColor
	new_bg_color = (
		random.randint(0, 255),
		random.randint(0, 255),
		random.randint(0, 255)
		)
	new_bg_surf = pygame.Surface(
		(
			windows_width,
			window_height
			)
		)
	new_bg_surf = new_bg_surf.convert_alpha()
	r, g, b = new_bg_color
	for alpha in range(0, 255, animation_speed): #animation loop
		check_for_quit()
		display_surf.fill(bgColor)
		new_bg_surf.fill((r, g, b, alpha))
		display_surf.blit(new_bg_surf, (0, 0))
		drawButtons() #redraw the button on top of the tint
		pygame.display.update()
		fpsclock.tick(fps)
	bgColor = new_bg_color

def gameOverAnimation(color = WHITE, animation_speed = 50):
	#play all beeps at once, then flash the background
	origSurf = display_surf.copy()
	flashSurf = pygame.Surface(display_surf.get_size())
	flashSurf = flashSurf.convert_alpha()
	#play all 4 beeps at the same time, roughly
	beep1.play()
	beep2.play()
	beep3.play()
	beep4.play()
	r, g, b = color
	for i in range(3): #do the flash 3 times
		for start, end, step in ((0, 255, 1), (255, 0, -1)):
			'''
			the first iteration in this loop sets the following
			for loop to go from 0 to 255, the second
			from 255 to 0.
			'''
			for alpha in range(start, end, animation_speed * step): #animation loop
				#alpha means tranparancy. 255 is opaque, 0 is invisible
				check_for_quit()
				flashSurf.fill((r, g, b, alpha))
				display_surf.blit(origSurf, (0, 0))
				display_surf.blit(flashSurf, (0, 0))
				drawButtons()
				pygame.display.update()
				fpsclock.tick(fps)

def getButtonClicked(x, y):
	if YELLOWRECT.collidepoint((x, y)):
		return YELLOW
	elif BLUERECT.collidepoint((x, y)):
		return BLUE
	elif REDRECT.collidepoint((x, y)):
		return RED
	elif GREENRECT.collidepoint((x, y)):
		return GREEN
	return None

if __name__ == '__main__':
	main()
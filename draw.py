#-*- coding: utf-8 -*-
from __future__ import print_function

import pygame
import eye_detect
from data_filter import filter_data
import time

import numpy as np
import numpy.linalg as LA

pygame.init()

width = 600
hight = 300

width = 1100
hight = 700

# screen = pygame.display.set_mode((1300,700))
screen = pygame.display.set_mode((width,hight))

i = 0

# keypoints = [(0, 0), (0.25, 0), (0.5, 0), (0.75, 0),	 (1, 0),
# 			 (0, 0.25), (0.25, 0.25), (0.5, 0.25), (0.75, 0.25), (1, 0.25),
# 			 (0, 0.5), (0.25, 0.5), (0.5, 0.5), (0.75, 0.5), (1, 0.5),
# 			 (0, 0.75), (0.25, 0.75), (0.5, 0.75), (0.75, 0.75), (1, 0.75),
# 			 (0, 1), (0.25, 1), (0.5, 1), (0.75, 1), (1, 1)]

# keypoints = [(0, 0), (0.5, 0), (1, 0),
# 			 (0.25, 0.25), (0.75, 0.25),
# 			 (0, 0.5), (0.5, 0.5), (1, 0.5),
# 			 (0.25, 0.75), (0.75, 0.75),
# 			 (0, 1), (0.5, 1), (1, 1)]

keypoints = [(0, 0), (0.5, 0), (1, 0), 
			(0, 1),  (0.5, 1), (1, 1)]

# keypoints = [(0, 0), (0, 1), (1, 1), (1, 0)]
keypoints = [(int(x*width), int(y*hight)) for x, y in keypoints]

print('pad adjusting')
pad = [0, 3, 2, 1, 0, 3, 2, 3, 1, 2, 2, 2, 3, 2, 1, 3, 0, 0, 0, 1, 3, 2, 0, 2, 0, 1, 0, 2, 2, 1, 2, 2, 0, 3]

screen_point_letter_mapping = [0, 2, 3, 5]
space_pad_n = 4
alth = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

print(alth)

letter_pad_map = []
for cur_pad_n in range(max(pad) + 1):
	cur_pad_n_letters = []
	for letter, pad_n in zip(alth, pad):
		if pad_n == cur_pad_n:
			cur_pad_n_letters.append(letter)

	letter_pad_map.append(''.join(cur_pad_n_letters))

print(letter_pad_map)

# if (np.max(pad)) + 1 != len(keypoints):
# 	print('Pad and keypoints are not coherent! Exit.')
# 	exit(0)

print('start traking')
eye_detect.start_thread()


# waiting for SPACE
def wait_until_space():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				print("SPACE")
				return

wait_until_space()

print('calibrating')
eye_pairs = []
screen_pairs = []

for k_x, k_y in keypoints:
	
	eyepoints = []

	screen.fill([0,0,0])
	pygame.draw.circle(screen, (0, 255, 0), (k_x,k_y), 30, 10)
	pygame.display.update()
	time.sleep(1)

	screen.fill([0,0,0])
	stop = time.time()+3
	while time.time() < stop:
		eyepoints.append((eye_detect.x, eye_detect.y))

	x_m = 0
	y_m = 0
	for x, y in eyepoints:
		x_m += x
		y_m += y

	x_m = float(x_m) / len(eyepoints)
	y_m = float(y_m) / len(eyepoints)

	print(k_x, k_y)
	print(x_m, y_m)

	eye_pairs.append( np.asarray([x_m, y_m]) )
	screen_pairs.append( np.asarray([k_x, k_y]) )

screen.fill([0,0,0])

bufsize = 5
buf = [[0, 0]]*bufsize

typing = False

tape = []

stop = None

def space_pressed():
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			return True

	return False

print('mouse moving')
while True:
	screen.fill([0,0,0])

	buf.pop(0)
	buf.append([eye_detect.x, eye_detect.y])
	eyepos = np.median(np.asarray(buf), axis = 0)

	dists = [ LA.norm(eyepos - x) for x in eye_pairs]
	
	dists = dists / np.sum(dists)
	weights = (1 - dists)

	weights = (weights / LA.norm(weights))**2
	best_point_n = np.argmax(weights)
	best_screen_point = screen_pairs[ best_point_n ]

	font = pygame.font.Font(None, 25)

	point = np.zeros((2, ))
	for w, p in zip(weights, screen_pairs):
		point += w*p
		screen.blit(font.render("%f.3" % w, True, [255, 255, 255]), p*0.9)

	# print(eye_detect.x, eye_detect.y, point, end='\r')

	
	pygame.draw.circle(screen, (0, 255, 0), (int(point[0]),int(point[1])), 30, 10)
	pygame.draw.circle(screen, (255, 0, 0), (int(best_screen_point[0]),int(best_screen_point[1])), 30, 10)

	# letters on the screen
	bigfont = pygame.font.Font(None, 45)
	
	for string, screen_point_id in zip(letter_pad_map, screen_point_letter_mapping):
		p = screen_pairs[screen_point_id]
		screen.blit(bigfont.render(string, True, [255, 255, 255]), p*0.7 + np.array([0, 20]))

	# when SPACE start typing

	if typing:
		tape.append(best_point_n)
		if space_pressed():
			print( tape )
			print( filter_data(tape, verbose = True) )
			tape = []
	else:
		if space_pressed():
			print("start typing")
			typing = True

	pygame.display.update()
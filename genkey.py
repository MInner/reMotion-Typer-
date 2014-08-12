#-*- coding: utf-8 -*-
from collections import defaultdict
import random
pairs = []

alth = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

reverce = dict([(y, x) for x, y in enumerate(alth)])

npad = 4

words = []

maxn = 5000

good = []

with open('goodwords.txt') as gf:
	for line in gf:
		word = line[:-1].decode('utf-8')
		good.append(word)

with open('words.txt') as f:
	for line in f:
		n, freq, word = line.split()
		word = word.decode('utf-8')
		words.append(word)

		# all pairs:
		# - (a, b) -> seq on single - error 3
		# - (a, b) + (a, c) -> a \ c on single - error 1

		if int(n) < maxn:
			for i in range(len(word) - 1):
				pairs.append((word[i:i+2], int(float(freq))))

	for word in good:
		for i in range(len(word) - 1):
			pairs.append((word[i:i+2], 10000))

finalpairs = defaultdict(int)
for letters, freq in pairs:
	finalpairs[letters] += freq

lastpad = []
word_to_path_cache = {}

def path_to_word(path, pad, n = 10):
	global lastpad, word_to_path_cache
	match = []
	if pad != lastpad:
		lastpad = pad
		for word in words:
			word_to_path_cache[word] = word_to_path(word, pad)

	for word in words:
		if len(word) == len(path) and word_to_path_cache[word] == path:
			match.append(word)
			if len(match) == n:
				return match

	return match

def word_to_path(word, pad):
	return [pad[reverce[letter]] for letter in word]

def energy(pad):
	error = 0
	for (l1, l2), freq in finalpairs.items():
		if pad[alth.index(l1)] == pad[alth.index(l2)]:
			error += freq*3
	
	freqpart = error

	print('Pad: ', pad)
	for w in good:
		path = word_to_path(w, pad)
		matches = path_to_word(path, pad)
		if w in matches:
			place = matches.index(w)
		else:
			place = 10
		print(w, '\t', place, '\t', path)

	avgplace = 0
	first_n_words = 500

	for w in words[:first_n_words] + good:
		path = word_to_path(w, pad)
		matches = path_to_word(path, pad)
		if w in matches:
			place = matches.index(w)
		else:
			place = 10

		if w in good:
			place = place*4

		error += 500*(2**place)
		avgplace += place

	print('Error:', error, '[freq: %d]' % freqpart)
	print('Avg place:', avgplace/(first_n_words + 500))
	return error

def move(pad):
	i = random.randint(0, len(pad) - 1)
	choice = list(range(0, npad))
	choice.remove(pad[i])
	pad[i] = random.choice(choice)

from anneal import Annealer

def optimize():
	state =  [0, 3, 2, 1, 0, 3, 2, 3, 1, 2, 2, 2, 3, 2, 1, 3, 0, 0, 0, 1, 3, 2, 0, 2, 0, 1, 0, 2, 2, 1, 2, 2, 0, 3]
	annealer = Annealer(energy, move)
	schedule = annealer.auto(state, minutes=0.1)
	state, e = annealer.anneal(state, schedule['tmax'], schedule['tmin'], 
	                            schedule['steps'], updates=6)
	print(state)  # the "final" solution


def printpad(pad):
	for l in alth:
		print(l, ' ', pad[reverce[l]])

def main():
	optimize()
	# pad = [0, 2, 1, 1, 0, 3, 2, 2, 0, 2, 0, 2, 1, 0, 1, 3, 2, 3, 0, 1, 3, 1, 0, 3, 2, 0, 3, 1, 2, 2, 3, 3, 1, 0]
	# for path in '232131 1 02001121'.split():
	# 	n = [int(x) for x in path]
	# 	print(n)
	# 	print(path_to_word(n, pad))

if __name__ == '__main__':
	main()

# state = [random.randint(0, npad-1) for x in range(len(alth))]
# state = [2, 2, 3, 0, 1, 3, 3, 0, 1, 3, 3, 0, 0, 0, 1, 2, 1, 3, 0, 1, 0, 1, 1, 2, 3, 1, 1, 3, 2, 3, 3, 0, 3, 1]
# state = [3, 0, 0, 2, 1, 1, 0, 3, 3, 0, 0, 2, 1, 2, 1, 3, 2, 2, 3, 1, 0, 1, 2, 2, 0, 1, 3, 3, 2, 2, 3, 2, 0, 0]
# state =  [0, 0, 0, 2, 1, 1, 0, 3, 3, 0, 0, 2, 2, 2, 1, 3, 2, 1, 3, 1, 0, 1, 0, 2, 0, 0, 3, 3, 2, 2, 3, 3, 0, 0]
# state = [0, 0, 0, 2, 1, 1, 0, 3, 3, 2, 0, 2, 2, 2, 1, 3, 2, 1, 3, 1, 0, 1, 0, 2, 2, 0, 3, 2, 2, 2, 3, 3, 0, 1]
# state = [0, 1, 0, 1, 2, 3, 2, 3, 3, 2, 0, 2, 1, 3, 1, 3, 2, 1, 0, 1, 3, 1, 0, 2, 2, 3, 3, 1, 2, 2, 2, 3, 1, 0]
# state = [0, 2, 1, 1, 0, 3, 2, 2, 0, 2, 0, 2, 1, 0, 1, 3, 2, 3, 0, 1, 3, 1, 0, 3, 2, 0, 3, 1, 2, 2, 3, 3, 1, 0]
# state = [0, 3, 2, 1, 0, 3, 3, 2, 1, 2, 2, 2, 3, 2, 2, 3, 0, 3, 0, 1, 3, 1, 1, 2, 0, 0, 0, 3, 2, 1, 3, 3, 0, 0]
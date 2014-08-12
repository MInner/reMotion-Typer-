import numpy as np

def filter_data(data, verbose = False, wsize = 10, low_filter = 0.5, high_filter = 2):
	prev = -1
	clustered = []
	periods = []
	filtered = []
	counter = 0

	mod_data = data[:]
	mod_data.extend(data[-wsize/2:])

	window = data[:wsize + 1]

	for element in mod_data[wsize+1:]:
		filtered.append(window.pop(0))
		window.append(element)
		if window.count(window[wsize/2]) < 3:
			if window.count(window[0]) > window.count(window[-1]):
				window[wsize/2] = window[0]
			else:
				window[wsize/2] = window[-1]

	filtered.extend(window)
	filtered = filtered[:-wsize/2]

	for element in filtered:
		if prev != element:
			prev = element
			clustered.append(element)
			periods.append(counter)
			counter = 1
		else:
			counter += 1

	periods.append(counter)
	periods = periods[1:]

	med_period = np.median(periods)
	final = []
	for dt, pr in zip(clustered, periods):
		if pr > med_period*low_filter:
			final.append(dt)
		if pr > med_period*high_filter:
			final.append(dt)


	if verbose:
		print("Data: ", data)
		print("Filtered: ", filtered)
		print("Clustered: ", clustered)
		print("Periods: ", periods)
		print("Median period: ", med_period)
		print("Final: ", final)

	return final

def test():
	data = [0, 0, 0, 0, 2, 0, 0, 1, 3, 3, 3, 2, 2, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2, 2] + [2]*20
	final = filter_data(data, verbose = True)

if __name__ == '__main__':
	test()
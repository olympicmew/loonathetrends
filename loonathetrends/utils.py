import ephem

def get_moon_phase(date):
	date = ephem.Date(date.datetime)
	nnm = ephem.next_new_moon(date)
	pnm = ephem.previous_new_moon(date)
	return (date-pnm) / (nnm-pnm)

def get_moon_emoji(phase):
	emojis = '🌑🌒🌓🌔🌕🌖🌗🌘'
	idx = round(phase*8) % 8
	return emojis[idx]

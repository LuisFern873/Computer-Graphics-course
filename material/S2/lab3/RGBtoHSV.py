# Python3 program change RGB Color 
# Model to HSV Color Model 

# https://www.geeksforgeeks.org/program-change-rgb-color-model-hsv-color-model/

def rgb_to_hsv(r, g, b): 

	# R, G, B values are divided by 255 
	# to change the range from 0..255 to 0..1: 
	r, g, b = r / 255.0, g / 255.0, b / 255.0

	print("r' = r / 255 = ", r)
	print("g' = g / 255 = ", g)
	print("b' = b / 255 = ", b)

	# h, s, v = hue, saturation, value 
	cmax = max(r, g, b) # maximum of r, g, b 
	print("cmax = ", cmax)
	cmin = min(r, g, b) # minimum of r, g, b 
	print("cmin = ", cmin)

	diff = cmax-cmin	 # diff of cmax and cmin. 
	print("diff = cmax - cmin = ", diff)

	# if cmax and cmax are equal then h = 0 
	if cmax == cmin: 
		h = 0
		print("cmax == cmin")
		print("h = ", h)
	# if cmax equal r then compute h 
	elif cmax == r: 
		h = (60 * ((g - b) / diff) + 360) % 360
		print("cmax == r")
		print("h = (60 * ((g' - b') / diff) + 360) % 360 = ", h)

	# if cmax equal g then compute h 
	elif cmax == g: 
		h = (60 * ((b - r) / diff) + 120) % 360
		print("cmax == g")
		print("h = (60 * ((b' - r') / diff) + 120) % 360 = ", h)

	# if cmax equal b then compute h 
	elif cmax == b: 
		h = (60 * ((r - g) / diff) + 240) % 360
		print("cmax == b")
		print("h = (60 * ((r' - g') / diff) + 240) % 360 = ", h)

	# if cmax equal zero 
	if cmax == 0: 
		s = 0
		print("cmax == 0")
		print("s = ", 0)
	else: 
		s = (diff / cmax) * 100
		print("cmax != 0")
		print("s = (diff / cmax) * 100 = ", s)

	# compute v 
	v = cmax * 100
	print("v = cmax * 100 = ", v)
	return h, s, v 

def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        # Black
        return 0, 0, 0, 100

    # Convert RGB to range [0, 1]
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0

    # Calculate CMY values
    c = 1 - r
    m = 1 - g
    y = 1 - b

    # Calculate K value
    k = min(c, m, y)

    # Calculate the final CMYK values
    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)
    k = k

    # Convert to percentages
    c = round(c * 100)
    m = round(m * 100)
    y = round(y * 100)
    k = round(k * 100)

    return c, m, y, k


''' Driver Code '''
# print(rgb_to_hsv(45, 215, 0)) 
# print(rgb_to_hsv(31, 52, 29)) 

print(rgb_to_hsv(34, 139, 34)) 

# print(rgb_to_cmyk(34, 139, 34)) 

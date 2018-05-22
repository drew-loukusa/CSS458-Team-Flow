import pylab as plt

# Load the image
img = plt.imread("airport.png")

# Grid lines at these intervals (in pixels)
# dx and dy can be different
dx, dy = 500,100
dx2 = dx+1
dy2 = dy+1

# Custom (rgb) grid color
grid_color = [140,140,140]

# Modify the image to include the grid


# Show the result
plt.imshow(img)
plt.show()
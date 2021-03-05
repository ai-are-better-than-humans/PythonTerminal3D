from stl import mesh
from os import system
from math import radians
from numpy import reshape
from readchar import readchar


# Open STL file and decide on orientation speed
stl_mesh = mesh.Mesh.from_file('teapot_simplified.stl', speedups=True)
rotation_speed = 30

def print_grid(coords, precision):
  # Since we cant print inbetween pixels or behind the monitor
  # We have to format the coordinates such that they are all positive whole numbers

  # We can make them non negative simply by adding the lowest value to each number
  # (And if none of them are negative we're already good to go)
  # But if we want them to be whole we'll have to round, truncating some of the digits.

  # This will result in a loss of quality yet improved speed.
  # We can multiply them by a power of 10 before we truncate to determine said quality 

  lowest = (min(min(coords, key = lambda t: t[0])[0], 0), min(min(coords, key = lambda t: t[1])[1], 0))
  formatted_coords = []
  grid = ""

  for i in coords:
    # Ensure that no point falls below 0 by adding the lowest value to everything
    # And round with "precision" digits of precision so that there are only integers
    new_point = (round((i[0]-lowest[0])*precision), round((i[1]-lowest[1])*precision))

    # Repeats are computationally expensive
    if new_point not in formatted_coords:
      formatted_coords.append(new_point)

  # Find the highest values, these will serve as our dimensions
  dimensions = (max(formatted_coords, key = lambda t: t[0])[0], max(formatted_coords, key = lambda t: t[1])[1])

  for x in range(dimensions[0]):
    for y in range(dimensions[1]):
      
      # Check if the current space is or is not a point
      if (x, y) in formatted_coords:
        grid += "•"
      else:
        grid += " "
        
    # Add newline for next set of y values
    grid += "\n"

  system('clear')
  print(grid)


def rotate_and_display(rotation_matrix, degrees):
  stl_mesh.rotate(rotation_matrix, radians(degrees))

  # When gathering coordinates, we truncate the z dimension
  # This does not mean it cant rotate, as the mesh object will update when we do said functions
  # This is simply done since our monitors cant display in 3D
  xy = list(stl_mesh.vectors.flatten())
  del xy[2::3]

  print_grid(reshape(xy, (-1, 2)), 5)


# Rotate to starting orientation
rotate_and_display([0, 0.5, 0], 90)

while True:
   # Get current keypress and decide on rotation from it
  keypress = readchar()

  if keypress == "d":
    rotate_and_display([0.5, 0, 0], rotation_speed)
  elif keypress == "a":
    rotate_and_display([0.5, 0, 0], -rotation_speed)
  elif keypress == "w":
    rotate_and_display([0, 0.5, 0], rotation_speed)
  elif keypress == "s":
    rotate_and_display([0, 0.5, 0], -rotation_speed)
  elif keypress == "z":
    rotate_and_display([0, 0, 0.5], rotation_speed)
  elif keypress == "x":
    rotate_and_display([0, 0, 0.5], -rotation_speed)

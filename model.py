import numpy as np
import plotly.graph_objects as go
from matplotlib import pyplot as plt
import sys as sys
from model_funcs import *

MODEL_FUNC = power
DARK_SIDE = 0
LATITUDE = 45

def psi(lat, time):

  # Bounds check latitude
  if (abs(lat)>90):
    sys.exit('Error. Latitude should be less than 90 degrees!')
  else:
    pass

  # Bounds check time
  if ((time < 6) or (time > 18)):
    sys.exit('Error. Time should be between dawn (0600) and dusk (1800) for the dayside!')
  else:
    pass

  time_angle_midnight = ((time/24)*(2*np.pi))%(2*np.pi)
  time_angle_noon = np.pi - time_angle_midnight

  # Define co-ordinate system
  # +z - out of the page (from the moon to the sun)
  # +y - from right to left in the page
  # +x - from bottom to top, in the page

  # Initial position vector - (x,y,z) triplet: [0,0,1]

  r = np.mat(np.array([[0],[0],[1]]))

  # 1. Latitudinal rotation

  # Given our co-ordinate system, latitudinal rotation is a rotation about the y-axis
  # Rotation matrix for rotation about the y-axis is:
  # [cos(theta), 0, sin(theta); 0, 1, 0; -sin(theta), 0, cos(theta)]

  lat_rad = (lat*np.pi/180)

  t11 = np.cos(lat_rad)
  t13 = np.sin(lat_rad)
  t31 = -t13
  t33 = t11

  R_y = np.mat(np.array([[t11,0,t13],[0,1,0],[t31,0,t33]]))

  r1 = R_y*r

  # 2. Longitudinal rotation

  # Rotate about the +x axis by the angle from noon.
  # R_x = [1, 0, 0; 0, cos(theta), -sin(theta); 0, sin(theta), cos(theta)]

  C = np.cos(time_angle_noon)
  S = np.sin(time_angle_noon)

  R_x = np.mat(np.array([[1,0,0],[0,C,-S],[0,S,C]]))
  r2 = R_x*r1

  # 3. Now taking the dot product, dividing by the square of the magnitudes of the vectors, and then taking cosine inverse.
  # Since we used unit vectors, we're basically only taking the cosine inverse.

  dot_product = r[0,0]*r2[0,0] + r[1,0]*r2[1,0] + r[2,0]*r2[2,0]
  psi = np.arccos(dot_product)

  return psi

def model(start_time, end_time, time_step, latitude):

  times = np.linspace(start_time, end_time, round((end_time-start_time)/time_step))
  output = np.zeros(len(times))

  for i in range(len(times)):
    time = times[i]
    time %= 24
    if time < 6 or time > 18:
      continue

    output[i] = MODEL_FUNC(psi(latitude, time))
  
  return times, output

step_size_times_hrs = 2/60
times_start = 6 # Dawn
times_stop = 18 # Dusk
# Bear in mind that this entire plot is only for dayside temperatures.

lat_min = -90
lat_max = 90
lat_step = 0.5

num_steps_time = int(((times_stop - times_start)/step_size_times_hrs))
num_steps_lat = int(((lat_max - lat_min)/lat_step))
print("Matrix size: ", num_steps_lat, "x", num_steps_time)

powers = np.zeros((num_steps_lat, num_steps_time), float)

lat_count = 0
for latitude in np.linspace(lat_min, lat_max, num_steps_lat):
  lat_count = lat_count + 1
  long_count = 0
  for time in np.linspace(times_start, times_stop, num_steps_time):
    long_count = long_count + 1
    powers[lat_count-1, long_count-1] = MODEL_FUNC(psi(latitude, time))

#concatenate ones to end of Temps array. This is a workaround for finding the actual values
#from the dark side of the moon. Implementation of the equation needs to be done.
dark_side = np.ones((num_steps_lat, num_steps_time), float) * DARK_SIDE
surface = np.concatenate((powers, dark_side), axis=1)

#Plotting the sphere.
u = np.linspace(0, np.pi, 360)
v = np.linspace(0, 2*np.pi, 720)
x=np.outer(np.cos(u), np.sin(v))
y=np.outer(np.sin(u), np.sin(v))
z=np.outer(np.ones(np.size(u)), np.cos(v))

fig = go.Figure(go.Surface(
    surfacecolor = surface,
    colorscale = 'hot',
    x = x,
    y = y,
    z = z))
fig.show()

m = model(0,24,step_size_times_hrs,LATITUDE)
plt.plot(m[0], m[1])

plt.title("Lunar Model At Latitude: " + str(LATITUDE) + " Degrees")
plt.xlabel("Lunar time (hr)")

if MODEL_FUNC == temp:
  y_lab = TEMP_AXIS_LABEL
elif MODEL_FUNC == power:
  y_lab = POWER_AXIS_LABEL
else:
  y_lab = "Unknown"
plt.ylabel(y_lab)

plt.show()
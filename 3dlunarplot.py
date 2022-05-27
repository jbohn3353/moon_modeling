from pylab import figure, cm
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.basemap import Basemap

import sys as sys

def SurfaceTemperature(lat, time):#From jupyter notebook

  # lat = 40 # in degrees

  if (abs(lat)>90):
    sys.exit('Error. Latitude should be less than 90 degrees!')
  else:
    pass

  # time_string = '09:26:00' #HH:MM:SS, 24 hour clock, local time

  '''
  if (len(time_string) != 8):
    sys.exit("Enter time in the correct format. Don't forget to prefix zeros if needed!")
  else:
    pass

  hour = int(time_string[0:2])
  min = int(time_string[3:5])
  sec = int(time_string[6:8])

  time = hour + (min/60) + (sec/3600)
  '''

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

  psi_d = psi*180/np.pi

  # 4. Calculating temperature
  # Analytical Equation for the Dayside Temperature (from Hurley et al, 2015)

  T = (262*(np.sqrt(np.cos(psi)))) + 130
  # print('Temperature at', time_string, 'at a latitude of', lat, 'degrees is:', T, 'Kelvin')
  return [T, psi_d]

step_size_times_hrs = 2/60
times_start = 6 # Dawn
times_stop = 18 # Dusk
# Bear in mind that this entire plot is only for dayside temperatures.

lat_min = -90
lat_max = 90
lat_step = 0.5

num_steps_time = int(((times_stop - times_start)/step_size_times_hrs) + 1)
num_steps_lat = int(((lat_max - lat_min)/lat_step) + 1)
print("Matrix size: ", num_steps_lat, "x", num_steps_time)
print(" ")

Temps = np.ones((num_steps_lat, num_steps_time), float)

lat_count = 0
y_axis_qty = np.linspace(lat_min, lat_max, num_steps_lat)
x_axis_qty = np.linspace(times_start, times_stop, num_steps_time)

for latitudes in np.linspace(lat_min, lat_max, num_steps_lat):
  lat_count = lat_count + 1
  long_count = 0
  for times in np.linspace(times_start, times_stop, num_steps_time):
    long_count = long_count + 1
    Temps[lat_count-1, long_count-1] = SurfaceTemperature(latitudes, times)[0]


def cart2sph(x, y, z):
    dxy = np.sqrt(x**2 + y**2)
    r = np.sqrt(dxy**2 + z**2)
    theta = np.arctan2(y, x)
    phi = np.arctan2(z, dxy)
    theta, phi = np.rad2deg([theta, phi])
    return theta % 360, phi, r

def sph2cart(theta, phi, r=1):
    theta, phi = np.deg2rad([theta, phi])
    z = r * np.sin(phi)
    rcosphi = r * np.cos(phi)
    x = rcosphi * np.cos(theta)
    y = rcosphi * np.sin(theta)
    return x, y, z

# random data
pts = 1 - 2 * np.random.rand(500, 3)
l = np.sqrt(np.sum(pts**2, axis=1))
pts = pts / l[:, np.newaxis]
T = 150 * np.random.rand(500)

# naive IDW-like interpolation on regular grid
theta, phi, r = cart2sph(*pts.T)
nrows, ncols = (361,361)
lon, lat = np.meshgrid(np.linspace(0,360,ncols), np.linspace(-90,90,nrows))
xg,yg,zg = sph2cart(lon,lat)
Ti = np.zeros_like(lon)
for r in range(nrows):
    for c in range(ncols):
        v = np.array([xg[r,c], yg[r,c], zg[r,c]])
        angs = np.arccos(np.dot(pts, v))
        idx = np.where(angs == 0)[0]
        if idx.any():
            Ti[r,c] = T[idx[0]]
        else:
            idw = 1 / angs**2 / sum(1 / angs**2)
            Ti[r,c] = np.sum(T * idw)

# set up map projection
map = Basemap(projection='ortho', lat_0=30, lon_0=180)
# draw lat/lon grid lines every 30 degrees.
map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))
# compute native map projection coordinates of lat/lon grid.
x, y = map(lon, lat)
# contour data over the map.
cs = map.contourf(x, y, Temps, 15)
plt.title('Contours of T')
plt.show()


#plt.imshow(Temps, cmap='hot', interpolation='nearest')
#plt.show()

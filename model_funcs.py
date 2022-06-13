import numpy as np

SOLAR_CONSTANT = 1360 # W/m^2
SURFACE_AREA = .0008772 #m^2
CELL_EFFICIENCY = 0.25

# Assumptions:
    # Solar output is constant - real variance is ~.1% over 11 year cycles
    # Variance in moons distance to sun is negligable (constant 1 AU) - real daily variance is ~.5%, yearly ~3.5%
    # Solar panel power efficiency is not dependent on angle of incidence - not mentioned in datasheet
    # No effect on irradiance by moons atmosphere - atmosphere is practically non existant 
    # No irradiance on the dark side - if there was any it would be EXTREMELY small
def power(psi):
  return np.cos(psi) * SOLAR_CONSTANT * SURFACE_AREA * CELL_EFFICIENCY

# Analytical Equation for the Dayside Temperature (from Hurley et al, 2015)
def temp(psi):
  return (262*(np.sqrt(np.cos(psi)))) + 130
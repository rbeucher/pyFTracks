import numpy as np
import cython
import numpy as np
cimport numpy as np
from libc.math cimport fabs
from scipy import interpolate


cdef calculate_annealing_temperature(double abs_gradient):
    """ Calculate the annealing temperature based on absolute temperature gradient
        The total annealing temperature (TA) for F-apatite
        for a given heating or cooling rate (R) is given by the equation:
      
                          Ta = 377.67 * R**0.019837

        This is taken from Ketcham et al, 2005
    """ 
    return 377.67 * abs_gradient**0.019837


class ThermalHistory(object):
    """Class defining a thermal history"""

    def __init__(self, time, temperature, name="unknown"):
        """ 
         time: list of time points in Myr.
         temperature: list of temperature points in deg Kelvin.
         name: a name for the thermal-history.

        """

        time = np.array(time)
        temperature = np.array(temperature)

        # If time is not increasing, reverse arrays
        if not np.all(np.diff(time) > 0):
            time = time[::-1]
            temperature = temperature[::-1]

        if np.any(temperature < 273.15):
            print("It looks like you have entered temperature in Celsius...Converting temperature to Kelvin")
            temperature += 273.15  

        self.name = name
        self.input_time = time
        self.input_temperature = temperature

        self.time = self.input_time
        self.temperature = self.input_temperature

        self.maxT = max(temperature)
        self.minT = min(temperature)
        self.totaltime = max(time) - min(time)
        self.dTdt = np.diff(self.temperature) / np.diff(self.time)
        self.get_isothermal_intervals()

    def get_isothermal_intervals(self, max_temperature_per_step=8.0,
                                 max_temperature_step_near_ta=3.5):

        """
        Interpolate Time Temperature path
        Takes the time-temperature path specification and subdivides it for
        calculation in isothermal intervals. 
        
        Reference:
        
        Ketcham, R. A. (2005). Forward and Inverse Modeling of Low-Temperature
        Thermochronometry Data. Reviews in Mineralogy and Geochemistry, 58(1),
        275–314. doi:10.2138/rmg.2005.58.11
        
        It is calibrated to facilitate 0.5% accuracy for end-member F-apatite by
        having a maximum temperature step of 3.5 degrees C when the model temperature
        is within 10C of the total annealing temperature. Before this cutoff the
        maximum temperature step required is 8 C. If the overall model tine steps are
        too large, these more distant requirement may not be meet.
        
        Quoted text:
        
        "The more segments a time-temperature path is subdivided into, the more accurate
        the numerical solution will be. Conversely, an excessive number of time steps
        will slow computation down unnecessarily. The optimal time step size to achieve a desired
        solution accuracy was examined in detail by Issler (1996b), who demonstrated that time
        steps should be smaller as the total annealing temperature of apatite is approached.
        For the Ketcham et al. (1999) annealing model for F-apatite, Ketcham et al. (2000) found that 0.5%
        precision is assured if there is no step with greater than a 3.5 ºC change within 10 ºC of
        the F-apatite total annealing temperature."""

        cdef double[::1] time = np.ascontiguousarray(self.input_time)
        cdef double[::1] temperature = np.ascontiguousarray(self.input_temperature)
        cdef double[::1] new_time = np.ndarray((200))
        cdef double[::1] new_temperature = np.ndarray((200))
        cdef double cmax_temp_per_step = max_temperature_per_step
        cdef double cmax_temp_step_near_ta = max_temperature_step_near_ta
        cdef int nsegments = time.shape[0] - 1

        cdef int index, npoints
        cdef double seg, t, T, dT, dt, dTdt
        cdef double Ta, tend, fact

        t = time[0]
        T = temperature[0]

        new_time[0] = t
        new_temperature[0] = T

        npoints = 0

        for index in range(nsegments):
        
            dT = temperature[index + 1] - temperature[index]
            dt = time[index + 1] - time[index]
            seg = dT / dt
            
            # Calculate Annealing Temperature for Fluoro-Apatite.
            Ta = 377.67 * seg**(0.019837) if seg > 0.1 else 1000.
            tend = time[index + 1]
            fact = 1 if seg > 0 else -1
                    
            while t < tend:
                
                if fabs(seg) < 0.01:
                    dt = 1.0
                    dT = 0.0    
                else:  
                    dT = cmax_temp_per_step * fact
                    dt = dT / seg
        
                if fabs(tend - t) < dt:
                    dt = tend - t
                    dT = dt * seg
                            
                if fabs(Ta - (T + dT)) < 10.0:
                    dT = cmax_temp_step_near_ta * fact 
                    dt = dT / seg
                
                t += dt
                T += dT

                npoints = npoints + 1 
                new_time[npoints] = t
                new_temperature[npoints] = T

        self.time = np.array(new_time)[:npoints + 1]
        self.temperature = np.array(new_temperature)[:npoints + 1]

        self.time = self.time[::-1]
        self.temperature = self.temperature[::-1]

        return self.time, self.temperature

    def get_temperature_at_time(self, time):
        f = interpolate.interp1d(self.input_time, self.input_temperature) 
        return f(time)


# Some useful thermal histories
WOLF1 = ThermalHistory(
    name="wolf1",
    time=[0., 43., 44., 100.],
    temperature=[283.15, 283.15, 403.15, 403.15]
)

WOLF2 = ThermalHistory(
    name="wolf2",
    time=[0., 100.],
    temperature=[283.15, 403.15]
)

WOLF3 = ThermalHistory(
    name="wolf3",
    time=[0., 19., 19.5, 100.],
    temperature=[283.15, 283.15, 333.15, 333.15]
)

WOLF4 = ThermalHistory(
    name="wolf4",
    time=[0., 24., 76., 100.],
    temperature=[283.15, 333.15, 333.15, 373.15]
)

WOLF5 = ThermalHistory(
    name="wolf5",
    time=[0., 5., 100.],
    temperature=[283.15, 373.15, 291.15]
)


FLAXMANS1 = ThermalHistory(
    name="Flaxmans1",
    #time=[109.73154362416108, 95.97315436241611, 65.10067114093958, 42.95302013422818, 27.069351230425042, 0.223713646532417], 
    #temperature=[10.472716661803325, 50.21343115594648, 90.20426028596441, 104.6346242027596, 124.63170619867442, 125.47709366793116]
    time=[0., 27, 43, 65, 96, 110], 
    temperature=[398.15, 399.15, 378.15, 363.15, 323.15, 283.15]
)

VROLIJ = ThermalHistory(
    name="Vrolij",
    #time=[112.84098861592778, 108.92457659225633, 101.04350962294087, 95.96509833052357, 4.910255922414279, -0.196743768208961],
    #temperature=[10.036248368327097, 14.455174285000524, 14.971122078085369, 18.945174136102615, 11.984858737246478, 11.027412104738094]
    time=[0., 5., 96., 101, 109, 113],
    temperature=[284.15, 285.15, 292.15, 288.15, 287.15, 283.15]
)

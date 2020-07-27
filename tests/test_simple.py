import pyFTracks as FT
import pytest
import numpy as np


def test_thermal_history():
    thermal_history = FT.ThermalHistory(name="My Thermal History",
        time=[0., 43., 44., 100.],
        temperature=[283., 283., 403., 403.])
    assert(np.all(thermal_history.input_time == np.array([0.0, 43.0, 44.0, 100.0])))
    assert(np.all(thermal_history.input_temperature == np.array([283.0, 283.0, 403.0, 403.0])))

def test_get_isothermal_interval():
    thermal_history = FT.ThermalHistory(name="My Thermal History",
        time=[0., 43., 44., 100.],
        temperature=[283., 283., 403., 403.])
    assert(np.all(np.isclose(thermal_history.time, np.array([
        100., 99., 98., 97.,
        96., 95., 94., 93.,
        92., 91., 90., 89.,
        88., 87., 86., 85.,
        84., 83., 82., 81.,
        80., 79., 78., 77.,
        76., 75., 74., 73.,
        72., 71., 70., 69.,
        68., 67., 66., 65.,
        64., 63., 62., 61.,
        60., 59., 58., 57.,
        56., 55., 54., 53.,
        52., 51., 50., 49.,
        48., 47., 46., 45.,
        44., 43.93333333, 43.86666667, 43.8,
        43.73333333,  43.66666667, 43.6,  43.53333333,
        43.46666667,  43.4, 43.33333333, 43.26666667,
        43.2,  43.13333333, 43.06666667, 43.,
        42., 41., 40., 39.,
        38., 37., 36., 35.,
        34., 33., 32., 31.,
        30., 29., 28., 27.,
        26., 25., 24., 23.,
        22., 21., 20., 19.,
        18., 17., 16., 15.,
        14., 13., 12., 11.,
        10.,  9.,  8.,  7.,
         6.,  5.,  4.,  3.,
         2.,  1.,  0.]))))

def test_isothermal_max_temperature_wolfs():
    from pyFTracks.thermal_history import WOLF1, WOLF2, WOLF3, WOLF4, WOLF5
    thermal_histories = [WOLF1, WOLF2, WOLF3, WOLF4, WOLF5]
    for thermal_history in thermal_histories:
        assert(np.diff(thermal_history.temperature).max() <= 8.0)

def test_isothermal_max_temperature_wolfs2():
    from pyFTracks.thermal_history import WOLF1, WOLF2, WOLF3, WOLF4, WOLF5
    thermal_histories = [WOLF1, WOLF2, WOLF3, WOLF4, WOLF5]
    for thermal_history in thermal_histories:
        thermal_history.get_isothermal_intervals(max_temperature_per_step=3.0)
        assert(np.diff(thermal_history.temperature).max() <= 3.0)

def test_import_sample_datasets():
    from pyFTracks.ressources import Miller, Gleadow

def test_calculate_central_age():
    Ns = [31, 19, 56, 67, 88, 6, 18, 40, 36, 54, 35, 52, 51, 47, 27, 36, 64, 68, 61, 30]
    Ni = [41, 22, 63, 71, 90, 7, 14, 41, 49, 79, 52, 76, 74, 66, 39, 44, 86, 90, 91, 41]
    zeta = 350. # megayears * 1e6 * u.cm2
    zeta_err = 10. / 350.
    rhod = 1.304 # 1e6 * u.cm**-2
    rhod_err = 0.
    Nd = 2936
    data = FT.central_age(Ns, Ni, zeta, zeta_err, rhod, Nd)
    assert(data["Central"] == pytest.approx(175.5672, rel=1e-2))
    assert(data["se"] == pytest.approx(8.5101, rel=1e-2))

def test_calculate_pooled_age():
    Ns = [31, 19, 56, 67, 88, 6, 18, 40, 36, 54, 35, 52, 51, 47, 27, 36, 64, 68, 61, 30]
    Ni = [41, 22, 63, 71, 90, 7, 14, 41, 49, 79, 52, 76, 74, 66, 39, 44, 86, 90, 91, 41]
    zeta = 350. # megayears * 1e6 * u.cm2
    zeta_err = 10. / 350.
    rhod = 1.304 # 1e6 * u.cm**-2
    rhod_err = 0.
    Nd = 2936
    data = FT.pooled_age(Ns, Ni, zeta, zeta_err, rhod, Nd)
    assert(data["Pooled Age"] == pytest.approx(175.5672, rel=1e-2))
    assert(data["se"] == pytest.approx(9.8784, rel=1e-2))

def test_calculate_single_grain_ages():
    Ns = [31, 19, 56, 67, 88, 6, 18, 40, 36, 54, 35, 52, 51, 47, 27, 36, 64, 68, 61, 30]
    Ni = [41, 22, 63, 71, 90, 7, 14, 41, 49, 79, 52, 76, 74, 66, 39, 44, 86, 90, 91, 41]
    zeta = 350. # megayears * 1e6 * u.cm2
    zeta_err = 10. / 350.
    rhod = 1.304 # 1e6 * u.cm**-2
    rhod_err = 0.
    Nd = 2936
    data = FT.single_grain_ages(Ns, Ni, zeta, zeta_err, rhod, Nd)
    actual_values = np.array([170.27277726, 194.12922188, 199.71847392, 211.82501094,
        219.35417906, 192.69120201, 286.91906312, 218.87597033,
        165.51402406, 154.12751783, 151.7948727 , 154.27595627,
        155.38512454, 160.49155828, 156.07978109, 184.05633985,
        167.62488355, 170.15231471, 151.18251036, 164.84973261])
    actual_errors = np.array([ 40.93820562,  61.15626671,  37.30358567,  36.79102639,
         33.72043367, 107.40365187, 102.70782874,  49.20922289,
         36.7660512 ,  27.71454167,  33.5872093 ,  28.25634367,
         28.7686159 ,  31.11427488,  39.43447289,  41.83466447,
         28.25353735,  27.94537164,  25.54017193,  40.0012906 ])
    assert np.testing.assert_allclose(data["Age(s)"], actual_values, rtol=0.01) is None
    assert np.testing.assert_allclose(data["se(s)"], actual_errors, rtol=0.01) is None

def test_chi2_test():
    Ns = [31, 19, 56, 67, 88, 6, 18, 40, 36, 54, 35, 52, 51, 47, 27, 36, 64, 68, 61, 30]
    Ni = [41, 22, 63, 71, 90, 7, 14, 41, 49, 79, 52, 76, 74, 66, 39, 44, 86, 90, 91, 41]
    chi2 = FT.chi2_test(Ns, Ni)
    assert chi2 == pytest.approx(0.9292, rel=1e-3)

def test_ketcham_1999_Dpar_to_rmr0():
    from pyFTracks.annealing_model import Ketcham1999
    from pyFTracks.thermal_history import WOLF1
    model = Ketcham1999(WOLF1, kinetic_parameter=0.3, kinetic_parameter_type="ETCH_PIT_LENGTH")
    assert model.convert_Dpar_to_rmr0(1.0) == pytest.approx(0.84)
    assert model.convert_Dpar_to_rmr0(1.74) == pytest.approx(0.84)
    assert model.convert_Dpar_to_rmr0(5.0) == pytest.approx(0.)
    assert model.convert_Dpar_to_rmr0(2.1) == pytest.approx(0.79962206086744075)

def test_ketcham_1999_clapfu_to_rmr0():
    from pyFTracks.annealing_model import Ketcham1999
    from pyFTracks.thermal_history import WOLF1
    model = Ketcham1999(WOLF1, kinetic_parameter=0.3, kinetic_parameter_type="ETCH_PIT_LENGTH")
    assert(model.convert_Cl_pfu_to_rmr0(0.130), 0.)
    assert(model.convert_Cl_pfu_to_rmr0(0.7), 0.30169548259180623)
    assert(model.convert_Cl_pfu_to_rmr0(0.4), 0.6288689335789452)

def test_ohapfu_to_rmr0():
    from pyFTracks.annealing_model import Ketcham1999
    from pyFTracks.thermal_history import WOLF1
    model = Ketcham1999(WOLF1, kinetic_parameter=0.3, kinetic_parameter_type="ETCH_PIT_LENGTH")
    assert(model.convert_OH_pfu_to_rmr0(0.9), 0.)
    assert(model.convert_OH_pfu_to_rmr0(0.7), 0.30169548259180623)
    assert(model.convert_OH_pfu_to_rmr0(0.4), 0.6288689335789452)

#def test_miller_sample():
#    from pyFTracks.ressources import Miller
#    assert Miller.central_age == pytest.approx(175.5672, rel=0.001)
#    assert Miller.central_age_se == pytest.approx(8.51013)
#    assert Miller.central_age_sigma == pytest.approx(5.1978e-5, rel=1e-7)

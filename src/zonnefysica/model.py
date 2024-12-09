import numpy as np
from controller import data_A, data_B
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt



def fitscan(order_N, range_1_A, range_2_A, range_1_B, range_2_B):
    data_order_N_A = data_A(order_N)
    data_order_N_B = data_B(order_N)


    x_pixelvalues_A = np.arange(len(data_order_N_A[0]))
    tungstenflat_A = data_order_N_A[1]
    dark_A = data_order_N_A[3]
    flux_object_A = data_order_N_A[4]
    SNR_A = data_order_N_A[5]
    darkflat_A = data_order_N_A[6]


    tungstenflat_B = data_order_N_B[1]
    dark_B = data_order_N_B[3]
    flux_object_B = data_order_N_B[4]
    SNR_B = data_order_N_B[5]
    darkflat_B = data_order_N_B[6]

    if order_N == 3:
        wavelength_list =   [6677.2817,
                            6538.1120,
                            6583.9059, 
                            6604.8534,
                            6591.4845,
                            6588.5396,
                            6554.1603,
                            6577.2145,
                            6684.2930,
                            6666.3589,
                            6664.0510,
                            6662.2686,
                            6660.6762,
                            6643.6976]
        x_list =            [1752,
                            4656,
                            3748,                    
                            3319,
                            3594,
                            3654,
                            4343,
                            3883,
                            1592,
                            1997,
                            2048,
                            2088,
                            2124,
                            2496]
        uncertainty_x =     [0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5]
        #Polynomial fit for wavelength calibration
        fit_order = 4

    if order_N == 7:
        wavelength_list =   [5912.0853,
                            5914.7139,
                            5916.5992,
                            5928.8130  ,
                            5888.584,
                            5882.6242,
                            5885.7016,
                            5860.3102,
                            5834.2633,
                            5938.8252,
                            5908.9257,
                            5891.451,
                            ]
        x_list =            [3271,
                            3211,
                            3165,
                            2878,
                            3808,
                            3942,
                            3874,
                            4437,
                            5001,
                            2546,
                            3344,
                            3744,
                            ]
        uncertainty_x =     [0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            ]
        #Polynomial fit for wavelength calibration
        fit_order = 3

    if order_N == 13:
        wavelength_list =   [5162.2845,
                            5158.604,
                            5154.243,
                            5151.612,
                            5145.3082,
                            5141.7827,
                            5187.7462,
                            5177.6227,
                            5125.7654,
                            5115.0448,
                            5090.495,
                            5067.9737]
        x_list =            [1704,
                            1814,
                            1940,
                            2020,
                            2197,
                            2297,
                            938,
                            1248,
                            2745,
                            3039,
                            3696,
                            4279]
        uncertainty_x =     [0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5,
                            0.5]

        # Polynomial fit for wavelength calibration
        fit_order = 2


    #5 of hoger valt buiten 
    fit_1 = np.polynomial.polynomial.polyfit(x_list,wavelength_list,fit_order,w=uncertainty_x)

    # x & y coordinaten van de fit
    wavelength_object = []
    for x in x_pixelvalues_A:
        y = 0
        # Calculate y_coordinate
        for n in range(len(fit_1)):
            y += fit_1[n] * (x)**n       
        # Save coordinates
        wavelength_object.append(y)   

    fit_order_norm = 10
    fit_2_A = np.polynomial.polynomial.polyfit(wavelength_object,(flux_object_A-dark_A)/(tungstenflat_A-darkflat_A),fit_order_norm)

    # x & y coordinaten van de fit
    normalisation_fit_A= []
    for x in wavelength_object:
        y = 0
        # Calculate y_coordinate
        for n in range(len(fit_2_A)):
            y += (fit_2_A[n] * (x)**n) + 0.1
        # Save coordinates
        normalisation_fit_A.append(y)   

    fit_2_B = np.polynomial.polynomial.polyfit(wavelength_object,(flux_object_B-dark_B)/(tungstenflat_B-darkflat_B),fit_order_norm)

    # x & y coordinaten van de fit
    normalisation_fit_B= []
    for x in wavelength_object:
        y = 0
        # Calculate y_coordinate
        for n in range(len(fit_2_B)):
            y += (fit_2_B[n] * (x)**n) + 0.1
        # Save coordinates
        normalisation_fit_B.append(y)   

    flux_object_norm_A = (flux_object_A-dark_A)/((tungstenflat_A-darkflat_A)*normalisation_fit_A)
    flux_object_norm_B = (flux_object_B-dark_B)/((tungstenflat_B-darkflat_B)*normalisation_fit_B)

    fit_A_wavelength = []
    fit_A_intensity = []
    fit_B_wavelength = []
    fit_B_intensity = []
    fit_A_error = []
    fit_B_error = []

    for i in range(len(wavelength_object)):
        if range_1_A < wavelength_object[i] < range_2_A:
            fit_A_wavelength.append(wavelength_object[i])
            fit_A_intensity.append(flux_object_norm_A[i])
            fit_A_error.append(flux_object_norm_A[i]/SNR_A[i])

    for i in range(len(wavelength_object)):
        if range_1_B < wavelength_object[i] < range_2_B:
            fit_B_wavelength.append(wavelength_object[i])
            fit_B_intensity.append(flux_object_norm_B[i])
            fit_B_error.append(flux_object_norm_B[i]/SNR_B[i])

    def normal_distribution(x, std, avg, c):
        return -(np.e**(-(((x-avg)/std)**2)/2))/(std*np.sqrt(2*np.pi))+c

    popt_A, pcov_A = curve_fit(normal_distribution, fit_A_wavelength, fit_A_intensity, p0=[1, (range_1_A+range_2_A)/2, 1], sigma=fit_A_error)

    popt_B, pcov_B = curve_fit(normal_distribution, fit_B_wavelength, fit_B_intensity, p0=[1, (range_1_B+range_2_B)/2, 1], sigma=fit_B_error)

    return popt_A, pcov_A, popt_B, pcov_B, wavelength_object, flux_object_norm_A, flux_object_norm_B, SNR_A, SNR_B, fit_A_wavelength, fit_B_wavelength, normal_distribution


range_1_A = 6561.83 
range_2_A = 6563.63
range_1_B = 6561.89 
range_2_B = 6563.68 

popt_A, pcov_A, popt_B, pcov_B, wavelength_object, flux_object_norm_A, flux_object_norm_B, SNR_A, SNR_B, fit_A_wavelength, fit_B_wavelength, normal_distribution= fitscan(3, range_1_A, range_2_A, range_1_B, range_2_B)


def plot():

    plt.plot(wavelength_object, flux_object_norm_A, linewidth=1, label="Dataset A")
    plt.plot(wavelength_object, flux_object_norm_B, linewidth=1, label="Dataset B")


    plt.plot(wavelength_object, (normal_distribution(wavelength_object, popt_A[0], popt_A[1], popt_A[2])), label='Gaussian fitfunction')
    plt.plot(wavelength_object, (normal_distribution(wavelength_object, popt_B[0], popt_B[1], popt_B[2])), label='Gaussian fitfunction')


    plt.errorbar(wavelength_object, flux_object_norm_A, yerr=flux_object_norm_A/SNR_A, markersize='1', fmt='.', ecolor='red', elinewidth=0.5)
    plt.errorbar(wavelength_object, flux_object_norm_B, yerr=flux_object_norm_B/SNR_B, markersize='1', fmt='.', ecolor='red', elinewidth=0.5)
    plt.ylim(0,)
    plt.xlabel('Wavelength (Angstrom)')
    plt.ylabel("Normalized intensity")
    plt.xlim(range_1_A - 0.5, range_2_A + 0.5)
    plt.legend(loc=2, prop={'size': 6})
    plt.show()


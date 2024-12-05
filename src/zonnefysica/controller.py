import os

import numpy as np

main_folder_A = r'C:\Users\15172104\OneDrive - UvA\Natuur- & Sterrenkunde Bachelor\2e Jaar\NSP2 & ECPC\ECPC\zonnefysica-GUI\Flux_raw_sunLimbA\Flux_raw_sunLimbA'
main_folder_B = r'C:\Users\15172104\OneDrive - UvA\Natuur- & Sterrenkunde Bachelor\2e Jaar\NSP2 & ECPC\ECPC\zonnefysica-GUI\Flux_raw_sunLimbB\Flux_raw_sunLimbB'

def data_A(N_order):
    data_order_N_A = np.loadtxt(os.path.join(main_folder_A, "data_raw_order_{}.csv").format(N_order),  delimiter=',')
    return data_order_N_A

def data_B(N_order):
    data_order_N_B = np.loadtxt(os.path.join(main_folder_B, "data_raw_order_{}.csv").format(N_order),  delimiter=',')
    return data_order_N_B




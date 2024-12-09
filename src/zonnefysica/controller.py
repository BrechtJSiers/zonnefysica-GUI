import os

import numpy as np

pathnameA = r"C:\Users\15107469\OneDrive - UvA\ECPC\zonnefysicagui\Flux_raw_sunLimbA\Flux_raw_sunLimbA"
pathnameB = r"C:\Users\15107469\OneDrive - UvA\ECPC\zonnefysicagui\Flux_raw_sunLimbB\Flux_raw_sunLimbB"


class Controller:
    def __init__(self, pathnameA, pathnameB):
        self.main_folder_A = pathnameA
        self.main_folder_B = pathnameB

    def data_A(self, N_order):
        data_order_N_A = np.loadtxt(
            os.path.join(self.main_folder_A, "data_raw_order_{}.csv").format(N_order),
            delimiter=",",
        )
        return data_order_N_A

    def data_B(self, N_order):
        data_order_N_B = np.loadtxt(
            os.path.join(self.main_folder_B, "data_raw_order_{}.csv").format(N_order),
            delimiter=",",
        )
        return data_order_N_B

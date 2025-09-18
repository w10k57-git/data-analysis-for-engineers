import numpy as np
import pandas as pd


class Bolt:
    def __init__(self, designation: str, klasa: str, preload: float = 0.6) -> None:
        self.designation = designation
        self.klasa = klasa
        self.preload = preload

        self._load_data()
        self.Re, self.Rm = self._get_bolt_strength(klasa)

    def _load_data(self) -> None:
        bolts_df = pd.read_csv("data/bolts.csv", index_col="designation")
        self.dim = bolts_df.loc[self.designation]

        # Extract bolt dimensions using column names
        self.P = self.dim["p_mm"]
        self.d = self.dim["d_mm"]
        self.d2 = self.dim["d2_mm"]
        self.d1 = self.dim["d1_mm"]
        self.d3 = self.dim["d3_mm"]
        self.A = self.dim["A_mm2"]

    def _get_bolt_strength(self, klasa: str) -> tuple[float, float]:
        first_sign = int(klasa.split(".")[0])
        second_sign = int(klasa.split(".")[1])
        Re = first_sign * second_sign * 10
        Rm = second_sign * 100
        return Re, Rm

    def _calculate_axial_load(self) -> float:
        return round(self.preload * self.Re * self.A / 1000, 2)  # kN

    def get_axial_load(self) -> float:
        return self._calculate_axial_load()

    def calculate_torque(self, dm, mi=0.15):
        incl_angle = self.P / (np.pi * self.d2)
        friction_angle = np.arctan(mi)
        axial_load = self.get_axial_load()
        return round(axial_load / 2 * (self.d2 * np.tan(incl_angle + friction_angle) + dm * mi), 2)


def main():
    bolt1 = Bolt("M10", "8.8")
    dm = (24 + 13.5) / 2  # based on DIN125
    print(f"Axial load: {bolt1.get_axial_load()} kN")
    print(f"Torque: {bolt1.calculate_torque(dm)} Nm")


if __name__ == "__main__":
    main()

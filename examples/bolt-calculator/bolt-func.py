import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

BOLTS_PATH = "data/bolts.csv"


class Bolt(BaseModel):
    designation: str = Field(..., description='Bolt designation, e.g., "M10" or "M12x1.5"')
    klasa: str = Field("8.8", description='Bolt class, e.g., "8.8" or "10.9"')
    preload: float = Field(0.6, description="Preload factor (0 < preload <= 1)", gt=0, le=1)
    p: float
    d: float
    d2: float
    d1: float
    d3: float
    A: float


def get_bolt_data(designation: str) -> Bolt:
    bolts_df = pd.read_csv(BOLTS_PATH, index_col="designation")
    if designation not in bolts_df.index:
        raise ValueError(f"Designation {designation} not found in data.")
    return Bolt(
        designation=designation,
        p=bolts_df.loc[designation, "p_mm"],
        d=bolts_df.loc[designation, "d_mm"],
        d2=bolts_df.loc[designation, "d2_mm"],
        d1=bolts_df.loc[designation, "d1_mm"],
        d3=bolts_df.loc[designation, "d3_mm"],
        A=bolts_df.loc[designation, "A_mm2"],
    )


def calculate_axial_load(bolt: Bolt) -> float:
    first_sign = int(bolt.klasa.split(".")[0])
    second_sign = int(bolt.klasa.split(".")[1])
    Re = first_sign * second_sign * 10  # MPa
    return round(bolt.preload * Re * bolt.A / 1000, 2)  # kN


def calculate_torque(bolt: Bolt, dm: float, mi: float = 0.15) -> float:
    axial_load = calculate_axial_load(bolt)
    incl_angle = bolt.p / (np.pi * bolt.d2)
    friction_angle = np.arctan(mi)
    return round(axial_load / 2 * (bolt.d2 * np.tan(incl_angle + friction_angle) + dm * mi), 2)


if __name__ == "__main__":
    bolt1 = get_bolt_data("M10")
    dm = (24 + 13.5) / 2  # based on DIN125
    torque = calculate_torque(bolt1, dm)
    print(f"Calculated torque for {bolt1.designation}: {torque} Nm")

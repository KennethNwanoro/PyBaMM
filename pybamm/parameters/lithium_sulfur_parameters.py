#
# Standard parameters for lithium-sulfur battery models
#
import pybamm


class LithiumSulfurParameters:
    """
    Standard parameters for lithium-sulfur battery models

    Layout:
        1. Dimensional Parameters
        2. Dimensional Functions
        3. Scalings
        4. Dimensionless Parameters
        5. Dimensionless Functions
        6. Input Current

    """

    def __init__(self):

        # Physical constants
        self.R = pybamm.constants.R
        self.F = pybamm.constants.F
        self.T_ref = pybamm.Parameter("Reference temperature [K]")

        # Model-specific known parameters
        self.Ms = pybamm.Parameter("Molar mass of S8 [g.mol-1]")
        self.ns = pybamm.Parameter("Number of S atoms in S [atoms]")
        self.ns2 = pybamm.Parameter("Number of S atoms in S2 [atoms]")
        self.ns4 = pybamm.Parameter("Number of S atoms in S4 [atoms]")
        self.ns8 = pybamm.Parameter("Number of S atoms in S8 [atoms]")
        self.ne = pybamm.Parameter("Electron number per reaction [electrons]")
        self.ih0 = pybamm.Parameter("Exchange current density H [A.m-2]")
        self.il0 = pybamm.Parameter("Exchange current density L [A.m-2]")
        self.m_s = pybamm.Parameter("Mass of active sulfur per cell [g]")
        self.rho_s = pybamm.Parameter("Density of precipitated Sulfur [g.L-1]")
        self.EH0 = pybamm.Parameter("Standard Potential H [V]")
        self.EL0 = pybamm.Parameter("Standard Potential L [V]")

        self.voltage_low_cut_dimensional = pybamm.Parameter("Lower voltage cut-off [V]")
        self.voltage_high_cut_dimensional = pybamm.Parameter(
            "Upper voltage cut-off [V]"
        )
        self.n_cells = pybamm.Parameter(
            "Number of cells connected in series to make a battery"
        )

        # Model-specific unknown parameters
        self.v = pybamm.Parameter("Electrolyte volume per cell [L]")
        self.ar = pybamm.Parameter("Active reaction area per cell [m2]")
        self.k_p = pybamm.Parameter("Precipitation rate [s-1]")
        self.S_star = pybamm.Parameter("S saturation mass [g]")
        self.k_s_charge = pybamm.Parameter(
            "Shuttle rate coefficient during charge [s-1]"
        )
        self.k_s_discharge = pybamm.Parameter(
            "Shuttle rate coefficient during discharge [s-1]"
        )

        # Current
        # Note: pybamm.t is non-dimensional so we need to multiply by the model
        # timescale. Since the lithium-sulfur models are written in dimensional
        # form the timescale is just 1s.
        self.timescale = 1
        self.dimensional_current_with_time = pybamm.FunctionParameter(
            "Current function [A]", {"Time[s]": pybamm.t * self.timescale}
        )
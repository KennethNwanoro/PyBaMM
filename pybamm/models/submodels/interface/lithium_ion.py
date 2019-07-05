#
# Lithium-ion interface classes
#
import pybamm
from .base_interface import BaseInterface
from .kinetics import butler_volmer, inverse_butler_volmer


class BaseModel(BaseInterface, pybamm.lithium_ion.BaseModel):
    """
    Base lead-acid interface class

    Parameters
    ----------
    param :
        model parameters
    domain : str
        The domain to implement the model, either: 'Negative' or 'Positive'.


    **Extends:** :class:`pybamm.interface.inverse_butler_volmer.BaseModel`
    and :class:`pybamm.lithium_ion.BaseModel`
    """

    def __init__(self, param, domain):
        super().__init__(param, domain)

    def _get_exchange_current_density(self, variables):
        """
        A private function to obtain the exchange current density for a lead acid
        deposition reaction.

        Parameters
        ----------
        variables: dict
        `   The variables in the full model.

        Returns
        -------
        j0 : :class: `pybamm.Symbol`
            The exchange current density.
        """
        c_s_surf = variables[self.domain + " particle surface concentration"]
        c_e = variables[self.domain + " electrolyte concentration"]

        if self.domain == "Negative":
            prefactor = 1 / self.param.C_r_n

        elif self.domain == "Positive":
            prefactor = self.param.gamma_p / self.param.C_r_p

        j0 = prefactor * (
            c_e ** (1 / 2) * c_s_surf ** (1 / 2) * (1 - c_s_surf) ** (1 / 2)
        )

        return j0

    def _get_standard_ocp_variables(self, variables):
        c_s_surf = variables[self.domain + " particle surface concentration"]
        # c_s_surf = pybamm.surf(c_s, set_domain=True)

        if self.domain == "Negative":
            ocp = self.param.U_n(c_s_surf)
            ocp_dim = self.param.U_n_ref + self.param.potential_scale * ocp
            dudT = self.param.dUdT_n(c_s_surf)

        elif self.domain == "Positive":
            ocp = self.param.U_p(c_s_surf)
            ocp_dim = self.param.U_p_ref + self.param.potential_scale * ocp
            dudT = self.param.dUdT_p(c_s_surf)

        ocp_av = pybamm.average(ocp)
        ocp_av_dim = pybamm.average(ocp_dim)
        dudT_av = pybamm.average(dudT)

        return {
            self.domain + " electrode open circuit potential": ocp,
            self.domain + " electrode open circuit potential [V]": ocp_dim,
            "Average "
            + self.domain.lower()
            + " electrode open circuit potential": ocp_av,
            "Average "
            + self.domain.lower()
            + " electrode open circuit potential [V]": ocp_av_dim,
            self.domain + " electrode entropic change": dudT,
            "Average " + self.domain.lower() + " electrode entropic change": dudT_av,
        }


class ButlerVolmer(BaseModel, butler_volmer.BaseButlerVolmer):
    def __init__(self, param, domain):
        super().__init__(param, domain)


class InverseButlerVolmer(BaseModel, inverse_butler_volmer.BaseModel):
    def __init__(self, param, domain):
        super().__init__(param, domain)

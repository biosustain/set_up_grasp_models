import os

import pandas as pd
from set_up_grasp_models.check_models.format_checks import check_met_rxn_order, check_kinetics_met_separators, \
    check_rxn_mechanism_order, check_kinetics_subs_prod_order
from set_up_grasp_models.check_models.thermodynamics_checks import check_thermodynamic_feasibility
from set_up_grasp_models.check_models.mass_balance_checks import check_flux_balance, check_balanced_metabolites


# import the model
file_in = os.path.join('models', 'HMP2360_r0_t0.xlsx')
data_dict = pd.read_excel(file_in, sheet_name=None)


# check metabolite lists separators in kinetics sheet
check_kinetics_met_separators(data_dict)

# check if the order of metabolites and reactions in all excel sheets is correct
check_met_rxn_order(data_dict)

# check consistency between stoic sheet and mets sheet, take the results with a grain of salt
check_balanced_metabolites(data_dict)

# check if fluxes and Gibbs energies are compatible
check_thermodynamic_feasibility(data_dict)

# check if all metabolites marked as balanced are indeed mass balance, only works if fluxes for all reactions are
# either specified or can be calculated
check_flux_balance(data_dict)

# checks if the enzymatic mechanisms come before massAction, freeExchange, fixedExchange, diffusion and if
#  is the very last one fixedExchange
check_rxn_mechanism_order(data_dict)

# checks if the metabolite names in the substrate and product order columns in the kinetics sheet are valid,
#  i.e., if they exist in the mets sheet
check_kinetics_subs_prod_order(data_dict)

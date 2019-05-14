.. set_up_grasp_models documentation master file, created by
   sphinx-quickstart on Tue May  7 16:49:18 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to set_up_grasp_models's documentation!
===============================================


This small package allows the user to both set up GRASP input model files and to check if they are valid.
At this point only the checks are fully working. These include:

 - format checks:
    - check if the order of reactions and metabolites is the same in all excel sheets and consistent with the order in the stoic sheet;
    - in the kinetics sheet check all cells that can contain lists of values to make sure these values are not separated by comma, semi-colon or dot (they should be separated by a space).
 - mass balance checks:
    - a basic check: checks if metabolites that are either only consumed or only produced in the stoichiometric matrix are marked as not balanced and maybe constant. Also checks if metabolites that are both consumed and produced in the stoichiometric matrix are marked as balanced and maybe not constant. The result of this check should be taken with a grain of salt, as it might identify false issues, to get a more accurate result reaction fluxes are needed.
    - a more accurate check: if fluxes are provided for all reactions in measRates, checks if all metabolites are mass balanced.
 - thermodynamics_checks:
    - if all fluxes in the model are specified or enough are specified such that the remaining can be determined by solving :math:`S_ {unknown} * v_{unknown} = S_{known} * v_{known}`, it checks if the fluxes are compatible with the Gibbs free energies.

For more details on the functions and arguments go to the respective pages using the sidebar.


.. toctree::
   :maxdepth: 2

   check_models
   io
   model
   set_up_models





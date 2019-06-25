Check GRASP models
===================


Format checks
---------------------

These checks mostly check if the file syntax is valid.

**Check the order of reactions and metabolites**

Checks if the order of metabolites and reactions in all excel sheets is consistent with the order in the ``stoic`` sheet.

.. code-block:: python

    from set_up_grasp_models.check_models.format_checks import check_met_rxn_order

    model_name = 'glycolysis_v3'
    file_in = os.path.join('example_files', 'output', model_name + '.xlsx')
    data_dict = pd.read_excel(file_in, sheet_name=None)


    # check if the order of metabolites and reactions in all excel sheets is consistent
    check_met_rxn_order(data_dict)


**Check list separators in the kinetics sheet**

Checks if metabolite lists are separated by commas, semi-colons, or dots. These should be separated by a single space.

.. code-block:: python

    from set_up_grasp_models.check_models.format_checks import check_kinetics_met_separators

    model_name = 'glycolysis_v3'
    file_in = os.path.join('example_files', 'output', model_name + '.xlsx')
    data_dict = pd.read_excel(file_in, sheet_name=None)

    # check metabolite lists separators in kinetics sheet
    check_kinetics_met_separators(data_dict)


**Check substrate order and product order columns in the kinetics sheet**

Checks if the metabolites specified in ``the substrate order`` and ``product order`` columns are indeed substrates/products of the respective reaction. Metabolites marked as not active in the ``mets`` sheet are not considered.

.. code-block:: python

    from set_up_grasp_models.check_models.format_checks import check_kinetics_subs_prod_order

    model_name = 'glycolysis_v3'
    file_in = os.path.join('example_files', 'output', model_name + '.xlsx')
    data_dict = pd.read_excel(file_in, sheet_name=None)

    # checks if metabolite names in subtrate/product order columns are indeed
    #  substrates/products of the respective reaction
    check_kinetics_subs_prod_order(data_dict)



**Checks if reactions with enzymatic mechanisms come before reaction with non-enzymatic mechanisms**

In particular it checks if reactions with ``fixedExchange`` mechanisms are the last ones and reactions with ``massAction``, ``freeExchange``, and ``diffusion`` come after reactions with enzymatic mechanisms (e.g. ``orderedBiBi``) and before ``fixedExchange``.

.. code-block:: python

    from set_up_grasp_models.check_models.format_checks import check_rxn_mechanism_order

    model_name = 'glycolysis_v3'
    file_in = os.path.join('example_files', 'output', model_name + '.xlsx')
    data_dict = pd.read_excel(file_in, sheet_name=None)

    # checks if massAction/diffusion/freeExchange mechanism come after other enzyme
    #  mechanisms and fixedExchange comes at the end
    check_rxn_mechanism_order(data_dict)




Thermodynamic feasibility checks
----------------------------------

This check checks thermodynamic feasibility, i.e. consistency between Gibbs free energies and fluxes.

**Check if Gibbs energies and fluxes are compatible**

Checks if the mean flux for each reaction is compatible with the respective Gibbs free energy range.

If not all fluxes are defined in the `measRates` sheet, but enough fluxes are defined it calculates the remaining fluxes by solving :math:`S_ {unknown} * v_{unknown} = S_{known} * v_{known}`.


.. code-block:: python

    from set_up_grasp_models.check_models.thermodynamics_checks import check_thermodynamic_feasibility

    model_name = 'glycolysis_v3'
    file_in = os.path.join('example_files', 'output', model_name + '.xlsx')
    data_dict = pd.read_excel(file_in, sheet_name=None)

    # checks if massAction/diffusion/freeExchange mechanism come after other enzyme
    #  mechanisms and fixedExchange comes at the end
    flag, flux_df, dG_df = check_thermodynamic_feasibility(data_dict)






Mass balance checks
---------------------

These checks check metabolite mass balance.


**Check if metabolites are balanced based on stoichiometric matrix only**

Goes through the stoichiometric matrix and checks:

 - if a metabolite is both consumed and produced and if so, whether or not it is marked as *balanced* in the ``mets`` sheet;
 - if a metabolite is only consumed and produced and if so, whether or not it is marked as *balanced* and *fixed*  in the ``mets`` sheet;

The idea is that if a met is only consumed or produced it should be marked as *unbalanced* and *fixed* and if it is both consumed and produced it might actually be balanced. However, in the latter case it is possible to have many false positives, since having a metabolite that is both consumed and produced doesn't mean it is mass balanced. To decide that flux data is needed.

.. code-block:: python

    from set_up_grasp_models.check_models.mass_balance_checks import check_balanced_metabolites

    model_name = 'glycolysis_v3'
    file_in = os.path.join('example_files', 'output', model_name + '.xlsx')
    data_dict = pd.read_excel(file_in, sheet_name=None)

    # check consistency between stoic sheet and mets sheet
    check_balanced_metabolites(data_dict)



**Check if metabolites are mass balanced based on reaction fluxes**

If all reactions fluxes are defined in the ``measRates`` sheet, checks if all metabolites are mass balanced.

If enough fluxes are defined it calculates the remaining fluxes by solving :math:`S_ {unknown} * v_{unknown} = S_{known} * v_{known}`, and checks if all metabolites are mass balanced.

.. code-block:: python

    from set_up_grasp_models.check_models.mass_balance_checks import check_flux_balance

    model_name = 'glycolysis_v3'
    file_in = os.path.join('example_files', 'output', model_name + '.xlsx')
    data_dict = pd.read_excel(file_in, sheet_name=None)

    # check if all metabolites marked as balanced are indeed mass balanced
    check_flux_balance(data_dict)



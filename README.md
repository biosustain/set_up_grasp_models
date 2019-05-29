[![Build Status](https://travis-ci.com/biosustain/set_up_grasp_models.svg?branch=master)](https://travis-ci.com/biosustain/set_up_grasp_models)
[![Coverage Status](https://coveralls.io/repos/github/biosustain/set_up_grasp_models/badge.svg?branch=master)](https://coveralls.io/github/biosustain/set_up_grasp_models?branch=master)


# set_up_grasp_models

This small package is intended to generate GRASP input model files in a fairly automatic way, and check that these are valid.
At this point both the model checks and the mechanism generation are working fully, but not the actual process of building the input excel file.


### Model checks
 - `check_met_rxn_order`: checks if the order of reactions and metabolites in all sheets is consistent with the order in the stoichiometry matrix.
 - `check_kinetics_met_separators`: in the kinetics sheet for columns where cells can have multiple values, makes sure these values are not separated by a comma, semi-colon, or dot.
 - `check_balanced_metabolites`: checks if metabolites that are both consumed and produced in the stoichiometric matrix are marked as balanced and the other way around. Checking for mass balances is more accurate though.
 - `check_flux_balance`:  when all fluxes are specified in the measRates sheet, check if all metabolites are mass balanced (well, the ones that are marked as balanced in the mets sheet).
 - `check_thermodynamic_feasibility`: given a dictionary representing a GRASP input file, it checks if the reaction's dG are compatible with the respective fluxes. It works both when all fluxes are specified in measRates and when robust fluxes are calculated for a fully determined system. If the fluxes are not fully specified not the system is fully determined, it doesn't work.
 - `check_rxn_mechanism_order`: given a dictionary representing a GRASP input file, checks if the order of kinetic mechanisms in the kinetics sheet is correct, i.e. massAction, diffusion, freeExchange, and fixedExchange mechanisms come after enzymatic mechanisms and also if fixedExchange mechanisms are the very last ones. 
 
For an example on how to use these check the file `check_input_model.py` in the examples folder.

### Mechanism generation

Created a function `convert_er_mech_to_grasp_pattern` to convert an enzyme mechanism given in terms of elementary reactions (as in the [MASS-toolbox](http://opencobra.github.io/MASS-Toolbox/)) to the pattern file that GRASP takes as input.

As an example, the enzyme mechanism given in terms of elementary reactions for an orderedBiBi mechanism with competitive inhibiting with respect to the first substrate should look like:

```
E_c + accoa_c <-> E_c&accoa_c
E_c + pyr_c <-> E_c&pyr_c
E_c&accoa_c + srtn_c <-> E_c&accoa_c&srnt_c
E_c&accoa_c&srnt_c <-> E_c&coa_c&nactsrtn_c
E_c&coa_c&nactsrtn_c <-> E_c&coa_c + nactsrtn_c
E_c&coa_c <-> E_c + coa_c
```

The main rules here are: 
 - enzymes must start with `E_`;
 - reactions must be reversible and the conversion sign is `<->`;
 - each elementary reaction must be written in a new line.
 
For an example check the examples folder, script `convert_mechanism.py`.

Mechanisms currently tested:
 - orderedBiBi with and without all sorts of inhibitions and activations;
 - orderedUniBi;
 - randomUniBi;
 - randomBiBi with and without competitive inhibition;
 - pingPongBiBi;
 - promiscuous reactions up to a point.

For more details check the mechanism in the folder `tests/test_files/test_set_up_models/convert_mechanism`
 
***Always double check the resulting pattern file!***


### Getting standard Gibbs energies from [eQuilibrator](http://equilibrator.weizmann.ac.il)

Created a function `get_DGs` which, given a list of reaction strings in the form `['R_FBA: m_g3p_c + m_dhap_c <-> m_fdp_c', 'R_ENO: m_2pg_c <-> m_pep_c']` and a file with a mapping between bigg and kegg ids, returns the standard gibbs energy and respective uncertainty for each reaction.

In the folder data you can also find the file with a mapping between bigg and kegg ids named `map_bigg_to_kegg_ids.csv`.

For an example check `get_dGs.py` in the examples folder.


## Documentation

The documentation for the API can be found at [https://set-up-grasp-models.readthedocs.io/](https://set-up-grasp-models.readthedocs.io/).

There are also a couple of examples in the `examples` folder.
The jupyter lab example requires (besides jupyter lab or notebook) altair v2, altair v3 will probably not work. 

## Installation

To install simply go to the folder and do:

```pip install .```


## Requirements

#### For users
 - Python 3.6+
 - numpy==1.16.2
 - pandas==0.24.2
 - xlrd==1.2.0

While almost any version of numpy and XlsxWriter should work, the same might not be true for pandas.  

If you use this package to get Gibbs energies from equilibrator you will also need to install equilibrator-api v0.1.26 with `pip install equilibrator-api==0.1.26`.


#### Requirements files:
 - `requirements.txt` for users to install using pip.
 - `requirements_dev.txt` for developers to install using pip.
 - `environment_dev.yml` for developers using conda.
 

#### How to get Python 3.6+
If you don't have Python 3.6 or higher in your system, the best way to get it is either using pyenv or conda.
 
With conda you can create a virtual environment with a specific python version. To do so start by installing miniconda if you don't have any sort of conda installed yet, and then create a virtual environment using a specific version of python:

``` conda create -n virtual_env_name python=3.7```

To activate the virtual environment do

``` source activate virtual_env_ńame```

To install packages use either pip or conda: 

``` conda/pip install package_name ```

Alternatively, just use the `environment_dev.yml` file to create a conda environment with the right version of python and packages:

```conda env create -f environment_dev.yml```

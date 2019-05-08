# set_up_grasp_models

This small package is intended to generate GRASP input model files in a fairly automatic way, and check that these are valid.
At this point only the model checks are working fully, though.


### Model checks
 - `check_met_rxn_order`: checks if the order of reactions and metabolites in all sheets is consistent with the order in the stoichiometry matrix.
 - `check_kinetics_met_separators`: in the kinetics sheet for columns where cells can have multiple values, makes sure these values are not separated by a comma, semi-colon, or dot.
 - `check_balanced_metabolites`: checks if metabolites that are both consumed and produced in the stoichiometric matrix are marked as balanced and the other way around. Checking for mass balances is more accurate though.
 - `check_flux_balance`:  when all fluxes are specified in the measRates sheet, check if all metabolites are mass balanced (well, the ones that are marked as balanced in the mets sheet).
 - `check_thermodynamic_feasibility`: given a dictionary representing a GRASP input file, it checks if the reaction's dG are compatible with the respective fluxes. It works both when all fluxes are specified in measRates and when robust fluxes are calculated for a fully determined system. If the fluxes are not fully specified not the system is fully determined, it doesn't work.
 

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
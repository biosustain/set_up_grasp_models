# set_up_grasp_models

This small package is intended to generate GRASP input model files in a fairly automatic way and check that these are valid.

[![Build Status](https://travis-ci.com/biosustain/set_up_grasp_models.svg?branch=master)](https://travis-ci.com/biosustain/set_up_grasp_models)
[![Coverage Status](https://coveralls.io/repos/github/biosustain/set_up_grasp_models/badge.svg?branch=master)](https://coveralls.io/github/biosustain/set_up_grasp_models?branch=master)


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)



Introduction
------------

The idea behind this project is to help us create and validate input excel files for our GRASP in a way that it won't complain or produce wrong results without complaining.

To accomplish this, the package is divided into two main parts:
 - set_up_models to actually generate the excel files;
 - check_models to validate existing excel files.

Besides these, there are a few more functions that allows the user to:
 - change reaction order;
 - generate GRASP pattern files from mechanisms written in terms of elementary reactions;
 - remove all leading and trailing spaces from strings;
 - convert kinetic model's matlab file into a format that can be used for ODE simulation by Matlab.
 
The documentation can be found at [https://set-up-grasp-models.readthedocs.io/](https://set-up-grasp-models.readthedocs.io/).

Examples can be found in the `examples` folder, including a comprehensive jupyter notebook.



Installation
-------------


To install go to the main folder and do:

```pip install .```


## Requirements

#### For users
 - Python 3.6+
 - numpy==1.16.2
 - pandas==0.24.2
 - XlsxWriter==1.1.7
 - equilibrator-api==0.2.1b1

While almost any version of numpy and XlsxWriter should work, the same might not be true for pandas, and certainly is not for equilibrator-api.  


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


Usage
-----

#### Generate GRASP models


To generate GRASP input excel files from a plaintext file containing the model reactions and a base GRASP file:

```python
from set_up_grasp_models.set_up_models.set_up_model import set_up_model
import os

# file with model reactions
file_in_stoic = os.path.join('example_files', 'glycolysis_example.txt')
# GRASP input file with general sheet
base_excel_file = os.path.join('..', 'base_files', 'GRASP_general.xlsx')

# define metabolomics input file
file_in_mets_conc = os.path.join('example_files', 'met_concs.xlsx')

# define model name
model_name = 'glycolysis_v1'
# define output file
file_out = os.path.join('example_files', 'output', model_name + '.xlsx')

# generate model
set_up_model(model_name, file_in_stoic, base_excel_file, file_out,
            use_equilibrator=True, # optional
            file_in_mets_conc=file_in_mets_conc) #optional
```

The reactions defined in the plaintext file should look like:

```
R_PGM: m_3pg_c <-> m_2pg_c
R_ENO: m_2pg_c <-> m_pep_c + 1.0 m_h2o_c
R_PYK: m_adp_c + m_pep_c <-> m_atp_c + 1 m_pyr_c
```

Where reaction names should be preceeded by ``R_`` and metabolite names by ``m_``, and BiGG IDs should be used as much as possible.

The standard Gibbs energies of reaction can be obtained from equilibrator by setting `use_equilibrator=True`, this is optional.

The `thermoMets` and `metsData` sheets can be filled in if an excel file in long data format is provided with metabolite concentrations (`file_in_mets_conc`).

If there is already a model and you only want to add/remove reactions, you can provide the existing model as `base_excel_file` and the new model will contain the relevant data  defined in `base_excel_file`. 


#### Check if a model is valid

To check if a GRASP input excel file is valid:

```python
from set_up_grasp_models.check_models.format_checks import check_met_rxn_order, check_kinetics_met_separators, \
    check_kinetics_subs_prod_order, check_rxn_mechanism_order
from set_up_grasp_models.check_models.thermodynamics_checks import check_thermodynamic_feasibility
from set_up_grasp_models.check_models.mass_balance_checks import check_flux_balance, check_balanced_metabolites
import os
import pandas as pd

model_name = 'glycolysis_v3'
file_in = os.path.join('example_files', 'output', model_name + '.xlsx')
data_dict = pd.read_excel(file_in, sheet_name=None)


# check if the order of metabolites and reactions in all excel sheets is consistent
check_met_rxn_order(data_dict)

# check metabolite lists separators in kinetics sheet
check_kinetics_met_separators(data_dict)

# checks if metabolite names in subtrate/product order columns are indeed substrates/products of the respective reaction
check_kinetics_subs_prod_order(data_dict)

# checks if massAction/diffusion/freeExchange mechanism come after other enzyme mechanisms and fixedExchange comes at the end
check_rxn_mechanism_order(data_dict)


# check if fluxes and Gibbs energies are compatible
check_thermodynamic_feasibility(data_dict)

# check consistency between stoic sheet and mets sheet, take the results with a grain of salt, there are false positives
check_balanced_metabolites(data_dict)


# check if all metabolites marked as balanced are indeed mass balance, only works if fluxes for all reactions are
# either specified or can be calculated
check_flux_balance(data_dict)

```


To run the above tests it is important that the columns in each sheet have certain names. 

If you didn't use `set_up_model` to build your model, it is highly likely that the columns don't have the expected names. To rename them using the expected names, just run `rename_columns()` as follows:


```python
import os
import pandas as pd

from set_up_grasp_models.set_up_models.manipulate_model import rename_columns


# path to current model
model_name = 'glycolysis_v2'
file_in = os.path.join('example_files', 'output', model_name + '.xlsx')

# import current model with pandas
data_dict = pd.read_excel(file_in, sheet_name=None, index_col=0)

# path to the model with re-ordered reactions - just substitute current one
file_out = file_in

# remove any leading or trailing spaces in all string cells
rename_columns(data_dict, file_out)
```



Known issues and limitations
------------------------------

It is possible that even after running all the model checks GRASP still complains about the input file, in that case please file a new issue.

Also the model checks are likely to give you false positives, in the sense that they will say something is wrong when in fact it isn't, be critical :)


**Altair**

If using altair v3.0.0, you might get the following output when trying to visualize Gibbs energies and reactions fluxes:

```
<VegaLite 3 object>

If you see this message, it means the renderer has not been properly enabled
for the frontend that you are using. For more information, see
https://altair-viz.github.io/user_guide/troubleshooting.html
```

In that case either follow the advice on [https://altair-viz.github.io/user_guide/troubleshooting.html](https://altair-viz.github.io/user_guide/troubleshooting.html) or downgrade to altair v2.0.0.


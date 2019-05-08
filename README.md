# set_up_grasp_models

This small package is intended to generate GRASP input model files in a fairly automatic way, and check that these are valid.
At this point only the model checks are working fully, though.


## Documentation

The documentation for the package can be found at [https://set-up-grasp-models.readthedocs.io/](https://set-up-grasp-models.readthedocs.io/).

## Requirements

#### For users
 - Python 3.6+
 - numpy==1.16.2
 - pandas==0.24.2
 - XlsxWriter==1.1.7

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
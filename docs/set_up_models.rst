Set up GRASP models
=========================

This subpackage generates GRASP input excel files in a fairly automatic way. From here on i'll refer to these files as models.

Models can be generated either from scratch or from an existing model.


Generate a model from scratch
----------------------------------------------

To generate a model from scratch only a plaintext file with the model reactions and a base excel file that contains the `general` sheet. The latter can be found in the package's folder `base_files`.


.. code-block:: python

    from set_up_grasp_models.set_up_models.set_up_model import set_up_model

    # plaintext file with model reactions
    file_in_stoic = os.path.join('example_files', 'glycolysis_example.txt')
    # GRASP input file with general sheet
    base_excel_file = os.path.join('..', 'base_files', 'GRASP_general.xlsx')

    # define model name
    model_name = 'glycolysis_v1'
    # define output file
    file_out = os.path.join('example_files', 'output', model_name + '.xlsx')

    # generate model
    set_up_model(model_name, file_in_stoic, base_excel_file, file_out)


The plaintext file with the model reactions should look like the following:
::

 R_PGM: m_3pg_c <-> m_2pg_c
 R_ENO: m_2pg_c <-> m_pep_c + 1.0 m_h2o_c
 R_PYK: m_adp_c + m_pep_c <-> m_atp_c + 1 m_pyr_c


Where reaction names should be preceeded by ``R_`` and metabolite names by ``m_``.
BiGG IDs should be used as much as possible.

From this input, the ``general`` and ``stoic`` sheets will be properly filled in, while all the other excel sheets will be filled with default values that must be manually changed.



Gibbs energies
""""""""""""""""""""""""""

Optionally, one can also fill in the ``thermoRxns`` sheet with standard Gibbs energies by specifying the argument ``use_equilibrator=True``.


.. code-block:: python

    set_up_model(model_name, file_in_stoic, base_excel_file, file_out,
                 use_equilibrator=True)

If you decide to use this feature, it is very important that all metabolite IDs are BiGG IDs.


Metabolite concentrations
""""""""""""""""""""""""""

To fill in the ``thermoMets`` and ``metsData`` sheets, you can provide an excel file with metabolite concentrations in long format (for long vs. wide data format see _here: https://sejdemyr.github.io/r-tutorials/basics/wide-and-long/).
Columns must have metabolite IDs, which should be consistent witt the metabolite IDs used so far, and there must be two rows named ``average`` and ``stdev``.


.. code-block:: python

    # define metabolomics input file
    file_in_mets_conc = os.path.join('example_files', 'met_concs.xlsx')

    # generate model
    set_up_model(model_name, file_in_stoic, base_excel_file, file_out,
                 use_equilibrator=True,
                 file_in_mets_conc=file_in_mets_conc)


Generate a model from an existing model
-----------------------------------------------

If you already have a model and want to, for instance, remove or add reactions but keep all the info related to reactions included in the existing model vs. having to fill in all reactions/metabolites info again, all you need to do is to provide the existing model as ``base_excel_file``:

.. code-block:: python

    # GRASP input file with general sheet
    base_excel_file = os.path.join('example_files', 'model_v2.3.xlsx')

    # generate model
    set_up_model(model_name, file_in_stoic, base_excel_file, file_out)

If ``use_equilibrator=True`` is specified, the eQuilibrator Gibbs energies will overwrite the values from ``thermoRxns`` in ``base_excel_file``.
Likewise, if ``file_in_mets_conc`` is specified, the concentrations specified in that file will overwrite the values  from ``thermoMets`` and ``metsData`` in ``base_excel_file``.


Generating mechanism GRASP patterns
-----------------------------------------------

Finally, it is now possible to generate GRASP pattern files, which are used to generate reactions' rate laws.

As an example, a GRASP pattern file for a uni uni  mechanism looks like this:
::

    1 2 k01.*A
    2 1 k02
    2 3 k03
    3 2 k04
    3 1 k05
    1 3 k06.*P

Now, these mechanisms can be specified in terms of elementary reactions and automatically converted to a GRASP pattern:


.. code-block:: python

    from set_up_grasp_models.set_up_models.convert_mechanisms import convert_er_mech_to_grasp_pattern

    # path to file with mechanism defined in terms of elementary reactions
    file_in = os.path.join('mechanisms', 'uniUni_mech_er.txt')

    # path to file with output GRASP pattern
    file_out = os.path.join('mechanisms', 'uniUni.txt')

    convert_er_mech_to_grasp_pattern(file_in, file_out)

Where the mechanism defined in terms of elementary reactions for a uni uni mechanism looks like this:
::

    E_c + m_3pg_c <-> E_c&m_3pg_c
    E_c&m_3pg_c <-> E_c&m_2pg_c
    E_c&m_2pg_c <-> E_c + m_2pg_c

The key constraints to specifying a mechanism in terms of elementary reactions are:

 - enzymes must start with ``E_``;
 - reactions must be reversible and the conversion sign is ``<->``;
 - each elementary reaction must be written in a new line.

**Always double check the resulting pattern file!**

Generate GRASP pattern files from model
""""""""""""""""""""""""""""""""""""""""

It is also possible to automatically generate GRASP pattern files for the mechanisms specified in the model's ``kinetics`` sheet, given a folder with mechanisms specified in terms of elementary reactions.


.. code-block:: python

    # define model name
    model_name = 'glycolysis_v2'
    # define input file
    file_in_model = os.path.join('example_files', 'output', model_name + '.xlsx')

    # define path to folder with elementary reaction mechanisms
    mech_in_dir = os.path.join('example_files', 'mechanisms')

    # define path to folder where the pattern files will be generated
    pattern_out_dir = os.path.join('/home', 'mrama', 'GRASP_test', 'GRASP', 'patterns')

    generate_mechanisms(file_in_model, mech_in_dir, pattern_out_dir)


Here, ``generate_mechanisms`` will go through the ``mechanism`` column in the ``kinetics`` sheet and check if a file with the same name exists in the patterns folder (``pattern_out_dir``), if not it will check if a file with the same name exists in the mechanisms folder (``mech_in_dir``), if so it will convert it to a GRASP pattern and write it to the patterns folder.
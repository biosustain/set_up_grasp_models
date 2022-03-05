Misc
===================


Reorder model reactions
-------------------------

By providing a list with the new reaction order, you can re-order the reactions in all model sheets.

.. code-block:: python

    from set_up_grasp_models.set_up_models.manipulate_model import reorder_reactions

    # list with reaction order
    rxn_order = ['R_PGL', 'R_EDD', 'R_EDA', 'R_PGI', 'R_FBP', 'R_FBA', 'R_TPI', 'R_GAPD',
                 'R_PGK', 'R_PGM', 'R_ENO', 'R_PYK', 'R_G6PDH2','R_EX_pyr', 'R_EX_pep',
                 'R_EX_g6p', 'R_EX_6pgc', 'R_EX_g3p', 'R_EX_f6p', 'R_EX_3pg']

    # path to current model
    model_name = 'glycolysis_v2'
    file_in = os.path.join('example_files', 'output', model_name + '.xlsx')

    # import current model with pandas
    data_dict = pd.read_excel(file_in, sheet_name=None, index_col=0)

    # path to the model with re-ordered reactions - just substitute current one
    file_out = file_in

    # re-order reactions according to rxn_list
    reorder_reactions(data_dict, rxn_order, file_out)



Remove leading and trailing spaces
------------------------------------

This function removes all leading and trailing spaces from string fields.

.. code-block:: python

    from set_up_grasp_models.set_up_models.manipulate_model import remove_spaces

    # path to current model
    model_name = 'glycolysis_v2'
    file_in = os.path.join('example_files', 'output', model_name + '.xlsx')

    # import current model with pandas
    data_dict = pd.read_excel(file_in, sheet_name=None, index_col=0)

    # path to the model with re-ordered reactions - just substitute current one
    file_out = file_in

    # remove any leading or trailing spaces in all string cells
    remove_spaces(data_dict, file_out)




Rename columns in the model
--------------------------------------

Since this package assumes certain column names, it is important that they are correct. To make sure just run:

.. code-block:: python

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


This will rename all columns to standard names.
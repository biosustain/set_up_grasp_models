"""
The aim of this module is to get standard Gibbs energies for reactions given in a plain text file with the
format "R_FBA: m_g3p_c + m_dhap_c <-> m_fdp_c". BiGG IDs must be used for metabolites.
"""

import re
import os
from math import isnan
import numpy as np
import pandas as pd
from equilibrator_api import ComponentContribution, Reaction, Q_, ccache, parse_reaction_formula

from set_up_grasp_models.model.parser import ReactionParser


def _parse_rxns(rxn_list: list) -> set:

    parser = ReactionParser()
    met_bigg_ids = set()

    for rxn_str in rxn_list:
        r_id, reversible, stoichiometry = parser.parse_reaction(rxn_str)
        met_bigg_ids.update(stoichiometry.keys())

    return met_bigg_ids


def _convert_met_ids_to_kegg(met_bigg_ids: set, map_bigg_to_kegg_ids: pd.DataFrame):

    mets_without_kegg_id = []
    mets_kegg_dic = {}

    for met in met_bigg_ids:
        try:
            bigg_id = re.findall('m_(\S+)_\w+$', met)[0]

            try:
                kegg_ids = map_bigg_to_kegg_ids.loc[bigg_id]
                mets_kegg_dic[bigg_id] = [kegg_ids['id_kegg']] if type(kegg_ids) is pd.Series else list(
                    kegg_ids['id_kegg'])

                if len(mets_kegg_dic[bigg_id]) > 1:
                    id_to_keep = ''

                    while not id_to_keep:
                        id_to_keep = input(f'There have been multiple matches for {bigg_id}.' +
                                           f' Please type below the one you want to keep from: {mets_kegg_dic[bigg_id]}:\n')
                    mets_kegg_dic[bigg_id] = [id_to_keep]

                if type(mets_kegg_dic[bigg_id][0]) is not str and isnan(mets_kegg_dic[bigg_id][0]):
                    id_to_keep = ''
                    mets_kegg_dic[bigg_id] = ''
                    id_to_keep = input(f'No KEGG id was found for {bigg_id}. If you know it, please insert it below,' +
                                       f'otherwise all reaction involving {bigg_id} will be ignored.\n')
                    if id_to_keep:
                        mets_kegg_dic[bigg_id] = [id_to_keep]
                    else:
                        mets_without_kegg_id.append(bigg_id)

            except KeyError:
                raise SyntaxError(f'Didn\'t find a match for {bigg_id} in the list of bigg ids. ' +
                                  f'Make sure you are using bigg ids.\n An easy mistake is to use glc_D instead of glc__D.')

        except IndexError:
            raise SyntaxError(f'Didn\'t find any matches for {met} in the stoichiometry matrix. ' +
                              f'Make sure metabolite ids have the form "m_biggId_compartment".')

    return mets_kegg_dic, mets_without_kegg_id


def _convert_rxn_str_to_kegg_ids(rxn_list: list, mets_kegg_dic: dict, mets_without_kegg_id: list) -> dict:

    rxn_dict = {}
    for rxn_str in rxn_list:
        if not rxn_str.startswith('R_EX_'):
            try:
                rxn_id = re.findall('(R_\S+):', rxn_str)[0]
            except IndexError:
                raise SyntaxError('Didn\'t match reaction id. Make sure the reaction id has the format "R_rxnId" ' +
                                  'and is followed by ":".')

            rxn_str = re.sub('R_\S+:\s*', '', rxn_str)

            if mets_without_kegg_id:
                for met in mets_without_kegg_id:
                    if rxn_str.find(met) == -1:
                        rxn_str = re.sub('m_(\S+)_\w+', lambda m: mets_kegg_dic[m.group(1)][0], rxn_str)
                        rxn_str = rxn_str.replace('<->', '=')
                        rxn_dict[rxn_id] = rxn_str

            else:
                rxn_str = re.sub('m_(\S+)_\w+', lambda m: mets_kegg_dic[m.group(1)][0], rxn_str)
                rxn_str = rxn_str.replace('<->', '=')
                rxn_dict[rxn_id] = rxn_str

    return rxn_dict


def convert_rxns_to_kegg(rxn_list: list, map_bigg_to_kegg_ids: pd.DataFrame) -> dict:
    """
    Given a plain text file with a list of reactions in the form: R_FBA: m_g3p_c + m_dhap_c <-> m_fdp_c, where
    metabolite ids are bigg ids, it converts the metabolite IDs to KEEG ids: R_FBA: C00118 + C00111 = C00354.
    To do the conversion it uses a dataframe with BiGG IDs on the index and respective KEEG ids on the column "id_kegg".
    It skips exchange reactions, which should start with 'R_EX_'.

    Args:
        file_rxns: path to file with plain text reactions.
        map_bigg_to_kegg_ids: dataframe with bigg IDs and corresponding KEGG ids.

    Returns:
        A dictionary where the keys are the reaction IDs (e.g. R_FBA) and the values the reaction in terms of
        KEGG IDs (e.g. C00118 + C00111 = C00354).
    """

    met_bigg_ids = _parse_rxns(rxn_list)

    mets_kegg_dic, mets_without_kegg_id = _convert_met_ids_to_kegg(met_bigg_ids, map_bigg_to_kegg_ids)

    rxn_dict = _convert_rxn_str_to_kegg_ids(rxn_list, mets_kegg_dic, mets_without_kegg_id)

    return rxn_dict


def get_dGs(rxn_list: list, file_bigg_kegg_ids: str, pH: float = 7.0, ionic_strength: float = 0.1,
            digits: int = 2) -> dict:
    """
    Given a plain text file with reactions in the form R_FBA: m_g3p_c + m_dhap_c <-> m_fdp_c and a file with a
    mapping between bigg and kegg ids, returns the standard gibbs energy and respective uncertainty for each reaction.
    It skips exchange reactions, which should start with 'R_EX_'.

    Args:
        file_rxns: path to file with plain text reactions.
        file_bigg_kegg_ids: path to file with mapping between bigg and kegg ids.
        pH: pH value to use to calculate standard Gibbs energies.
        ionic_strength: ionic strength value to use to calculate standard Gibbs energies.
        digits: number of digits to round standard gibbs energies and respective uncertainty.

    Returns:
       Dictionary with bigg reaction ids as keys and (standard Gibbs energy, uncertainty) as values.
    """

    map_bigg_to_kegg_ids = pd.read_csv(file_bigg_kegg_ids, index_col=0)

    rxn_dict = convert_rxns_to_kegg(rxn_list, map_bigg_to_kegg_ids)

    rxn_dG_dict = {}
    eq_api = ComponentContribution(p_h=Q_(pH), ionic_strength=Q_(ionic_strength, 'M'))

    for rxn_id in rxn_dict.keys():

        rxn = parse_reaction_formula(rxn_dict[rxn_id])
        if not rxn.is_balanced():
            print(f'{rxn_id} is not balanced.')

        res = eq_api.standard_dg_prime(rxn)
        dG0 = res.value.magnitude
        dG0_std = res.error.magnitude

        rxn_dG_dict[rxn_id] = (round(dG0, digits), round(dG0_std, digits))

    return rxn_dG_dict


def _set_up_model_thermo_rxns(base_df: pd.DataFrame, rxns_order: list, rxn_list: list, use_equilibrator:bool,
                              file_bigg_kegg_ids: str = None, pH: float = 7.0, ionic_strength: float = 0.1) \
        -> pd.DataFrame:
    """
    Fills in the thermoRxns sheet on the excel GRASP input file.
    If use_equilibrator is set to True, it first gets all standard Gibbs energies from eQuilibrator, then it copies any
    values that may be defined in base_df.

    Args:
        base_df: dictionary with base excel input file.
        rxns_order: list with reaction IDs.
        rxn_list: list with reaction strings.
        use_equilibrator: flag determining whether or not to get the standard Gibbs energies from eQuilibrator.
        pH : pH value to use to get the standard Gibbs energies from eQuilibrator.
        ionic_strength: ionic strength value to use to get the standard Gibbs energies from eQuilibrator.
        file_bigg_kegg_ids: path to the file containing the metabolites mapping from BiGG to KEGG ids,

    Returns:
        thermoRxns dataframe for the output excel file.
    """

    columns = ['∆Gr\'_min (kJ/mol)', '∆Gr\'_max (kJ/mol)']
    thermo_rxns_df = pd.DataFrame(index=rxns_order, columns=columns, data=np.zeros([len(rxns_order), len(columns)]))
    thermo_rxns_df.index.name = 'reaction ID'



    if use_equilibrator:
        if file_bigg_kegg_ids and not os.path.isfile(file_bigg_kegg_ids):
            raise FileNotFoundError(f'Didn\'t find {file_bigg_kegg_ids}. Please provide a valid ' +
                                    'path to the file with metabolite mappings from BiGG to KEGG ids.')

        elif not file_bigg_kegg_ids:
            this_dir, this_filename = os.path.split(__file__)
            file_bigg_kegg_ids = os.path.join(this_dir, '..', '..', 'data', 'map_bigg_to_kegg_ids.csv')
            if not os.path.isfile(file_bigg_kegg_ids):
                raise FileNotFoundError(f'Didn\'t find map_bigg_to_kegg_ids.csv in the data folder. Please provide ' +
                                        'the path to the file with metabolite mappings from BiGG to KEGG ids.')

        rxn_dG_dict = get_dGs(rxn_list, file_bigg_kegg_ids, pH=pH, ionic_strength=ionic_strength, digits=2)
        rxn_dG_df = pd.DataFrame().from_dict(rxn_dG_dict, orient='index')
        rxn_dG_df.columns = ['average', 'stdev']

        rxn_dG_df['min'] = rxn_dG_df['average'] - 2 * rxn_dG_df['stdev']
        rxn_dG_df['max'] = rxn_dG_df['average'] + 2 * rxn_dG_df['stdev']
        thermo_rxns_df.loc[rxn_dG_df.index.values, '∆Gr\'_min (kJ/mol)'] = rxn_dG_df.loc[rxn_dG_df.index.values, 'min']
        thermo_rxns_df.loc[rxn_dG_df.index.values, '∆Gr\'_max (kJ/mol)'] = rxn_dG_df.loc[rxn_dG_df.index.values, 'max']

    if 'thermoRxns' in base_df.keys():
        index_intersection = set(base_df['thermoRxns'].index.values).intersection(thermo_rxns_df.index.values)
        thermo_rxns_df.loc[index_intersection, :] = base_df['thermoRxns'].loc[index_intersection, :]

    return thermo_rxns_df

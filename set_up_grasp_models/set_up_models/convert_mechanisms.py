"""
The purpose of this module is to convert an enzyme mechanism given in terms of elementary reactions into the
pattern format currently accepted by GRASP.
"""

import os

import numpy as np
import pandas as pd


def _get_enz_states(er_mech: str) -> list:
    """
    Given a string with the enzyme mechanism written as a sequence of elementary reactions produces a list with the
    enzyme state numbers and metabolites that bind/unbind to the respective enzyme states.

    Args:
        er_mech (str): string with elementary reactions that describe the enzyme mechanism.

    Returns:
        enz_states_list (list): list with all enzyme state numbers and substrates
    """

    er_mech = er_mech.replace('<->', '')
    er_mech = er_mech.replace('+', '')
    er_mech_list = er_mech.split()

    enz_states_dic = {}
    enz_states_list = []
    state_i = 1

    for i, entry in enumerate(er_mech_list):
        if entry.startswith('E_'):
            if entry not in enz_states_dic.keys():
                enz_states_dic[entry] = state_i
                enz_states_list.append([state_i])
                state_i += 1
            else:
                enz_states_list.append([enz_states_dic[entry]])

            if not er_mech_list[i + 1].startswith('E_'):
                enz_states_list[-1].append(er_mech_list[i + 1])

    return enz_states_list


def _generate_grasp_pattern(enz_states_list: list, promiscuous: bool, inhib_list: list,
                            activ_list: list) -> str:
    """
    Given a list of enzyme state numbers and metabolites that bind/unbind to them, generates the respective
    GRASP pattern.

    For this to work both with promiscuous reactions where one reaction has an ordered mechanism and another a random
     mechanism as well as ping-pong mechanisms a few steps are taken:
       - the number of reactions in a mechanism is counted. A new reaction starts when the enzyme state to which
       a ligand can bind is 1 (i.e. the free enzyme), there has been more than one transition step and there
       has been a new transition step since it was checked. This allows
       one to distinguish different reactions in a given promiscuous enzyme mechanism and naming each first product
       to be released after a transition step as P{i}, where i stands for the number of the reaction. This is important
       so GRASP can later on write the flux equation correctly for each reaction catalyzed by a promiscuous enzyme.
       The reason reactions are counted and not only transition steps is because ping-pong mechanisms also have
       multiple transition steps and yet the first product to be released after a transition step should be named
       P, Q, R, S instead of P{i}.

       - whether we are in a state right after the transition step or not is tracked, so that we can name the product
       as P{i} instead of Q, R, S, etc.

    Inhibiting and activating metabolites are assumed to only bind to the enzyme and not be released, except as
    a "reverse binding".

    Args:
        enz_states_list (list): list of all enzyme state numbers and ligands that bind/unbind.
        promiscuous (bool): to indicate whether reaction is promiscuous or not.
        inhib_list (list): list of inhibiting metabolites.
        activ_list (list): list of activating metabolites.

    Returns:
        grasp_pattern (str): the grasp pattern

    """
    subs_list = ['A', 'B', 'C', 'D', 'E']
    prod_list = ['P', 'Q', 'R', 'S', 'T']
    subs_dic = {}
    prod_dic = {}
    subs_i = 0
    prod_i = 0
    inhib_dic = dict((met, f'I{i+1}') for i, met in enumerate(inhib_list)) if inhib_list else dict()
    activ_dic = dict((met, f'Z{i+1}') for i, met in enumerate(activ_list)) if activ_list else dict()

    rxn_i = 0
    n_transitions = 0
    previous_n_transitions = 0
    after_transition = False

    grasp_pattern = ''
    rate_i = 1

    for state_i in range(0, len(enz_states_list), 2):

        # if there is more than one transition step, there has been a transition step since the last one
        #  and the enzyme state is 1 again then it is a new reaction
        # if the enzyme is promiscuous restart dictionaries so that no repeated ligand names are used.
        if n_transitions > 0 and n_transitions > previous_n_transitions and enz_states_list[state_i][0] == 1:
            previous_n_transitions = n_transitions
            rxn_i += 1

            if promiscuous:
                subs_dic = {}
                prod_dic = {}

        # get binding ligand name
        bind_ligand = ''

        if len(enz_states_list[state_i]) == 2:
            if enz_states_list[state_i][1] in inhib_dic.keys():
                bind_ligand = f'.*{inhib_dic[enz_states_list[state_i][1]]}'
            elif enz_states_list[state_i][1] in activ_dic.keys():
                bind_ligand = f'.*{activ_dic[enz_states_list[state_i][1]]}'
            else:
                if not enz_states_list[state_i][1] in subs_dic.keys():
                    subs_dic[enz_states_list[state_i][1]] = subs_list[subs_i]
                    subs_i += 1

                bind_ligand = f'.*{subs_dic[enz_states_list[state_i][1]]}'

        # write forward step
        grasp_pattern += f'{enz_states_list[state_i][0]} {enz_states_list[state_i + 1][0]} k{rate_i:02}{bind_ligand}\n'
        rate_i += 1

        # get unbinding ligand name
        release_ligand = ''
        if len(enz_states_list[state_i + 1]) == 2:
            if not enz_states_list[state_i + 1][1] in prod_dic.keys():
                prod_dic[enz_states_list[state_i + 1][1]] = prod_list[prod_i]
                prod_i += 1

            # by default P is named P1
            release_ligand = f'.*P1' if prod_dic[enz_states_list[state_i + 1][1]] == 'P' \
                             else f'.*{prod_dic[enz_states_list[state_i + 1][1]]}'

            # if ligand unbinding is the first one after the transition step name it Pi
            if after_transition and promiscuous:
                release_ligand = f'.*P{rxn_i+1}'
                prod_dic[enz_states_list[state_i + 1][1]] = f'P{rxn_i+1}'
                after_transition = False

                if rxn_i > 0:
                    prod_i -= 1

        else:  # check if this is a transition step
            if not bind_ligand:
                n_transitions += 1
                after_transition = True

        # write reverse step
        grasp_pattern += f'{enz_states_list[state_i + 1][0]} {enz_states_list[state_i][0]} k{rate_i:02}{release_ligand}\n'
        rate_i += 1

    # if there is only one reaction all P1 products should be P
    if rxn_i == 0:
        grasp_pattern = grasp_pattern.replace('P1', 'P')

    # remove last new line
    grasp_pattern = grasp_pattern[:-1]

    return grasp_pattern


def convert_er_mech_to_grasp_pattern(file_in: str, file_out: str, promiscuous: bool = False,
                                     inhib_list: list = None, activ_list: list = None):
    """
    Given an input file with a mechanism in the form of elementary reactions, converts it to a GRASP pattern file.

    Args:
        file_in (str): path to the input file with elementary reactions mechanism.
        file_out: path to the output file with GRASP pattern.
        promiscuous (bool): to indicate whether reaction is promiscuous or not.
        inhib_list (list): list of inhibiting metabolites.
        activ_list (list): list of activating metabolites.

    Returns:
        None
    """

    with open(file_in, 'r') as f_in:
        er_mech = f_in.read()

    enz_states_list = _get_enz_states(er_mech)
    grasp_pattern = _generate_grasp_pattern(enz_states_list, promiscuous, inhib_list, activ_list)

    with open(file_out, 'w+') as f_out:
        f_out.write(grasp_pattern)


def generate_mechanisms(file_in_model: str, mech_in_dir: str, pattern_out_dir: str,
                        hard_coded_mechs: list = None):
    """
    Given the GRASP input excel file, goes through the mechanisms defined in the kinetics sheet and checks if a .txt
    file with the same name exists in the pattern_out_dir, if not it checks the mech_in_dir for a .txt file with
    the mechanism name and converts it to a patter file to be stored in the pattern_out_dir.

    Args:
        file_in_model (str): path to GRASP input excel file.
        mech_in_dir: path to folder with the mechanism files in terms of elementary reactions.
        pattern_out_dir: path to folder with pattern files used by GRASP.

    Returns:
        None
    """

    hard_coded_mechs = {'massAction', 'diffusion', 'fixedExchange', 'freeExchange'} if not hard_coded_mechs \
        else set(hard_coded_mechs)

    kinetics_df = pd.read_excel(file_in_model, sheet_name='kinetics1')

    for ind, mech in enumerate(kinetics_df['kinetic mechanism']):

        if mech not in hard_coded_mechs:
            if not os.path.isfile(os.path.join(pattern_out_dir, mech + '.txt')):
                print(mech)

                file_in = os.path.join(mech_in_dir, mech + '.txt')
                file_out = os.path.join(pattern_out_dir, mech + '.txt')

                promiscuous = False if type(kinetics_df.loc[ind, 'promiscuous']) is float else True

                inhib_list = None if type(kinetics_df.loc[ind, 'inhibitors']) is float or np.float \
                    else kinetics_df.loc[ind, 'inhibitors'].split()
                activ_list = None if type(kinetics_df.loc[ind, 'activators']) is float or np.float \
                    else kinetics_df.loc[ind, 'activators'].split()

                convert_er_mech_to_grasp_pattern(file_in, file_out, promiscuous, inhib_list, activ_list)

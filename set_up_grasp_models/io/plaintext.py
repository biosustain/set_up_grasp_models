""" This module implements methods for reading and writing models using a plain text format.
Adapted from  https://github.com/cdanielmachado/framed

Author: Daniel Machado

"""

from os.path import splitext, basename

from ..model.model import Model

INSTRUCTIONS = """
# Text based model representation
# Format: "Reaction id : substrates --> products [lower bound, upper bound]"
# valid identifiers can contain letters, numbers or underscore (_) but must begin with a letter (for SBML compatibility)
# Use --> or <-> for irreversible or reversible reactions respectively
# bounds are optional and can be specified only in one direction, eg: [-10.0,]
# begin with # to comment out any line

"""


def import_model_from_plaintext(filename: str) -> Model:
    """ Reads a model from a file.
    
    Arguments:
        filename: file path.

    Returns:
        A Model object (or respective subclass).
    """

    with open(filename, 'r') as stream:
        model_id = splitext(basename(filename))[0]
        model = Model(model_id)

        for line in stream:
            line = line.strip()
            if not line:
                continue

            # If line ends with comment ignore it as well
            line = line.split("#", 1)[0]
            line = line.strip()
            if not line:
                continue

            model.add_reaction_from_str(line, clear_tmp=False)

    return model


def write_to_plaintext(rxn_strings: list, file_out: str, print_instructions: bool = True):
    """ Writes a model to a file.

    Arguments:
        rxn_strings: list of string reactions.
        file_out: file path.
        print_instructions: print plain text format instructions as header.

    Returns:
        None
    """
    with open(file_out, 'w') as f_out:
        if print_instructions:
            f_out.write(INSTRUCTIONS)
        for rxn in rxn_strings:
            f_out.write(f'{rxn}\n')

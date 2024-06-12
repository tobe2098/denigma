# from tkinter import Menubutton
# from ast import unparse
from ...core import plugboards
from ...utils import utils
from ...utils import utils_cli
from ...utils.utils import simplify_simple_dictionary_paired_unpaired


def _show_config_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """

    paired_df, unpaired_list = simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    utils_cli.printOutput("Paired letters:", paired_df)
    utils_cli.printOutput("Unpaired letters:", unpaired_list)
    utils_cli.printOutput(
        "Number of connections:", (plugboard_ref._characters_in_use - unpaired_list) / 2
    )
    utils_cli.returningToMenu()


def _choose_connection_to_delete_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    paired_df, _ = utils.simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )

    if paired_df.shape[0] == 0:
        utils_cli.returningToMenu("There are no available connections")

    utils_cli.printOutput("Current connections are:\n", paired_df)
    row = utils_cli.askingInput("Choose a connection to delete (by index)")
    row = utils_cli.checkInputValidity(row, int, range(0, paired_df.shape[0]))

    if row:
        _delete_a_connection_pb(
            plugboard_ref=plugboard_ref,
            letter1=paired_df.iloc[row][0],
        )
        utils_cli.returningToMenu("Connection was deleted")
    else:
        utils_cli.returningToMenu("Index invalid", "e")


def _delete_a_connection_pb(plugboard_ref: plugboards.PlugBoard, letter1: str):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
        connIndex (_type_): _description_
    """
    # del plugboard_ref._board_dict[entry] #Requires testing
    (
        plugboard_ref._board_dict[letter1],
        plugboard_ref._board_dict[plugboard_ref._board_dict[letter1]],
    ) = (
        plugboard_ref._board_dict[plugboard_ref._board_dict[letter1]],
        plugboard_ref._board_dict[letter1],
    )

    plugboard_ref._update_dicts()
    # del d['k2']


def _create_a_single_connection_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    if len(unpaired_list) < 2:
        utils_cli.returningToMenu(
            "There are no letters left to pair (one or fewer left unconnected)"
        )
    utils_cli.printOutput("Unpaired letters:", unpaired_list)
    letter1 = utils_cli.askingInput("Choose a letter to pair").upper()
    letter1 = utils_cli.checkInputValidity(letter1, _range=unpaired_list)
    if not letter1:
        utils_cli.printError("Invalid input")
        return False
    remaining_letters = list(set(unpaired_list) - set(letter1))
    utils_cli.printOutput("Remaining letters:", remaining_letters)
    letter2 = utils_cli.askingInput("Choose the second letter").upper()
    letter2 = utils_cli.checkInputValidity(letter2, _range=remaining_letters)
    if not letter2:
        utils_cli.printError("Invalid input")
        return False
    plugboard_ref._board_dict[letter1] = letter2
    plugboard_ref._board_dict[letter2] = letter1
    plugboard_ref._update_dicts()
    utils_cli.printOutput("The connection was formed")
    return True


# First get a letter, show unconnected again, then choose to connect. If wrong choice, go back to start


# def _connect_two_letters_pb(plugboard_ref: plugboards.PlugBoard):
#     """_summary_

#     Args:
#         plugboard_ref (plugboards.PlugBoard): _description_
#     """
#     _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
#         plugboard_ref._board_dict
#     )
#     if len(unpaired_list) < 2:
#         utils_cli.returningToMenu(
#             "There are no letters left to pair (one or fewer left unconnected)"
#         )
#     while True:
#         utils_cli.printOutput("Unpaired letters:", (unpaired_list))
#         utils_cli.printOutput(
#             "If you want to stop configurating the board, press Enter"
#         )
#         letters = utils_cli.askingInput("Input two letters to pair:").strip().upper()
#         if letters.isalpha() and len(letters) == 2:
#             pass
#         elif not letters:
#             # utils_cli.returningToMenu("No input")
#             return
#         else:
#             print("Error: Input 2 letters please")
#             continue
#         letters = list(letters)
#         for i in range(2):
#             letters[i] = utils_cli.checkInputValidity(letters[i], _range=unpaired_list)
#         if not all(letters):
#             # if not all(map(lambda v: v in letters, unpaired_list)):
#             utils_cli.printOutput("One of the letters is already connected")
#             continue
#         break
#     plugboard_ref._board_dict[letters[0]] = letters[1]
#     plugboard_ref._board_dict[letters[1]] = letters[0]
#     utils_cli.printOutput("Connection formed")


def _form_numbered_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _show_config_pb(plugboard_ref)
    _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    connections = input(
        utils_cli.askingInput(
            f"How many connections do you want to create (Max. {len(unpaired_list)/2})?"
        )
    )
    if connections > len(unpaired_list) / 2:
        utils_cli.returningToMenu("Number exceeds the maximum", "e")
    _form_n_extra_connections_pb(plugboard_ref, connections)


def _reset_and_form_n_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _reset_connections_pb(plugboard_ref)
    _form_numbered_connections_pb(plugboard_ref)


def _form_n_extra_connections_pb(plugboard_ref: plugboards.PlugBoard, connections: int):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
        connections (int): _description_
    """
    c = 0
    while connections - c:
        utils_cli.clearScreenConvenienceCli()
        utils_cli.printOutput(f"Creating connection {c+1} of {connections}")
        if _create_a_single_connection_pb(plugboard_ref):
            c += 1


# def _reset_and_form_all_connections_by_pairs_pb(plugboard_ref: plugboards.PlugBoard):
#     """_summary_

#     Args:
#         plugboard_ref (plugboards.PlugBoard): _description_
#     """
#     _reset_connections_pb(plugboard_ref)
#     while True:
#         accbool = utils_cli.askingInput(
#             "Do you want to keep making changes?[y/n]"
#         ).lower()
#         if accbool == "n":
#             utils_cli.returningToMenu()
#         elif accbool == "y":
#             _create_a_single_connection_pb(plugboard_ref)


## The board is fully connected (one or fewer letters left unconnected). If wrong choice, go back to start


def _reset_and_randomize_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    seed = utils_cli.getSeedFromUser()
    plugboard_ref._reset_dictionaries()
    plugboard_ref.random_setup(seed)
    utils_cli.printOutput("Board random setup is done")


def _reset_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    plugboard_ref._reset_dictionaries()
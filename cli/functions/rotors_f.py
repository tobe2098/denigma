## New seeds for standalone generated rotors, reflectors and boards
### EACH OBJECT SET OF MENUS TAKES THE REFERENCE FROM THE MACHINE, AND THEN OPERATES ON IT, EFFECTIVELY NOT TOUCHING THE MACHINE ITSELF BUT ITS OBJECTS
### EXCEPT FOR LOADING!!!!!! LOADING OF ITEMS HAS TO BE DONE DIRECTLY IN THE MACHINE MENU
### ALSO EXCEPT ALL GENERALISTIC CONFIG CALLS
### PUT WARNING IN ALL MENUING RELATED TO JUMP (IN RANDOM JUMP IS ALWAYS 1?)never zero or no_chars%jump==0!!, write explanation of interplay between notches and jump
# Intern setup functions
from utils.types_utils import isDashedObject
from ...core import rotors
from ...utils import utils
from ...utils import utils_cli
import random
import os
import pickle

# from copy import copy


def _show_config_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    (paired_df, unpaired, unformed, _) = (
        utils.simplify_rotor_dictionary_paired_unpaired(
            rotor_ref._forward_dict, rotor_ref._backward_dict
        )
    )
    unpaired.extend(unformed)
    utils_cli.printOutput(
        "Rotor letter position :",
        str(rotor_ref._conversion_in_use[rotor_ref._position]),
    )
    utils_cli.printOutput("Rotor letter jumps:", str(rotor_ref._jump))
    notchlist = [rotor_ref._conversion_in_use[i] for i in rotor_ref._notches]
    utils_cli.printOutput("Rotor notches:", str(notchlist))
    utils_cli.printOutput("Forward connections in the rotor:\n", paired_df)
    utils_cli.printOutput("Bad connections (self or none) in the rotor:", str(unpaired))

    # utils_cli.printOutput(
    #     "Backward connections in the rotor:", str(rotor_ref._backward_dict)
    # )
    utils_cli.printOutput("Rotor name:", str(rotor_ref._name))
    (
        _,
        unpaired,
        unformed,
        _,
    ) = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    if not unformed:
        rotor_ref.lacks_connections = False
    if len(unpaired) > 0:
        utils_cli.printWarning(
            "One or more connections are self-connections. This may go against proper practice"
        )
    utils_cli.returningToMenu()


# For now, in text, there will be no connection deletion? Or will there?
def _choose_connection_to_delete_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    paired_df, _, _, _ = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )

    if paired_df.shape[0] == 0:
        utils_cli.returningToMenu("There are no available connections")

    utils_cli.printOutput("Current connections are:\n", paired_df)
    row = utils_cli.askingInput("Choose a connection to delete (by index)")

    row = utils_cli.checkInputValidity(row, int, range(0, paired_df.shape[0]))

    if row:
        # if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        _delete_a_connection_rt(rotor_ref=rotor_ref, letter1=paired_df.iloc[row][0])
        utils_cli.returningToMenu("Connection was deleted")
    else:
        utils_cli.returningToMenu("Index invalid", output_type="e")


def _delete_a_connection_rt(rotor_ref: rotors.Rotor, letter1: str):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
        connIndex (_type_): _description_
    """
    rotor_ref._backward_dict[rotor_ref._forward_dict[letter1]] = ""
    # del rotor_ref._board_dict[entry] #Requires testing
    rotor_ref._forward_dict[letter1] = ""
    rotor_ref.lacks_connections = True
    rotor_ref._update_dicts()
    # del d['k2']


def _create_a_connection_single_choice_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    (
        _,
        _,
        front_unformed,
        back_unformed,
    ) = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    if len(front_unformed) == 0 and len(back_unformed) == 0:
        rotor_ref.lacks_connections = False
        utils_cli.returningToMenu(
            "There are no letters left to pair (one or fewer left unconnected)",
        )
    utils_cli.printOutput("Unpaired letters in front side:", front_unformed)

    letter1 = utils_cli.askingInput("Choose a letter to pair from front side").upper()
    letter1 = utils_cli.checkInputValidity(letter1, _range=front_unformed)
    if not letter1:
        # if letter1 not in front_unformed:
        utils_cli.returningToMenu("Invalid input", output_type="e")
    utils_cli.printOutput("Unpaired letters in back side:", back_unformed)
    letter2 = utils_cli.askingInput(
        "Choose the second letter from the back side"
    ).upper()
    letter2 = utils_cli.checkInputValidity(letter2, _range=back_unformed)
    if not letter2:
        # if letter2 not in back_unformed:
        utils_cli.returningToMenu("Invalid input", output_type="e")
    rotor_ref._forward_dict[letter1] = letter2
    rotor_ref._backward_dict[letter2] = letter1
    rotor_ref._update_dicts()
    utils_cli.returningToMenu("The connection was formed")
    if len(front_unformed) - 1 == 0 and len(back_unformed) - 1 == 0:
        rotor_ref.lacks_connections = False


# First get a letter, show unconnected again, then choose to connect. If wrong choice, go back to start


def _connect_all_letters_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    # (
    #     _,
    #     _,
    #     front_unformed,
    #     back_unformed,
    # ) = utils.simplify_rotor_dictionary_paired_unpaired(
    #     rotor_ref._forward_dict, rotor_ref._backward_dict
    # )
    # if len(front_unformed) == 0 and len(back_unformed) == 0:
    #     rotor_ref.lacks_conn = True
    #     utils_cli.returningToMenuMessage(
    #         "There are no letters left to pair (one or fewer left unconnected)"
    #     )
    while True:
        (
            _,
            _,
            front_unformed,
            back_unformed,
        ) = utils.simplify_rotor_dictionary_paired_unpaired(
            rotor_ref._forward_dict, rotor_ref._backward_dict
        )
        if len(front_unformed) == 0 and len(back_unformed) == 0:
            rotor_ref.lacks_connections = False
            utils_cli.returningToMenu(
                "There are no letters left to pair (one or fewer left unconnected)",
            )
        utils_cli.printOutput("Unpaired letters in front side:", (front_unformed))
        utils_cli.printOutput("Unpaired letters in back side:", (back_unformed))
        utils_cli.printOutput(
            "If you want to stop configurating the board, just press Enter"
        )
        letters = (
            utils_cli.askingInput(
                "Input one letter from front side, one from back side (in order)"
            )
            .strip()
            .upper()
        )
        letters = list(letters)
        if len(letters) == 2 and all(
            letter in rotor_ref._characters_in_use for letter in letters
        ):
            pass
        elif not letters:
            return
        else:
            utils_cli.printError("Input only two allowed characters")
            continue
        letters[0] = utils_cli.checkInputValidity(letters[0], _range=front_unformed)
        letters[1] = utils_cli.checkInputValidity(letters[1], _range=back_unformed)
        if not all(letters):
            # if letters[0] not in front_unformed or letters[1] not in back_unformed:
            utils_cli.printError("One or more letters are already connected")
            continue
        # break
        rotor_ref._forward_dict[letters[0]] = letters[1]
        rotor_ref._backward_dict[letters[1]] = letters[0]
        utils_cli.printOutput("Connection formed")


def _form_all_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _show_config_rt(rotor_ref)
    # _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
    #     rotor_ref._board_dict
    # )
    _connect_all_letters_rt(rotor_ref)
    rotor_ref.lacks_connections = True
    utils_cli.returningToMenu(
        "You exited without forming all connections!", output_type="w"
    )

    # utils_cli.returningToMenuMessage(
    #     "There are no letters left to pair (one or fewer left unconnected)"
    # )


# def reset_and_form_all_connections(rotor_ref: rotors.Rotor):
#     """_summary_

#     Args:
#         rotor_ref (rotors.Rotor): _description_
#     """
#     reset_connections(rotor_ref)
#     form_all_connections(rotor_ref)


def _swap_two_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
        connections (int): _description_
    """
    (paired_df, _, _, _) = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    utils_cli.printOutput("Current connections are:\n", paired_df)
    letter1 = utils_cli.askingInput("Choose a frontside connection by the index")
    letter1 = utils_cli.checkInputValidity(letter1, int, range(0, paired_df.shape[0]))
    # letter1 = utils_cli.checkInputValidity(letter1, _range=rotor_ref._characters_in_use)
    if not letter1:
        # if letter1 not in rotor_ref._characters_in_use:
        utils_cli.printError("Invalid input")
        return
    letter2 = utils_cli.askingInput(
        "Choose a second frontside connection by the index to swap"
    )
    letter2 = utils_cli.checkInputValidity(letter2, int, range(0, paired_df.shape[0]))
    # letter2 = utils_cli.checkInputValidity(letter2, _range=rotor_ref._characters_in_use)
    if not letter2:
        # if letter2 not in rotor_ref._characters_in_use:
        utils_cli.printError("Invalid input")
        return
    (
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter1]],
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter2]],
    ) = (
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter2]],
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter1]],
    )
    rotor_ref._forward_dict[letter1], rotor_ref._forward_dict[letter2] = (
        rotor_ref._forward_dict[letter2],
        rotor_ref._forward_dict[letter1],
    )
    rotor_ref._update_dicts()
    utils_cli.printOutput("The connection was swapped")


def _swap_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    while True:
        accbool = utils_cli.askingInput(
            "If you do not want to continue swapping, enter N"
        ).upper()
        if accbool == "N":
            utils_cli.returningToMenu()
        _swap_two_connections_rt(rotor_ref=rotor_ref)

    # utils_cli.returningToMenuMessage(
    #     "There are no letters left to pair (one or fewer left unconnected)."
    # )


def _reset_and_streamline_connections_by_pairs_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _reset_connections_rt(rotor_ref)
    # while True:
    #     accbool = utils_cli.utils_cli.askingInput("Do you still want to make changes?[y/n]").lower()
    #     if accbool == "n":
    #         utils_cli.returningToMenu()
    #     elif accbool == "y":
    #         break
    _connect_all_letters_rt(rotor_ref)
    rotor_ref.lacks_connections = True
    utils_cli.returningToMenu(
        "You exited without forming all connections!", output_type="w"
    )


def _reset_and_randomize_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    seed = utils_cli.getSeedFromUser()

    # rotor_ref._reset_dictionaries() Necessary?
    rotor_ref._randomize_dictionaries(seed)
    utils_cli.returningToMenu("Rotor connections established")


def _reset_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    rotor_ref._reset_dictionaries()
    rotor_ref.lacks_connections = True


def _print_name_rt(rotor_ref: rotors.Rotor):
    utils_cli.printOutput("Current rotor name:", rotor_ref._name)


def _change_rotor_name_rt(rotor_ref: rotors.Rotor):
    _print_name_rt(rotor_ref)
    new_name = utils_cli.askingInput("Input a new name for the rotor")
    while not rotor_ref._is_name_valid(new_name):
        utils_cli.printOutput("Input only alphanumerical characters or underscores")
        new_name = utils_cli.askingInput("Input a new name for the rotor")
    rotor_ref._change_name(new_name)
    utils_cli.returningToMenu("Rotor name changed to:", rotor_ref._name)


def _randomize_name_rt(rotor_ref: rotors.Rotor):
    seed = utils_cli.getSeedFromUser()
    rotor_ref._random_name(seed)
    utils_cli.returningToMenu("Rotor name changed to:", rotor_ref._name)


def _change_notches_rt(rotor_ref: rotors.Rotor):
    utils_cli.printOutput("Rotor notches:", rotor_ref.get_notchlist_letters())
    positions = [
        i
        for i in utils_cli.askingInput(
            "Input new notches separated by a space (empty to skip)"
        )
        .upper()
        .split()
    ]
    if not positions:
        utils_cli.returningToMenu()
    while not rotor_ref._are_notches_invalid(positions):
        utils_cli.printError("Input invalid")
        positions = [
            i
            for i in utils_cli.askingInput(
                "Input new notches separated by a space (empty to skip)"
            )
            .upper()
            .split()
        ]
        if not positions:
            utils_cli.returningToMenu()

    rotor_ref._define_notches(positions)


def _randomize_notches_rt(rotor_ref: rotors.Rotor):
    seed = utils_cli.getSeedFromUser()
    random.seed(seed)
    positions = [
        i
        for i in set(
            random.sample(range(0, rotor_ref._no_characters), random.randint(1, 5))
        )
    ]
    rotor_ref._define_notches(positions)
    utils_cli.printOutput("New rotor notches:", rotor_ref.get_notchlist_letters())
    utils_cli.returningToMenu("Rotor notches established")


def _change_position_rt(rotor_ref: rotors.Rotor):
    new_position = utils_cli.askingInput(
        "Input a single allowed letter to set the rotor to a new position"
    ).upper()
    while rotor_ref._is_position_invalid(new_position):
        utils_cli.printError("Input only allowed letters")
        utils_cli.printOutput(rotor_ref._characters_in_use)
        new_position = utils_cli.askingInput(
            "Input a single allowed letter to set the rotor to a new position"
        ).upper()
    rotor_ref._define_position(new_position)
    utils_cli.returningToMenu("Rotor position set to:", rotor_ref.get_position())


def _randomize_position_rt(rotor_ref: rotors.Rotor, seed: int):
    seed = utils_cli.getSeedFromUser()
    random.seed(seed)
    new_position = random.sample(range(0, rotor_ref._characters_in_use), 1)
    rotor_ref._define_position(new_position)
    utils_cli.returningToMenu("Rotor position set to:", rotor_ref.get_position())


def _save_in_current_directory_rt(rotor_ref: rotors.Rotor):
    new_name = rotor_ref.get_name()
    while not rotor_ref._is_name_valid(new_name):
        new_name = utils_cli.askingInput(
            "Please assign a new name to the rotor:"
        ).strip()
    rotor_ref._change_name(new_name)

    current_path = os.getcwd()
    new_folder = utils.ROTORS_FILE_HANDLE
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        os.mkdir(path)
        utils_cli.printOutput("Directory '% s' created" % path)
    if utils_cli.checkIfFileExists(path, rotor_ref._name, "rotor"):
        utils_cli.printOutput("A rotor with this name already exists")
        accbool = ""
        while not accbool == "n" or not accbool == "y":
            accbool = input(
                utils_cli.askingInput("Do you want to overwrite the saved rotor? [y/n]")
            ).lower()
        if accbool == "n":
            utils_cli.returningToMenu()
    save_file = open(r"{}\\{}.rotor".format(path, rotor_ref._name), "wb")
    pickle.dump(rotor_ref, save_file)
    utils_cli.returningToMenu(
        "{} has been saved into {}.rotor in {}".format(
            rotor_ref._name, rotor_ref._name, path
        )
    )


def _load_saved_rotor():
    current_path = os.path.dirname(__file__)
    new_folder = utils.ROTORS_FILE_HANDLE
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        utils_cli.returningToMenu("There is no {} folder".format(path), output_type="e")
    list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
    if len(list_of_files) == 0:
        utils_cli.returningToMenu("There are no rotors saved", "e")
    utils_cli.printOutput("Your available rotors are:")
    utils_cli.printListOfOptions(list_of_files)
    rotor = utils_cli.askingInput("Input reflector's position in the list:")
    rotor = utils_cli.checkInputValidity(rotor, int, range(0, len(list_of_files)))
    while not rotor:
        # while not isinstance(rotor, int) or rotor > len(list_of_files) - 1 or rotor < 0:
        utils_cli.printError("Please input a valid index")
        utils_cli.printListOfOptions(list_of_files)
        rotor = utils_cli.askingInput("Input rotor's position in the list:")
        rotor = utils_cli.checkInputValidity(rotor, int, range(0, len(list_of_files)))
    filehandler = open(r"{}\\{}.reflector".format(path, list_of_files[rotor]), "rb")
    return pickle.load(filehandler)


def _exitMenu_rt(rotor_ref: rotors.Rotor):
    # (
    #     _,
    #     _,
    #     front_unformed,
    #     _,
    # ) = utils.simplify_rotor_dictionary_paired_unpaired(
    #     rotor_ref._forward_dict, rotor_ref._backward_dict
    # )
    if not rotor_ref.is_set_up():
        utils_cli.returningToMenu(
            "Due to implementation reasons, an improperly setup rotor is not allowed",
            "e",
        )
    utils_cli.exitMenu()
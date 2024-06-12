# from platform import machine
# from numpy import format_float_positional
import os
from ...core import reflectors
from ...utils import utils_cli
from ...utils import utils
from ..functions.reflectors_f import (
    _change_reflector_name_rf,
    _randomize_name_rf,
    _choose_connection_to_delete_rf,
    _create_a_connection_single_choice_rf,
    _form_all_connections_rf,
    _exitMenu_rf,
    _reset_and_form_all_connections_by_pairs_rf,
    _reset_and_randomize_connections_rf,
    _reset_connections_rf,
    _save_in_current_directory_rf,
    _show_config_rf,
    # _print_name_rf,
    _load_saved_reflector,
    # _form_n_connections_rf,  # Deprecated
)

_menu_reflector_name_options = {
    "1": ("Change name", _change_reflector_name_rf),
    "2": ("Randomize name", _randomize_name_rf),
    "0": ("Exit menu", utils_cli.exitMenu),
}

_menu_reflector_connections_options = {
    "1": ("Delete a single connection", _choose_connection_to_delete_rf),
    "2": ("Create a single connection", _create_a_connection_single_choice_rf),
    "3": ("Form all connections left", _form_all_connections_rf),
    "0": ("Exit menu", _exitMenu_rf),
}

_menu_reflector_reset_options = {
    "1": (
        "Reset and form max. connections",
        _reset_and_form_all_connections_by_pairs_rf,
    ),
    "2": ("Reset and randomize connections", _reset_and_randomize_connections_rf),
    "3": ("Reset connections", _reset_connections_rf),
    "0": ("Exit menu", utils_cli.exitMenu),
}

# _menu_reflector_saved_reflector = {
#     "1": ("Save rotor", _save_in_current_directory_rf),
#     "2": ("Change rotor name", _change_reflector_name_rf),
#     "3": ("Delete a single connection", _choose_connection_to_delete_rf),
#     "4": ("Create a single connection", _create_a_connection_single_choice_rf),
#     "5": ("Form all connections left", _form_all_connections_rf),
#     "6": (
#         "Reset and form max. connections",
#         _reset_and_form_all_connections_by_pairs_rf,
#     ),
#     "7": ("Reset and randomize connections", _reset_and_randomize_connections_rf),
#     "8": ("Reset connections", _reset_connections_rf),
#     "0": ("Exit menu", utils_cli.exitMenu),
# }


def _load_saved_reflector_for_editing(
    reflector: reflectors.Reflector = None, recursive: bool = False
):
    if not recursive:
        reflector = _load_saved_reflector()
    utils_cli.runNodeMenu(reflector, _menu_reflector)
    try:
        _save_in_current_directory_rf(reflector)
        utils_cli.returningToMenu()
    except utils_cli.MenuExitException:
        current_path = os.getcwd()
        new_folder = utils.REFLECTORS_FILE_HANDLE
        path = os.path.join(current_path, new_folder)
        if not utils_cli.checkIfFileExists(path, reflector._name, "reflector"):
            utils_cli.printOutput("A file with the reflector's name was not detected")
            accbool = ""
            while not accbool == "n" or not accbool == "y":
                accbool = input(
                    utils_cli.askingInput("Do you want to exit anyway?[y/n]")
                ).lower()
            if accbool == "n":
                _load_saved_reflector_for_editing(reflector=reflector, recursive=True)
                # utils_cli.returningToMenu()
            utils_cli.returningToMenu((f"Reflector {reflector.name} was discarded"))
    # Conda activation: conda info --envs, conda activate {}


_menu_reflector = {
    "1": ("Show current reflector setup", _show_config_rf),
    "2": ("Save rotor", _save_in_current_directory_rf),
    "3": ("Naming menu", _menu_reflector_name_options),
    "4": ("Connections options menu", _menu_reflector_connections_options),
    "5": ("Resetting options menu", _menu_reflector_reset_options),
    # "6": ("Edit a previously saved rotor", _load_saved_reflector_for_editing),
    "0": ("Exit menu", _exitMenu_rf),
}
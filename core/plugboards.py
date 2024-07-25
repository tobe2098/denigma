import copy
import random

from utils.exceptions import raiseBadInputException

from ..utils.utils import (
    CHARACTERS,
    CHARACTERS_dash,
    EQUIVALENCE_DICT,
    Constants,
    EQUIVALENCE_DICT_dash,
    is_valid_seed,
    transform_single_dict,
)


class PlugBoard:
    def __init__(
        self, characters=Constants.CHARACTERS, conversion=Constants.EQUIVALENCE_DICT
    ) -> None:
        self._characters_in_use = copy.copy(characters)
        self._conversion_in_use = copy.copy(conversion)
        self._board_dict = dict(
            zip(copy.copy(self._characters_in_use), copy.copy(self._characters_in_use))
        )
        self._update_dicts()

    def _update_dicts(self, character_to_num=True):
        if character_to_num:
            self._board_num_dict = transform_single_dict(
                self._board_dict, self._conversion_in_use
            )
        else:
            self._board_dict = transform_single_dict(
                self._board_num_dict, self._conversion_in_use
            )

    def _reset_dictionaries(self):
        self._board_dict = dict(
            zip(copy.copy(self._characters_in_use), copy.copy(self._characters_in_use))
        )
        self._update_dicts()

    def _input_output(self, number_io):
        return self._board_num_dict[number_io]

    def random_setup(self, seed=None):

        if not is_valid_seed(seed):
            raiseBadInputException()
        random.seed(seed)

        # Now set the connections
        ### !!! Make sure board is composed of pairs and is symmetrical!!! It is not as of now.
        num_list = list(range(0, len(self._characters_in_use)))
        random.shuffle(num_list)
        cable_num = random.randint(0, int(len(self._characters_in_use) / 2))
        while cable_num > 0 and len(num_list) > 1:
            characterA = num_list.pop()
            characterB = num_list.pop()
            self._board_num_dict[characterA] = characterB
            self._board_num_dict[characterB] = characterA
            cable_num -= 1

        self._update_dicts(False)
        # Show final configuration
        # print(">>>Board config:\n", simplify_board_dict(self.board_dict))

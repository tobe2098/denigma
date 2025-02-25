"""This module contains the rotor classes"""

import random
import copy
import string

from denigma.core.abstract import AbstractBaseClass

from denigma.utils.utils import (
    Constants,
    create_dictionary_from_charlist,
    transform_single_dict,
    is_valid_seed,
)
from denigma.utils.exceptions import raiseBadInputException


class Reflector(AbstractBaseClass):
    def __init__(self, characters=Constants.UPP_LETTERS):
        super().__init__(charlist=characters)
        self._conversion_in_use = create_dictionary_from_charlist(characters)
        self._reflector_dict = dict(
            zip(copy.copy(self._charlist), copy.copy(self._charlist))
        )
        self._reflector_num_dict = {}
        self._update_dicts()
        self.lacks_connections = True




    def reflect(self, input_character_number):
        # input_character_number -= prev_rotor_position
        # input_character_number %= len(self.characters_in_use)
        return self._reflector_num_dict[input_character_number]

    def _reset_dictionaries(self):
        self._reflector_dict = dict(
            zip(copy.copy(self._charlist), copy.copy(self._charlist))
        )
        self._update_dicts()

    def _update_dicts(self, character_to_num=True):
        if character_to_num:
            self._reflector_num_dict = transform_single_dict(
                self._reflector_dict, self._conversion_in_use
            )
        else:
            self._reflector_dict = transform_single_dict(
                self._reflector_num_dict, self._conversion_in_use
            )

    def is_set_up(self):
        unpaired=0
        for key in self._reflector_num_dict:
            if key==self._reflector_num_dict[key]:
                unpaired+=1
        self.lacks_connections=(unpaired>1)
        return not self.lacks_connections

    # def export_reflector(self):
    #     # if self.name == "name":
    #     #     print(
    #     #         ">Please assign a new name to the reflector with the function self.configure() or self.change_name()"
    #     #     )
    def _random_name(self, seed=None):
        if not is_valid_seed(seed):
            raiseBadInputException()
        random.seed(seed)
        # random.seed(seed)
        # Set name
        # !!! Make sure characters do not connect to themselves!!!
        name_list = [random.sample(range(0, 26), 1)[0] for _ in range(0, 10)]
        name_list[0:6] = [chr(num + 65) for num in name_list[0:6]]
        name_list[6:10] = [str(i % 10) for i in name_list[6:10]]
        string1 = ""  # Why is this here? I am not super sure
        new_name = string1.join(name_list)
        self._change_name(new_name)

    def _random_setup(self, seed=None):
        if not is_valid_seed(seed):
            raiseBadInputException()
        random.seed(seed)
        # character_list1 = [key for key, _ in self._charlist]
        character_list1 = copy.copy(self._charlist)
        random.shuffle(character_list1)
        # character_list2 = copy.copy(self.characters_in_use)
        # random.shuffle(character_list2)
        while len(character_list1) > 1:
            characterA = character_list1.pop()
            characterB = character_list1.pop()
            self._reflector_dict[characterA] = characterB
            self._reflector_dict[characterB] = characterA
        if len(character_list1) == 1:
            self._reflector_dict[character_list1[0]] = character_list1[0]
        self._update_dicts()
        # Show final configuration
        # if showConfig:
        #     self._show_config()
        # Export
        # self.export_reflector()

    # def _update_dicts(self, character_to_num=True):
    #     if character_to_num:
    #         self.reflector_num_dict = transform_single_dict_dash(self.reflector_dict)
    #     else:
    #         self.reflector_dict = transform_single_dict_dash(self.reflector_num_dict)

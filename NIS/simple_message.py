# -*- coding: utf-8 -*-
# Copyright 2021 Tampere University and VTT Technical Research Centre of Finland
# This software was developed as a part of the ProCemPlus project: https://www.senecc.fi/projects/procemplus
# This source code is licensed under the MIT license. See LICENSE in the repository root directory.
# Author(s): Ville Heikkilä <ville.heikkila@tuni.fi>

"""
Module containing the message class for simple message type.
"""

from __future__ import annotations
from typing import Any, Dict, Optional

from tools.exceptions.messages import MessageError, MessageValueError
from tools.messages import AbstractResultMessage


class SimpleMessage(AbstractResultMessage):
    """Description for the SimpleMessage class"""
    CLASS_MESSAGE_TYPE = "Simple"
    MESSAGE_TYPE_CHECK = True

    SIMPLE_VALUE_ATTRIBUTE = "SimpleValue"
    SIMPLE_VALUE_PROPERTY = "simple_value"

    # all attributes specific that are added to the AbstractResult should be introduced here
    MESSAGE_ATTRIBUTES = {
        SIMPLE_VALUE_ATTRIBUTE: SIMPLE_VALUE_PROPERTY
    }
    # list all attributes that are optional here (use the JSON attribute names)
    OPTIONAL_ATTRIBUTES = []

    # all attributes that are using the Quantity block format should be listed here
    QUANTITY_BLOCK_ATTRIBUTES = {}

    # all attributes that are using the Quantity array block format should be listed here
    QUANTITY_ARRAY_BLOCK_ATTRIBUTES = {}

    # all attributes that are using the Time series block format should be listed here
    TIMESERIES_BLOCK_ATTRIBUTES = []

    # always include these definitions to update the full list of attributes to these class variables
    # no need to modify anything here
    MESSAGE_ATTRIBUTES_FULL = {
        **AbstractResultMessage.MESSAGE_ATTRIBUTES_FULL,
        **MESSAGE_ATTRIBUTES
    }
    OPTIONAL_ATTRIBUTES_FULL = AbstractResultMessage.OPTIONAL_ATTRIBUTES_FULL + OPTIONAL_ATTRIBUTES
    QUANTITY_BLOCK_ATTRIBUTES_FULL = {
        **AbstractResultMessage.QUANTITY_BLOCK_ATTRIBUTES_FULL,
        **QUANTITY_BLOCK_ATTRIBUTES
    }
    QUANTITY_ARRAY_BLOCK_ATTRIBUTES_FULL = {
        **AbstractResultMessage.QUANTITY_ARRAY_BLOCK_ATTRIBUTES_FULL,
        **QUANTITY_ARRAY_BLOCK_ATTRIBUTES
    }
    TIMESERIES_BLOCK_ATTRIBUTES_FULL = (
        AbstractResultMessage.TIMESERIES_BLOCK_ATTRIBUTES_FULL +
        TIMESERIES_BLOCK_ATTRIBUTES
    )

    # for each attributes added by this message type provide a property function to get the value of the attribute
    # the name of the properties must correspond to the names given in MESSAGE_ATTRIBUTES
    # template for one property:
    @property
    def simple_value(self) -> float:
        """TODO: Description what the simple value is."""
        return self.__simple_value

    # for each attributes added by this message type provide a property setter function to set the value of
    # the attribute the name of the properties must correspond to the names given in MESSAGE_ATTRIBUTES
    # template for one property setter:
    @simple_value.setter
    def simple_value(self, simple_value: float):
        if self._check_simple_value(simple_value):
            self.__simple_value = simple_value
        else:
            raise MessageValueError(f"Invalid value for SimpleValue: {simple_value}")

    # provide a new implementation for the "test of message equality" function
    def __eq__(self, other: Any) -> bool:
        return (
            super().__eq__(other) and
            isinstance(other, SimpleMessage) and
            self.simple_value == other.simple_value
        )

    # Provide a class method for each attribute added by this message type to check if the value is acceptable
    # These should return True only when the given parameter corresponds to an acceptable value for the attribute
    @classmethod
    def _check_simple_value(cls, simple_value: float) -> bool:
        return isinstance(simple_value, float)

    # Provide a new implementation for the class method from_json method
    # Only the return type should be changed here
    @classmethod
    def from_json(cls, json_message: Dict[str, Any]) -> Optional[SimpleMessage]:
        """TODO: description for the from_json method"""
        try:
            message_object = cls(**json_message)
            return message_object
        except (TypeError, ValueError, MessageError):
            return None


SimpleMessage.register_to_factory()

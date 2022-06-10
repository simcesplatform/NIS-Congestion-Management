# -*- coding: utf-8 -*-
# Copyright 2021 Tampere University.
# This software was developed as a part of the ProCemPlus project: https://www.interrface.eu
# This source code is licensed under the MIT license. See LICENSE in the repository root directory.
# Author(s): Mehdi Attar <mehdi.attar@tuni.fi>


'''
Contains classes related to reading the NIS data from a JSON file.
'''

# from dataclasses import dataclass

# import csv
import json


# @dataclass
# class ResourceState():
#     '''
#     Represents required attributes read from the json file.
#     '''

#     PowerBase: dict
#     DeviceId: list
#     SendingEndBus: list
#     ReceivingEndBus: list
#     Resistance: dict
#     Reactance: dict
#     ShuntAdmittance: dict
#     ShuntConductance: dict
#     RatedCurrent: dict
#     BusName: list
#     BusType: list
#     BusVoltageBase: dict

class JsonFileError(Exception):
    '''
    JsonFileNIS was unable to read the given json file.
    '''


class JsonFileNIS():
    '''
    Class for getting the network information data from a JSON file.
    '''
    COMPONENT_KEYS = set(
        'PowerBase',
        'DeviceId',
        'SendingEndBus',
        'ReceivingEndBus',
        'Resistance',
        'Reactance',
        'ShuntAdmittance',
        'ShuntConductance',
        'RatedCurrent'
    )
    BUS_KEYS = set(
        'BusName',
        'BusType',
        'BusVoltageBase'
    )
    REQUIRED_FIELDS = COMPONENT_KEYS + BUS_KEYS

    def __init__(self, file_name: str):
        '''
        Create object which uses the given json file that uses the given delimiter.
        Raises JsonFileError if file cannot be read e.g. file not found, or it is missing required attributes.
        '''
        self._file = None  # required if there is no file and the __del__ method is executed
        try:
            self._file = open(file_name, newline="", encoding="utf-8")

        except Exception as e:
            raise JsonFileError(f'Unable to read json file {file_name}: {str( e )}.')

        self._pythonComponent = json.load(self._file)

        # check that self._json.keys has required attributes
        fields = set(self._pythonComponent.keys())           # .keys are attributes of the json file
        # missing contains fields that do not exist or is empty if all fields exist.
        missing = JsonFileNIS.REQUIRED_FIELDS.difference(fields)
        if len(missing) > 0:
            raise JsonFileError(f'Resource state source json file missing required attribute: {",".join( missing )}.')

        self._component_content = {key: self._pythonComponent[key] for key in JsonFileNIS.COMPONENT_KEYS}
        self._bus_content = {key: self._pythonComponent[key] for key in JsonFileNIS.BUS_KEYS}

    def get_data(self):
        '''Return the data parsed from the JSON file.'''
        return self._component_content, self._bus_content

    def __del__(self):
        '''
        Close the json file when this object is destroyed.
        '''
        if self._file is not None:
            self._file.close()

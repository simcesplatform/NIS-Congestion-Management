# -*- coding: utf-8 -*-
# Copyright 2021 Tampere University and VTT Technical Research Centre of Finland
# This software was developed as a part of the ProCemPlus project: https://www.senecc.fi/projects/procemplus
# This software was developed as a part of EU project INTERRFACE: http://www.interrface.eu/.
#  This source code is licensed under the MIT license. See LICENSE in the repository root directory.
# Author(s): Mehdi Attar <mehdi.attar@tuni.fi>
#            Ville Heikkilä <ville.heikkila@tuni.fi>


import asyncio
# import json
# from multiprocessing import _BoundedSemaphoreType
# from typing import Any, cast, Set, Union

from tools.components import AbstractSimulationComponent
from tools.exceptions.messages import MessageError
# from tools.messages import BaseMessage
from tools.tools import FullLogger, load_environmental_variables

from Fetcher import JsonFileNIS


# import all the required messages from installed libraries
from NIS.NISBusMessage import NISBusMessage
from NIS.NISComponentMessage import NISComponentMessage

# initialize logging object for the module
LOGGER = FullLogger(__name__)

# topics
BusDataTopic = "BUS_DATA_TOPIC"
ComponentDataTopic= "COMPONENT_DATA_TOPIC"

# time interval in seconds on how often to check whether the component is still running
TIMEOUT = 2.0

# input file name
NIS_JSON_FILE = "NIS_JSON_FILE"


class NIS(AbstractSimulationComponent): # the NIS class inherits from AbstractSimulationComponent class
    """
    The NIS component is initialized in the beginning of the simulation by the platform manager.
    NIS gets its input data (NIS data) from the json file containing the bus and component data.
    the JSON structure for bus data is available:
    https://simcesplatform.github.io/energy_msg-init-nis-networkbusinfo/
    The JSON structure for component data is available :
    https://simcesplatform.github.io/energy_msg-init-nis-networkcomponentinfo/
    """

    # Constructor
    def __init__(
            self,
            component_data: dict,
            bus_data: dict):
        """
        The NIS component is initiated in the beginning of the simulation by the simulation manager
        and in every epoch, it publishes the NIS data. The NIS data is fetched from a class data called Fetcher.
        """

        super().__init__()
        self._component_data = component_data
        self._bus_data = bus_data

        # Load environmental variables for those parameters that were not given to the constructor.
        environment = load_environmental_variables(
            (ComponentDataTopic, str, "Init.NIS.NetworkComponentInfo"),
            (BusDataTopic, str, "Init.NIS.NetworkBusInfo")
        )
        self.ComponentDataTopic=environment[ComponentDataTopic]
        self.BusDataTopic=environment[BusDataTopic]
        # The easiest way to ensure that the component will listen to all necessary topics

    def clear_epoch_variables(self) -> None:
        """Clears all the variables that are used to store information about the received input within the
           current epoch. This method is called automatically after receiving an epoch message for a new epoch.

           NOTE: this method should be overwritten in any child class that uses epoch specific variables
        """
        pass

    async def process_epoch(self) -> bool:
        """
        Process the epoch and do all the required calculations.
        Returns False, if processing the current epoch was not yet possible.
        Otherwise, returns True, which indicates that the epoch processing was fully completed.
        This also indicated that the component is ready to send a Status Ready message to the Simulation Manager.
        """
        # send the output message
        # await asyncio.sleep(self._output_delay)

        # create and send NISBusMessage
        try:
            bus_message = self._message_generator.get_message(
                NISBusMessage,
                EpochNumber=self._latest_epoch,
                TriggeringMessageIds=self._triggering_message_ids,
                BusName={key: self._bus_data[key] for key in ["BusName"]},
                BusType={key: self._bus_data[key] for key in ["BusType"]},
                BusVoltageBase={key: self._bus_data[key] for key in ["BusVoltageBase"]}
            )
        except (ValueError, TypeError, MessageError) as message_error:
            # When there is an exception while creating the message, it is in most cases a serious error.
            LOGGER.error(f"{type(message_error).__name__}: {message_error}")
            await self.send_error_message("Internal error when creating bus message.")
            return False

        await self._send_message(bus_message, self.BusDataTopic)

        # create and send NISComponentMessage
        try:
            component_message = self._message_generator.get_message(
                NISComponentMessage,
                EpochNumber=self._latest_epoch,
                TriggeringMessageIds=self._triggering_message_ids,
                PowerBase={key: self._component_data[key] for key in ["PowerBase"]},
                SendingEndBus={key: self._component_data[key] for key in ["SendingEndBus"]},
                ReceivingEndBus={key: self._component_data[key] for key in ["ReceivingEndBus"]},
                DeviceId={key: self._component_data[key] for key in ["DeviceId"]},
                Resistance={key: self._component_data[key] for key in ["Resistance"]},
                Reactance={key: self._component_data[key] for key in ["Reactance"]},
                ShuntAdmittance={key: self._component_data[key] for key in ["ShuntAdmittance"]},
                ShuntConductance={key: self._component_data[key] for key in ["ShuntConductance"]},
                RatedCurrent={key: self._component_data[key] for key in ["RatedCurrent"]}
            )
        except (ValueError, TypeError, MessageError) as message_error:
            # When there is an exception while creating the message, it is in most cases a serious error.
            LOGGER.error(f"{type(message_error).__name__}: {message_error}")
            await self.send_error_message("Internal error when creating component message.")
            return False

        await self._send_message(component_message, self.ComponentDataTopic)

        # return True to indicate that the component is finished with the current epoch
        return True


    #async def general_message_handler(self, message_object: Union[BaseMessage, Any],
    #                                  message_routing_key: str) -> None:
        # the NIS component does not need to listen to any topic except SimState and Epoch.
        # Epoch and SimState messages are listened through the parent class.
    #    pass

    async def _send_message(self, MessageContent, Topic):
        await self._rabbitmq_client.send_message(
            topic_name=Topic,
            message_bytes=MessageContent.bytes())


def create_component() -> NIS:         # Factory function. making instance of the class
    """
    Creates and returns a NIS Component based on the environment variables.
    """
    env_variables = load_environmental_variables(
        (NIS_JSON_FILE, str, None )
    )
    json_file = JsonFileNIS(env_variables[NIS_JSON_FILE])
    component_content, bus_content = json_file.get_data()
    return NIS(component_content, bus_content)    # the birth of the NIS object


async def start_component():
    """
    Creates and starts a SimpleComponent component.
    """
    simple_component = create_component()

    # The component will only start listening to the message bus once the start() method has been called.
    await simple_component.start()

    # Wait in the loop until the component has stopped itself.
    while not simple_component.is_stopped:
        await asyncio.sleep(TIMEOUT)


if __name__ == "__main__":
    asyncio.run(start_component())

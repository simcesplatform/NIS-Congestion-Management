# NIS

## Introduction

NIS components to be used in SimCES.

The component publishes the network information system data (i.e., electricity network topology).

## Requirements

- python
- pip for installing requirements

Install requirements:

```bash
# optional create a virtual environment:
python3 -m venv .env
# activate it
. .env/bin/activate # *nix
.env\scripts\activate # windows.
# install required packages
pip install -r requirements.txt
```

## **Workflow of NIS**

1. NIS publishes the network information data including [bus ](https://simcesplatform.github.io/energy_msg-init-nis-networkbusinfo/)data and [component ](https://simcesplatform.github.io/energy_msg-init-nis-networkcomponentinfo/)data.

## **Epoch workflow**

In beginning of the simulation the NIS component will wait for [SimState](https://simcesplatform.github.io/core_msg-simstate/)(running) message, when the message is received component will initialize and send [Status](https://simcesplatform.github.io/core_msg-status/)(Ready) message with epoch number 0. If SimState(stopped) is received component will close down. Other message are ignored at this stage.

After startup component will begin to listen for [epoch](https://simcesplatform.github.io/core_msg-epoch/) messages. In the current implementation, it only published the network information data in the epoch 1. For other epoches other than 1, it only sends ready message when epoch starts.

If at any stage of the execution Status (Error) message is received component will immediately close down

## **Implementation details**

* Language and platform

| Programming language | Python 3.11.4                                              |
| -------------------- | ---------------------------------------------------------- |
| Operating system     | Docker version 20.10.21 running on windows 10 version 22H2 |

## **External packages**

The following packages are needed.

| Package          | Version   | Why needed                                                                                | URL                                                                                                   |
| ---------------- | --------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Simulation Tools | (Unknown) | "Tools for working with simulation messages and with the RabbitMQ message bus in Python." | [https://github.com/simcesplatform/simulation-tools](https://github.com/simcesplatform/simulation-tools) |

## Usage

The component is based on the AbstractSimulationCompoment class from the [simulation-tools](https://github.com/simcesplatform/simulation-tools)
 repository. It is configured via environment variables which include common variables for all AbstractSimulationComponent subclasses such as rabbitmq connection and component name. Environment variables specific to this component are listed below:

- NIS_JSON_FILE (required): Location of the json file which contains the electricty grid's data. Relative file paths are in relation to the current working directory.

When using a json file as input data. the file must contain the following keys: PowerBase, SendingEndBus, ReceivingEndBus, Resistance, Reactance, ShuntConductance, ShuntAddmitance, RatedCurrent, BusName, BusType, BusVoltageBase.

The component can be started with:

    python -m NIS.component

It can be also used with docker via the included dockerfile.

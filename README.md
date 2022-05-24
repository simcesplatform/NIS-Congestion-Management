# NIS
NIS components to be used in SimCES.

The component publishes the network information system data (i.e., electricity network topology) to the message broker.
## Requirements

- python 3.7
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

## Usage

The component is based on the AbstractSimulationCompoment class from the [simulation-tools](https://github.com/simcesplatform/simulation-tools)
 repository. It is configured via environment variables which include common variables for all AbstractSimulationComponent subclasses such as rabbitmq connection and component name. Environment variables specific to this component are listed below:

- NIS_JSON_FILE (required): Location of the json file which contains the electricty grid's data. Relative file paths are in relation to the current working directory.

When using a json file as inout data. the file must contain the following keys: PowerBase, SendingEndBus, ReceivingEndBus, Resistance, Reactance, ShuntConductance, ShuntAddmitance, RatedCurrent, BusName, BusType, BusVoltageBase.

The component can be started with:

    python -m NIS.component

It can be also used with docker via the included dockerfile.
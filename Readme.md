# Peblar py-modbus-api-client

## Introduction
This tool serves as a basic example how to consume the Peblar Modbus API with Python.

## Preparation
To run the project, you need the following dependencies:
  * Python3

Set up the virtual env:
  * `python -m venv venv` (see https://docs.python.org/3/tutorial/venv.html)
    * On Windows: `.\venv\Scripts\activate`
    * On Linux: `source venv/bin/activate`

Install the python dependencies with pip:
  * `pip install -r requirements.txt`

## Execute
Run the script:
`python modbus_test.py <hostname/IP>`

Example output:
```
Reading/Writing all modbus registers...
Read sEnergyTotalAddress: 0
Read sSessionEnergyAddress: 0
Read sPowerPhase1Address: 0
Read sPowerPhase2Address: Failure
Read sPowerPhase3Address: Failure
Read sPowerTotalAddress: 0
Read sVoltagePhase1Address: 232
Read sVoltagePhase2Address: Failure
Read sVoltagePhase3Address: Failure
Read sCurrentPhase1Address: 0
Read sCurrentPhase2Address: Failure
Read sCurrentPhase3Address: Failure
Read sSerialNumberAddress: 25-12-A2V-B3W
Read sProductNumberAddress: 6001-2194-0801
Read sFwIdentifierAddress: 1.6.2-PT
Read sHwIdentifierAddress: 0
Read sPhaseCountAddress: 1
Read sIndepRelayAddress: 0
Read sCurrentLimitSourceAddress: CurrentLimitSource.CHARGING_CABLE
Read sCurrentLimitActualAddress: 0
Read sModbusCurrentLimitAddress: 1
Read sForce1PhaseAddress: False
Read sWlanSignalStrenthAddress: -1000
Read sCellSignalStrenthAddress: -1000
Read sUptimeAddress: 96489
Read sCpStateAddress: A
Read sLockStateAddress: False
Read sActiveWarning1Address: 0
Read sActiveWarning2Address: 0
Read sActiveWarning3Address: 0
Read sActiveWarning4Address: 0
Read sActiveWarning5Address: 0
Read sActiveError1Address: 0
Read sActiveError2Address: 0
Read sActiveError3Address: 0
Read sActiveError4Address: 0
Read sActiveError5Address: 0
Read sModbusApiVersionMajor: 0
Read sModbusApiVersionMinor: 0
Write '1' to sModbusCurrentLimitAddress: Success
Write '1' to sForce1PhaseAddress: Failure
```

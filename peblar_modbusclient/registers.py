# Copyright (c) 2025 Prodrive Technologies New Energies B.V.
# This code is licensed under MIT license (see LICENSE for details)

from dataclasses import dataclass
from typing import Callable, Any
from pymodbus.client.mixin import ModbusClientMixin
from pymodbus.constants import Endian
from enum import Enum
from functools import partial


class CurrentLimitSource(Enum):
    UNKNOWN = 0
    FIXED_CABLE = 1
    HIGH_TEMPERATURE = 2
    INSTALLATION_LIMIT = 3
    DYNAMIC_LOAD_BALANCING = 4
    GROUP_LOAD_BALANCING = 5
    CHARGING_CABLE = 6
    OVERCURRENT_PROTECTION = 7
    HARDWARE_LIMITATION = 8
    POWER_FACTOR = 9
    OCPP_SMART_CHARGING = 10
    PHASE_IMBALANCE = 11
    LOCAL_SCHEDULED_CHARGING = 12
    SOLAR_CHARGING = 13
    CURRENT_LIMITER = 14
    LOCAL_REST_API = 15
    LOCAL_MODBUS_API = 16
    EXTERNAL_POWER_LIMIT = 17
    HOUSEHOLD_POWER_LIMIT = 18


@dataclass
class ModbusAddress:
    address: int
    size: int
    encoder: Callable[[any], bytes]
    decoder: Callable[[(list[int] | list[bool] | None)], any]


def string(val: (list[int] | list[bool] | None)) -> str:
    return ModbusClientMixin.convert_from_registers(registers=val, data_type=ModbusClientMixin.DATATYPE.STRING, word_order=Endian.BIG, string_encoding="ascii")

def integer(val: (list[int] | list[bool] | None), type: ModbusClientMixin.DATATYPE) -> int:
    return ModbusClientMixin.convert_from_registers(registers=val, data_type=type, word_order=Endian.BIG)

def float32(val: (list[int] | list[bool] | None)) -> float:
    return ModbusClientMixin.convert_from_registers(registers=val, data_type=ModbusClientMixin.DATATYPE.FLOAT32, word_order=Endian.BIG)

def boolean(val: (list[int] | list[bool] | None)) -> bool:
    data = ModbusClientMixin.convert_from_registers(registers=val, data_type=ModbusClientMixin.DATATYPE.UINT16, word_order=Endian.BIG)
    assert (data == 0) or (data == 1)
    return bool(data)

def current_source(val: (list[int] | list[bool] | None)) -> CurrentLimitSource:
    data = ModbusClientMixin.convert_from_registers(registers=val, data_type=ModbusClientMixin.DATATYPE.UINT16, word_order=Endian.BIG)
    return CurrentLimitSource(data)

def encode_int(val: int, num_registers: int):
    raw_bytes = val.to_bytes(num_registers*2, 'big')
    grouped_bytes = ([raw_bytes[i], raw_bytes[i+1]] for i in range(0, num_registers, 2))
    data = [int.from_bytes([byte[0], byte[1]], byteorder='big') for byte in grouped_bytes]
    return data


class ModbusAddresses(Enum):
    sEnergyTotalAddress = ModbusAddress(30_000, 4, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT64))
    sSessionEnergyAddress = ModbusAddress(30_004, 4, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT64))
    sPowerPhase1Address = ModbusAddress(30_008, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))
    sPowerPhase2Address = ModbusAddress(30_010, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))
    sPowerPhase3Address = ModbusAddress(30_012, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))
    sPowerTotalAddress = ModbusAddress(30_014, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))
    sVoltagePhase1Address = ModbusAddress(30_016, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))
    sVoltagePhase2Address = ModbusAddress(30_018, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))
    sVoltagePhase3Address = ModbusAddress(30_020, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))
    sCurrentPhase1Address = ModbusAddress(30_022, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))
    sCurrentPhase2Address = ModbusAddress(30_024, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))
    sCurrentPhase3Address = ModbusAddress(30_026, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))

    # Config addresses
    sSerialNumberAddress = ModbusAddress(30_050, 12, None, partial(string))
    sProductNumberAddress = ModbusAddress(30_062, 12, None, partial(string))
    sFwIdentifierAddress = ModbusAddress(30_074, 12, None, partial(string))
    sHwIdentifierAddress = ModbusAddress(30122, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))
    sPhaseCountAddress = ModbusAddress(30_092, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))
    sIndepRelayAddress = ModbusAddress(30_093, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))

    # CurrentControl addresses
    # Read
    sCurrentLimitSourceAddress = ModbusAddress(30_112, 1, None, current_source)
    sCurrentLimitActualAddress = ModbusAddress(30_113, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT32))

    # Write
    sModbusCurrentLimitAddress = ModbusAddress(40_000, 2, partial(encode_int, num_registers=1), partial(integer, type=ModbusClientMixin.DATATYPE.UINT32))
    sForce1PhaseAddress = ModbusAddress(40_002, 1, int, boolean)

    # Diagnostic addresses
    sWlanSignalStrenthAddress = ModbusAddress(30_086, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))
    sCellSignalStrenthAddress = ModbusAddress(30_088, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.INT32))
    sUptimeAddress = ModbusAddress(30_090, 2, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT32))
    sCpStateAddress = ModbusAddress(30_110, 1, None, partial(string))
    sLockStateAddress = ModbusAddress(30_111, 1, None, boolean)

    sActiveWarning1Address = ModbusAddress(30100, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))
    sActiveWarning2Address = ModbusAddress(30101, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))
    sActiveWarning3Address = ModbusAddress(30102, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))
    sActiveWarning4Address = ModbusAddress(30103, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))
    sActiveWarning5Address = ModbusAddress(30104, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))

    sActiveError1Address = ModbusAddress(30105, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))
    sActiveError2Address = ModbusAddress(30106, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))
    sActiveError3Address = ModbusAddress(30107, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))
    sActiveError4Address = ModbusAddress(30108, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))
    sActiveError5Address = ModbusAddress(30109, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))

    sModbusApiVersionMajor = ModbusAddress(30122, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))
    sModbusApiVersionMinor = ModbusAddress(30124, 1, None, partial(integer, type=ModbusClientMixin.DATATYPE.UINT16))

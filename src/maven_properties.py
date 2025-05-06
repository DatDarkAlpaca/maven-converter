from dataclasses import dataclass, field
from enum import Enum, auto


class DataType(Enum):
    SignedMSB8 = auto()
    IEEE754MSBSingle = auto()
    IEEE754MSBDouble = auto()


@dataclass
class MavenData:
    electron_density_values: list[float]         = field(default_factory=list)
    tt2000_time_values: list[int]                = field(default_factory=list)
    unix_time_values: list[float]                = field(default_factory=list)
    lower_uncertainty_values: list[float]        = field(default_factory=list)
    upper_uncertainty_values: list[float]        = field(default_factory=list)
    data_quality_values: list[float]             = field(default_factory=list)
    instrument_information_values: list[float]   = field(default_factory=list)

@dataclass
class MavenProperties:
    filename: str
    checksum: str
    filesize: int
    
    header_offset: int
    header_length: int

    electron_density_offset: int                # offset in bytes in the CDF file
    electron_density_elements: int              # amount of elements
    electron_density_data_type: DataType
    electron_density_unit: str

    tt2000_time_offset: int
    tt2000_time_elements: int
    tt2000_time_data_type: DataType
    tt2000_time_unit: str

    unix_time_offset: int
    unix_time_elements: int
    unix_time_data_type: DataType
    unix_time_unit: str

    lower_uncertainty_offset: int
    lower_uncertainty_elements: int
    lower_uncertainty_data_type: DataType
    lower_uncertainty_unit: str

    upper_uncertainty_offset: int
    upper_uncertainty_elements: int
    upper_uncertainty_data_type: DataType
    upper_uncertainty_unit: str

    data_quality_flag_offset: int
    data_quality_flag_elements: int
    data_quality_flag_data_type: DataType

    instrument_information_offset: int
    instrument_information_elements: int
    instrument_information_data_type: DataType


def get_data_type(type: str) -> DataType:
    if type.lower() == 'SignedMSB8'.lower():
        return DataType.SignedMSB8
    
    elif type.lower() == 'IEEE754MSBSingle'.lower():
        return DataType.IEEE754MSBSingle
    
    elif type.lower() == 'IEEE754MSBDouble'.lower():
        return DataType.IEEE754MSBDouble

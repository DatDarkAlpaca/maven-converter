from enum import Enum, auto


class DataType(Enum):
    SignedMSB8 = auto()
    IEEE754MSBSingle = auto()
    IEEE754MSBDouble = auto()


def get_data_type(type: str) -> DataType:
    if type.lower() == 'SignedMSB8'.lower():
        return DataType.SignedMSB8
    
    elif type.lower() == 'IEEE754MSBSingle'.lower():
        return DataType.IEEE754MSBSingle
    
    elif type.lower() == 'IEEE754MSBDouble'.lower():
        return DataType.IEEE754MSBDouble

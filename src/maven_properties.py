from dataclasses import dataclass, field
from maven_data_type import DataType


@dataclass
class MavenFieldProperties:
    name: str
    offset: int
    elements: int
    data_type: DataType
    unit: str = ''


@dataclass
class MavenProperties:
    filename: str
    checksum: str
    filesize: int
    
    header_offset: int
    header_length: int

    field_properties: list[MavenFieldProperties] = field(default_factory=list)

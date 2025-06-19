import struct
from file import load_xml_file
from maven_data_type import DataType, get_data_type
from maven_properties import MavenFieldProperties, MavenProperties

__all__ = ['read_maven_properties_file', 'parse_maven_data']


def read_maven_properties_file(filepath: str, namespace='http://pds.nasa.gov/pds4/pds/v1') -> MavenProperties:
    namespace_mapping = { 'pds': namespace }

    read_element = lambda root, element_name: root.find(f"pds:{element_name}", namespaces=namespace_mapping)
    read_all = lambda root, element_name: root.findall(f"pds:{element_name}", namespaces=namespace_mapping)

    root = load_xml_file(filepath)
    file_area_props = read_element(root, 'File_Area_Observational')
    
    # File:
    file_props = read_element(file_area_props, 'File')
    filename = read_element(file_props, 'file_name').text
    filesize = int(read_element(file_props, 'file_size').text)
    checksum = read_element(file_props, 'md5_checksum').text

    # Header:
    header_props = read_element(file_area_props, 'Header')
    header_offset = int(read_element(header_props, 'offset').text)
    header_length = int(read_element(header_props, 'object_length').text)
    
    # Fields (Arrays):
    field_property_list = []
    for field in read_all(file_area_props, 'Array'):
        name = read_element(field, 'name').text
        offset = int(read_element(field, 'offset').text)
        
        element_array = read_element(field, 'Element_Array')
        data_type = get_data_type(read_element(element_array, 'data_type').text)
        try:
            unit = read_element(element_array, 'unit').text
        except Exception:
            unit = ''
        
        axes = int(read_element(field, 'axes').text)
        if axes <= 0:
            elements = 0
        else:
            # Assumes the main axis is the first axis displayed
            main_axis = read_all(field, 'Axis_Array')[0]    
            elements = int(read_element(main_axis, 'elements').text)

        field_properties = MavenFieldProperties(
            name=name,
            offset=offset,
            elements=elements, 
            data_type=data_type,
            unit=unit
        )
        
        field_property_list.append(field_properties)


    return MavenProperties(
        filename=filename, 
        checksum=checksum, 
        filesize=filesize, 
        header_offset=header_offset,
        header_length=header_length,
        field_properties=field_property_list
    )


def __get_value_from_type(file, data_type: DataType):
    if data_type == DataType.SignedMSB8:
        return struct.unpack('b', file.read(1))[0]

    elif data_type == DataType.IEEE754MSBSingle:
        return struct.unpack('>f', file.read(4))[0]
    
    elif data_type == DataType.IEEE754MSBDouble:
        return struct.unpack('>d', file.read(8))[0]


def parse_maven_data(filepath: str, properties: MavenProperties) -> dict:
    maven_data = {}

    with open(filepath, 'rb') as maven_file:
        for field in properties.field_properties:
            field_values = []

            maven_file.seek(field.offset)
            for _ in range(field.elements):
                field_values.append(__get_value_from_type(maven_file, field.data_type))
            
            maven_data[field.name] = field_values

    return maven_data

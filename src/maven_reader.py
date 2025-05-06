import struct
from file import load_xml_file
from maven_properties import MavenProperties, MavenData, DataType, get_data_type


def read_maven_properties_file(filepath: str) -> MavenProperties:
    properties = load_xml_file(filepath)
    
    file_area_props = properties[2]

    # File:
    file_props = file_area_props[0]
    filename = file_props[0].text
    filesize = int(file_props[2].text)
    checksum = file_props[3].text

    # Header:
    header_props = file_area_props[1]
    header_offset = int(header_props[1].text)
    header_length = int(header_props[2].text)
    
    # Electron Density:
    electron_density_props = file_area_props[2]
    electron_density_offset = int(electron_density_props[2].text)
    electron_density_data_type = get_data_type(electron_density_props[6][0].text)
    electron_density_unit = electron_density_props[6][1].text
    electron_density_elements = int(electron_density_props[7][1].text)
    
    # TT2000 Time:
    tt2000_time_props = file_area_props[3]
    tt2000_time_offset = int(tt2000_time_props[2].text)
    tt2000_time_data_type = get_data_type(tt2000_time_props[6][0].text)
    tt2000_time_unit = tt2000_time_props[6][1].text
    tt2000_time_elements = int(tt2000_time_props[7][1].text)

    # Unix Time:
    unix_time_props = file_area_props[4]
    unix_time_offset = int(unix_time_props[2].text)
    unix_time_data_type = get_data_type(unix_time_props[6][0].text)
    unix_time_unit = unix_time_props[6][1].text
    unix_time_elements = int(unix_time_props[7][1].text)

    # Lower uncertainty:
    lower_uncertainty_props = file_area_props[5]
    lower_uncertainty_offset = int(lower_uncertainty_props[2].text)
    lower_uncertainty_data_type = get_data_type(lower_uncertainty_props[6][0].text)
    lower_uncertainty_unit = lower_uncertainty_props[6][1].text
    lower_uncertainty_elements = int(lower_uncertainty_props[7][1].text)

    # Upper uncertainty:
    upper_uncertainty_props = file_area_props[6]
    upper_uncertainty_offset = int(upper_uncertainty_props[2].text)
    upper_uncertainty_data_type = get_data_type(upper_uncertainty_props[6][0].text)
    upper_uncertainty_unit = upper_uncertainty_props[6][1].text
    upper_uncertainty_elements = int(upper_uncertainty_props[7][1].text)

    # Data quality flag:
    data_quality_flag_props = file_area_props[7]
    data_quality_flag_offset = int(data_quality_flag_props[2].text)
    data_quality_flag_data_type = get_data_type(data_quality_flag_props[6][0].text)
    data_quality_flag_elements = int(data_quality_flag_props[7][1].text)

    # Instrument information:
    instrument_information_props = file_area_props[8]
    instrument_information_offset = int(instrument_information_props[2].text)
    instrument_information_data_type = get_data_type(instrument_information_props[6][0].text)
    instrument_information_elements = int(instrument_information_props[7][1].text)

    return MavenProperties(
        filename, checksum, filesize, 
        header_offset, header_length, 
        electron_density_offset, electron_density_elements, electron_density_data_type, electron_density_unit,
        tt2000_time_offset, tt2000_time_elements, tt2000_time_data_type, tt2000_time_unit,
        unix_time_offset, unix_time_elements, unix_time_data_type, unix_time_unit,
        lower_uncertainty_offset, lower_uncertainty_elements, lower_uncertainty_data_type, lower_uncertainty_unit,
        upper_uncertainty_offset, upper_uncertainty_elements, upper_uncertainty_data_type, upper_uncertainty_unit,
        data_quality_flag_offset, data_quality_flag_elements, data_quality_flag_data_type,
        instrument_information_offset, instrument_information_elements, instrument_information_data_type
    )


def get_value_from_type(file, data_type: DataType):
    if data_type == DataType.SignedMSB8:
        return struct.unpack('b', file.read(1))[0]

    elif data_type == DataType.IEEE754MSBSingle:
        return struct.unpack('>f', file.read(4))[0]
    
    elif data_type == DataType.IEEE754MSBDouble:
        return struct.unpack('>d', file.read(8))[0]


def parse_maven_data(filepath: str, properties: MavenProperties) -> MavenData:
    electron_density_values = []
    tt2000_time_values = []
    unix_time_values = []
    lower_uncertainty_values = []
    upper_uncertainty_values = []
    data_quality_values = []
    instrument_information_values = []

    with open(filepath, 'rb') as maven_file:

        # Electron density:
        maven_file.seek(properties.electron_density_offset)
        for _ in range(properties.electron_density_elements):
            electron_density_values.append(get_value_from_type(maven_file, properties.electron_density_data_type))

        # TT2000 Time:
        maven_file.seek(properties.tt2000_time_offset)
        for _ in range(properties.tt2000_time_elements):
            tt2000_time_values.append(get_value_from_type(maven_file, properties.tt2000_time_data_type))

        # Unix Time:
        maven_file.seek(properties.unix_time_offset)
        for _ in range(properties.unix_time_elements):
            unix_time_values.append(get_value_from_type(maven_file, properties.unix_time_data_type))
    
        # Unix Time:
        maven_file.seek(properties.unix_time_offset)
        for _ in range(properties.unix_time_elements):
            unix_time_values.append(get_value_from_type(maven_file, properties.unix_time_data_type))
    
        # Lower uncertainty:
        maven_file.seek(properties.lower_uncertainty_offset)
        for _ in range(properties.lower_uncertainty_elements):
            lower_uncertainty_values.append(get_value_from_type(maven_file, properties.lower_uncertainty_data_type))
        
        # Upper uncertainty:
        maven_file.seek(properties.upper_uncertainty_offset)
        for _ in range(properties.upper_uncertainty_elements):
            upper_uncertainty_values.append(get_value_from_type(maven_file, properties.upper_uncertainty_data_type))

        # Data quality:
        maven_file.seek(properties.data_quality_flag_offset)
        for _ in range(properties.data_quality_flag_elements):
            data_quality_values.append(get_value_from_type(maven_file, properties.data_quality_flag_data_type))

        # Instrument information:
        maven_file.seek(properties.instrument_information_offset)
        for _ in range(properties.instrument_information_elements):
            instrument_information_values.append(get_value_from_type(maven_file, properties.instrument_information_data_type))

    return MavenData(electron_density_values, tt2000_time_values, unix_time_values, lower_uncertainty_values,
                    upper_uncertainty_values, data_quality_values, instrument_information_values)
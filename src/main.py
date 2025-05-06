import os
import sys
from pathlib import Path

from maven_reader import read_maven_properties_file, parse_maven_data
from maven_writer import write_csv_maven


ROOT_DIRECTORY = 'data'

def main():
    for dirpath, _, filenames in os.walk(ROOT_DIRECTORY):
        xml_files = [f for f in filenames if f.endswith('.xml')]

        for xml_file in xml_files:
            base_name = Path(xml_file).stem
            xml_filepath = os.path.join(dirpath, xml_file)
            cdf_filepath = os.path.join(dirpath, base_name + '.cdf')
            result_csv_filepath = os.path.join(dirpath, base_name + '.csv')

            sys.stdout.write(f"\rProcessing: {xml_filepath}, {cdf_filepath} -> {result_csv_filepath}")
            sys.stdout.flush()

            if not os.path.exists(cdf_filepath):
                return print('Error: XML file has no corresponding CDF file. Aborting.')
            
            maven_properties = read_maven_properties_file(xml_filepath)
            maven_data = parse_maven_data(cdf_filepath, maven_properties)

            write_csv_maven(result_csv_filepath, maven_data)
   

if __name__ == '__main__':
    main()

import os
import sys
from pathlib import Path

from maven_reader import read_maven_properties_file, parse_maven_data
from maven_writer import write_csv_maven

ROOT_DIRECTORY = 'data'


def run_parser_on_directory(directory: str) -> None:
    for dirpath, _, filenames in os.walk(directory):
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


def run_parser_on_file(xml_filepath: str, cdf_filepath, result_filepath) -> None:
    maven_properties = read_maven_properties_file(xml_filepath)
    maven_data = parse_maven_data(cdf_filepath, maven_properties)

    write_csv_maven(result_filepath, maven_data)


def main():
    # 1. Runs the conversion algorithm on every file on directory <directory>
    run_parser_on_directory(ROOT_DIRECTORY)

    # 2. Runs the conversion on a single file:
    # run_parser_on_file('example.xml', 'example.cdf', 'example.csv')
    

if __name__ == '__main__':
    main()

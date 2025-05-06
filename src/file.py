from xml.etree.ElementTree import Element
import xml.etree.ElementTree as et


def load_xml_file(filepath: str) -> Element:
    tree = et.parse(filepath)
    return tree.getroot()

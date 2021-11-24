import argparse
import lxml.etree as ET
from copy import deepcopy

def ParseCommandLine():
    # arg parse
    descr = '''A small utility that strips a CityGML 2.0 (XML) 
            file and serializes the result in a new CityGML (XML) 
            file. It removes appearences and generic attributes.'''
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('--input',
                        nargs='+',
                        type=str,
                        help='CityGML input file')
    parser.add_argument('--output',
                        nargs='+',
                        default='output.gml',
                        type=str,
                        help='Resulting file.')
    parser.add_argument('--remove-building-parts',
                        action='store_true',
                        help='If set, remove constistsOfBuildingPart and BuildingPart elements.')
    return parser.parse_args()

if __name__ == '__main__':
    cli_args = ParseCommandLine()
    filename = cli_args.input[0]

    # parse file
    parser = ET.XMLParser(remove_comments=True)
    parsed_file = ET.parse(filename, parser)

    # Refer to this doc for more information: https://lxml.de/api/index.html
    # in submodule lxml.etree, function strip_elements
    # Remove all elements in the namespace app
    ET.strip_elements(parsed_file,
                      '{' + parsed_file.getroot().nsmap['app'] + '}' + '*')
    # Remove all generic elements
    ET.strip_elements(parsed_file,
                      '{' + parsed_file.getroot().nsmap['gen'] + '}' + '*')
    # If remove-building-parts, get all BuildingParts and copy their content to the parent building
    if cli_args.remove_building_parts:
        for building_part in parsed_file.getroot().findall('.//{' + parsed_file.getroot().nsmap['bldg'] + '}BuildingPart'):
            building_part_copy = deepcopy(building_part)
            # get parent building, for reference the XML structure looks like this:
            # bldg:Building > bldg:consistsOfBuildingPart > bldg:BuildingPart
            building = building_part.getparent().getparent()
            # append the children of the BuildingPart to the parent building
            for child in building_part_copy:
                building.append(child)
        # Remove all bldg:constistsOfBuildingPart* elements
        ET.strip_elements(parsed_file,
                            '{' + parsed_file.getroot().nsmap['bldg'] + '}constistsOfBuildingPart' + '*')
                
    # Concerning the xml_declaration and encoding tags, refer e.g. to 
    # https://stackoverflow.com/questions/12966488/preserving-original-doctype-and-declaration-of-an-lxml-etree-parsed-xml
    parsed_file.write(cli_args.output[0],
                      xml_declaration=True,
                      encoding=parsed_file.docinfo.encoding)

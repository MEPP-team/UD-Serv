import argparse
import os
import lxml.etree as ET
from copy import deepcopy


def ParseCommandLine():
    # arg parse
    descr = """A small utility that strips a CityGML 2.0 (XML) 
            file and serializes the result in a new CityGML (XML) 
            file. It removes appearences and generic attributes."""
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument(
        "--input", required=True, type=str, help="CityGML input file."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Directory of output (created when not existant).",
    )
    parser.add_argument(
        "--output", default="output.gml", type=str, help="Resulting file."
    )
    parser.add_argument(
        "--remove-building-parts",
        action="store_true",
        help="Move constistsOfBuildingPart and BuildingPart content to parent Building.",
    )
    parser.add_argument(
        "--remove-empty-buildings",
        action="store_true",
        help="Remove Buildings which do not have any solid or surface geometry. This step will take place after --remove-building-parts if set.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    cli_args = ParseCommandLine()
    filename = cli_args.input
    geometry_list = [
        "boundedBy",
        "lod1Solid",
        "lod2Solid",
        "lod3Solid",
        "lod4Solid",
    ]

    # parse file
    parser = ET.XMLParser(remove_comments=True)
    parsed_file = ET.parse(filename, parser)

    # Refer to this doc for more information: https://lxml.de/api/index.html
    # in submodule lxml.etree, function strip_elements
    # Remove all elements in the namespace app
    ET.strip_elements(
        parsed_file, "{" + parsed_file.getroot().nsmap["app"] + "}*"
    )
    # Remove all generic elements
    ET.strip_elements(
        parsed_file, "{" + parsed_file.getroot().nsmap["gen"] + "}*"
    )
    # If remove-building-parts, get all BuildingParts and copy their content to the parent building
    if cli_args.remove_building_parts:
        for building_part in parsed_file.getroot().findall(
            ".//{" + parsed_file.getroot().nsmap["bldg"] + "}BuildingPart"
        ):
            building_part_copy = deepcopy(building_part)
            # get parent building, for reference the XML structure looks like this:
            # bldg:Building > bldg:consistsOfBuildingPart > bldg:BuildingPart
            building = building_part.getparent().getparent()
            # append the children of the BuildingPart to the parent building
            for child in building_part_copy:
                building.append(child)
        # Remove all bldg:constistsOfBuildingPart* elements
        ET.strip_elements(
            parsed_file,
            "{"
            + parsed_file.getroot().nsmap["bldg"]
            + "}consistsOfBuildingPart"
            + "*",
        )
    # If remove-empty-buildings, get all Buildings and remove them if they do not contain solids or boundary surfaces
    if cli_args.remove_empty_buildings:
        # map the Building namespace to the geometry list
        addBldgNamespace = (
            lambda tag: "{" + parsed_file.getroot().nsmap["bldg"] + "}" + tag
        )
        geometry_list = list(map(addBldgNamespace, geometry_list))
        for building in parsed_file.getroot().findall(
            ".//{" + parsed_file.getroot().nsmap["bldg"] + "}Building"
        ):
            has_geometry = False
            # If any Building children tags are in the geometry list, the
            # Building is not considered empty
            for child in building:
                if child.tag in geometry_list:
                    has_geometry = True
                    break
            # also check building parts if they have not already been removed
            if not cli_args.remove_building_parts:
                for building_part in building.findall(
                    ".//{"
                    + parsed_file.getroot().nsmap["bldg"]
                    + "}consistsOfBuildingPart"
                ):
                    for child in building_part[0]:
                        if child.tag in geometry_list:
                            has_geometry = True
                            break
                    if has_geometry:
                        break
            # if the building is considered empty, remove the cityObjectMember
            # element that contains it
            if not has_geometry:
                city_object_member = building.getparent()
                parsed_file.getroot().remove(city_object_member)

    if cli_args.output_dir:
        # Create the output directory "recusively"
        os.makedirs(cli_args.output_dir)
        output_filename = os.path.join(cli_args.output_dir, cli_args.output)
    else:
        output_filename = cli_args.output

    # Concerning the xml_declaration and encoding tags, refer e.g. to
    # https://stackoverflow.com/questions/12966488/preserving-original-doctype-and-declaration-of-an-lxml-etree-parsed-xml
    parsed_file.write(
        output_filename,
        xml_declaration=True,
        encoding=parsed_file.docinfo.encoding,
    )

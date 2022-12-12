import pprint
from typing import Dict, List

from kqs.waifu import Waifu


def show_hierarchy(relation_list: List[List[str]]) -> None:
    hierarchy: Dict[int, List[str]] = {}
    for relation in relation_list:
        admin_level = relation[1]
        if hierarchy.get(admin_level) == None:
            hierarchy[admin_level] = []
        hierarchy[admin_level].append(relation)
    pprint.pprint(hierarchy)


def extract_admin_relation(map: Waifu) -> List[List[str]]:
    admin_relation = []
    for id in map.relation_dict:
        flag_type_boundary = False
        flag_boundary_administrative = False
        admin_level = ""
        name = ""
        ref = ""
        this_relation = map.relation_dict[id]
        for key in this_relation.tags:
            if key == "type" and this_relation.tags[key] == "boundary":
                flag_type_boundary = True
            if (
                key == "boundary"
                and this_relation.tags[key] == "administrative"
            ):
                flag_boundary_administrative = True
            if (
                flag_type_boundary == True
                and flag_boundary_administrative == True
            ):
                if "admin_level" in this_relation.tags:
                    admin_level = this_relation.tags["admin_level"]
                if "name" in this_relation.tags:
                    name = this_relation.tags["name"]
                if "ref" in this_relation.tags:
                    ref = this_relation.tags["ref"]
        admin_relation.append([id, admin_level, name, ref])
    return admin_relation


def main():
    map = Waifu()
    map.read(mode="file", file_path="map.osm")
    admin_relation = extract_admin_relation(map)
    show_hierarchy(admin_relation)


if __name__ == "__main__":
    main()

import pprint

from kqs.waifu import Waifu

def main():
    map=Waifu()
    map.read(mode="file",file_path="map.osm")
    admin_relation={}
    for id in map.relation_dict:
        flag_type_boundary=False
        flag_boundary_administrative = False
        admin_level=""
        name=""
        ref=""
        this_relation = map.relation_dict[id]
        for key in this_relation.tags:
            if key=="type" and this_relation.tags[key]== "boundary":
                flag_type_boundary=True
            if key=="boundary" and this_relation.tags[key]== "administrative":
                flag_boundary_administrative=True
            if flag_type_boundary==True and flag_boundary_administrative==True:
                if "admin_level" in this_relation.tags:
                    admin_level=this_relation.tags["admin_level"]
                if "name" in this_relation.tags:
                    name=this_relation.tags["name"]
                if "ref" in this_relation.tags:
                    ref=this_relation.tags["ref"]
        if admin_relation.get(admin_level)==None:
            admin_relation[admin_level]=[]
        admin_relation[admin_level].append([id,admin_level,name,ref])
    pprint.pprint(admin_relation)


if __name__ == "__main__":
    main()
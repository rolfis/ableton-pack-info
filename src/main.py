import os
import json
import re
import utils

pack_dir = os.path.expanduser("~") + r"\Documents\Ableton\Factory Packs"

factory_packs = {
    "packs": []
}

with os.scandir(pack_dir) as packs:
    for pack in packs:
        if pack.is_dir():
            this_pack = {
                "packdisplayname": "",
                "packvendor": "",
                "packuniqueid": "",
                "packrevision": "",
                "total_size": "",
                "url": "",
                "items": []
            }

            with open(pack.path + '/' + 'Ableton Folder Info/Properties.cfg') as fp:
                metadata = fp.read()
                for match in re.finditer('PackUniqueID = \"([^\"]+)\"', metadata, re.DOTALL):
                    this_pack["packuniqueid"] = match.group(1)
                for match in re.finditer('PackDisplayName = \"([^\"]+)\"', metadata, re.DOTALL):
                    this_pack["packdisplayname"] = match.group(1)
                for match in re.finditer('PackVendor = \"([^\"]+)\"', metadata, re.DOTALL):
                    this_pack["packvendor"] = match.group(1)
                for match in re.finditer('PackRevision = ([^;]+);', metadata, re.DOTALL):
                    this_pack["packrevision"] = match.group(1)

            this_pack["total_size"] = utils.get_size_format(utils.get_directory_size(pack.path))

            with os.scandir(pack.path) as folders:
                for folder in folders:
                    if folder.is_dir() and folder.name != "Ableton Folder Info" and folder.name != "Ableton Project Info" and folder.name != "Lessons":
                        for root, d_names, f_names in os.walk(folder.path):
                            if f_names:
                                for f in f_names:
                                    this_pack["items"].append(f)

            factory_packs["packs"].append(this_pack)

print(json.dumps(factory_packs))

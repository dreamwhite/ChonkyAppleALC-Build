import os
import plistlib
import json


def find_layout_ids():

    os.chdir('Resources')

    codecs = [codec for codec in os.listdir(os.getcwd()) if not codec.endswith(
        'plist') and not codec.endswith('kext') and codec != '.DS_Store']
    final_output = {}

    for codec in codecs:
        final_output[codec] = {}
        layout_list = []

        with open(os.path.join(codec, 'Info.plist'), 'rb') as fp:
            pl = plistlib.load(fp)
        for layout in pl['Files']['Layouts']:
            layout_list.append(str(layout['Id']))
            layout_list = sorted(layout_list, key=int)

        for layout_id in layout_list:
            final_output[codec][layout_id] = ""
        for layout in pl['Files']['Layouts']:
            final_output[codec][str(layout['Id'])] = layout['Comment'] if 'Comment' in layout.keys(
            ) else 'No description available'

    return final_output

with open('codecs.json', 'w') as fp:
    json.dump(find_layout_ids(), fp, indent=4)

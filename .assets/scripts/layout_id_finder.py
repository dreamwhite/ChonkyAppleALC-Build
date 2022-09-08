import os
import plistlib
import json

from pprint import pprint
#1 cd onto Resources

def find_layout_ids(codec_name: str):

    os.chdir('Resources')

    codecs = [codec for codec in os.listdir(os.getcwd()) if not codec.endswith('plist') and not codec.endswith('kext') and codec != '.DS_Store']
    final_output = {}
    for codec in codecs:
        final_output[codec] = {}
        with open(os.path.join(codec, 'Info.plist'), 'rb') as fp:
            pl = plistlib.load(fp)
        for layout in pl['Files']['Layouts']:
            final_output[codec][layout['Id']] = layout['Comment'] if 'Comment' in layout.keys() else 'No description available'

    return final_output


with open('codecs.json', 'w') as fp:
    json.dump(find_layout_ids('CX20561'), fp, indent=4)
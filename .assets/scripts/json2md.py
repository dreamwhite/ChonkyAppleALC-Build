import json

with open('codecs.json', 'r') as f:
    json_data = json.load(f)

for k,v in json_data.items():
    with open(f'{k}.md', 'a') as codec_md:
        codec_md.write(f'# {k} Layout IDs\n\n')
        codec_md.write('| ID | Description |\n')
        codec_md.write('|---|---|\n')
        for x,y in json_data[k].items():
            codec_md.write(f'| {x} | {y} |\n')
                    

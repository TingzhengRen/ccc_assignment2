import ijson
import json
from ijson.common import IncompleteJSONError

def process_large_json(file_path):
    location_list = []

    with open(file_path, 'r') as f:
        parser = ijson.parse(f)
        current_object = {}
        current_key = None
        bbox_list = []

        try:
            for prefix, event, value in parser:
                if prefix.startswith('rows.item.doc'):
                    key = prefix.split('.')[-1]
                    if event == 'map_key':
                        current_key = value
                    elif event in ('string', 'number'):
                        if current_key == 'bbox':
                            bbox_list.append(value)
                        else:
                            current_object[current_key] = value

                        if len(bbox_list) == 4:
                            location = [float(x) for x in bbox_list]
                            text = current_object.get('text')
                            if location and text:
                                location_list.append({"location": location, "text": text})
                                current_object = {}
                                bbox_list = []
                elif prefix == 'rows.item.doc' and event == 'end_map':
                    location = [float(x) for x in bbox_list] if bbox_list else None
                    text = current_object.get('text')
                    if location and text:
                        location_list.append({"location": location, "text": text})
                    current_object = {}
        except IncompleteJSONError:
            pass

    return location_list

file_path = 'twitter-huge.json'
location_list = process_large_json(file_path)

with open("location_text.json", "w") as f:
    json.dump(location_list, f)

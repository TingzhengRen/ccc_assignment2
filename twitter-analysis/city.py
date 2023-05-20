import ijson
import json
from ijson.common import IncompleteJSONError

def process_large_json(file_path):
    city_list = []

    with open(file_path, 'r') as f:
        parser = ijson.parse(f)
        current_object = {}
        current_key = None

        try:
            for prefix, event, value in parser:
                if prefix.startswith('rows.item.doc'):
                    key = prefix.split('.')[-1]
                    if event == 'map_key':
                        current_key = value
                    elif event in ('string', 'number'):
                        current_object[current_key] = value

                        if current_key == 'full_name':
                            city = current_object.get('full_name')
                            text = current_object.get('text')
                            if city and text:
                                city_list.append({"city": city, "text": text})
                                current_object = {}
                elif prefix == 'rows.item.doc' and event == 'end_map':
                    city = current_object.get('full_name')
                    text = current_object.get('text')
                    if city and text:
                        city_list.append({"city": city, "text": text})
                    current_object = {}
        except IncompleteJSONError:
            pass

    return city_list

file_path = 'twitter-huge.json'
city_list = process_large_json(file_path)

with open("city_text.json", "w") as f:
    json.dump(city_list, f)

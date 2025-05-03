from typing import List, Type, Any
from option import Result, Option, Ok, Err # pylint: disable=unused-import

def json_to_objects(data: List[dict], cls: Type) -> Result[List[Any], str]:
    objects = []

    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each item in the JSON array must be a dictionary.")

        try:
            obj = cls(**item)
            objects.append(obj)
        except TypeError as e:
            return Err(f"Couldn't create an instance of {cls} from '{item}' due to: {e}")

    return Ok(objects)

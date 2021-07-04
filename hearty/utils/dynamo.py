from io import StringIO
from typing import Dict

from pydantic import BaseModel


class UpdateItemArguments(BaseModel):
    update_expression: str
    attribute_names: Dict[str, str]
    attribute_values: Dict[str, str]


def build_update_item_arguments(item: Dict[str, str]) -> UpdateItemArguments:
    update_expression = StringIO()
    names = {}
    values = {}

    count = 0
    for k, v in item.items():
        attr_name = f"#{k}"
        attr_value = f"val{count}"
        prefixed_value = f":{attr_value}"
        if count == 0:
            update_expression.write("SET ")
        else:
            update_expression.write(", ")

        update_expression.write(f"{attr_name} = prefixed_value")
        names[attr_name] = attr_value
        values[prefixed_value] = v

        count += 1

    arguments = UpdateItemArguments(
        update_expression=update_expression.getvalue(),
        attribute_names=names,
        attribute_values=values,
    )

    return arguments

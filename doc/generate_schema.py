import inspect
import importlib.util as imp
from pathlib import Path
from typing import Type

from pydantic import BaseModel

ROOT = "hearty"


def _build_schema_path(file: Path, cls: Type[BaseModel]) -> str:
    schema_path_parts = ["doc", "schema"]
    file_path_parts = file.parts
    for i in range(0, len(file_path_parts) - 1):
        if i == 0:
            continue
        else:
            schema_path_parts.append(file_path_parts[i])
    schema_path_parts.append("models")
    dir_path = "/".join(schema_path_parts)
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    schema_path = f"{dir_path}/{cls.__name__}.json"
    return schema_path


models_files = Path(ROOT).rglob("*models.py")
for file in models_files:
    spec = imp.spec_from_file_location("models", file)
    module = imp.module_from_spec(spec)
    spec.loader.exec_module(module)

    module_classes = inspect.getmembers(module, inspect.isclass)

    for cls_name, cls in module_classes:
        if issubclass(cls, BaseModel) and cls != BaseModel:
            schema = cls.schema_json()
            schema_file_path = _build_schema_path(file, cls)

            schema_file = open(schema_file_path, "w")
            schema_file.write(schema)
            schema_file.close()

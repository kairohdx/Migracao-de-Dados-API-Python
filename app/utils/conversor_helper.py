from dataclasses import fields, is_dataclass
from typing import Type, TypeVar

T = TypeVar("T")

def convert_dataclass(src, target_cls: Type[T]) -> T:
    if not is_dataclass(src) or not is_dataclass(target_cls):
        raise TypeError("Ambos devem ser dataclasses.")

    src_dict = src.__dict__
    target_fields = {f.name for f in fields(target_cls)}
    filtered_data = {k: v for k, v in src_dict.items() if k in target_fields}
    
    return target_cls(**filtered_data)

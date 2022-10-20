

def itemconfig(obj: object):

    from dataclasses import dataclass
    from dataclasses_json import dataclass_json, Undefined

    if not hasattr(obj, 'type'):
        raise NotImplementedError(f"Please implement '{obj.__name__}.type'")

    item_type = getattr(obj, 'type')
    if type(item_type) != int:
        item_type = int(item_type)
        setattr(obj, 'type', item_type)

    wrapped = dataclass(obj)
    return dataclass_json(wrapped, undefined=Undefined.EXCLUDE)


@itemconfig
class DefaultConfig:
    type: int = 0

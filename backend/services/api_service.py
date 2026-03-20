import enum


def enum_to_labels(enum_cls: type[enum.Enum]) -> dict[str, str]:
    return {
        item.value: item.value.replace("_", " ").title()
        for item in enum_cls
    }
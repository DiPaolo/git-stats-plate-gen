import enum


class DataType(enum.Enum):
    BYTES = 0
    LINES = 1


_TYPE_NAME = {
    DataType.BYTES: 'bytes',
    DataType.LINES: 'lines'
}


def get_data_type_name(data_type: DataType) -> str:
    if data_type not in [DataType.BYTES, DataType.LINES]:
        return 'unknown'

    return _TYPE_NAME[data_type]

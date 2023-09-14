import datetime
import enum
from typing import Optional


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


def get_output_image_filename(dt: datetime.datetime, str_template: Optional[str] = '') -> str:
    return replace_output_image_filename_template(str_template, dt)


def replace_output_image_filename_template(template: str, dt: datetime.datetime) -> str:
    allowed_directives = [
        ('Y', f'{dt.year:04}'),
        ('m', f'{dt.month:02}'),
        ('d', f'{dt.day:02}'),
        ('H', f'{dt.hour:02}'),
        ('M', f'{dt.minute:02}'),
        ('S', f'{dt.second:02}')
    ]

    out_str = template
    for item in allowed_directives:
        d = item[0]
        value = item[1]
        out_str = out_str.replace(f'%{d}', str(value))

    return out_str

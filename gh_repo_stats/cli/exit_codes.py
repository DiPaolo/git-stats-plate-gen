import enum


class ExitCode(enum.Enum):
    OK = 0
    INVALID_CMDLINE_USER = 1
    INVALID_CMDLINE_TOKEN = 2
    FAILED_COLLECT_STATS = 3

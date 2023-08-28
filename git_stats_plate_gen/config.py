class Defaults(object):
    _instance = None

    _use_cache = True
    _out_image_path = '.'
    _out_image_base_name = 'github_lang_stats-%Y_%m_%d-%H_%M_%S.png'
    _min_percent = 1.0

    _image_width = 1280
    _image_height = 720

    def __init__(self):
        pass

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            raise RuntimeError(f'{cls.__name__} assumed to be a singleton')
        return cls._instance

    @property
    def use_cache(self) -> bool:
        return self._use_cache

    @property
    def out_image_path(self) -> str:
        return self._out_image_path

    @property
    def out_image_base_name(self) -> str:
        return self._out_image_base_name

    @property
    def min_percent(self) -> float:
        return self._min_percent

    @property
    def image_width(self) -> int:
        return self._image_width

    @property
    def image_height(self) -> int:
        return self._image_height


class Config(object):
    _instance = None

    _defaults = Defaults()

    _is_debug = False

    _organization_name = "DiPaolo"
    _organization_domain = 'dipaolo.dev'
    _application_name = 'Git Stats Plate Generator'
    _application_name_lowercase = 'git_stats_plate_gen'

    _internal_image_type = 'png'

    def __init__(self):
        pass

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            raise RuntimeError(f'{cls.__name__} assumed to be a singleton')
        return cls._instance

    @property
    def defaults(self) -> Defaults:
        return self._defaults

    @property
    def is_debug(self) -> bool:
        return self._is_debug

    @property
    def max_repos_to_process(self) -> int:
        return 5 if self._is_debug else 2 ** 32  # applied in DEBUG only

    @property
    def organization_name(self) -> str:
        return self._organization_name

    @property
    def organization_domain(self) -> str:
        return self._organization_domain

    @property
    def application_name(self) -> str:
        return self._application_name

    @property
    def application_name_lowercase(self) -> str:
        return self._application_name_lowercase

    @property
    def internal_image_type(self) -> str:
        return self._internal_image_type


config = Config()

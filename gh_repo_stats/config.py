DEBUG=False
MAX_REPOS_TO_PROCESS = 5 if DEBUG else 2**32  # applied in DEBUG only

ORGANIZATION_NAME = "DiPaolo"
ORGANIZATION_DOMAIN = 'dipaolo.dev'
APPLICATION_NAME = 'gh-repo-stats'
APPLICATION_NAME_LOWERCASE = 'gh_repo_stats'

# defaults
DEFAULT_USE_CACHE = True
DEFAULT_OUT_IMAGE_BASE_NAME = 'github_lang_stats'
DEFAULT_MIN_PERCENT = 1.0

# image
DEFAULT_IMAGE_WIDTH = 1280
DEFAULT_IMAGE_HEIGHT = 720
INTERNAL_IMAGE_TYPE = 'png'

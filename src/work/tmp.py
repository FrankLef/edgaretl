import sys
from pathlib import Path
sys.path.insert(1, str(Path.cwd()))  # noqa
from src.edgar import registry
path = Path.home().parent.joinpath('Public', 'MyPy',
                                   'data', 'edgar', 'xbrlrss', '2020')
print(path)

path = Path(registry.rss_path(0))
print(type(path))
print(path)
print(type(str(path)))
print(str(path))

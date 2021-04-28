from pathlib import Path
import feedparser

a_path = Path(__file__).parent.resolve().joinpath('data')
if not a_path.exists:
    msg = f"Invalid path.\n{a_path}"
    raise FileNotFoundError(a_path)

the_files = a_path.glob(pattern='**/*')
files = [x for x in the_files if x.is_file()]

msg = f"print the files of\n{a_path}"
print(msg)
for f in files:
    print(f)

p = feedparser.parse(files[0])
print(p['feed']['title'])

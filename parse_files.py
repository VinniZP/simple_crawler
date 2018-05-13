import re

from simple_crawl.helpers import get_and_write

url_matcher = re.compile(
    '(?:url\(|<(?:link|script|img|div|a)[^>]+(?:src|srcset|href|data-src)\s*=\s*)(?![\'"]?(?:data|http))[\'"]?([^\'"\)\s>]+)', )
allowed = ['jpg', 'jpeg', 'png', 'gif', 'css', 'js', 'ico', 'woff', 'svg', 'ttf']

def parse_files(text, base_path='.', base_url=None):
    results = url_matcher.findall(text)

    for file in results:
        if file.startswith('//'):
            continue
        ext = file.split('.')[-1]
        if not ext in allowed:
            continue
        res = get_and_write(file, base_path, base_domain=base_url)
        ext = file.split('.')[-1]
        if ext in ['css', 'js']:
            # file_content = get_file(file, base_path)
            parse_css(str(res), file=file, base_path=base_path, base_url=base_url)
        if res:
            print('{} downloaded'.format(file))
        else:
            print('{} ERROR'.format(file))


def parse_css(content, file, base_path, base_url=None):
    results = url_matcher.findall(content)
    res = set()
    for r in results:
        res.add(r.split('?')[0])
    for file in res:
        ext = file.split('.')[-1]
        if not ext in allowed:
            continue
        print(file)
        # if file.startwith('/'):
        #     pass
        # else:

        # next_path = os.path.join(path, file)
        get_and_write(file, base_path, base_domain=base_url)

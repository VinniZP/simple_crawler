import os
import pathlib
import requests
import urllib.parse


def create_dir(path):
    if not os.path.exists(path):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def write_file(path, content, rewrite=False):
    if os.path.exists(path):
        if rewrite:
            os.remove(path)
        else:
            return False
    create_dir(os.path.dirname(path))
    type = 'wb+'
    if isinstance(content, str):
        type = 'w+'
    with open(path, type) as f:
        f.write(content)
        f.close()
    return True


def get_file(file, base_path):
    path = os.path.join(base_path, file)
    f = open(path)
    content = f.read()
    f.close()
    return content


def get_and_write(url, base_path='.', base_domain=None, rewrite=False):
    if url.startswith('/'):
        url = url[1:]
    file_url = url
    if base_domain:
        file_url = urllib.parse.urljoin(base_domain, url)
    path = os.path.realpath(os.path.join(base_path, url))
    if os.path.exists(path) and not url.split('.')[-1] == 'css':
        if rewrite:
            os.remove(path)
        else:
            return True
    r = get_request(file_url)
    if r.status_code == 200:
        content = r.content
        write_file(path, content, rewrite=True)
        return r.content
    else:
        print('FAILED to load {}'.format(url))



def get_request(url):
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    headers = requests.utils.default_headers()

    headers.update(
        {
            'User-Agent': ua
        }
    )

    return requests.get(url, headers=headers)

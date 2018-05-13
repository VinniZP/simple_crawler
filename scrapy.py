#!/usr/bin/env python
import optparse
import os
from urllib.parse import urlparse

from simple_crawl.helpers import create_dir, write_file, get_request
from simple_crawl.parse_files import parse_files


#


def main():
    p = optparse.OptionParser()
    p.add_option('--site', '-s')
    p.add_option('--out', '-o')
    options, arguments = p.parse_args()
    if not options.site or not (options.site.startswith('http') and options.site[-1] == '/'):
        raise Exception('Site is invalid. Valid - http://example.com/')

    o = urlparse(options.site)

    output = o.netloc
    if options.out:
        output = options.out

    result_dir = 'res/{}'.format(output)

    result_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), result_dir)

    r = get_request(options.site)

    create_dir(result_dir)

    write_file("%s/index.html" % result_dir, r.text, rewrite=True)

    parse_files(r.text, result_dir, base_url=options.site)


if __name__ == '__main__':
    main()

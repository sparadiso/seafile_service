#coding: UTF-8

import os
import sys
import ConfigParser


def main():
    cfg = ConfigParser.ConfigParser()
    seafile_conf_dir = os.environ['SEAFILE_CONF_DIR']
    seafile_conf = os.path.join(seafile_conf_dir, 'seafile.conf')
    cfg.read(seafile_conf)

    sections_map =  {
        'blocks': 'block_backend',
        'fs': 'fs_object_backend',
        'commits': 'commit_object_backend',
    }

    backends = {}
    for name, section in sections_map.iteritems():
        if cfg.has_option(section, 'name'):
            backend_name = cfg.get(section, 'name')
        else:
            backend_name = 'fs'
        backends[name] = backend_name

    if any([ bend == 's3' for bend in backends.values() ]):
        print 's3'
        return

    if any([ bend == 'ceph' for bend in backends.values() ]):
        print 'ceph'
        return

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        sys.stderr.write(str(e))
        sys.stderr.flush()

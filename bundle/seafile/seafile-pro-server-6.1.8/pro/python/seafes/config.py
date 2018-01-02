#coding: UTF-8

import os
import ConfigParser
import logging

logger = logging.getLogger('seafes')

SUPPORTED_LANGS = (
    "arabic",
    "armenian",
    "basque",
    "brazilian",
    "bulgarian",
    "catalan",
    "chinese",
    "cjk",
    "czech",
    "danish",
    "dutch",
    "english",
    "finnish",
    "french",
    "galician",
    "german",
    "greek",
    "hindi",
    "hungarian",
    "indonesian",
    "italian",
    "norwegian",
    "persian",
    "portuguese",
    "romanian",
    "russian",
    "spanish",
    "swedish",
    "turkish",
    "thai"
)



class SeafesConfig(object):
    def __init__(self):
        if 'SEAFILE_CENTRAL_CONF_DIR' in os.environ:
            confdir = os.environ['SEAFILE_CENTRAL_CONF_DIR']
        else:
            confdir = os.environ['SEAFILE_CONF_DIR']
        self.seafile_conf = os.path.join(confdir, 'seafile.conf')
        self.seafile_dir = os.environ['SEAFILE_CONF_DIR']

        self.host = '127.0.0.1'
        self.port = 9200
        self.index_office_pdf = False
        self.text_size_limit = 100 * 1024 # 100 KB
        self.office_size_limit = 10 * 1024 * 1024 # 10 MB
        self.debug = False
        self.lang = ''

        events_conf = os.environ.get('EVENTS_CONFIG_FILE', None)
        if not events_conf:
            raise Exception('EVENTS_CONFIG_FILE not set in os.environ')

        self.load_seafevents_conf(events_conf)

    def print_config(self):
        logger.info('index text of office and pdf files: %s',
                    'yes' if self.index_office_pdf else 'no')

    def load_seafevents_conf(self, events_conf):
        defaults = {
            'index_office_pdf': 'false',
            'external_es_server': 'false',
            'es_host': '127.0.0.1',
            'es_port': '9200',
            'debug': 'false',
            'lang': '',
        }

        cp = ConfigParser.ConfigParser(defaults)
        cp.read(events_conf)

        section_name = 'INDEX FILES'

        index_office_pdf = cp.getboolean(section_name, 'index_office_pdf')

        external_es_server = cp.getboolean(section_name, 'external_es_server')
        host = '127.0.0.1'
        port = 9200
        if external_es_server:
            host = cp.get(section_name, 'es_host')
            port = cp.getint(section_name, 'es_port')
            if port == 9500:
                # Seafile pro server earlier than 6.1.0 uses elasticsearch
                # thrift api. In Seafile Pro 6.1.0 we upgrade ES to 2.x, which
                # no longer supports thirft, thus we have to use elasticsearch
                # http api.
                port = 9200


        lang = cp.get(section_name, 'lang').lower()

        if lang:
            if lang not in SUPPORTED_LANGS:
                logger.warning('[seafes] invalid language ' + lang)
                lang = ''
            else:
                logger.info('[seafes] use language ' + lang)

        self.index_office_pdf = index_office_pdf
        self.host = host
        self.port = port

        self.debug = cp.getboolean(section_name, 'debug')
        self.lang = lang

seafes_config = SeafesConfig()

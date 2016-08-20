#! /usr/bin/env python3
import hashlib
import json
import logging
import sys

import lxml.etree
import requests

AMO_ADDON_URL = 'https://services.addons.mozilla.org/en-US/firefox/api/1.5/addon/%i'
AMO_XPATH_INSTALL = '/addon/install[not(@status="Beta")]'

session = requests.Session()
logging.basicConfig(level=logging.DEBUG)


class DownloaderAmo():
    @classmethod
    def download(cls, amoid) -> bytes:
        amo_response = session.get(AMO_ADDON_URL % amoid).content
        amo_xml = lxml.etree.fromstring(amo_response)

        # Extract data from XML
        install_url, install_hash = cls._select_install_option_by_os(amo_xml)

        # Download add-on content
        response = session.get(install_url).content

        # Check hash
        if cls._check_hash(install_hash, response):
            return response
        else:
            logging.error('Hash did not match downloaded content. Aborting.')
            raise Exception('Hash of add-on content did not match listing.')

    @classmethod
    def _select_install_option_by_os(cls, amo_xml) -> (str, str):
        install_files = amo_xml.xpath(AMO_XPATH_INSTALL)
        os_name = cls._get_os_name()

        for node in install_files:
            if node.get('os') == 'ALL' or node.get('os') == os_name:
                return (node.text, node.get('hash'))

        raise Exception('Could not find a suitable install file')

    @classmethod
    def _check_hash(cls, expected_hash, content):
        hash_type, hash_digest = cls._extract_hash(expected_hash)
        if hash_digest == hash_type(content).hexdigest():
            return True
        return False

    @classmethod
    def _extract_hash(cls, expected_hash) -> (object, str):
        if expected_hash.startswith('sha256:'):
            return (hashlib.sha256, expected_hash[len('sha256:'):])
        else:
            raise Exception('Uknown hash type provided: %s' % expected_hash)

    @classmethod
    def _get_os_name(cls) -> str:
        if sys.platform.startswith('linux'):
            return 'Linux'
        elif sys.platform.startswith('win32'):
            return 'WINNT'
        elif sys.platform.startswith('darwin'):
            return 'Darwin'
        else:  # Assume it's Linux or Linux-like
            return 'Linux'


class DownloaderUrl():
    @classmethod
    def download(cls, url) -> bytes:
        response = session.get(url)
        return response.content


def save_addon_file(addon_name, file_content):
    logging.debug('Saving add-on "%s" to file.' % addon_name)
    file_name = '%s.xpi' % (addon_name.lower().replace(' ', '_'))
    with open(file_name, 'wb') as fp:
        fp.write(file_content)


if __name__ == '__main__':
    with open('addon-list.json') as fp:
        addons = json.load(fp)

    for addon in addons:

        logging.info('Downloading %s' % addon['name'])

        if addon['source'] == 'amo':
            logging.debug('Using AMO as the download source')
            file_content = DownloaderAmo.download(addon['amoid'])
            save_addon_file(addon['name'], file_content)
        elif addon['source'] == 'url':
            logging.debug('Using URL as the download source')
            file_content = DownloaderUrl.download(addon['url'])
            save_addon_file(addon['name'], file_content)
        else:
            logging.debug('Uknown download source provided')
            raise Exception('Unknown add-on source.')

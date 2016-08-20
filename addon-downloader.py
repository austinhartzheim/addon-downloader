#! /usr/bin/env python3
import hashlib
import json
import logging

import lxml.etree
import requests

AMO_ADDON_URL = 'https://services.addons.mozilla.org/en-US/firefox/api/1.5/addon/%i'
AMO_XPATH_ALLOS_INSTALL = '/addon/install[not(@status="Beta")][@os="ALL"]'

session = requests.Session()
logging.basicConfig(level=logging.DEBUG)


class DownloaderAmo():
    @classmethod
    def download(cls, amoid) -> bytes:
        amo_response = session.get(AMO_ADDON_URL % amoid).content
        amo_xml = lxml.etree.fromstring(amo_response)

        # Extract data from XML
        install_files = amo_xml.xpath(AMO_XPATH_ALLOS_INSTALL)
        if len(install_files) == 0:
            logging.error('No install could be found for this add-on.')
            raise Exception('Could not find an install option for this add-on')
        if len(install_files) > 1:
            logging.warn('Multiple install options found. Choosing the first.')

        install_url = install_files[0].text
        content_hash = install_files[0].get('hash')

        # Download add-on content
        response = session.get(install_url).content

        # Check hash
        if cls._check_hash(content_hash, response):
            return response
        else:
            logging.error('Hash did not match downloaded content. Aborting.')
            raise Exception('Hash of add-on content did not match listing.')

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

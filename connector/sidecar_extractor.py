import os
import shutil
import logging

from pyclowder.extractors import Extractor
from pyclowder.utils import CheckMessage
import pyclowder.files


class WorkbenchSidecar(Extractor):
    def __init__(self):
        Extractor.__init__(self)

        # parse command line and load default logging configuration
        self.setup()

        # setup logging for the exctractor
        logging.getLogger('pyclowder').setLevel(logging.DEBUG)
        logging.getLogger('__main__').setLevel(logging.DEBUG)

    # Check whether dataset already has metadata
    def check_message(self, connector, host, secret_key, resource, parameters):
        return CheckMessage.bypass

    def process_message(self, connector, host, secret_key, resource, parameters):
        logger = logging.getLogger('__main__')

        home_dir = os.getenv('NDSLABS_HOME', "/home/worksman")
        type = resource["type"]

        if type=="file":
            dest = os.path.join(home_dir, resource["name"])
            logger.info("Downloading %s " % dest)

            url = '%sapi/files/%s?key=%s' % (host, resource['id'], secret_key)
            result = connector.get(url, stream=True, verify=connector.ssl_verify if connector else True)
            try:
                with open(dest, "wb") as outputfile:
                    for chunk in result.iter_content(chunk_size=10*1024):
                        outputfile.write(chunk)
            except Exception:
                raise

        elif type=="dataset":
            for f in resource["files"]:
                dest = os.path.join(home_dir, f["filename"])
                logger.info("Downloading %s " % dest)

                url = '%sapi/files/%s?key=%s' % (host, f['id'], secret_key)
                result = connector.get(url, stream=True, verify=connector.ssl_verify if connector else True)
                try:
                    with open(dest, "wb") as outputfile:
                        for chunk in result.iter_content(chunk_size=10*1024):
                            outputfile.write(chunk)
                except Exception:
                    raise

if __name__ == "__main__":
    extractor = WorkbenchSidecar()
    extractor.start()
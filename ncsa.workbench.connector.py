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
        # TODO: Return bypass and download it directly to destination ourselves
        return CheckMessage.bypass

    def process_message(self, connector, host, secret_key, resource, parameters):
        logger = logging.getLogger('__main__')

        home_dir = os.getenv('NDSLABS_HOME', "/home/worksman")
        secret_key = os.getenv('SECRET_KEY', secret_key)

        headers = {'X-API-KEY': secret_key}
        file_id = resource['id']

        # TODO: Need to determine this from resource object
        type="file"

        if type=="file":
            dest = os.path.join(home_dir, resource["name"])
            logger.info("Downloading %s " % dest)
            
            #version = 1
            #dataset_id = resource['dataset_id']
            url = f'{host}api/v2/files/{file_id}?increment=false'   # &dataset_id={dataset_id}'

            result = connector.get(url, stream=True, headers=headers, verify=connector.ssl_verify if connector else True)
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

                url = f'{host}api/v2/files/{file_id}?increment=false'
                result = connector.get(url, stream=True, headers=headers, verify=connector.ssl_verify if connector else True)
                try:
                    with open(dest, "wb") as outputfile:
                        for chunk in result.iter_content(chunk_size=10*1024):
                            outputfile.write(chunk)
                except Exception:
                    raise

if __name__ == "__main__":
    extractor = WorkbenchSidecar()
    extractor.start()

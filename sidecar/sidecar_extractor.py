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
        return CheckMessage.download

    def process_message(self, connector, host, secret_key, resource, parameters):
        logger = logging.getLogger('__main__')

        home_dir = os.getenv('NDSLABS_HOME', "/home/worksman")

        for p in resource["local_paths"]:
            # TODO: Include dataset name as intermediary
            dest = os.path.join(home_dir, resource["name"])
            logger.debug("Shoveling %s to %s" % (p, dest))

            # TODO: Add parameter for the path to send the data (avoid ../../..)

            if p.startswith("/tmp/"):
                os.rename(p, os.path.join(home_dir, resource["name"]))
                # File name too long: '/tmp/tmpasfprs39.py' -> '/home/worksman/¡ ¢ £ ¤ ¥ ¦ § ¨ © ª « ¬ \xad ® ¯ ° ± ² ³ ´ µ ¶ · ¸ ¹ º » ¼ ½ ¾ ¿ À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï Ð Ñ Ò Ó Ô Õ Ö × Ø Ù Ú Û Ü Ý Þ ß à á â ã ä å æ ç è é ê ë ì í î ï ð ñ ò ó ô õ ö ÷ ø ù ú û ü ý þ ÿ.py'
                # TODO: pyclowder tries to delete tmp file, but copying seems unnecessary here so should look at pyc
                logger.info("Downloaded %s " % dest)
            else:
                # NOTE: Other workbench containers will need this same directory path accessible for symlinks to work.
                os.symlink(p, dest)
                logger.info("Symlinked %s" % dest)

if __name__ == "__main__":
    extractor = WorkbenchSidecar()
    extractor.start()
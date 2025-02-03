# V2/utils.py
import logging

def setup_logger():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("V2/log/Logger.log"),  # Dosya yolunu güncelle
                            logging.StreamHandler()
                        ])
    return logging.getLogger()

logger = setup_logger()
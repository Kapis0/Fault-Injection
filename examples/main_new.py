import argparse
import logging
from sdinjection.configuration import Configuration


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser(description='sd injection')
    parser.add_argument('config_file', metavar='CONFIG_FILE', type=str, default="conf/config.json",
                        help='the configuration file')

    args = parser.parse_args()
    logging.info("using ", args.config_file, " as configuration file")
    # Usa il modulo configuration per leggere il file config.json
    conf = Configuration(args.config_file)
    conf.load()

    # Monta la partizione
    # Crea gli scheduler
    # Carica gli eventi
    # Fai partire gli eventi
    # smonta/monta la partizione
    # esegui  e2fsck se il montaggio non è andato a buon fine
    pass
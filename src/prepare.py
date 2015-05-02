from diethack._storage import rebuildCache
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)-8s %(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.INFO)
    rebuildCache()

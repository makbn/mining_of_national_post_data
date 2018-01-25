import pandas as pd
import logging
import pickle
from os.path import join, isfile

logger = logging.getLogger(__name__)


class path_len:
    def __init__(self):
        data_path = 'data'
        exchange_in_path = join(data_path, 'exchange_in.csv')
        exchange_out_path = join(data_path, 'exchange_out.csv')
        self.exchanges = {}

        self.exchange_in_csv = pd.read_csv(exchange_in_path)
        self.exchange_out_csv = pd.read_csv(exchange_out_path)

        exchanges_path = join(data_path, 'exchanges.pkl')
        if isfile(exchanges_path):
            logger.info('Loading from file...')
            with open(exchanges_path, 'rb') as dates_file:
                self.exchanges = pickle.load(dates_file)
        else:
            logger.info('Computing data')

            for index, row in self.exchange_in_csv.iterrows():
                if row[0] in self.exchanges.keys():
                    self.exchanges.get(row[0], []).append(row)
                else:
                    row_array = [row]
                    self.exchanges[row[0]] = row_array
            logger.info('exchange_in data read completely!')

            for index, row in self.exchange_out_csv.iterrows():
                if row[0] in self.exchanges.keys():
                    self.exchanges.get(row[0], []).append(row)
                else:
                    row_array = [row]
                    self.exchanges[row[0]] = row_array
            logger.info('exchange_out data read completely!')

            for key, value in self.exchanges.items():
                value.sort(key=lambda x: x[2])

            logger.info('exchanges data sorted completely!')

            with open(exchanges_path, 'wb') as exchanges_file:
                pickle.dump(self.exchanges, exchanges_file)
            logger.info('exchanges data saved on exchanges.pkl!')

    def get_path_len(self, parcel_code):
        assert parcel_code in self.exchanges.keys(), "parcel coed is invalid!"


if __name__ == '__main__':
    logging.basicConfig(filename='logs/path_len.log',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    a = path_len()

import pandas as pd
from yahoo_finance import Share
import pickle
import os


def data_preparation(beta_index_list,start_date,end_date):
    beta_index_container = []
    if not os.path.exists('index_data'):
        os.makedirs('index_data')
    for i in beta_index_list:
        beta_index = None
        file_path = os.path.join(os.path.abspath('./index_data'), '_'.join([i,start_date,end_date]))
        if os.path.exists(file_path):
            print 'retrieving ' + i + ' from local file'
            with open(file_path,'r') as input:
                beta_index = pickle.load(input)
        else:

            print 'retrieving ' + i + ' from yahoo'
            beta_index = pd.DataFrame(Share(i).get_historical(start_date,end_date))
            beta_index.index = beta_index['Date']
            beta_index.columns = beta_index.columns + '_' + i
            pickle.dump(beta_index, open(file_path,'w'))

        beta_index_container.append(beta_index[['Close' + '_' + i]])

    return pd.concat(beta_index_container,axis=1)


if __name__ == '__main__':
    beta_index_list = ['XIV','VXX','SPY','CRTO']
    start_date = '2014-12-01'
    end_date = '2017-03-01'
    rst = data_preparation(beta_index_list,start_date,end_date)
    print str(len(rst) - len(rst.dropna())) + ' lines are removed'

    rst = rst.iloc[::-1]

    import matplotlib.pyplot as plt
    plt.figure()
    for i in rst.columns:
        plt.plot(rst[i])
    #plt.plot(rst[rst.columns[1]])
    plt.legend([x for x in rst.columns],loc='upper left')
    plt.show()
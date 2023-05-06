import pandas as pd
import matplotlib.pyplot as plt

class Standardizer():
    def __init__(self, csv_path):
        self.csv_path = csv_path
    def barPlot(self):
        df = pd.read_csv(fr'{self.csv_path}')
        price_column = df['bidding_price'].values
        print(price_column)
        value_dict = {}
        for price in price_column:
            try:
                amount = float(price.lower().replace('$', '').replace('free', '0'))
                if amount == 0.0:
                    value_dict['0'] = value_dict.get('0', 0)+1
                elif 0.0 < amount < 1000:
                    value_dict['1 - 1000'] = value_dict.get(amount, 0)+1
                elif 1000 < amount < 2000:
                    value_dict['1000 - 2000'] = value_dict.get(amount, 0)+1
                else:
                    value_dict['>= 2000'] = value_dict.get(amount, 0)+1
            except:
                pass
            # print(value_dict)

        plt.figsize=(14,8)
        plt.title("Bidding Cost Range")
        plt.bar(list(value_dict.keys()), list(value_dict.values()))
        plt.savefig('standardizer.jpg')




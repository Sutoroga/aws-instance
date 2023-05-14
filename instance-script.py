import csv
import matplotlib.pyplot as plt
import boto3

class BankData:
    DATA_SRC = '{valcode}_rate_2021.csv'

    def __init__(self, valcode):
        self.valcode = valcode
        self.data_src = BankData.DATA_SRC.format(valcode=valcode)
        self.exchangedate_array, self.rate_array = BankData.read_from_csv(self.data_src)

    @staticmethod
    def read_from_csv(file_name):
        try:
            with open(file_name, 'r', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # skip header row
                exchangedate_array = []
                rate_array = []
                for row in reader:
                    if len(row) == 2:
                        exchangedate_array.append(row[0])
                        rate_array.append(float(row[1]))
                return exchangedate_array, rate_array
        except:
            print(f'Error reading file {file_name}')
            return [], []

    def draw_diagram(self):
        title = f'Exchange rate 2021 ({self.valcode})'
        plt.plot(self.exchangedate_array, self.rate_array)
        plt.xlabel('x - exchange date')
        plt.ylabel('y - rate')
        plt.title(title)
        plt.savefig(f'{self.valcode}.png')




def main():
    valcode = input("Enter valcode (usd/eur): ")
    s3 = boto3.client('s3')
    s3.download_file('lab2-e2c-1', f'{valcode}_rate_2021.csv', f'{valcode}_rate_2021.csv')

    bank_data = BankData(valcode)
    bank_data.draw_diagram()
    s3.upload_file(f'{valcode}.png', 'lab2-e2c-1', f'{valcode}.png')



if __name__ == '__main__':
    main()

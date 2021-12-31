import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import itertools as it
import numpy as np
import sqlite3

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)


class partition:

    def __init__(self, df, feedback: str, groupby: str, target: str, parts: int):
        self.df = df
        self.feedback = feedback
        self.groupby = groupby  # column
        self.target = target
        self.parts = parts

    def means(self):
        means = []
        unique = self.df.Condition.unique()
        personal_data = self.df.groupby(self.groupby)
        bin_counter = 0
        for groups in unique:
            data = personal_data[self.target].get_group(groups)
            data = np.array(data)
            data = np.array_split(np.array(data), self.parts)
            bin_counter = 0
            for i in data:
                bin_counter += 1
                means.append({f'{bin_counter}':
                                  {f'{self.feedback}_{groups}': np.mean(i)}})
        return pd.DataFrame(means)


def main():
    # mean.update({f'{self.feedback}_{unique}': np.mean(unique_groups, axis=0)})

    with sqlite3.connect('RT_Data.db') as connection:
        # tables = pd.read_sql('SELECT * FROM sqlite_master ', connection)

        personal_data = pd.read_sql('SELECT * FROM FB_Personal', connection)  # personal_data.Condition.unique() # ['fb_uni' 'nfb_uni' 'fb_bi' 'nfb_bi']
        process_data = pd.read_sql('SELECT * FROM FB_Process', connection)

        personal_data = partition(df=personal_data, feedback='personal', groupby='Condition', target='Mean', parts=5)
        process_data = partition(df=process_data, feedback='process', groupby='Condition', target='Mean', parts=5)
        print(personal_data.means())


if __name__ == '__main__':
    main()

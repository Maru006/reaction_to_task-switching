import pandas as pd
import logging
import re
import numpy as np
import itertools
from matplotlib import pyplot as plt
import seaborn as sns

# pd.set_option('display.max_rows', 1000)
# pd.set_option('display.max_columns', 1000)
# pd.set_option('display.width', 1000)
logging.basicConfig(level=logging.DEBUG, # helps debug visualizations later in the app process.
                    format='%(funcName)s :: %(message)s')


class manipulate:

    def __init__(self, url, sheet):
        self.url = url
        self.sheet = sheet

    def data(self):
        sheets = pd.read_excel(self.url, sheet_name=self.sheet)
        return sheets

    def process_type(self):  # condition = feedback type.
        sheets = pd.read_excel(self.url, sheet_name=self.sheet)
        sheets.columns = sheets.columns.str.replace('Personal feedback', 'removed')
        for column in sheets.columns:
            try:
                task_feedback = re.findall(r'[Pp]rocess', column)
                trait_feedback = re.findall(r'[Pp]ersonal', column)
                for match in task_feedback or trait_feedback:
                    logging.info(f'In {self.sheet} sheet, {match} was found')
                    if match == 'process':
                        return 'process'
                    if match == 'personal':
                        return 'personal'
                    if not task_feedback or trait_feedback:
                        continue
            except TypeError:  # instances columns contain an int
                continue

    def process_variables(self, argument): # condition = task conditions.
        data = pd.read_excel(self.url, sheet_name=self.sheet)
        data = pd.concat([data.iloc[2:102], data.iloc[107:157]]).reset_index()
        fb = data.loc[0:99, :].reset_index()
        nfb = data.loc[100:155, :].reset_index()

        variables = {'fb': data.loc[0:99, :].reset_index(),
                     'nfb': data.loc[100:155, :].reset_index(),

                     'bi': data.loc[np.where(data['Unnamed: 24'] != ' ')],
                     'uni': data.loc[np.where(data['Unnamed: 25'] != ' ')],

                     'fb_bi': fb.loc[np.where(fb['Unnamed: 24'] != ' ')],
                     'fb_uni': fb.loc[np.where(fb['Unnamed: 25'] != ' ')],

                     'nfb_bi': nfb.loc[np.where(nfb['Unnamed: 24'] != ' ')],
                     'nfb_uni': nfb.loc[np.where(nfb['Unnamed: 25'] != ' ')],
                     }
        if argument in variables:
            return variables[argument]
        else:
            logging.warning(f'{argument} not found in specified variables')


def main():
    # isolating relevant sheets from the excel database.
    ID = []
    sheets = pd.read_excel('RawData.xlsx', None)
    sheet = list(sheets.keys())
    for participant_sheet in sheet:
        matches = re.findall(r'[fF][pP]\d+_[vV]isit_\d', participant_sheet)
        for match in matches:
            ID.append(match)

    # for i in ID:
    #     data = manipulate('C:\\Users\\Maru\\PycharmProjects\\Dissertation\\RawData.xlsx', i)

    data = manipulate('C:\\Users\\Maru\\PycharmProjects\\Dissertation\\RawData.xlsx', ID[1])
    print(data.process_variables('notdict' # add your switch-case statements)) 


if __name__ == '__main__':
    main()

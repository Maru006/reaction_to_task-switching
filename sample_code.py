import pandas as pd
import logging
import re
import numpy as np
import itertools
from matplotlib import pyplot as plt
import seaborn as sns

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
logging.basicConfig(level=logging.DEBUG,
                    format='%(funcName)s :: %(message)s')


def sheets(url, regex):
    # takes out sheet names specified by a regex function specifying the sheets
    _sheets = []
    _sheet_lst = pd.read_excel(url, None)
    sheet = list(_sheet_lst.keys())
    for participant_sheet in sheet:
        matches = re.findall(regex, participant_sheet)
        for match in matches:
            _sheets.append(match)
    return _sheets


class manipulate:

    def __init__(self, url, sheet, setVolume=False):
        self.url = url
        self.sheet = sheet
        self.setVolume = setVolume

        self.untData = pd.read_excel(self.url, self.sheet)

        self.grpType = []  # process_type, volume parameter
        self.grpData = []  # process_variables, volume parameter

    @property
    def grpType(self):
        print(self.grpType)

    @property
    def grpData(self):
        return self._grpData

    def process_type(self):  # regex):  # helps group data, condition = feedback type
        data = self.untData
        data.columns = data.columns.str.replace('Personal feedback', 'removed')

        if self.setVolume:
            logging.info(f'setVolume was set to {self.setVolume}')

        for column in data.columns:
            try:
                task_feedback = re.findall(r'[Pp]rocess', column)
                trait_feedback = re.findall(r'[Pp]ersonal', column)

                if not self.setVolume:
                    for match in task_feedback or trait_feedback:
                        logging.info(f'In {self.sheet} sheet, {match} was found')
                        if match == 'process':
                            return {self.sheet: match}
                        if match == 'personal':
                            return {self.sheet: match}
                        if not task_feedback or trait_feedback:
                            continue

                if self.setVolume:
                    for match in task_feedback or trait_feedback:
                        logging.info(f'In {self.sheet} sheet, {match} was found')
                        if match == 'process':
                            self.grpType.append({self.sheet: match})
                        if match == 'personal':
                            self.grpType.append({self.sheet: match})
                        if not task_feedback or trait_feedback:
                            continue

            except TypeError as error:  # instances columns contain an int; detrimental to regex functions
                logging.warning(f'{error}')
                continue

    def process_variables(self, argVar):  # if multiple dataframes are expected, and a process type grouping is required.
        data = self.untData
        data = pd.concat([data.iloc[2:102], data.iloc[107:157]]).reset_index()
        fb = data.loc[0:99, :].reset_index()
        nfb = data.loc[100:155, :].reset_index()

        variables = {  # switch-case statement
            'fb': data.loc[0:99, :].reset_index(),
            'nfb': data.loc[100:155, :].reset_index(),

            'bi': data.loc[np.where(data['Unnamed: 24'] != ' ')],
            'uni': data.loc[np.where(data['Unnamed: 25'] != ' ')],

            'fb_bi': fb.loc[np.where(fb['Unnamed: 24'] != ' ')],
            'fb_uni': fb.loc[np.where(fb['Unnamed: 25'] != ' ')],

            'nfb_bi': nfb.loc[np.where(nfb['Unnamed: 24'] != ' ')],
            'nfb_uni': nfb.loc[np.where(nfb['Unnamed: 25'] != ' ')],
        }
        if not self.setVolume:
            if argVar in variables:
                return variables[argVar]

        if self.setVolume:
            logging.info(f'{argVar} variable included')
            self.grpData.append({self.sheet: variables[argVar]})
        else:
            logging.warning(f'{argVar} not in specified variables')


def main():
    url = 'C:\\Users\\Maru\\PycharmProjects\\Dissertation\\RawData.xlsx'
    sheet = sheets(url, regex=r'[fF][pP]\d+_[vV]isit_\d')
    
    #for i in sheet:
    #  manipulate(url, sheet[1], setVolume=True)
    #  print(manipulate.grpType)
  
    manipulate(url, sheet[1], setVolume=True)
    print(manipulate.grpType)


if __name__ == '__main__':
    main()

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


class manipulate:

    def __init__(self, url, setVolume=False):
        self.url = url
        self.setVolume = setVolume # If True, changes processing path for _type and _variables
          
        self.sheets = [] # process_sheets by default.
        self.grpType = []  # process_type, volume parameter
        self.grpData = []  # process_variables, volume parameter

    def Type(self, info_mode=False):
        if not info_mode:
            if self.setVolume:
                types = self.grpType
                if self.setVolume:
                    return types
                if self.setVolume:
                    logging.warning(f'You have set self.setVolume (or by default) at {self.setVolume}. This function is only useful for checking memory when'
                                    f' setVolume (default=False) parameter for Class:manipulate is set to True to store data. \n Instead, print '
                                    f' either process functions instead.')
        if info_mode:
            logging.info(f' There are {len(self.grpType) + 1} Labels currently sitting in your memory. \n'
                         f' The last label is: ')
            return self.grpType[len(self.grpType) - 1]

    def Data(self, info_mode=False):
        if not info_mode:
            if self.setVolume:
                grpData = self.grpData
                return grpData
            if not self.setVolume:
                logging.warning(f'You have set self.setVolume (or by default) at {self.setVolume}. This function is only useful for checking memory when'
                                f' setVolume (default=False) parameter for Class:manipulate is set to True to store data. \n Instead, print '
                                f' either process functions instead.')
        if info_mode:
            logging.info(f' There are {len(self.grpData) + 1} Dataframes currently sitting in your memory \n'
                         f'The last dataframe consists of: ')
            return self.grpData[len(self.grpData) - 1]
          
    def process_sheets(self, regex):
        # takes out sheet names specified by a regex function specifying the sheets
        _sheet_lst = pd.read_excel(self.url, None)
        sheet = list(_sheet_lst.keys())
        for participant in sheet:
            matches = re.findall(regex, participant)
            for match in matches:
                self.sheets.append(match)

    def process_type(self):
        for sheet in self.sheets:
            data = pd.read_excel(self.url, sheet)
            data.columns = data.columns.str.replace('Personal feedback', 'removed')
            
            for column in data.columns:
                try:
                    task_feedback = re.findall(r'[Pp]rocess', column)
                    trait_feedback = re.findall(r'[Pp]ersonal', column)

                    if not self.setVolume:
                        for match in task_feedback or trait_feedback:
                            logging.info(f'In {sheet} sheet, {match} was found')
                            if match == 'process':
                                return {sheet: match}
                            if match == 'personal':
                                return {sheet: match}
                            if not task_feedback or trait_feedback:
                                continue

                    if self.setVolume:
                        for match in task_feedback or trait_feedback:
                            logging.info(f'In {sheet} sheet, {match} was found')
                            if match == 'process':
                                self.grpType.append({sheet: match})
                            if match == 'personal':
                                self.grpType.append({sheet: match})
                            if not task_feedback or trait_feedback:
                                continue

                except TypeError as error:  # instances columns contain an int; detrimental to regex functions
                    logging.warning(f'{error}')
                    continue

    def process_variables(self, argVar):  # if multiple dataframes are expected, and a process type grouping is required.
        for sheet in self.sheets:
            data = pd.read_excel(self.url, sheet)
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
                self.grpData.append({sheet: variables[argVar]})
            else:
                logging.warning(f'{argVar} not in specified variables')


def main():
    url = '***URL***'
    regex=r'[fF][pP]\d+_[vV]isit_\d'
    
    process = manipulate(url, setVolume=True)
    process.process_sheets(regex)
    process.process_type()
    process.process_variables('bi')

    print(process.grpType)
    print(process.grpData)



if __name__ == '__main__':
    main()

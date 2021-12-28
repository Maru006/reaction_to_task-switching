import pandas as pd
import logging
import re
import sqlite3

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)

logging.basicConfig(level=logging.DEBUG,
                    format='%(funcName)s :: %(message)s')


class preprocessing:

    def __init__(self, url, setVolume=False):
        self.url = url
        self.setVolume = setVolume  # If True, changes processing path for _type and _variables

        self.sheets = []  # process_sheets by default.
        self.grpType = []  # process_type, volume parameter
        self.grpData = []  # process_variables, volume parameter

    def Type(self, info_mode=False):
        if not info_mode:
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

    def __repr__(self):
        pass

    def __str__(self):
        pass

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
            fb = data.loc[0:99, :]
            nfb = data.loc[100:155, :]
            variables = {  # switch-case statement
                'fb': data.loc[0:99, :],
                'nfb': data.loc[100:155, :],

                'bi': data.loc[data['Unnamed: 24'] == ' '],
                'uni': data.loc[data['Unnamed: 25'] == ' '],

                'fb_bi': fb.loc[fb['Unnamed: 24'] == ' '],
                'fb_uni': fb.loc[fb['Unnamed: 25'] == ' '],

                'nfb_bi': nfb.loc[nfb['Unnamed: 24'] == ' '],
                'nfb_uni': nfb.loc[nfb['Unnamed: 25'] == ' ']
            }
            if not self.setVolume:
                if argVar.lower() in variables:
                    return {sheet: variables[argVar]}

            if self.setVolume:
                logging.info(f'{argVar.lower()} variable included for {sheet}')
                self.grpData.append({sheet: variables[argVar]})
            else:
                logging.warning(f'{argVar.lower()} not in specified variables')


class framework:

    def __init__(self, types, argstypes, data, argsdata):
        self.types = types
        self.argstypes = argstypes
        self.data = data
        self.argsdata = argsdata

        self.included = {}
        self.excluded = {}

        self.included_indexes = {}
        self.excluded_indexes = {}

    def frame(self, inclusive=True):  # I believe this method can't ask for forgiveness as it heavily relies on accuracy, thus permissions.
        if isinstance(self.types, list) and isinstance(self.data, list):
            for types, datas in zip(self.types, self.data):
                for type_keys, type_values in types.items():
                    if type_values == self.argstypes:
                        for data_user, dataframe in datas.items():
                            self.included.update({data_user: dataframe['Unnamed: 10'].astype(float)})
                            self.included_indexes.update({data_user: dataframe['Unnamed: 1']})
                        continue
                    if type_values != self.argstypes:
                        for data_user, dataframe in datas.items():
                            self.excluded.update({data_user: dataframe['Unnamed: 10'].astype(float)})
                            self.excluded_indexes.update({data_user: dataframe['Unnamed: 1']})
                            logging.info(f'{type_keys} was not included in this analysis')
                        continue
            if inclusive:
                self.included = pd.DataFrame(self.included)
                return self.included
            if not inclusive:
                self.excluded = pd.DataFrame(self.excluded)
                return self.excluded
        else:
            logging.warning(f'Type parameter must be in dictionary form. You have given a {type(self.types)}')
            logging.warning(f'Data parameter must be in dictionary form. You have given a {type(self.data)}')


class group:

    def __init__(self, data, url, regressor: str):
        self.data = data
        self.url = url
        self.regressor = regressor.lower()

    def regress(self, sample_sheet=7):
        sample_data = (pd.read_excel(io=self.url, sheet_name=sample_sheet))
        sample_data = pd.concat([sample_data.iloc[2:102], sample_data.iloc[107:157]]).reset_index()
        full_timeRegressor = sample_data['Unnamed: 1']
        fb_timeRegressor = sample_data.loc[0:99, :]['Unnamed: 1']
        nfb_timeRegressor = sample_data.loc[100:155, :]['Unnamed: 1']

        if self.regressor == 'fb':
            try:
                # dataframe = pd.concat([self.data, fb_timeRegressor.loc[self.data.index]], axis=1, ignore_index=True)
                regressor = fb_timeRegressor.loc[self.data.index]
                self.data = self.data.assign(Time=regressor)
                return self.data
            except KeyError as error:
                logging.warning(f'Index mismatch. Check whether preprocessed variables are within the parameters set in arguments: process_variables(argVar:str)')
                print(error)

        if self.regressor == 'nfb':
            try:
                # dataframe = pd.concat([self.data, nfb_timeRegressor.loc[self.data.index]], axis=1, ignore_index=True)
                regressor = nfb_timeRegressor.loc[self.data.index]
                self.data = self.data.assign(Time=regressor)
                return self.data
            except KeyError as error:
                logging.warning(f'Index mismatch. Check whether preprocessed variables are within the parameters set in arguments: process_variables(argVar:str)')
                print(error)

        if self.regressor == 'full':
            try:
                # dataframe = pd.concat([self.data, full.loc[self.data.index]], axis=1, ignore_index=True)
                regressor = full_timeRegressor.loc[self.data.index]
                self.data = self.data.assign(Time=regressor)
                return self.data
            except KeyError as error:
                logging.warning(f'Index mismatch. Check whether preprocessed variables are within the parameters set in arguments: process_variables(argVar:str)')
                print(error)

        else:
            logging.info(f"Select between, 'fb', 'nfb' or 'full' instead of {self.regressor}")


def automate(argVar: str, regressor: str, argtypes: str):
    url = 'Original Directory for Data'
    regex = r'[fF][pP]\d+_[vV]isit_\d'

    create = preprocessing(url, setVolume=True)
    create.process_sheets(regex=regex)
    create.process_type()
    create.process_variables(argVar=argVar.lower())  # variables of interest
    types = create.Type(info_mode=False)
    data = create.Data(info_mode=False)

    data = framework(types=types, argstypes=argtypes.lower(), data=data, argsdata='Unnamed: 10').frame()  # type process or personal

    data = data.assign(Condition=argVar)
    data = data.assign(Feedback=argtypes)
    data = data.assign(Mean=data.mean(axis=1))

    dataframe = group(data=data, url=url, regressor=regressor.lower()).regress()  # time regressor 'fb' or 'nfb'

    if argtypes == 'personal':
        return dataframe
    if argtypes == 'process':
        return dataframe


def main():
    # conditions: fb, nfb, bi, uni, fb_bi, fb_uni, nfb_bi, nfb_uni
    fb_per_uni = automate(argVar='fb_uni', argtypes='personal', regressor='fb')  # 22
    fb_pro_uni = automate(argVar='fb_uni', argtypes='process', regressor='fb')  # 21
    nfb_per_uni = automate(argVar='nfb_uni', argtypes='personal', regressor='nfb')  # 22
    nfb_pro_uni = automate(argVar='nfb_uni', argtypes='process', regressor='nfb')  # 21

    fb_per_bi = automate(argVar='fb_bi', argtypes='personal', regressor='fb')  # 22
    fb_pro_bi = automate(argVar='fb_bi', argtypes='process', regressor='fb')  # 21
    nfb_per_bi = automate(argVar='nfb_bi', argtypes='personal', regressor='nfb')  # 22
    nfb_pro_bi = automate(argVar='nfb_bi', argtypes='process', regressor='nfb')  # 21

    per_fb_uni = automate(argVar='fb_uni', argtypes='personal', regressor='fb')  # 22
    pro_fb_uni = automate(argVar='fb_uni', argtypes='process', regressor='fb')  # 21
    pro_fb_bi = automate(argVar='fb_bi', argtypes='process', regressor='fb')  # 21
    per_fb_bi = automate(argVar='fb_bi', argtypes='personal', regressor='fb')  # 22

    per_pivot_table = pd.concat([fb_per_uni,
                                 nfb_per_uni,
                                 fb_per_bi,
                                 nfb_per_bi,
                                 per_fb_uni,
                                 per_fb_bi], axis=0)
    pro_pivot_table = pd.concat([fb_pro_uni,
                                 nfb_pro_uni,
                                 fb_pro_bi,
                                 nfb_pro_bi,
                                 pro_fb_uni,
                                 pro_fb_bi], axis=0)

    connection = sqlite3.connect('Desired Directory For Database')

    per_pivot_table.to_sql('FB_Personal', con=connection)
    pro_pivot_table.to_sql('FB_Process', con=connection)


if __name__ == '__main__':
    main()

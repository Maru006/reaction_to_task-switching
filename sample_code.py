import pandas as pd

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
import re
import itertools

# recorded data for each participant separated between sheets
data = pd.read_excel('RawData.xlsx', None)
sheets = list(data.keys())  # shows all sheet names.

# isolating relevant sheets.
ID = []
for participant_sheet in sheets:
    matches = re.findall(r'[fF][pP]\d+_[vV]isit_\d', participant_sheet)
    for match in matches:
        ID.append(match)
# used to confirm isolated sheet names to only participants'.
sheets = data.keys()

# # all sheets naturally contain reaction times for all trials regardless of rule or feedback type.
fb = []
nfb = []
# FB-type
fb_personal = []
fb_process = []
# rule-type
bivalent = []
univalent = []                        # might include or not until i find a more efficient way

# FB/NFB x rule-type
fb_bivalent = []
fb_univalent = []

nfb_bivalent = []
nfb_univalent = []

# FB-type x rule-type
bivalentProcess = []
univalentProcess = []
bivalentPersonal = []
univalentPersonal = []


def feedback(IDs):
    # BEWARE: driving an 'else' statement may be misleading when detecting 'equality': as is required with regex related functions.
    # considering the analytical approach here, an 'identity' specific script may be more time consuming, hence it is avoided entirely.
    sample = pd.read_excel('RawData.xlsx', sheet_name=IDs)
    sample = sample.iloc[2:102, :]
    univalent_regressor = sample[sample['Unnamed: 24'] == ' ']
    bivalent_regressor = sample[sample['Unnamed: 24'] != ' ']

    for column in list(sample.columns):
        try:
            feedback_type1 = re.findall(r'[pP]rocess', column)
            feedback_type2 = re.findall(r'[pP]ersonal', column)
            for t in feedback_type1 or feedback_type2:
                if t == 'process':
                    # print(IDs, '', column)
                    fb.append({IDs: sample['Unnamed: 10']})
                    fb_process.append({IDs: sample['Unnamed: 10']})

                    bivalent.append({IDs: bivalent_regressor['Unnamed: 10']})
                    fb_bivalent.append({IDs: bivalent_regressor['Unnamed: 10']})
                    bivalentProcess.append({IDs: bivalent_regressor['Unnamed: 10']})

                    univalent.append({IDs: univalent_regressor['Unnamed: 10']})
                    fb_univalent.append({IDs: univalent_regressor['Unnamed: 10']})
                    univalentPersonal.append({IDs: univalent_regressor['Unnamed: 10']})

                if t == 'personal':
                    # print(IDs, '', column)
                    fb.append({IDs: sample['Unnamed: 10']})
                    fb_personal.append({IDs: sample['Unnamed: 10']})

                    bivalent.append({IDs: bivalent_regressor['Unnamed: 10']})
                    fb_bivalent.append({IDs: bivalent_regressor['Unnamed: 10']})
                    bivalentPersonal.append({IDs: bivalent_regressor['Unnamed: 10']})

                    univalent.append({IDs: univalent_regressor['Unnamed: 10']})
                    fb_univalent.append({IDs: univalent_regressor['Unnamed: 10']})
                    univalentPersonal.append({IDs: univalent_regressor['Unnamed: 10']})

            if None:
                print(f"{IDs}'s sheet did not specify whether it had either the feedback condition compiled in regex. \n\t And so, {IDs} was skipped in the process")
                continue
        except TypeError:
            # should you encounter this error: This statement only capture raw strings based on the expression statement compiled at re.findall(r'') or specified by your own formats.
            print(f"{IDs}'s did not specify whether it had either the feedback condition compiled in regex format.\n\t this may incur further error... you may wish to 'break' or 'continue'.")
            user_input = input("type 'break' or 'continue': ")
            if user_input == 'break':
                break
            if user_input == 'continue':
                continue
            if user_input != 'break' or 'continue':
                return user_input


def no_feedback(IDs):
    sample = pd.read_excel('RawData.xlsx', sheet_name=IDs)
    sample = sample.iloc[107:157, :]
    nfb.append({IDs: sample['Unnamed: 10']})


def rule_type(IDs):
    sample = pd.read_excel('RawData.xlsx', sheet_name=IDs)
    feedback_sample = sample.iloc[2:102, :]
    no_feedback_sample = sample.iloc[107:157, :]

    bivalent_cue = sample['Unnamed: 24'].index
    univalent_cue = sample['Unnamed: 25'].index


def terminal():
    for i in ID:
        feedback(i)
        # no_feedback(i)


terminal()

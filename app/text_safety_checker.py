"""
    pip install nltk

    git clone https://github.com/clips/pattern.git
    cd pattern
    sed -i '140d' setup.py
    python setup.py install

    Usage:
        from text_safety_checker import handle_text

        handled_text = handle_text(original_text)
"""

import json
import os.path

import nltk

blocklist = set()

nltk.download("omw-1.4")

## ModuleNotFoundError: No module named 'pattern.en'
#from pattern.en import pluralize, singularize

# read text file line by line and return a list
def read_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


# write json file
def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f)


def neutralize_gender(text):
    # replace gendered words
    # also take care of pluralization
    tokens = text.split()

    tokens_neutral = []

    for i, token in enumerate(tokens):
        token = token.lower()

	# TODO: change these back after fixing pattern.en
        # if it is plural, make it singular
        #singular_form = singularize(token)
        singular_form = token
        #is_plural = singular_form != token
        is_plural = False

        if singular_form in rplc:
            token_neutral = rplc[singular_form]
            # if is_plural:
            #     token_neutral = pluralize(token_neutral)

            tokens_neutral.append(token_neutral)
        else:
            tokens_neutral.append(token)

    return " ".join(tokens_neutral)


def rm_nsfw(text):
    # remove nsfw words
    tokens = text.split()

    tokens_clean = []

    for token in tokens:
        if token not in blocklist:
            for i, bl in enumerate(blocklist):
                if bl in token:
                    break

            if i == len(blocklist) - 1:
                tokens_clean.append(token)
            else:
                tokens_clean.append("******")
        else:
            tokens_clean.append("******")

    return " ".join(tokens_clean)


def handle_text(text):
    text = neutralize_gender(text)
    text = rm_nsfw(text)

    return text


rplc = {
    "actor": "performer",
    "actress": "performer",
    "aunt": "pibling",
    "barman": "bartender",
    "barwoman": "bartender",
    "beautiful": "attractive",
    "boy": "child",
    "boyfriend": "partner",
    "brother": "sibling",
    "buddy": "friend",
    "businessman": "business executive",
    "businesswoman": "business executive",
    "cameraman": "camera operator",
    "camerawoman": "camera operator",
    "chairman": "chairperson",
    "chairwoman": "chairperson",
    "congressman": "legislator",
    "congresswoman": "legislator",
    "councilman": "councilperson",
    "councilwoman": "councilperson",
    "daughter": "child",
    "dude": "friend",
    "father": "parent",
    "female lawyer": "lawyer",
    "fireman": "firefighter",
    "firewoman": "firefighter",
    "freshman": "first-year student",
    "gentleman": "person",
    "girl": "child",
    "girlfriend": "partner",
    "grandfather": "grandparent",
    "grandmother": "grandparent",
    "handsome": "attractive",
    "he": "person",
    #"her": "person",
    "hero": "heroix",
    "heroine": "heroix",
    "hers": "person's",
    "herself": "person",
    "him": "person",
    "himself": "person",
    "his": "person's",
    "hostess": "host",
    "househusband": "homemaker",
    "housewife": "homemaker",
    "husband": "partner",
    "lady": "person",
    "landlady": "landlord",
    "mailman": "mail carrier",
    "male lawyer": "lawyer",
    "man": "person",
    "man-made": "artificial",
    "mankind": "human beings",
    "manned": "crewed",
    "manpower": "workforce",
    "mother": "parent",
    "nephews": "nibling",
    "nieces": "nibling",
    "policeman": "police officer",
    "policewoman": "police officer",
    "postman": "mail carrier",
    "postwoman": "mail carrier",
    "repairman": "repairer",
    "repairwoman": "repairer",
    "salesman": "salesperson",
    "saleswoman": "salesperson",
    "she": "person",
    "sister": "sibling",
    "son": "child",
    "spokesman": "spokesperson",
    "spokeswoman": "spokesperson",
    "steward": "flight attendant",
    "stewardess": "flight attendant",
    "uncle": "pibling",
    "waiter": "waitperson",
    "waitress": "waitperson",
    "wife": "partner",
    "woman": "person",
    "workman": "worker",
    "workwoman": "worker",
}


if os.path.exists("app/block_list"):
    with open("app/block_list") as block_list:
        for line in block_list:
            blocklist.add(line.strip())

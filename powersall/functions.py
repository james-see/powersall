import markovify
import random
import json
import datetime


def markover(data):
    """Takes in data list of strings."""
    fixeddata = '\n'.join(map(str, data))
    text_model = markovify.NewlineText(fixeddata)
    return text_model.make_sentence()


def randomeyes(db=False):
    """Gets random numbers for powerball and return as list."""
    selection = dict()
    for counter in range(1, 6):
        selected = random.randint(1, 69)
        if selected not in selection:
            selection[counter] = selected
        else:
            return randomeyes()
    selection['powerball'] = random.randint(1, 26)
    if db:
        outjson = {}
        outjson['results'] = selection
        with open(f'selection_{datetime.datetime.now().strftime("%m-%d-%y-%h-%m-%s")}.json', 'w+') as f:
            f.write(json.dumps(outjson))
    return selection

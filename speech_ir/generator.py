from collections import defaultdict, Counter
import random
import sys

# This is the length of the "state" the current character is predicted from.
# For Markov chains with memory, this is the "order" of the chain. For n-grams,
# n is STATE_LEN+1 since it includes the predicted character as well.
from speech_ir.visualizer import read_full_data, read_input_folder, \
    hillary_input_folder, donald_input_folder

STATE_LEN = 10
prediction_size = 5000
hillary_output = "/media/disk/crawler/PEPr_Project_Code/speech_ir/data/speech_generation/hillary.txt"
donal_output = "/media/disk/crawler/PEPr_Project_Code/speech_ir/data/speech_generation/trump.txt"

def markov_build(input_folder, output_file):
    data = "\n".join(read_input_folder(input_folder))
    model = defaultdict(Counter)

    # print('Learning model...')
    for i in range(len(data) - STATE_LEN):
        state = data[i:i + STATE_LEN]
        next = data[i + STATE_LEN]
        model[state][next] += 1


    print('Sampling...')
    state = random.choice(list(model))
    out = list(state)
    for i in range(prediction_size):
        out.extend(random.choices(list(model[state]), model[state].values()))
        state = state[1:] + out[-1]

    pred = "\n".join(''.join(out).split("."))


    # for sent in pred.split("."):
    #     print(sent)
    print(type(pred))
    with open(output_file, 'w') as fp:
        fp.write(pred)


markov_build(hillary_input_folder, hillary_output)
markov_build(donald_input_folder, donal_output)
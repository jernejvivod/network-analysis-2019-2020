import pickle

# Initialize word and decompose into list of constituent letters.
WORD = "Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz"
word_decomposed = list(WORD.lower())

# Map contained letters to their IDs.
letters = sorted(set(WORD.lower()))
letter_to_id = dict(zip(letters, range(len(letters))))

# Save inverted dictionary to file for ID decoding.
id_to_letter = {letter_id : letter for (letter, letter_id) in letter_to_id.items()}
with open('id_to_letter.pkl', 'wb') as f:
        pickle.dump(id_to_letter, f, pickle.HIGHEST_PROTOCOL)

# Initialize mapping for adjacencies.
adj_mapping = dict().fromkeys(letters)
for key in adj_mapping.keys():
    adj_mapping[key] = dict().fromkeys(letters, 0)

# Find letter adjacencies.
for idx in range(len(word_decomposed)-1):
    adj_mapping[word_decomposed[idx]][word_decomposed[idx+1]] += 1

# Construct network and save results to file.
SAVE_FILE_PATH = './longest.txt'
with open(SAVE_FILE_PATH, 'w') as f:
    for key1 in adj_mapping.keys():
        for key2 in adj_mapping[key1].keys():
            if adj_mapping[key1][key2] > 0:
                f.write("{0} {1}\n".format(letter_to_id[key1], letter_to_id[key2]))


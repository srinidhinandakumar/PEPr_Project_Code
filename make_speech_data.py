import os

winners = ["1960_Data_John F. Kennedy", "1968_Data_Richard Nixon", "2008_Data_Barack Obama", "2016_Data_Donald Trump"]

def get_all_folders(parent_folder):
    directory_list = []
    for root, dirs, files in os.walk(parent_folder, topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(root, name))

    directory_list = [name for name in directory_list if len(name.split("/")) > 2]
    print (directory_list)
    return directory_list


def load_labeled_data(directory_list):
    texts, candidates, labels = [], [], []

    for folder_path in directory_list:
        if "Full_Speech" in str(folder_path):
            continue

        print(folder_path)

        if os.path.exists(folder_path):
            is_winner = 1 if len([True for winner in winners if winner in str(folder_path)]) > 0 else 0
            print(is_winner)

            for file in os.listdir(folder_path):
                file_name = folder_path + "/" + file
                if not os.path.isfile(file_name):
                    continue

                text_as_string = open(file_name, 'r').read().replace("\n", " ")

                texts.append(text_as_string)
                labels.append(str(is_winner))
                candidates.append(file.split("_")[0])
                #     return texts, labels
    f = open("labeled_data.txt", "w+")
    for text, candidate, label in zip(texts, candidates, labels):
        f.write(candidate + "# " + text + "# " + label + "\n")
    f.close()


directory_list = get_all_folders("speeches")
# Make a file with candidate, speech and label separated by #
load_labeled_data(directory_list)

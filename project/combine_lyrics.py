from os import listdir
import csv


def combine_data(path, mood):
    files = [file for file in listdir(path) if file.startswith(mood)]
    save_data = [['song', 'artist', 'url', 'lyrics', 'year', 'mood']]

    for file in files:
        print (file)
        with open(path + file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader, None) # skip header
            for row in csv_reader:
                row.append(mood)
                save_data.append(row)

    return (save_data)


def save_data(file_name, data):
    with open(file_name, "w") as f:
        w = csv.writer(f)
        w.writerows(data)
    print ("Done!")


path = "lyrics/row data/"
mood = "happy"
data = combine_data(path, mood)
save_data("lyrics/" + mood + ".csv", data)

path = "lyrics/row data/"
mood = "sad"
data = combine_data(path, mood)
save_data("lyrics/" + mood + ".csv", data)

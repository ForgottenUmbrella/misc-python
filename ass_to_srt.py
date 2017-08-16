def end_index(): return start_index + len("0:00:00")


def timestamp():
    return (line[start_index:end_index()] + ","
          + line[end_index()+1 : end_index()+3])


with open("inp.txt") as inp, open("out.srt", "w") as out:
    counter = 0
    for line in inp:
        counter += 1

        if counter == 1 or counter == 2:
            print(line)

        out.write(str(counter) + "\n")

        start_index = len("dialogue: 0,")
        timestamp_1 = timestamp()
        start_index += len("0:00:00.00,")
        timestamp_2 = timestamp()
        out.write("0" + timestamp_1 + "0 --> 0" + timestamp_2 + "0\n")

        mark = ",,0,0,0,,"
        start_dialogue_index = line.find(mark) + len(mark)
        dialogue_string = line[start_dialogue_index:-1]
        out.write(dialogue_string + "\n\n")

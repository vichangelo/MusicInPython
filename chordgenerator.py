import json
import notes
import intervals
import chords

thirds = {"bIII": "m", "III": ""}
fifths = {"bV": ["5-", "dim", "(b5)"], "V": ["", "5"], "#V":
          ["5+", "aug"]}
sevenths = {"bVII": "7", "VII": ["maj7", "7M"]}
ninths = {"bII": "b9", "II": ["2", "9"], "#II": "#9"}
elevenths = {"bIV": "b11", "IV": ["4", "11"], "#IV": "#11"}
thirteenths = {"bVI": "b13", "VI": ["6", "13"], "#VI": "#13"}
roots = notes.note_list


def format_name(root, chord_name):
    new_chord_name = chord_name
    if chord_name in [f"{root}/2", f"{root}/4", f"{root}/6",
                      f"{root}/9/", f"{root}/11/", f"{root}/13/",
                      f"{root}/2/", f"{root}/4/", f"{root}/6/"]:
        new_chord_name = chord_name.replace("/", "")
    elif chord_name.count("/") == 2:
        if "(b5)" in chord_name:
            new_chord_name = chord_name[:-1]
        else:
            new_chord_name = chord_name.replace("/", "(", 1)
            new_chord_name = new_chord_name.replace("/", ")", 1)
    elif "/" in chord_name:
        new_chord_name = chord_name.replace("//", "/")
        new_chord_name = new_chord_name[:-1]
    return new_chord_name


def generate_triads(root):
    chord_name = root
    chord_intervals = {"I"}
    name_list = []
    interval_list = []

    for third in thirds:
        for fifth in fifths:
            chord_intervals = {"I", third, fifth}
            for tone in fifths[fifth]:
                if third == "III" and tone == "dim":
                    continue
                if third == "bIII" and tone in ["5", "+", "aug", "5+"]:
                    continue
                chord_name = root + thirds[third] + tone

                if third == "bIII" and tone == "dim":
                    chord_name = chord_name.replace("m", "", 1)
                name_list.append(chord_name)

                if tone == "5":
                    interval_list.append(chord_intervals - {"III", "bIII"})
                else:
                    interval_list.append(chord_intervals)
    return name_list, interval_list

def add_sevenths(root):
    triad_name_list, triad_interval_list = generate_triads(root)
    name_list = []
    interval_list = []
    chord_name = ""
    chord_intervals = set()

    for name in triad_name_list:
        if name == root + "5":
            continue
        if name not in [f"{root}m(b5)", f"{root}m", f"{root}(b5)",
                        root, f"{root}5+"]:
            continue
        chord_name = name
        index = triad_name_list.index(name)
        chord_intervals = triad_interval_list[index]

        for seventh in sevenths:
            new_chord_intervals = chord_intervals.union({seventh})
            new_chord_name = chord_name
            if seventh == "bVII":
                new_chord_name += sevenths[seventh]
                name_list.append(new_chord_name)
                interval_list.append(new_chord_intervals)
            else:
                for tone in sevenths["VII"]:
                    new_chord_name = chord_name
                    if "m" in new_chord_name and tone == "maj7":
                        continue
                    new_chord_name += tone
                    name_list.append(new_chord_name)
                    interval_list.append(new_chord_intervals)

    for name in name_list:
        index = name_list.index(name)
        if "(b5)" in name:
            name = name.replace("(b5)", "") + "(b5)"
            name_list[index] = name
    return name_list, interval_list


def add_extensions(root):
    triad_name_list, triad_interval_list = generate_triads(root)
    seventh_name_list, seventh_interval_list = add_sevenths(root)
    previous_name_list = (triad_name_list.copy()
                          + seventh_name_list.copy())
    previous_interval_list = (triad_interval_list.copy()
                              + seventh_interval_list.copy())
    name_list = []
    interval_list = []
    chord_name = ""
    chord_intervals = set()

    for name in previous_name_list:
        if name == root + "5":
            continue
        chord_name = name + "/"
        index = previous_name_list.index(name)
        chord_intervals = previous_interval_list[index]

        for ninth in ninths:
            new_chord_name = chord_name
            new_chord_intervals = chord_intervals.union({ninth})
            if ninth == "II":
                for tone in ninths[ninth]:
                    new_chord_name = chord_name
                    if tone == "2":
                        if new_chord_name != root + "/":
                            continue
                        new_chord_name += tone
                        interval_list.append(new_chord_intervals)
                        name_list.append(new_chord_name)
                    else:
                        new_chord_name += tone + "/"
                        interval_list.append(new_chord_intervals)
                        name_list.append(new_chord_name)
            else:
                new_chord_name += ninths[ninth] + "/"
                interval_list.append(new_chord_intervals)
                name_list.append(new_chord_name)

    previous_name_list = previous_name_list + name_list
    previous_interval_list = previous_interval_list + interval_list
    for name in previous_name_list:
        if name == root + "5":
            continue
        chord_name = name + "/"
        index = previous_name_list.index(name)
        chord_intervals = previous_interval_list[index]

        for eleventh in elevenths:
            new_chord_name = chord_name
            new_chord_intervals = chord_intervals.union({eleventh})
            if eleventh == "IV":
                for tone in elevenths[eleventh]:
                    new_chord_name = chord_name
                    if tone == "4":
                        if new_chord_name != root + "/":
                            continue
                        new_chord_name += tone
                        interval_list.append(new_chord_intervals)
                        name_list.append(new_chord_name)
                    else:
                        new_chord_name += tone + "/"
                        interval_list.append(new_chord_intervals)
                        name_list.append(new_chord_name)
            else:
                new_chord_name += elevenths[eleventh] + "/"
                interval_list.append(new_chord_intervals)
                name_list.append(new_chord_name)

    previous_name_list = previous_name_list + name_list
    previous_interval_list = previous_interval_list + interval_list
    for name in previous_name_list:
        if name == root + "5":
            continue
        chord_name = name + "/"
        index = previous_name_list.index(name)
        chord_intervals = previous_interval_list[index]

        for thirteenth in thirteenths:
            new_chord_name = chord_name
            new_chord_intervals = chord_intervals.union({thirteenth})
            if thirteenth == "VI":
                for tone in thirteenths[thirteenth]:
                    new_chord_name = chord_name
                    if tone == "6":
                        if new_chord_name != root + "/":
                            continue
                        new_chord_name += tone
                        interval_list.append(new_chord_intervals)
                        name_list.append(new_chord_name)
                    else:
                        new_chord_name += tone + "/"
                        interval_list.append(new_chord_intervals)
                        name_list.append(new_chord_name)
            else:
                new_chord_name += thirteenths[thirteenth] + "/"
                interval_list.append(new_chord_intervals)
                name_list.append(new_chord_name)

    previous_name_list = previous_name_list + name_list
    previous_interval_list = previous_interval_list + interval_list

    for name in previous_name_list:
        index = previous_name_list.index(name)
        previous_name_list[index] = format_name(root, name)
    return previous_name_list, previous_interval_list


chord_dump = dict()
for root in roots:
    chord_names = add_extensions(root)[0]
    chord_intervals = add_extensions(root)[1]
    for name in chord_names:
        index = chord_names.index(name)
        interval_set = chord_intervals[index]
        interval_list = list(interval_set)
        interval_list.sort(key=intervals.all_intervals.index)
        interval_string = " ".join(interval_list)
        name_interval = f"{name} ({interval_string})"
        chord_notes = chords.get_chord_notes(root, interval_string)
        chord_dump[name_interval] = chord_notes

with open("chords.json", "w") as chordsfile:
    json.dump(chord_dump, chordsfile, indent=4, sort_keys=True)
exit()

import statistics

FOLDER = '../Chapter3/swimdata/'

def read_swim_data(filename):
    swimmer, age, distance, stroke = filename.removesuffix(".txt").split("-")

    with open(FOLDER + filename) as file:
        lines = file.readlines()

    converts = []
    times = lines[0].strip().split(",")

    for t in times:

        if ":" in t:
            mins, rest = t.split(":")
            secs, hundredths = rest.split(".")
        else:
            mins = 0
            secs, hundredths = t.split(".")
        
        converts.append((int(mins) * 60 * 100) + (int(secs) * 100) + int(hundredths))

    avg = statistics.mean(converts)

    mins_secs, hundredths = str(round(avg / 100, 2)).split(".")
    mins_secs = int(mins_secs)
    mins = mins_secs // 60
    secs = mins_secs - (mins * 60)

    avg = f"{mins}:{secs}.{hundredths}"

    return swimmer, age, distance, stroke, times, avg
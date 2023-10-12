import statistics
import hfpy_utils

FOLDER = "swimdata/"
CHARTS = "charts/"

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

    mins_secs, hundredths = f"{(avg / 100):.2f}".split(".")
    mins_secs = int(mins_secs)
    mins = mins_secs // 60
    secs = mins_secs - (mins * 60)

    avg = f"{mins}:{secs:0>2}.{hundredths}"

    return swimmer, age, distance, stroke, times, avg, converts

def produce_bar_chart(fn, location=CHARTS):
    """
        Given the name of a swimmer's file, produce an HTML/SVG-based bar chart.
        Save the chart to the CHARTS folder. Return the path to the bar chart files.
    """

    swimmer, age, distance, stroke, times, avg, converts = read_swim_data(fn)

    from_max = max(converts)
    svgs = ""
    times.reverse()
    converts.reverse()
    title = f"{swimmer} (Under {age}) {distance} {stroke}"
    header = f"""<!DOCTYPE html>
    <html>
        <head>
            <title>{title}</title>
            <link rel="stylesheet" href="../static/webapp.css"/>
        </head>
        <body>
            <h2>{title}</h2>
    """
    body = ""

    for n, t in enumerate(times):
        bar_width = hfpy_utils.convert2range(converts[n], 0, from_max, 0, 400)
        body = body + f"""
                    <svg height="30" width="400">
                        <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
                    </svg>{t}<br />
                        """
        
    footer = f"""
            <p>Average time: {avg}</p>
        </body>
    </html>
    """

    page = header + body + footer
    save_to = f"{location}{fn.removesuffix('.txt')}.html"

    with open(save_to, "w") as sf:
        print(page, file=sf)
    
    return save_to
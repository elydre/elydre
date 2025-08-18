from flask import Flask

# https://www.dolmetsch.com/musictheory27t.htm

app = Flask(__name__)

html_header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Temperament Calculator</title>
    <style>
        body {
            color: #fff;
            background-color: #222;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #aaa;
            padding: 8px;
            text-align: left;
        }
    </style>
</head>
"""

class Interval:
    def __init__(self, ratio, name, bold=False):
        self.ratio = ratio
        self.name = name
        self.bold = bold

JUST_INTONATION = [
    Interval(1/1,   "unison"),
    Interval(16/15, "half tone"),
    Interval(9/8,   "whole tone"),
    Interval(6/5,   "minor third"),
    Interval(5/4,   "major third", bold=True),
    Interval(4/3,   "perfect fourth"),
    Interval(45/32, "diminished fifth"),
    Interval(3/2,   "perfect fifth", bold=True),
    Interval(8/5,   "minor sixth"),
    Interval(5/3,   "major sixth"),
    Interval(9/5,   "minor seventh"),
    Interval(15/8,  "major seventh"),
    Interval(2/1,   "octave")
]

NAMES = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
]

def gen_color(r):
    GRADIENT_COLORS = [
    "#00ff00",  # 0 - vert pur
    "#44ff00",  # 1
    "#88ff00",  # 2 - lime
    "#ccff00",  # 3
    "#ffff00",  # 4 - presque jaune
    "#ffff00",  # 5 - jaune pur
    "#ffdd00",  # 6
    "#ffbb00",  # 7
    "#ffaa00",  # 8
    "#ff9900",  # 9
    "#ff8800",  # 10
    "#ff7700",  # 11
    "#ff6600",  # 12
    "#ff5500",  # 13
    "#ff4400",  # 14
    "#ff3300",  # 15
    "#ff3300",  # 16
    "#ff2200",  # 17
    "#ff1100",  # 18
    "#ff1100",  # 19
    "#ff0000",  # 20 - rouge pur
    ]

    r = abs(r)
    if r > 2:
        r = 2

    return GRADIENT_COLORS[int(r * 10)]

class temperament:
    def __init__(self, name, values, A4 = 440):
        if len(values) != 12:
            raise ValueError("Temperament must have 12 values.")
        self.name = name
        self.values = values
        self.A4 = A4
        self.calculate_note()

    def generate_equal(self):
        C4 = self.A4 / (2 ** (9 / 12))

        frequencies = []
        for i in range(12):
            frequency = C4 * (2 ** (i / 12))
            frequencies.append(frequency)
        return frequencies

    def calculate_note(self):
        self.notes = []
        equal_notes = self.generate_equal()
        for i in range(len(self.values)):
            frequency = equal_notes[i] * (2 ** (self.values[i] / 1200))
            self.notes.append(frequency)
        return self.notes

    def print(self):
        print(f"Temperament: {self.name}")
        for i in range(len(self.values)):
            print(f"Note {i}: {self.values[i]} cents, Frequency: {self.notes[i]:.2f} Hz")

    def calculate_ratio(self, note1, note2):
        if note1 > note2:
            note1, note2 = note2, note1

        note1_val = ((note1 // 12) + 1) * (self.notes[note1 % 12])
        note2_val = ((note2 // 12) + 1) * (self.notes[note2 % 12])

        rap = note2 - note1

        while rap >= 12:
            rap = rap - 12

        ratio = note2_val / note1_val

        return JUST_INTONATION[rap].ratio, ratio

    def make_table(self):
        table = f"<h1>{self.name}</h1><table><tr><th>Note</th>"
        for name in NAMES:
            table += f"<th>{name}</th>"

        table += "</tr><tr><th>Frequency</th>"

        for i in range(len(self.notes)):
            table += f"<td>{self.notes[i]:.2f}</td>"

        table += "</tr><tr><th>Cents from Equal</th>"

        for i in range(len(self.notes)):
            table += f"<td>{self.values[i]:.2f}</td>"

        for i in range(1, 12):
            table += "</tr><tr><th>" + JUST_INTONATION[i].name + "</th>"
            for j in range(12):
                jr, tr = self.calculate_ratio(j, i + j)
                r = tr / jr * 100 - 100
                table += f"<td><span title=\"{NAMES[(j + i) % 12]}\"><b style='color: {gen_color(r)}'>{r:.2f}</b></span></td>"

        table += "</tr></table>"

        return table

@app.route('/')
def index():
    t = [
        temperament(
            "1/4 Comma meantone",
            [10.26, -13.69, 3.42, 20.52, -3.43, 13.68, -10.27, 6.84, -17.11, 0, 17.1, -6.85]
        ),

        temperament(
            "Just Pure Major",
            [16, 28, 20, 32, 0, 14, 6, 18, 30, 0, 12, 4]
        ),
        
        temperament(
            "Equal Temperament",
            [0] * 12
        ),

        temperament(
            "Mercadier 1/12 & 1/6",
            [5.87, 0, 1.96, 1.95, -1.95, 5.87, 0, 3.91, 0, 0, 3.91, 0]
        ),

        temperament(
            "Kirnberger III",
            [10.264, 0.489, 3.421, 4.399, -3.422, 8.309, 0.488, 6.842, 2.444, 0, 6.354, -1.467]
        ),

        temperament(
            "1/6 Comma meantone",
            [5.000, -6.000, 2.000, 10.000, -2.000, 7.000, -5.000, 3.000, -8.000, 0.000, 8.000, -3.000]
        )
    ]

    return html_header + "".join([e.make_table() for e in t])

if __name__ == '__main__':
    app.run(debug=True)

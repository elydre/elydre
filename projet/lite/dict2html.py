import os

full_dico = eval(input("dico | list: "))

def make_table(elmt):

    out = ""

    if isinstance(elmt, dict):
        out += "<table>"
        for key in elmt.keys():
            out += f"<tr><td style=\"background-color:#121;\">{make_table(key)}</td>"
            out += f"<td style=\"background-color:#112;\">{make_table(elmt[key])}</td></tr>"
        out += "</table>"

    elif isinstance(elmt, list):
        out += "<table>"
        for e in elmt:
            out += f"<tr><td style=\"background-color:#211;\">{make_table(e)}</td><tr>"
        out += "</table>"

    else:
        out = elmt
    

    return out

file_path = f"{os.path.dirname(os.path.abspath(__file__))}/index.html"

with open(file_path, "w") as f:
    f.write("""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {
                    background-color: #111;
                    color: #bbb;
                    font-size: x-large;
                }
                td {
                    border: 1px solid #444;
                    padding:5px;
                }
            </style>
            <title>dict -> html</title>
        </head>
        <body>
    """ + make_table(full_dico) + """
        </body>
    </html> 
    """)

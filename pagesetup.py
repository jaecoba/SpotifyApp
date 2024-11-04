import os
import config
def setup():
    os.chdir(config.TEMPLATE_PATH)
    file = open("test.html", "w+")
    file.write("""<!DOCTYPE html>\n<html lang="en">\n<head>\n<title>Spotify Stats</title>
    \n</head>\n<body>\n<h1 style="font-size:45px;">Spotify Top Tracks</h1>
    \n<h2>Short Term</h2>\n""")
    file.close()
    return 

def finish():
    file = open("test.html", "a+")
    file.write("\n</body>\n</html>")
    file.close()

    return
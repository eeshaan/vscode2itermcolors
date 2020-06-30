import json
import plistlib
from jsoncomment import JsonComment
from argparse import ArgumentParser

ANSI_COLORS = {
    "Ansi 0 Color": "terminal.ansiBlack",
    "Ansi 1 Color": "terminal.ansiRed",
    "Ansi 2 Color": "terminal.ansiGreen",
    "Ansi 3 Color": "terminal.ansiYellow",
    "Ansi 4 Color": "terminal.ansiBlue",
    "Ansi 5 Color": "terminal.ansiMagenta",
    "Ansi 6 Color": "terminal.ansiCyan",
    "Ansi 7 Color": "terminal.ansiWhite",
    "Ansi 8 Color": "terminal.ansiBrightBlack",
    "Ansi 9 Color": "terminal.ansiBrightRed",
    "Ansi 10 Color": "terminal.ansiBrightGreen",
    "Ansi 11 Color": "terminal.ansiBrightYellow",
    "Ansi 12 Color": "terminal.ansiBrightBlue",
    "Ansi 13 Color": "terminal.ansiBrightMagenta",
    "Ansi 14 Color": "terminal.ansiBrightCyan",
    "Ansi 15 Color": "terminal.ansiBrightWhite",
}


def hex2rgbcomponents(hex):
    rgb = tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))
    value = [x / 255.0 for x in rgb]
    return value


def main():
    parser = ArgumentParser()
    parser.add_argument("input", help=".json filename")
    args = parser.parse_args()

    with open(args.input) as f:
        # wrapping json with jsoncomment to avoid error on trailing comma
        parser = JsonComment(json)
        theme = parser.load(f)

    itermcolors = {}

    for color_index in range(16):
        key = "Ansi %d Color" % color_index
        itermcolors[key] = {
            "Red Component": hex2rgbcomponents(
                theme["colors"][ANSI_COLORS[key]].lstrip("#")
            )[0],
            "Green Component": hex2rgbcomponents(
                theme["colors"][ANSI_COLORS[key]].lstrip("#")
            )[1],
            "Blue Component": hex2rgbcomponents(
                theme["colors"][ANSI_COLORS[key]].lstrip("#")
            )[2],
            "Color Space": "sRGB",
        }

    itermcolors["Background Color"] = {
        "Red Component": hex2rgbcomponents(
            theme["colors"]["editor.background"].lstrip("#")
        )[0],
        "Green Component": hex2rgbcomponents(
            theme["colors"]["editor.background"].lstrip("#")
        )[1],
        "Blue Component": hex2rgbcomponents(
            theme["colors"]["editor.background"].lstrip("#")
        )[2],
        "Color Space": "sRGB",
    }

    with open("%s.itermcolors" % args.input.split(".json")[0], "wb") as f:
        plistlib.dump(itermcolors, f)


if __name__ == "__main__":
    main()

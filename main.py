import sys

from capture_imgs import CaptureImages
from createDistortion import CreateDistortion


def main():
    if len(sys.argv) == 1:
        printHelp()
        sys.exit()

    camIds = getCamIds()
    maxFPS = getCommandValues("-fps")
    if maxFPS is None:
        maxFPS = 30

    height = getCommandValues("-h")
    if height is None:
        height = 1920

    width = getCommandValues("-w")
    if width is None:
        width = 1080

    """"" Not supported jet
    withScreen = getCommandValues("-withScreen")
    if withScreen is None:
        withScreen = False
    else:
        withScreen = True
    """

    if len(sys.argv) >= 2:
        command = sys.argv[1]

    if command == "generate":
        generate = CaptureImages(camIds, int(maxFPS), int(width), int(height))
        generate.captureImages()
    elif command == "distortion":
        distortion = CreateDistortion()
        distortion.generateDistortionJson(width, height)


def getCamIds():
    camIds = []
    i = 0
    for x in sys.argv:
        if x == "-camIds":
            j = i + 1
            for y in sys.argv:
                if len(sys.argv) < j + 1:
                    continue
                if sys.argv[j].__contains__("-"):
                    continue
                camIds.append(int(sys.argv[j]))
                j += 1
        i += 1
    return camIds


def getCommandValues(command):
    i = 0
    for x in sys.argv:
        if x.__contains__(command):
            if len(sys.argv) <= i + 1:
                print("Empty parameter", command, "using default value")
                return
            else:
                return sys.argv[i + 1]
        i += 1


def printHelp():
    print("Please tell me what to do. \nFollowing commands are allowed: python main.py <command> \n"
          " <command> \n"
          "     generate        - generates calibration pictures \n"
          "     distortion      - creates the distortion.json\n\n"
          " You need to add all values here, python main.py generate <camId> <max FPS> <height> <width>\n"
          " You need to add all these information, python main.py distortion <height> <width>")


if __name__ == "__main__":
    main()

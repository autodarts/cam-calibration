import cv2
from pathlib import Path

from cam import Cam


class CaptureImages:
    camIds = []
    fps = 30
    width = 1920
    height = 1080
    folder = "calibrationImages"

    # default constructor
    def __init__(self, camIds, fps, width, height):
        self.camIds = camIds
        self.fps = fps
        self.width = width
        self.height = height

    def captureImages(self):
        print("Generating images, be ready. You can press esc to stop capturing")

        cams = [Cam(id, self.fps, self.width, self.height).start() for id in self.camIds]

        for id in self.camIds:
            Path(self.folder, str(id)).mkdir(parents=True, exist_ok=True)

        snap = []
        for i in range(len(self.camIds)):
            print(i)
            snap.append(False)

        x = 1
        j = 0

        while True:
            if x % 60 * 5 == 0:
                for i in range(len(self.camIds)):
                    snap[i] = True
                j += 1
            x += 1
            for i, cam in enumerate(cams):
                if snap[i]:
                    cv2.imwrite(f'{self.folder}/{cam.device}/img_{self.width}x{self.height}_{j}.jpg', frame)
                    print("Captured", cam.device)
                    snap[i] = False
                    frame = cam.read()
                    cv2.rectangle(frame, (0, 0), (self.width, self.height), (0, 255, 0), 10)
                    cv2.imshow(f'Cam {i}', frame)
                else:
                    frame = cam.read()
                    cv2.imshow(f'Cam {i}', frame)

            if cv2.waitKey(33) == 27:
                break  # esc to quit

        cv2.destroyAllWindows()


def createImages(cap, folder, width, height):
    i = 1
    j = 0
    while True:
        _, frame = cap.read()

        cv2.imshow('Capture', frame)

        if i % 30 * 5 == 0:
            cv2.imwrite(f'{folder}/img_{width}x{height}_{j}.jpg', frame)
            print("Captured and saved in ", folder)
            cv2.rectangle(frame, (0, 0), (width, height), (0, 255, 0), 10)
            cv2.imshow('Capture', frame)
            j += 1
        i += 1
        if cv2.waitKey(33) == 27:
            break  # esc to quit

    cv2.destroyAllWindows()

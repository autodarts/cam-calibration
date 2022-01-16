import threading

import cv2


class Cam:
    def __init__(self, device, fps=30, width=1920, height=1080):
        self.video_capture = None
        self.fps = 0
        self.frame = None
        self.running = False
        self.__fps = 0
        self.__read_thread = None
        self.__read_lock = threading.Lock()

        self.device = device
        self.fps = fps
        self.width = width
        self.height = height

        self.video_capture = cv2.VideoCapture(self.device, cv2.CAP_V4L2)
        self.video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        self.video_capture.set(cv2.CAP_PROP_FPS, self.fps)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        ret, self.frame = self.video_capture.read()
        print('warm up worked', ret)

    def read(self):
        with self.__read_lock:
            return self.frame

    def start(self):
        if self.running:
            return
        self.running = True
        self.__read_thread = threading.Thread(target=self.__update)
        self.__read_thread.start()
        return self

    def release(self):
        self.running = False

        if self.video_capture is not None:
            self.video_capture.release()
            self.video_capture = None

        if self.__read_thread is not None:
            self.__read_thread.join()
            self.__read_thread = None

    def __update(self):
        while self.running:
            try:
                ret, frame = self.video_capture.read()
                if ret:
                    with self.__read_lock:
                        self.frame = frame
                        self.__fps += 1
            except RuntimeError:
                print("could not read image from camera")

import time
import logging


class FPSLogger:
    def __init__(self):
        self.lastFPS: float = 0
        self.lastFPSUpdateTime: float = time.time()
        self.previousFrame: float = time.time()
        self.toLog: bool = False

    def updateTime(self):
        now = time.time()
        elapsed = now - self.previousFrame
        self.previousFrame = now

        if now - self.lastFPSUpdateTime >= 1:
            self.lastFPS = 1 / elapsed
            self.lastFPSUpdateTime = now
            self.toLog = True

    def logFPS(self):
        if self.toLog:
            logging.info(f"The FPS is {self.lastFPS: .2f}")
            self.toLog = False

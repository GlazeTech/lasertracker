from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass
class TrackConfig:
    pass


def _load_movie(movie_path: Path) -> cv2.VideoCapture:
    return cv2.VideoCapture(str(movie_path))


def track(movie_path: Path, config: TrackConfig) -> None:
    """Tracks a laser dot in a movie.

    Args:
    ----
        movie_path: Path to movie to analyze
        config: Tracking configuration
    """
    movie = _load_movie(movie_path)
    count = 0
    while movie.isOpened():
        read_correctly, frame = movie.read()
        from matplotlib import pyplot as plt

        blurred = cv2.medianBlur(frame, ksize=11)
        median = np.median(blurred.flatten())
        maximum = np.max(blurred.flatten())
        midpoint = (median + maximum) / 2
        mask = frame[:, :, 2] < midpoint
        blurred[mask] = 0
        print(median, maximum)
        print("ey")
        print(blurred[:, :, 2])
        plt.imshow(blurred[:, :, 2])
        plt.show()
        exit()


if __name__ == "__main__":
    import os

    track(os.environ["LASERTRACKER_MOV_PATH"], config=TrackConfig())

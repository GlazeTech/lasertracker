import os
from pathlib import Path

import cv2
import pytest

import lasertracker


@pytest.fixture()
def movie_path() -> Path:
    return Path(os.environ[("LASERTRACKER_MOV_PATH")])


def test_tracking(movie_path: Path) -> None:
    points = lasertracker.find_red_laserdots(movie_path, downscale=20)
    movie = lasertracker._tracking._load_video(movie_path)
    assert len(points) == movie.get(cv2.CAP_PROP_FRAME_COUNT)

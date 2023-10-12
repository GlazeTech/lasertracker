import os
from pathlib import Path

import pytest

from lasertracker import TrackConfig, track
from lasertracker.track import _load_movie


@pytest.fixture()
def movie_path() -> Path:
    return Path(os.environ[("LASERTRACKER_MOV_PATH")])


def test_track(movie_path: Path) -> None:
    track(movie_path, TrackConfig())

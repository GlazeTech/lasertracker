from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
import numpy.typing as npt
from cv2.typing import MatLike


@dataclass
class Point:
    x: int
    y: int

    def __mul__(self: "Point", number: int) -> "Point":
        return Point(self.x * number, self.y * number)


def _load_video(movie_path: Path) -> cv2.VideoCapture:
    return cv2.VideoCapture(str(movie_path))


def _get_hist(
    img: MatLike,
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    hist, edges = np.histogram(img.flatten(), bins=np.arange(257) - 0.5)
    mask = hist > 0
    centers = (edges[:-1] + edges[1:]) / 2
    return centers[mask], hist[mask]


def _remove_background(img: MatLike) -> MatLike:
    centers, hist = _get_hist(img)
    flattened = img.flatten()
    median = centers[np.argmax(hist)]
    maximum = np.max(flattened)
    midpoint = (median + maximum) / 2
    mask = img < midpoint
    img[mask] = 0

    return img


def _add_blue_dot(frame: MatLike, point: Point, radius: int = 10) -> MatLike:
    blue_color = (255, 0, 0)  # BGR color for blue
    cv2.circle(frame, (point.x, point.y), radius, blue_color, -1)
    return frame


def find_laserdot_singleframe(channel: MatLike) -> Point:
    """Finds a laserdot in a single channel of a video-frame.

    Args:
        channel: Channel of a video.

    Returns:
        Point: Found laserdot position.
    """
    ksize = 2 * int(np.min(channel.shape) // 40) + 1
    median_blurred = cv2.medianBlur(channel, ksize=ksize)
    img_no_bg = _remove_background(median_blurred)
    moments = cv2.moments(img_no_bg)
    x = moments["m10"] / moments["m00"]
    y = moments["m01"] / moments["m00"]
    return Point(int(x), int(y))


def find_red_laserdots(video_path: str, downscale: int = 1) -> list[Point]:
    """Tracks a red laserdot in a movie.

    Args:
        video_path: Path on filesystem to video.
        downscale: Number to downscale videosize with for faster analysis, but less precise results. Defaults to 1.

    Returns:
        list[Point]: Pixel-values for each frame of the found laserdots
    """
    movie = _load_video(Path(video_path))
    tracked_points: list[Point] = []
    while movie.isOpened():
        read_correctly, frame = movie.read()
        if not read_correctly:
            break
        channel = frame[:, :, 2][::downscale, ::downscale]
        tracked_points.append(find_laserdot_singleframe(channel) * downscale)
    return tracked_points


def make_tracked_video(
    video_path: str,
    output_name: str = "tracked_video",
    downscale: int = 1,
) -> None:
    """Tracks a laser dot in a movie.

    Args:
        video_path (Path): Path on filesystem to video.
        output_name (str, optional): Name of output video with tracked laser. Defaults to "tracked_video".
        downscale (int, optional): Number to downscale videosize with for faster analysis, but less precise results. Defaults to 1.
    """
    movie = _load_video(Path(video_path))

    output_video = cv2.VideoWriter(
        f"{output_name}.mp4",
        cv2.VideoWriter.fourcc(*"mp4v"),
        movie.get(cv2.CAP_PROP_FPS),
        (int(movie.get(3)), int(movie.get(4))),
    )

    while movie.isOpened():
        read_correctly, frame = movie.read()
        if not read_correctly:
            break
        channel = frame[:, :, 2][::downscale, ::downscale]

        point = find_laserdot_singleframe(channel)
        frame_with_dot = _add_blue_dot(frame.copy(), point * downscale)
        output_video.write(frame_with_dot)

    output_video.release()
    movie.release()
    cv2.destroyAllWindows()

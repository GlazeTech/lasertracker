# Lasertracker

This is a small package for tracking a laserpointer in a movie.

## Usage
First, install the package using 
```
pip install git+https://github.com/GlazeTech/App.git@v<DESIRED_VERSION>
```
e.g.
```
pip install git+https://github.com/GlazeTech/App.git@v0.1.0
```

To track a pointer in a movie and save a new movie, run

```python
import lasertracker

lasertracker.make_tracked_video(
    video_path="my_video.mp4",
    output_name="my_tracked_movie",
)
```

If you are only interested in the tracked points for further processing, run

```python
import lasertracker

points = lasertracker.find_red_laserdots(
    video_path="my_video.mp4"
)

print(points[0].x, points[0].y)
```
```
> 810 410
```

## Shortcomings
As of right now, it is only possible to track a red laserdot. Reach out if further functionality is required.
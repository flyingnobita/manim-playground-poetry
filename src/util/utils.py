from manim import *


def displayNumberPlane(self):
    """
    Creates and returns a NumberPlane with predefined styling.
    """
    number_plane = NumberPlane(
        background_line_style={
            "stroke_color": TEAL,
            "stroke_width": 4,
            "stroke_opacity": 0.6,
        }
    )
    self.add(number_plane)

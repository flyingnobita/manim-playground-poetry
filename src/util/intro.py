from manim import *


def displayLogo(self):
    """
    Creates and displays a logo group consisting of an image and text.
    """
    logo = ImageMobject("assets/flying_nobita_logo_upscale_no_bg.png")
    logo.scale(0.5)
    logoText1 = Text("Flying", font_size=30, color=WHITE, font="DORAEMON")
    logoText1.next_to(logo, LEFT, buff=0.25)
    logoText2 = Text("Nobita", font_size=30, color="#ECAE5C", font="DORAEMON")
    logoText2.next_to(logo, RIGHT, buff=0.25)
    logoGroup = Group(logo, logoText1, logoText2)
    logoGroup.center()

    # Animate the logo
    self.play(FadeIn(logoGroup))
    self.wait(1)
    self.play(FadeOut(logoGroup))


def displayTitle(self, title_text, intro_text=None):
    """
    Creates and displays a title and optional introduction text with animations.

    Args:
        title_text (str): The main title text to display
        intro_text (str, optional): The introduction text to display below the title
    """
    # Title
    title = Text(title_text, font_size=40)

    if intro_text:
        # Title
        title.center().move_to(UP * 0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Introduction text
        intro = Text(intro_text, font_size=30)
        intro.next_to(title, DOWN, buff=0.5)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro), FadeOut(title))
    else:
        title.center()
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

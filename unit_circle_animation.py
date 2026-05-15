"""
The Unit Circle: How Sine and Cosine Are Born from Rotation.

A Manim Community animation that turns one of the most memorized — and
least understood — high-school facts into an "aha!" moment:

    sin(theta) is just the height of a point spinning on the unit circle,
    cos(theta) is just its horizontal distance,
    and sin^2(theta) + cos^2(theta) = 1 is the Pythagorean theorem
    applied to a radius of length 1.

Run:  manim -pqh unit_circle_animation.py UnitCircleSymphony
"""

from manim import *
import numpy as np


class UnitCircleSymphony(Scene):
    def construct(self):
        self.opening_title()
        circle_axes, wave_axes, circle = self.build_stage()
        theta = ValueTracker(1e-3)
        moving = self.add_rotating_apparatus(circle_axes, theta)
        self.trace_sine_wave(circle_axes, wave_axes, theta, moving)
        self.trace_cosine_wave(circle_axes, wave_axes, theta, moving)
        self.pythagorean_finale(circle_axes, circle, theta, moving)

    # ------------------------------------------------------------------ #
    # 1. Title card                                                      #
    # ------------------------------------------------------------------ #
    def opening_title(self):
        title = Text("The Unit Circle", font_size=64, color=BLUE_B)
        subtitle = Text(
            "where sine and cosine are born",
            font_size=30,
            color=GREY_B,
            slant=ITALIC,
        ).next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.8)
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.wait(1.6)
        self.play(FadeOut(VGroup(title, subtitle)))

    # ------------------------------------------------------------------ #
    # 2. Stage: circle on the left, wave canvas on the right             #
    # ------------------------------------------------------------------ #
    def build_stage(self):
        circle_axes = Axes(
            x_range=[-1.4, 1.4, 1],
            y_range=[-1.4, 1.4, 1],
            x_length=4.2,
            y_length=4.2,
            tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        ).to_edge(LEFT, buff=0.6)

        wave_axes = Axes(
            x_range=[0, 2 * PI + 0.3, PI / 2],
            y_range=[-1.4, 1.4, 1],
            x_length=7,
            y_length=4.2,
            tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        ).next_to(circle_axes, RIGHT, buff=0.6)

        radius_px = circle_axes.c2p(1, 0)[0] - circle_axes.c2p(0, 0)[0]
        circle = Circle(radius=radius_px, color=BLUE_C, stroke_width=3).move_to(
            circle_axes.c2p(0, 0)
        )

        # Pi-flavored x-axis ticks on the wave canvas.
        pi_labels = VGroup(
            MathTex(r"\tfrac{\pi}{2}"),
            MathTex(r"\pi"),
            MathTex(r"\tfrac{3\pi}{2}"),
            MathTex(r"2\pi"),
        )
        for lbl, x in zip(pi_labels, [PI / 2, PI, 3 * PI / 2, 2 * PI]):
            lbl.scale(0.6).next_to(wave_axes.c2p(x, 0), DOWN, buff=0.15)

        circle_label = MathTex(r"x^2 + y^2 = 1", color=BLUE_C).scale(0.7)
        circle_label.next_to(circle_axes, UP, buff=0.15)

        wave_label = Text("the wave canvas", font_size=22, color=GREY_B)
        wave_label.next_to(wave_axes, UP, buff=0.15)

        self.play(Create(circle_axes), Create(wave_axes), run_time=1.2)
        self.play(
            Create(circle),
            Write(pi_labels),
            FadeIn(circle_label, shift=DOWN * 0.2),
            FadeIn(wave_label, shift=DOWN * 0.2),
        )
        self.wait(0.6)

        return circle_axes, wave_axes, circle

    # ------------------------------------------------------------------ #
    # 3. The spinning apparatus: dot, radius, angle, projections         #
    # ------------------------------------------------------------------ #
    def add_rotating_apparatus(self, circle_axes, theta):
        def cs(x, y):
            return circle_axes.c2p(x, y)

        origin = cs(0, 0)

        dot = always_redraw(
            lambda: Dot(
                cs(np.cos(theta.get_value()), np.sin(theta.get_value())),
                color=YELLOW,
                radius=0.08,
            )
        )

        radius_line = always_redraw(
            lambda: Line(
                origin,
                cs(np.cos(theta.get_value()), np.sin(theta.get_value())),
                color=YELLOW,
                stroke_width=3,
            )
        )

        angle_arc = always_redraw(
            lambda: Arc(
                radius=0.45,
                start_angle=0,
                angle=max(theta.get_value(), 1e-3),
                color=ORANGE,
                stroke_width=4,
            ).move_arc_center_to(origin)
        )

        theta_label = always_redraw(
            lambda: MathTex(r"\theta", color=ORANGE)
            .scale(0.7)
            .move_to(
                cs(
                    0.7 * np.cos(theta.get_value() / 2),
                    0.7 * np.sin(theta.get_value() / 2),
                )
            )
        )

        # Vertical drop from point to x-axis (this segment IS sin theta).
        sin_segment = always_redraw(
            lambda: Line(
                cs(np.cos(theta.get_value()), 0),
                cs(np.cos(theta.get_value()), np.sin(theta.get_value())),
                color=GREEN,
                stroke_width=5,
            )
        )

        # Horizontal segment from origin to x-axis foot (this IS cos theta).
        cos_segment = always_redraw(
            lambda: Line(
                origin,
                cs(np.cos(theta.get_value()), 0),
                color=RED,
                stroke_width=5,
            )
        )

        self.play(
            FadeIn(dot, scale=0.5),
            Create(radius_line),
            Create(angle_arc),
            Write(theta_label),
        )
        self.wait(0.4)

        # Spin the radius once just to introduce theta.
        self.play(theta.animate.set_value(PI / 3), run_time=1.2, rate_func=smooth)
        self.wait(0.4)

        return {
            "dot": dot,
            "radius_line": radius_line,
            "angle_arc": angle_arc,
            "theta_label": theta_label,
            "sin_segment": sin_segment,
            "cos_segment": cos_segment,
        }

    # ------------------------------------------------------------------ #
    # 4. Trace the sine wave from the vertical projection                #
    # ------------------------------------------------------------------ #
    def trace_sine_wave(self, circle_axes, wave_axes, theta, moving):
        def cs(x, y):
            return circle_axes.c2p(x, y)

        def ws(x, y):
            return wave_axes.c2p(x, y)

        # Reveal: the green segment IS sin(theta).
        sin_callout = MathTex(r"\sin\theta", color=GREEN).scale(0.7)
        sin_callout.add_updater(
            lambda m: m.next_to(
                cs(np.cos(theta.get_value()), np.sin(theta.get_value()) / 2),
                RIGHT,
                buff=0.1,
            )
        )

        self.play(FadeIn(moving["sin_segment"]))
        self.play(Write(sin_callout))
        self.wait(0.6)

        # Sine wave being drawn on the wave canvas.
        sine_curve = always_redraw(
            lambda: ParametricFunction(
                lambda t: ws(t, np.sin(t)),
                t_range=[0, max(theta.get_value(), 1e-3)],
                color=GREEN,
                stroke_width=4,
            )
        )
        sine_dot = always_redraw(
            lambda: Dot(
                ws(theta.get_value(), np.sin(theta.get_value())),
                color=GREEN,
                radius=0.07,
            )
        )
        height_link = always_redraw(
            lambda: DashedLine(
                cs(np.cos(theta.get_value()), np.sin(theta.get_value())),
                ws(theta.get_value(), np.sin(theta.get_value())),
                color=GREEN,
                stroke_opacity=0.45,
                dash_length=0.08,
            )
        )

        self.add(sine_curve)
        self.play(FadeIn(sine_dot), Create(height_link))

        # The headline equation.
        formula = MathTex(
            r"y(\theta) = \sin\theta", color=GREEN
        ).scale(0.8).to_corner(UR, buff=0.5)
        self.play(Write(formula))

        # Slow, hypnotic full rotation while the wave is drawn.
        self.play(
            theta.animate.set_value(2 * PI),
            run_time=7,
            rate_func=linear,
        )
        self.wait(0.8)

        # Park theta and tidy callouts before introducing cosine.
        sin_callout.clear_updaters()
        self.play(FadeOut(sin_callout), FadeOut(formula))

        # Rewind to a generic angle.
        self.play(theta.animate.set_value(PI / 3), run_time=0.8)

        moving["sine_curve"] = sine_curve
        moving["sine_dot"] = sine_dot
        moving["height_link"] = height_link

    # ------------------------------------------------------------------ #
    # 5. Trace the cosine wave from the horizontal projection            #
    # ------------------------------------------------------------------ #
    def trace_cosine_wave(self, circle_axes, wave_axes, theta, moving):
        def cs(x, y):
            return circle_axes.c2p(x, y)

        def ws(x, y):
            return wave_axes.c2p(x, y)

        cos_callout = MathTex(r"\cos\theta", color=RED).scale(0.7)
        cos_callout.add_updater(
            lambda m: m.next_to(
                cs(np.cos(theta.get_value()) / 2, 0),
                DOWN,
                buff=0.12,
            )
        )

        self.play(FadeIn(moving["cos_segment"]))
        self.play(Write(cos_callout))
        self.wait(0.5)

        cosine_curve = always_redraw(
            lambda: ParametricFunction(
                lambda t: ws(t, np.cos(t)),
                t_range=[PI / 3, max(theta.get_value(), PI / 3 + 1e-3)],
                color=RED,
                stroke_width=4,
            )
        )
        cosine_dot = always_redraw(
            lambda: Dot(
                ws(theta.get_value(), np.cos(theta.get_value())),
                color=RED,
                radius=0.07,
            )
        )

        # A fresh starting segment of the cosine curve from 0..PI/3 so it
        # looks continuous even though theta starts at PI/3 here.
        cos_prelude = ParametricFunction(
            lambda t: ws(t, np.cos(t)),
            t_range=[0, PI / 3],
            color=RED,
            stroke_width=4,
        )

        self.add(cosine_curve, cos_prelude)
        self.play(FadeIn(cosine_dot))

        formula = MathTex(
            r"x(\theta) = \cos\theta", color=RED
        ).scale(0.8).to_corner(UR, buff=0.5)
        self.play(Write(formula))

        # Another graceful full rotation, this time both waves grow together.
        self.play(
            theta.animate.set_value(2 * PI + PI / 3),
            run_time=7,
            rate_func=linear,
        )
        self.wait(0.6)

        cos_callout.clear_updaters()
        self.play(FadeOut(cos_callout), FadeOut(formula))

        moving["cosine_curve"] = cosine_curve
        moving["cosine_dot"] = cosine_dot
        moving["cos_prelude"] = cos_prelude

    # ------------------------------------------------------------------ #
    # 6. The Pythagorean punchline                                       #
    # ------------------------------------------------------------------ #
    def pythagorean_finale(self, circle_axes, circle, theta, moving):
        # Bring theta back to a clean, illustrative angle.
        self.play(theta.animate.set_value(PI / 3 + 2 * PI), run_time=0.8)

        def cs(x, y):
            return circle_axes.c2p(x, y)

        # Highlight the right triangle: radius (hypotenuse=1), cos, sin.
        c = np.cos(PI / 3)
        s = np.sin(PI / 3)
        triangle = Polygon(
            cs(0, 0), cs(c, 0), cs(c, s),
            color=YELLOW, fill_color=YELLOW, fill_opacity=0.12, stroke_width=3,
        )

        # Tiny right-angle square at the foot.
        right_angle = Square(side_length=0.18, color=WHITE, stroke_width=2)
        right_angle.move_to(cs(c, 0) + np.array([-0.09, 0.09, 0]))

        hyp_label = MathTex("1", color=YELLOW).scale(0.7).move_to(
            cs(c / 2 - 0.15, s / 2 + 0.15)
        )
        sin_lbl = MathTex(r"\sin\theta", color=GREEN).scale(0.55).next_to(
            cs(c, s / 2), RIGHT, buff=0.08
        )
        cos_lbl = MathTex(r"\cos\theta", color=RED).scale(0.55).next_to(
            cs(c / 2, 0), DOWN, buff=0.1
        )

        self.play(FadeIn(triangle), FadeIn(right_angle))
        self.play(Write(hyp_label), Write(sin_lbl), Write(cos_lbl))
        self.wait(0.6)

        # The grand reveal at the bottom: Pythagoras on a unit hypotenuse.
        identity = MathTex(
            r"\sin^2\theta", "+", r"\cos^2\theta", "=", "1",
            font_size=56,
        )
        identity[0].set_color(GREEN)
        identity[2].set_color(RED)
        identity[4].set_color(YELLOW)
        identity.to_edge(DOWN, buff=0.5)

        self.play(Write(identity), run_time=2.2)
        self.wait(1.2)

        # Final flourish: gently spin the whole picture so the identity
        # visibly holds for every theta.
        box = SurroundingRectangle(identity, color=BLUE_B, buff=0.18, corner_radius=0.1)
        self.play(Create(box))
        self.play(theta.animate.set_value(PI / 3 + 4 * PI), run_time=6, rate_func=linear)
        self.wait(1.5)


# A short, social-friendly cut: just the unit-circle-to-sine loop.
class CircleToSineLoop(Scene):
    def construct(self):
        axes_l = Axes(
            x_range=[-1.4, 1.4, 1], y_range=[-1.4, 1.4, 1],
            x_length=4, y_length=4, tips=False,
        ).to_edge(LEFT, buff=0.7)
        axes_r = Axes(
            x_range=[0, 2 * PI + 0.3, PI / 2], y_range=[-1.4, 1.4, 1],
            x_length=7, y_length=4, tips=False,
        ).next_to(axes_l, RIGHT, buff=0.5)

        r = axes_l.c2p(1, 0)[0] - axes_l.c2p(0, 0)[0]
        circle = Circle(radius=r, color=BLUE_C).move_to(axes_l.c2p(0, 0))

        theta = ValueTracker(1e-3)
        dot = always_redraw(
            lambda: Dot(axes_l.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())), color=YELLOW)
        )
        radius = always_redraw(
            lambda: Line(axes_l.c2p(0, 0),
                         axes_l.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())),
                         color=YELLOW)
        )
        drop = always_redraw(
            lambda: Line(axes_l.c2p(np.cos(theta.get_value()), 0),
                         axes_l.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())),
                         color=GREEN, stroke_width=5)
        )
        curve = always_redraw(
            lambda: ParametricFunction(
                lambda t: axes_r.c2p(t, np.sin(t)),
                t_range=[0, max(theta.get_value(), 1e-3)],
                color=GREEN,
            )
        )

        self.add(axes_l, axes_r, circle, radius, dot, drop, curve)
        self.play(theta.animate.set_value(2 * PI), run_time=6, rate_func=linear)
        self.wait(0.5)

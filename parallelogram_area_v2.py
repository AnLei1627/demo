"""114 學測數學甲第 11 題 — 平行四邊形面積（直線方程式 + 點到直線距離）"""

from manim import *
import numpy as np


# ---- 板書配色 ----
COLOR_L1     = YELLOW           # ℓ₁: 5x - y = 0
COLOR_L2     = PINK             # ℓ₂: 2x + 3y = 0
COLOR_BIG_L1 = ORANGE           # L₁: 5x - y = 102
COLOR_BIG_L2 = RED              # L₂: 2x + 3y = 34
COLOR_P      = "#FF5577"
COLOR_Q      = BLUE_C
COLOR_R      = TEAL
COLOR_RP     = GREEN
COLOR_BASE   = GREEN
COLOR_HEIGHT = PURPLE_A
COLOR_FILL   = "#FFD54F"
COLOR_GOLD   = "#FFD700"

CJK = "Noto Sans CJK TC"


def line_endpoints(a, b, c, x_min, x_max, y_min, y_max):
    """ax + by = c 與矩形 [x_min,x_max]×[y_min,y_max] 的兩個交點。"""
    pts = []
    if abs(b) > 1e-9:
        for x in (x_min, x_max):
            y = (c - a * x) / b
            if y_min - 1e-6 <= y <= y_max + 1e-6:
                pts.append((x, y))
    if abs(a) > 1e-9:
        for y in (y_min, y_max):
            x = (c - b * y) / a
            if x_min - 1e-6 <= x <= x_max + 1e-6:
                pts.append((x, y))
    seen, uniq = set(), []
    for p in pts:
        k = (round(p[0], 4), round(p[1], 4))
        if k not in seen:
            seen.add(k)
            uniq.append(p)
    return uniq[:2]


def make_line(a, b, c, plane, **style):
    eps = line_endpoints(a, b, c,
                         plane.x_range[0], plane.x_range[1],
                         plane.y_range[0], plane.y_range[1])
    if len(eps) < 2:
        return None
    return Line(plane.c2p(*eps[0]), plane.c2p(*eps[1]), **style)


class ParallelogramAreaV2(Scene):
    def construct(self):
        self.section_1_setup()
        self.wait(1.8)
        self.section_2_lines_through_P()
        self.wait(1.8)
        self.section_3_find_Q_R()
        self.wait(1.8)
        self.section_4_lines_through_R()
        self.wait(1.8)
        self.section_5_find_Rp()
        self.wait(1.8)
        self.section_6_base_length()
        self.wait(1.8)
        self.section_7_height()
        self.wait(1.8)
        self.section_8_area_finale()

    # ------------------------------------------------------------------
    # Section 1: 場景建立
    # ------------------------------------------------------------------
    def section_1_setup(self):
        # y range 用 [-13, 11] 以收進整個平行四邊形（含 R''(2,10) 與
        # L₂ 垂足 (68/13, 102/13)≈(5.23, 7.85)）。x 仍用 [-3, 25]。
        plane = NumberPlane(
            x_range=[-3, 25, 1],
            y_range=[-13, 11, 1],
            x_length=7.2,
            y_length=6.2,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.35,
                "stroke_width": 1,
            },
            axis_config={"stroke_color": GREY_B, "stroke_width": 1.5},
        ).to_edge(LEFT, buff=0.35).shift(DOWN * 0.35)
        self.plane = plane

        title = Text("114 數甲第 11 題", font=CJK,
                     font_size=34, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.18)
        self.title = title

        hint = Text("將 P 平移到原點（平移不改變面積）",
                    font=CJK, font_size=22, color=GREY_B)
        hint.next_to(title, DOWN, buff=0.12)

        self.play(Write(title), FadeIn(plane), run_time=2.4)
        self.play(FadeIn(hint, shift=DOWN * 0.2))
        self.wait(2.0)
        self.play(FadeOut(hint))

    # ------------------------------------------------------------------
    # Section 2: 過 P 的兩條邊所在直線
    # ------------------------------------------------------------------
    def section_2_lines_through_P(self):
        plane = self.plane
        P_pt = plane.c2p(0, 0)
        self.P_pt = P_pt

        P_dot = Dot(P_pt, color=COLOR_P, radius=0.09)
        P_label = MathTex("P", color=COLOR_P).scale(0.7).next_to(P_dot, UL, buff=0.05)
        self.P_dot, self.P_label = P_dot, P_label

        ell1 = make_line(5, -1, 0, plane, color=COLOR_L1, stroke_width=3)
        ell2 = make_line(2, 3, 0, plane, color=COLOR_L2, stroke_width=3)
        self.ell1, self.ell2 = ell1, ell2

        eq_ell1 = MathTex(r"\ell_1:\ 5x - y = 0", color=COLOR_L1).scale(0.62)
        eq_ell2 = MathTex(r"\ell_2:\ 2x + 3y = 0", color=COLOR_L2).scale(0.62)
        eq_box = VGroup(eq_ell1, eq_ell2).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        eq_box.to_edge(RIGHT, buff=0.35).shift(UP * 2.4)
        self.eq_box = eq_box

        note1 = Text("ℓ₁ 平行於 5x−y=0",
                     font=CJK, font_size=18, color=GREY_B)
        note2 = Text("ℓ₂ 垂直於 3x−2y=0",
                     font=CJK, font_size=18, color=GREY_B)
        notes = VGroup(note1, note2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        notes.next_to(eq_box, DOWN, buff=0.25).align_to(eq_box, LEFT)
        self.notes = notes

        self.play(FadeIn(P_dot, scale=0.5), Write(P_label))
        self.wait(0.3)
        self.play(Create(ell1), Write(eq_ell1), FadeIn(note1, shift=LEFT * 0.2),
                  run_time=1.4)
        self.wait(0.4)
        self.play(Create(ell2), Write(eq_ell2), FadeIn(note2, shift=LEFT * 0.2),
                  run_time=1.4)

    # ------------------------------------------------------------------
    # Section 3: 由 PQ⃗ 找 Q 與對角頂點 R
    # ------------------------------------------------------------------
    def section_3_find_Q_R(self):
        plane = self.plane
        P_pt = self.P_pt
        Q_pt = plane.c2p(10, -1)
        R_pt = plane.c2p(20, -2)
        self.Q_pt, self.R_pt = Q_pt, R_pt

        Q_dot = Dot(Q_pt, color=COLOR_Q, radius=0.085)
        R_dot = Dot(R_pt, color=COLOR_R, radius=0.085)
        Q_label = MathTex("Q", color=COLOR_Q).scale(0.65).next_to(Q_dot, UP, buff=0.08)
        R_label = MathTex("R", color=COLOR_R).scale(0.65).next_to(R_dot, UR, buff=0.05)
        self.Q_dot, self.R_dot = Q_dot, R_dot

        PQ_arrow = Arrow(P_pt, Q_pt, color=COLOR_Q, buff=0.05,
                         stroke_width=4, tip_length=0.18,
                         max_tip_length_to_length_ratio=0.08)
        PQ_lbl = MathTex(r"\vec{PQ}=(10,-1)", color=COLOR_Q).scale(0.5)
        PQ_lbl.next_to(PQ_arrow.get_center(), UP, buff=0.04)
        QR_arrow = Arrow(Q_pt, R_pt, color=COLOR_R, buff=0.05,
                         stroke_width=4, tip_length=0.18,
                         max_tip_length_to_length_ratio=0.08)

        R_eq = MathTex(r"R = 2Q = (20,\,-2)", color=COLOR_R).scale(0.6)
        R_eq.next_to(self.notes, DOWN, buff=0.3).align_to(self.notes, LEFT)
        Q_note = Text("Q 為對角線中點 ⇒ R 與 P 對角",
                      font=CJK, font_size=17, color=GREY_B)
        Q_note.next_to(R_eq, DOWN, buff=0.15).align_to(R_eq, LEFT)
        self.R_eq, self.Q_note = R_eq, Q_note

        self.play(GrowArrow(PQ_arrow), FadeIn(Q_dot),
                  Write(Q_label), FadeIn(PQ_lbl), run_time=1.4)
        self.wait(0.8)
        self.play(GrowArrow(QR_arrow), FadeIn(R_dot), Write(R_label),
                  run_time=1.4)
        self.wait(0.4)
        self.play(Write(R_eq), FadeIn(Q_note, shift=UP * 0.2))
        self.PQ_arrow, self.QR_arrow, self.PQ_lbl = PQ_arrow, QR_arrow, PQ_lbl

    # ------------------------------------------------------------------
    # Section 4: 過 R 畫平行邊 L₁, L₂
    # ------------------------------------------------------------------
    def section_4_lines_through_R(self):
        plane = self.plane

        # 騰出右側面板
        self.play(FadeOut(self.Q_note), FadeOut(self.PQ_lbl))

        L1 = make_line(5, -1, 102, plane, color=COLOR_BIG_L1, stroke_width=3)
        L2 = make_line(2, 3, 34, plane, color=COLOR_BIG_L2, stroke_width=3)
        self.L1, self.L2 = L1, L2

        calc1 = MathTex(r"5(20)-(-2)=102", color=COLOR_BIG_L1).scale(0.55)
        eq_L1 = MathTex(r"L_1:\ 5x-y=102", color=COLOR_BIG_L1).scale(0.6)
        calc2 = MathTex(r"2(20)+3(-2)=34", color=COLOR_BIG_L2).scale(0.55)
        eq_L2 = MathTex(r"L_2:\ 2x+3y=34", color=COLOR_BIG_L2).scale(0.6)

        calc_group = VGroup(calc1, eq_L1, calc2, eq_L2).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18)
        calc_group.next_to(self.R_eq, DOWN, buff=0.3).align_to(self.R_eq, LEFT)
        self.calc_group = calc_group

        self.play(Write(calc1))
        self.play(Create(L1), Write(eq_L1), run_time=1.4)
        self.wait(0.7)
        self.play(Write(calc2))
        self.play(Create(L2), Write(eq_L2), run_time=1.4)
        self.wait(0.5)

        # 平行四邊形填色
        para_pts = [
            plane.c2p(0, 0),       # P
            plane.c2p(18, -12),    # R'
            plane.c2p(20, -2),     # R
            plane.c2p(2, 10),      # R''
        ]
        para = Polygon(*para_pts,
                       fill_color=COLOR_FILL, fill_opacity=0.20,
                       stroke_width=0)
        self.para = para
        self.play(FadeIn(para), run_time=1.4)
        self.wait(0.6)

    # ------------------------------------------------------------------
    # Section 5: 解聯立求 R'
    # ------------------------------------------------------------------
    def section_5_find_Rp(self):
        plane = self.plane

        # 清右側面板
        self.play(FadeOut(self.calc_group), FadeOut(self.R_eq))

        sys_eq = MathTex(
            r"\begin{cases} 2x + 3y = 0 \\[2pt] 5x - y = 102 \end{cases}"
        ).scale(0.6)
        sys_eq.next_to(self.notes, DOWN, buff=0.3).align_to(self.notes, LEFT)

        step1 = MathTex(r"(2)\times 3:\ 15x-3y=306").scale(0.5)
        step2 = MathTex(r"(1)+(2)\times 3:\ 17x=306").scale(0.5)
        step3 = MathTex(r"x=18,\ \ y=-12").scale(0.6).set_color(COLOR_RP)

        steps = VGroup(step1, step2, step3).arrange(
            DOWN, aligned_edge=LEFT, buff=0.16)
        steps.next_to(sys_eq, DOWN, buff=0.25).align_to(sys_eq, LEFT)
        self.sys_eq, self.steps = sys_eq, steps

        self.play(Write(sys_eq))
        self.wait(0.4)
        self.play(Write(step1))
        self.wait(0.3)
        self.play(Write(step2))
        self.wait(0.3)
        self.play(Write(step3))
        self.wait(0.6)

        Rp_pt = plane.c2p(18, -12)
        Rp_dot = Dot(Rp_pt, color=COLOR_RP, radius=0.09)
        Rp_label = MathTex(r"R'(18,-12)", color=COLOR_RP).scale(0.55)
        Rp_label.next_to(Rp_dot, DR, buff=0.05)
        self.Rp_pt, self.Rp_dot, self.Rp_label = Rp_pt, Rp_dot, Rp_label

        base_line = Line(self.P_pt, Rp_pt, color=COLOR_BASE, stroke_width=6)
        self.base_line = base_line

        self.play(FadeIn(Rp_dot, scale=0.5), Write(Rp_label))
        self.wait(0.5)
        self.play(Create(base_line), run_time=1.4)

        # 「底」標籤，貼在 PR' 外側
        mid = (np.array(self.P_pt) + np.array(Rp_pt)) / 2
        diff = np.array(Rp_pt) - np.array(self.P_pt)
        perp = np.array([-diff[1], diff[0], 0])
        perp = perp / np.linalg.norm(perp) * 0.35
        base_callout = Text("底", font=CJK, font_size=24,
                            color=COLOR_BASE, weight=BOLD)
        base_callout.move_to(mid + perp)
        self.play(FadeIn(base_callout))
        self.base_callout = base_callout

    # ------------------------------------------------------------------
    # Section 6: 計算底長
    # ------------------------------------------------------------------
    def section_6_base_length(self):
        self.play(FadeOut(self.sys_eq), FadeOut(self.steps))

        c1 = MathTex(r"|PR'|=\sqrt{18^2+(-12)^2}", color=COLOR_BASE).scale(0.6)
        c2 = MathTex(r"=\sqrt{324+144}=\sqrt{468}", color=COLOR_BASE).scale(0.6)
        c3 = MathTex(r"=6\sqrt{13}", color=COLOR_BASE).scale(0.78)

        grp = VGroup(c1, c2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        grp.next_to(self.notes, DOWN, buff=0.3).align_to(self.notes, LEFT)
        c3.next_to(grp, DOWN, buff=0.18).align_to(grp, LEFT)
        self._base_intermediate = VGroup(c1, c2)

        self.play(Write(c1))
        self.wait(0.4)
        self.play(Write(c2))
        self.wait(0.4)
        self.play(TransformFromCopy(c2, c3), run_time=1.4)
        self.wait(1.2)

        # 收合：保留簡化後的 6√13
        self.play(FadeOut(c1), FadeOut(c2))
        c3.generate_target()
        c3.target.next_to(self.notes, DOWN, buff=0.3).align_to(self.notes, LEFT)
        self.play(MoveToTarget(c3))
        self.base_label = c3

    # ------------------------------------------------------------------
    # Section 7: 計算高（點到直線距離）
    # ------------------------------------------------------------------
    def section_7_height(self):
        plane = self.plane

        # 從 P=(0,0) 沿 (2,3) 方向到 L₂: 2x+3y=34 的垂足
        F_plane = (68 / 13, 102 / 13)
        F_pt = plane.c2p(*F_plane)
        perp_line = DashedLine(self.P_pt, F_pt,
                               color=COLOR_HEIGHT, stroke_width=4,
                               dash_length=0.14)

        # 在垂足處畫直角小方塊（朝向 P）
        size = 0.20
        pf_vec = np.array(self.P_pt) - np.array(F_pt)
        pf_unit = pf_vec / np.linalg.norm(pf_vec)
        tangent = np.array([-pf_unit[1], pf_unit[0], 0])
        ra_square = Polygon(
            np.array(F_pt),
            np.array(F_pt) + pf_unit * size,
            np.array(F_pt) + pf_unit * size + tangent * size,
            np.array(F_pt) + tangent * size,
            color=COLOR_HEIGHT, stroke_width=2,
            fill_color=COLOR_HEIGHT, fill_opacity=0.0,
        )

        mid = (np.array(self.P_pt) + np.array(F_pt)) / 2
        # 垂線「外側」放置標籤
        side = tangent * 0.32
        height_lbl = Text("高", font=CJK, font_size=24,
                          color=COLOR_HEIGHT, weight=BOLD)
        height_lbl.move_to(mid + side)

        self.play(Create(perp_line), run_time=1.4)
        self.play(FadeIn(ra_square), Write(height_lbl))
        self.wait(0.4)

        # 點到直線距離公式
        f1 = VGroup(
            Text("高", font=CJK, color=COLOR_HEIGHT).scale(0.45),
            MathTex(r"=d(P,L_2)", color=COLOR_HEIGHT).scale(0.6),
        ).arrange(RIGHT, buff=0.08)
        f2 = MathTex(r"=\dfrac{|2(0)+3(0)-34|}{\sqrt{2^2+3^2}}",
                     color=COLOR_HEIGHT).scale(0.6)
        f3 = MathTex(r"=\dfrac{34}{\sqrt{13}}",
                     color=COLOR_HEIGHT).scale(0.78)

        grp = VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        grp.next_to(self.base_label, DOWN, buff=0.3).align_to(self.base_label, LEFT)
        f3.next_to(grp, DOWN, buff=0.18).align_to(grp, LEFT)

        self.play(Write(f1))
        self.wait(0.4)
        self.play(Write(f2))
        self.wait(0.5)
        self.play(TransformFromCopy(f2, f3), run_time=1.4)
        self.wait(1.2)

        # 收合
        self.play(FadeOut(f1), FadeOut(f2))
        f3.generate_target()
        f3.target.next_to(self.base_label, DOWN, buff=0.3).align_to(self.base_label, LEFT)
        self.play(MoveToTarget(f3))
        self.height_label = f3
        self.perp_assets = VGroup(perp_line, ra_square, height_lbl)

    # ------------------------------------------------------------------
    # Section 8: 面積收尾
    # ------------------------------------------------------------------
    def section_8_area_finale(self):
        plane = self.plane

        line1 = VGroup(
            Text("面積", font=CJK).scale(0.45),
            MathTex("=").scale(0.62),
            Text("底", font=CJK, color=COLOR_BASE).scale(0.45),
            MathTex(r"\times").scale(0.62),
            Text("高", font=CJK, color=COLOR_HEIGHT).scale(0.45),
        ).arrange(RIGHT, buff=0.08)
        line2 = MathTex(r"=", r"6\sqrt{13}", r"\times",
                        r"\dfrac{34}{\sqrt{13}}").scale(0.72)
        line2[1].set_color(COLOR_BASE)
        line2[3].set_color(COLOR_HEIGHT)
        line3 = MathTex(r"=6\times 34").scale(0.78)
        line4 = MathTex(r"=204").scale(1.05).set_color(COLOR_GOLD)

        grp = VGroup(line1, line2, line3).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18)
        grp.next_to(self.height_label, DOWN, buff=0.35).align_to(self.height_label, LEFT)
        line4.next_to(line3, DOWN, buff=0.22).align_to(line3, LEFT)

        self.play(Write(line1))
        self.wait(0.4)
        self.play(Write(line2))
        self.wait(0.4)

        # 強調 √13 約掉
        circle1 = SurroundingRectangle(line2[1], color=RED,
                                       buff=0.05, stroke_width=2.5)
        circle2 = SurroundingRectangle(line2[3], color=RED,
                                       buff=0.05, stroke_width=2.5)
        self.play(Create(circle1), Create(circle2))
        self.wait(1.2)
        self.play(FadeOut(circle1), FadeOut(circle2))

        self.play(Write(line3))
        self.wait(0.4)
        self.play(Write(line4))
        self.wait(0.8)

        # 把答案 204 放大、金框
        line4.generate_target()
        line4.target.scale(1.5).set_color(COLOR_GOLD)
        line4.target.next_to(line3, DOWN, buff=0.32).align_to(line3, LEFT)
        self.play(MoveToTarget(line4))
        box = SurroundingRectangle(line4, color=COLOR_GOLD,
                                   buff=0.18, stroke_width=3,
                                   corner_radius=0.05)
        self.play(Create(box))

        # 平行四邊形改金色邊框
        para_pts = [
            plane.c2p(0, 0),
            plane.c2p(18, -12),
            plane.c2p(20, -2),
            plane.c2p(2, 10),
        ]
        gold_para = Polygon(*para_pts, color=COLOR_GOLD,
                            stroke_width=5,
                            fill_color=COLOR_GOLD, fill_opacity=0.14)
        self.play(Transform(self.para, gold_para), run_time=2.0)
        self.wait(5.5)


# 執行指令：manim -pqh parallelogram_area_v2.py ParallelogramAreaV2

# The Unit Circle Symphony

A Manim animation that turns the most over-memorized fact in high-school
trigonometry into an "aha!" moment:

> `sin θ` is the **height** of a point spinning on the unit circle.
> `cos θ` is its **horizontal distance**.
> `sin²θ + cos²θ = 1` is the **Pythagorean theorem** on a hypotenuse of length 1.

The animation walks the viewer through three movements:

1. **The Stage** — a unit circle on the left, a blank "wave canvas" on the right.
2. **Sine Is Born** — a point rotates around the circle, and its vertical
   projection traces out the sine wave in real time.
3. **Cosine Joins In** — the horizontal projection traces the cosine wave,
   showing both functions as two views of the same rotation.
4. **The Pythagorean Punchline** — a right triangle inscribed in the circle
   reveals `sin²θ + cos²θ = 1`, true for every angle.

## Run it

```bash
pip install -r requirements.txt
manim -pqh unit_circle_animation.py UnitCircleSymphony
```

Quality flags:

- `-pql` low quality (fast preview)
- `-pqm` medium quality
- `-pqh` high quality (1080p)
- `-pqk` 4K

There is also a short loop-friendly cut:

```bash
manim -pqh unit_circle_animation.py CircleToSineLoop
```

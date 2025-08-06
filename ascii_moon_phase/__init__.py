#!/usr/bin/env python3
"""
ascii_moon_phase: Display the current lunar phase as ASCII art.

API:
- moon_phase(phase_date: date | None) -> float in [0.0, 1.0]
- render_moon(size=24, northern_hemisphere=True, phase_date=None,
              light_char='@', dark_char='.', empty_char=' ') -> str
- animate_phases(delay=0.05)
- animate_future(delay=0.2)
"""

from __future__ import annotations
import math
from datetime import date, datetime, timezone, timedelta

__all__ = ["moon_phase", "render_moon", "animate_phases", "animate_future"]

SYNODIC_MONTH = 29.530588853  # days
REF_JD = 2451550.1            # Julian Day number near a new moon (2000-01-06 18:14 UTC)

def _julian_day(dt_utc: datetime) -> float:
    """Convert a UTC datetime to Julian Day."""
    y, m = dt_utc.year, dt_utc.month
    d = dt_utc.day + (dt_utc.hour + (dt_utc.minute + dt_utc.second / 60) / 60) / 24
    if m <= 2:
        y -= 1
        m += 12
    A = y // 100
    B = 2 - A + A // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5

def moon_phase(phase_date: date | None = None) -> float:
    """
    Return lunar phase fraction p = [0.0, 1.0]:
      0.0 = new, 0.5 = full, 1.0 = new (again).
      0.0..0.5 waxing; 0.5..1.0 waning.

    Uses 12:00 UTC on the given date to avoid timezone boundary issues.
    """
    if phase_date is None:
        phase_date = date.today()
    dt_utc = datetime(phase_date.year, phase_date.month, phase_date.day, 12, 0, 0, tzinfo=timezone.utc)
    p = ((_julian_day(dt_utc) - REF_JD) / SYNODIC_MONTH) % 1.0
    return p

def _render_core(
    size: int,
    northern_hemisphere: bool,
    phase: float,
    light_char: str,
    dark_char: str,
    empty_char: str,
) -> str:
    if size < 2:
        raise ValueError("size must be at least 2")
    if not (0.0 <= phase <= 1.0):
        raise ValueError("phase must be in [0.0, 1.0]")
    height, width = size, size * 2

    if not light_char or not dark_char or not empty_char:
        raise ValueError("light_char, dark_char, and empty_char must be non-empty strings")
    L, Dk, E = light_char[0], dark_char[0], empty_char[0]

    theta = 2.0 * math.pi * phase            # 0=new, pi=full
    sx = -math.sin(theta) if northern_hemisphere else math.sin(theta)
    sz = math.cos(theta)

    rows: list[str] = []
    for j in range(height):
        y = 2.0 * ((j + 0.5) / height) - 1.0
        row = []
        for i in range(width):
            x = 2.0 * ((i + 0.5) / width) - 1.0
            r2 = x * x + y * y
            if r2 <= 1.0:
                z = math.sqrt(max(0.0, 1.0 - r2))
                lit = (sx * x + sz * z) < 0.0
                row.append(L if lit else Dk)
            else:
                row.append(E)
        rows.append("".join(row))
    return "\n".join(rows)

def render_moon(
    size: int = 24,
    northern_hemisphere: bool = True,
    phase_date: date | None = None,
    light_char: str = "@",
    dark_char: str = ".",
    empty_char: str = " ",
    phase: float | None = None,

) -> str:
    """Render from a calendar date (None ⇒ today)."""
    if phase is None:
        p = moon_phase(phase_date)
    else:
        p = phase
    return _render_core(size, northern_hemisphere, p, light_char, dark_char, empty_char)


def animate_phases(delay=0.05):
    import os, time
    try:
        while True:
            for i in range(200):
                p = i / 200
                print(render_moon(phase=p))
                time.sleep(delay)
                os.system('cls' if os.name == 'nt' else 'clear')
    except KeyboardInterrupt:
        pass

def animate_future(delay=0.2):
    import os, time
    try:
        dt = date.today()
        while True:
            print(render_moon(phase_date=dt))
            print(dt.strftime('%a %b %d, %Y'))
            time.sleep(delay)
            os.system('cls' if os.name == 'nt' else 'clear')
            dt += timedelta(days=1)
    except KeyboardInterrupt:
        pass

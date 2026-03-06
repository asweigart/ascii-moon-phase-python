"""
ascii_moon_phase: Display the current moon phase as ASCII art.

API:
- date_to_moon_phase(phase_date: date | None) -> float in [0.0, 1.0]
- render_moon(size=24, rotation=0.0, phase_date=None,
              light_char='@', dark_char='.', empty_char=' ',
              phase=None) -> str
- animate_phases(delay=0.05)
- animate_future(delay=0.2)
"""

from __future__ import annotations
import math
from datetime import date, datetime, timezone, timedelta

__all__ = ["date_to_moon_phase", "render_moon", "animate_phases", "animate_future"]

SYNODIC_MONTH = 29.530588853  # days
REF_JD = 2451550.1            # Julian Day number near a new moon (2000-01-06 18:14 UTC)

class AsciiMoonPhaseException(Exception):
    pass

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


def date_to_moon_phase(phase_date: date | None = None) -> float:
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


def render_moon(
    size: int = 24,
    rotation: float = 0.0,
    phase_date: date | None = None,
    light_char: str = "@",
    dark_char: str = ".",
    empty_char: str = " ",
    phase: float | None = None,
) -> str:
    """
    Render the moon as ASCII art.

    Parameters:
        size: Height in rows (width is 2*size)
        rotation: Clockwise rotation in degrees. At 0 (default), phases move
                  right to left. At 180, phases move left to right.
        phase_date: Calendar date to calculate phase from
        light_char: Character for illuminated area
        dark_char: Character for dark area
        empty_char: Character outside the disc
        phase: Override phase fraction [0.0, 1.0]; 0.0=new, 0.5=full
    """
    if not isinstance(light_char, str) or len(light_char) != 1:
        raise AsciiMoonPhaseException('light_char must be a single character str')
    if not isinstance(dark_char, str) or len(dark_char) != 1:
        raise AsciiMoonPhaseException('dark_char must be a single character str')
    if not isinstance(empty_char, str) or len(empty_char) != 1:
        raise AsciiMoonPhaseException('empty_char must be a single character str')
    if size < 2:
        raise AsciiMoonPhaseException("size must be 2 or larger")

    if phase is None:
        phase = date_to_moon_phase(phase_date)
    if not (0.0 <= phase <= 1.0):
        raise AsciiMoonPhaseException("phase must be between 0.0 and 1.0")
    height, width = size, size * 2

    theta = 2.0 * math.pi * phase  # 0=new, 2*pi=full
    sx = -math.sin(theta)
    sz = math.cos(theta)

    # Negate rotation so positive degrees rotate clockwise on screen
    rot_rad = math.radians(-rotation)
    cos_r, sin_r = math.cos(rot_rad), math.sin(rot_rad)

    rows: list[str] = []
    for j in range(height):
        y = 2.0 * ((j + 0.5) / height) - 1.0  # From -1.0 to 1.0, where j is on scale of 0 to height.
        row = []
        for i in range(width):
            x = 2.0 * ((i + 0.5) / width) - 1.0  # From -1.0 to 1.0, where i is on scale of 0 to width.
            r2 = x * x + y * y
            if r2 <= 1.0:
                # Apply inverse rotation to find the original sphere coordinates
                # This rotates our view of the moon by the specified angle
                orig_x = x * cos_r + y * sin_r
                orig_y = -x * sin_r + y * cos_r

                # This space is within the moon disk, place the light or dark character.
                z = math.sqrt(max(0.0, 1.0 - r2))
                is_light_space = (sx * orig_x + sz * z) < 0  # Use rotated x coordinate
                row.append(light_char if is_light_space else dark_char)
            else:
                # This space is beyond the moon disk, place the empty character.
                row.append(empty_char)
        rows.append("".join(row))
    return "\n".join(rows)


def animate_phases(size: int = 24,
    rotation: float = 0.0,
    light_char: str = "@",
    dark_char: str = ".",
    empty_char: str = " ",
    delay: float = 0.05):
    """Play an animation of the phases of the moon. (Uses cls/clear to clear the screen.)"""
    import os, time
    try:
        while True:
            for i in range(200):
                p = i / 200
                print(render_moon(size=size, rotation=rotation, light_char=light_char, dark_char=dark_char, empty_char=empty_char, phase=p))
                time.sleep(delay)
                os.system('cls' if os.name == 'nt' else 'clear')
    except KeyboardInterrupt:
        pass

def animate_future(size: int = 24,
    rotation: float = 0.0,
    light_char: str = "@",
    dark_char: str = ".",
    empty_char: str = " ",
    delay: float = 0.2):
    """Play an animation of the phases of the moon for each day in the future. (Uses cls/clear to clear the screen.)"""
    import os, time
    try:
        dt = date.today()
        while True:
            print(render_moon(size=size, rotation=rotation, light_char=light_char, dark_char=dark_char, empty_char=empty_char, phase_date=dt))
            print(dt.strftime('%a %b %d, %Y'))
            time.sleep(delay)
            os.system('cls' if os.name == 'nt' else 'clear')
            dt += timedelta(days=1)
    except KeyboardInterrupt:
        pass

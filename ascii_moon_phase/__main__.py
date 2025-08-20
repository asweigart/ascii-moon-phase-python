#!/usr/bin/env python3
from __future__ import annotations
import argparse
from datetime import date
from . import render_moon, date_to_moon_phase, animate_phases, animate_future


def _parse_date(s: str) -> date:
    try:
        y, m, d = s.split("-")
        return date(int(y), int(m), int(d))
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid date {s!r}; expected YYYY-MM-DD") from e


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ascii-moon",
        description="Render the lunar phase as filled ASCII art."
    )
    parser.add_argument("--size", type=int, default=24,
                        help="Height in rows (width is 2*size). Default: 24")
    parser.add_argument("--hemisphere", choices=("north", "south"), default="north",
                        help="Orientation: 'north' shows waxing on the right (default).")
    parser.add_argument("--date", type=_parse_date, default=None,
                        help="Calendar date YYYY-MM-DD (default: today).")
    parser.add_argument("--phase", type=float, default=None,
                        help="Phase fraction in [0.0, 1.0]; 0.0=new, 0.5=full, 1.0=new. Overrides --date.")
    parser.add_argument("--light-char", default="@", metavar="CHAR",
                        help="Character for illuminated area (default: '@').")
    parser.add_argument("--dark-char", default=".", metavar="CHAR",
                        help="Character for dark area (default: '.').")
    parser.add_argument("--empty-char", default=" ", metavar="CHAR",
                        help="Character outside the disc (default: space).")
    parser.add_argument("--show-phase", action="store_true",
                        help="Print the numeric phase after the art.")
    parser.add_argument("--phases", action="store_true",
                        help="Animate the full cycle of lunar phases.")
    parser.add_argument("--future", action="store_true",
                        help="Animate upcoming lunar phases.")

    args = parser.parse_args()

    # Handle special animation flags
    if args.phases:
        animate_phases(size=args.size,
                       northern_hemisphere=(args.hemisphere == "north"),
                       light_char=args.light_char,
                       dark_char=args.dark_char,
                       empty_char=args.empty_char)
        return

    if args.future:
        animate_future(size=args.size,
                       northern_hemisphere=(args.hemisphere == "north"),
                       light_char=args.light_char,
                       dark_char=args.dark_char,
                       empty_char=args.empty_char)
        return

    # Normal single moon rendering
    if args.phase is not None and not (0.0 <= args.phase <= 1.0):
        parser.error("--phase must be between 0.0 and 1.0")

    northern = (args.hemisphere == "north")

    moon_str = render_moon(
        size=args.size,
        northern_hemisphere=northern,
        phase_date=args.date,
        light_char=args.light_char,
        dark_char=args.dark_char,
        empty_char=args.empty_char,
        phase=args.phase,
    )
    p = date_to_moon_phase(args.date)

    print(moon_str)

    if args.show_phase:
        if abs(p - 0.5) < 1e-12:
            status = "full"
        elif p < 0.5:
            status = "waxing"
        else:
            status = "waning"
        print(f"\nphase={p:.6f}  ({status})")


if __name__ == "__main__":
    main()

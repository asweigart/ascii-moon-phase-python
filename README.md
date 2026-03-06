# ascii-moon-phase-python

Prints the current moon phase as ASCII art. Install with `pip install ascii-moon-phase` and run with `python3 -m ascii_moon_phase`.

    usage: ascii-moon-phase [-h] [--size SIZE] [--rotate DEGREES] [--date DATE] [--phase PHASE] [--light-char CHAR]
                      [--dark-char CHAR] [--empty-char CHAR] [--show-phase]

    Render the lunar phase as filled ASCII art.

    options:
      -h, --help            show this help message and exit
      --size SIZE           Height in rows (width is 2*size). Default: 24
      --rotate DEGREES      Clockwise rotation in degrees. At 0 (default), phases move
                            right to left. At 180, phases move left to right.
      --date DATE           Calendar date YYYY-MM-DD (default: today).
      --phase PHASE         Phase fraction in [0.0, 1.0]; 0.0=new, 0.5=full, 1.0=new. Overrides --date.
      --light-char CHAR     Character for illuminated area (default: '@').
      --dark-char CHAR      Character for dark area (default: '.').
      --empty-char CHAR     Character outside the disc (default: space).
      --show-phase          Print the numeric phase after the art.

You can also call these functions from Python:

    >>> import ascii_moon_phase as amp
    >>> print(amp.render_moon())
                     ...@@@@@@@@@@@
                .....@@@@@@@@@@@@@@@@@@@
             .......@@@@@@@@@@@@@@@@@@@@@@@
           .......@@@@@@@@@@@@@@@@@@@@@@@@@@@
         ........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        ........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
       .........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      .........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
     ..........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
     ..........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    ..........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    ..........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    ..........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    ..........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
     ..........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
     ..........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      .........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
       .........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        ........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
         ........@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
           .......@@@@@@@@@@@@@@@@@@@@@@@@@@@
             .......@@@@@@@@@@@@@@@@@@@@@@@
                .....@@@@@@@@@@@@@@@@@@@
                     ...@@@@@@@@@@@

The parameters of `render_moon()` are:

    def render_moon(
        size: int = 24,
        rotation: float = 0.0,
        phase_date: date | None = None,
        light_char: str = "@",
        dark_char: str = ".",
        empty_char: str = " ",
        phase: float | None = None,
    ) -> str:


You can also call `animate_phases()` to play a smooth animation of the moon, or call `animate_future()` to show the phase of each day progressing into the future.


The Rust version is at [https://github.com/asweigart/ascii-moon-phase-rust](https://github.com/asweigart/ascii-moon-phase-rust)

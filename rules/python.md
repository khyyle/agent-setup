# Python conventions

Type function and method signatures using syntax supported by the project. Prefer built-in generics where supported. Keep dependencies explicit. Use a named constant for a shared policy, such as a retry limit, and use the project's logger for diagnostics. A CLI may print its intended output. Guard a script's entry point when the module should also be importable.

Give a module a docstring that orients a new reader to its purpose and any assumptions that apply throughout. Document nontrivial functions, methods and classes in NumPy style. Describe units, array shapes and axis order, missing values, side effects, or expected failures when callers need them. For an approximation, state the conditions under which the result has the claimed interpretation. Self-explanatory private helpers can rely on their names and signatures.

Use plain section names with matching underlines. Write parameters as `name : type` followed by an indented description. Include the sections the caller needs. [NumPy docstring format](https://numpydoc.readthedocs.io/en/latest/format.html)

```python
"""Assign observations to the calendar day used in site reports.

An observation denotes an instant. Each site's time zone determines which
daily report receives it, including during daylight-saving transitions.
"""

from datetime import date, datetime
from zoneinfo import ZoneInfo


def reporting_day(observed_at: datetime, site_zone: ZoneInfo) -> date:
    """Return the site's calendar date at the instant of observation.

    Parameters
    ----------
    observed_at : datetime
        Observation time with a known UTC offset.
    site_zone : ZoneInfo
        Time zone in which the site's reports close at midnight.

    Raises
    ------
    ValueError
        If the observation has no UTC offset.
    """
    if observed_at.utcoffset() is None:
        raise ValueError("Observation time must include a UTC offset")
    return observed_at.astimezone(site_zone).date()
```

The signature expresses the return type. The docstring supplies the calendar convention the type cannot express. The conversion can raise a specific error to its caller. Log a failure at the boundary that handles it so one incident produces one diagnostic.

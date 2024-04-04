__all__ = [
    'DeltaSplit',
]

from ._base import *
from .aliases import *
from .consts import *
from ._types import *


_field_size_map: Dict[str, T_NUMBER] = {
    'years': DAYS_IN_MEAN_YEAR,  # Days
    'months': DAYS_IN_MEAN_MONTH,  # Days
    'weeks': 7,  # Days

    'hours': SECONDS_IN_ONE_HOUR,
    'minutes': SECONDS_IN_ONE_MINUTE,
}

_DEFAULT_DIRECTIONALS = ('in {}', '{} ago')


@dataclasses.dataclass(frozen=True)
class DeltaSplit:
    """Splits a timedelta into the time periods it approximately
    contains. Mean length of years and months are used and fractional
    days/seconds might get shaved of but this is useful to evaluate individual
    period lengths of displaying the maximum chunk of period a timedelta
    contains.

    This class includes an `is_past` property which is True if the timedelta
    contained a negative value but all the values in the split are nevertheless
    kept positive.

    It also includes a few `largest` and `second_largest` properties that
    contain the first and second period units that contain values greater than 0
    in order of increasing accuracy (i.e. from year to second).
    """

    # Names of unit fields with non-zero values in order of unit size
    field_order: Tuple[str] = dataclasses.field(default_factory=tuple, init=False)

    is_past: bool = dataclasses.field(default=False, init=False)  # Is this counting backwards in time?

    years: Optional[int] = dataclasses.field(default=None, init=False)  # Optional
    months: Optional[int] = dataclasses.field(default=None, init=False)  # Optional
    weeks: Optional[int] = dataclasses.field(default=None, init=False)  # Optional
    days: int = dataclasses.field(default=0, init=False)
    hours: int = dataclasses.field(default=0, init=False)
    minutes: int = dataclasses.field(default=0, init=False)
    seconds: int = dataclasses.field(default=0, init=False)

    time_delta: dataclasses.InitVar[TimeDelta]
    include_weeks: dataclasses.InitVar[bool] = True
    include_months: dataclasses.InitVar[bool] = True
    include_years: dataclasses.InitVar[bool] = True

    def get(self, field_name: str) -> str:
        return f'{self.get_value(field_name)} {self._render_field_name(field_name)}'

    def get_value(self, field_name: str) -> int:
        return getattr(self, field_name, 0) or 0

    def _render_field_name(self, field_name: str) -> str:
        if self.get_value(field_name) == 1:
            return field_name[:-1]  # Cut off the trailing 's'
        return field_name

    def _be_greedy(self, field_name: str, total: T_NUMBER) -> T_NUMBER:
        object.__setattr__(self, field_name, (int(total // _field_size_map[field_name])))
        return total % _field_size_map[field_name]

    def __post_init__(self, time_delta: TimeDelta, include_weeks: bool = True,
                      include_months: bool = True, include_years: bool = True):
        field_order = []
        if time_delta.total_seconds() < 0:
            object.__setattr__(self, 'is_past', True)
            # Invert deltas in the past because they track negative days but positive seconds, which gets confusing
            time_delta = datetime.timedelta(seconds=-time_delta.total_seconds())

        days = abs(time_delta.days)
        if include_years:
            days = self._be_greedy('years', days)
            if self.years:
                field_order.append('years')

        if include_months:
            days = self._be_greedy('months', days)
            if self.months:
                field_order.append('months')

        if include_weeks:
            days = self._be_greedy('weeks', days)
            if self.weeks:
                field_order.append('weeks')

        object.__setattr__(self, 'days', int(days))
        if self.days:
            field_order.append('days')

        seconds = self._be_greedy('hours', abs(time_delta.seconds))
        if self.hours:
            field_order.append('hours')

        seconds = self._be_greedy('minutes', seconds)
        if self.minutes:
            field_order.append('minutes')

        object.__setattr__(self, 'seconds', int(seconds))
        if self.seconds:
            field_order.append('seconds')

        object.__setattr__(self, 'field_order', tuple(field_order))

    @property
    def largest(self) -> str:
        """
        :return: The largest
        """
        if self.field_order:
            return f'{self.largest_value} {self._render_field_name(self.largest_field_name)}'
        return ''

    @property
    def largest_field_name(self) -> Optional[str]:
        """
        :return: The name of the largest unit field with a non-zero value or None if there is none.
        """
        if self.field_order:
            return self.field_order[0]
        else:
            return None

    @property
    def largest_value(self) -> int:
        """
        :return: The value of the largest unit field with a non-zero value or 0.
        """
        return self.get_value(self.largest_field_name) if self.largest_field_name else 0

    @property
    def second_largest(self) -> str:
        """
        :return: The largest
        """
        if len(self.field_order) > 1:
            return f'{self.second_largest_value} {self._render_field_name(self.second_largest_field_name)}'
        return ''

    @property
    def second_largest_field_name(self) -> Optional[str]:
        """
        :return: The name of the second-largest unit field with a non-zero value or None if there is none.
        """
        if len(self.field_order) > 1:
            return self.field_order[1]
        else:
            return None

    @property
    def second_largest_value(self) -> int:
        """
        :return: The value of the second-largest unit field with a non-zero value or 0.
        """
        return self.get_value(self.second_largest_field_name) if self.second_largest_field_name else 0

    def to_str(self, max_number_of_fields: int = 2, include_seconds: bool = False,
               directionals: Optional[Tuple[str, str]] = _DEFAULT_DIRECTIONALS,
               no_time_str: str = 'no time at all',
               only_sec_str: str = 'a few seconds',
               granularity_halting_threshold: Optional[int] = 1) -> str:
        """Returns a "human-readable" textual representation of this DeltaSplit, e.g.
        - "3 weeks"
        - "a few seconds"
        - "1 year and 7 months"
        - "7 years, 3 months, 1 week, 6 days, 34 minutes and 7 seconds"
        - "no time at all"

        :param max_number_of_fields: Maximum number of fields to include in the
                                     output. There can at most be 7 fields with
                                     values so any number than 6 will include
                                     all possible fields. The default is 2.
        :param include_seconds: By default, the seconds field is allways omitted
                                if there are any other larger unit fields with
                                non-zero values (even if `max_number_of_fields`
                                says it should be included) and if the only
                                non-zero value field is seconds, then the text
                                "a few seconds" is returned. If
                                `include seconds` is True, then the seconds
                                field is treated as all other fields and
                                returned if `max_number_of_fields` allows and
                                the exact number of seconds are always used.
        :param directionals: A two-tuple of strings to use as final formatters
                             (using `{}` as placeholder for the actual string)
                             for future and past values respectively. By
                             default, this is `('in {}', '{} ago')` so future
                             values format like "in 3 weeks" and past like "7
                             days and 3 hours ago". This can be fully excluded
                             by setting the `directionals` to None.
        :param no_time_str: The string to return if this DeltaSplit contains no
                            time (or less than a whole second).
        :param only_sec_str: The string to return if `include_seconds` is False
                             and the DeltaSplit only contains seconds. Default
                             is `a few seconds`.
        :param granularity_halting_threshold: An optional threshold value that,
                                              if a field value exceeds, causes
                                              the rendering to halt its granular
                                              descent. E.g. if `granularity_halting_threshold=1`
                                              and `max_number_of_fields=2` and
                                              we have the fields `days=1,
                                              hours=2, minutes=3` we'll get "1
                                              day and 2 hours" while if `days=2,
                                              hours=2, minutes=3` we'll just get
                                              "2 days" because `days` exceeds
                                              the threshold of 1 and thus halts
                                              diving into more granular fields.
                                              The default is `1` but setting
                                              this to `None` will just turn this
                                              check off entirely.
        """
        if not self.field_order:
            return no_time_str

        def _internal() -> str:
            # First of all, let's take care of this case where we only have seconds!
            if self.largest_field_name == 'seconds':
                if include_seconds:
                    return self.largest  # Include them
                else:
                    return only_sec_str  # Skip them

            # Now for a more "generic" approach
            fields = list(self.field_order[0:max_number_of_fields])
            if not include_seconds and fields[-1] == 'seconds':  # We have, but don't want seconds!
                fields = fields[0:-1]  # Remove Seconds

            as_strings = []
            for f in fields:
                as_strings.append(self.get(f))
                if granularity_halting_threshold and self.get_value(f) > granularity_halting_threshold:
                    break

            if len(as_strings) == 1:
                return as_strings[0]

            elif len(as_strings) == 2:
                return f'{as_strings[0]} and {as_strings[1]}'

            else:
                return f'{", ".join(as_strings[0:-1])} and {as_strings[-1]}'

        if directionals:
            if self.is_past:
                return directionals[1].format(_internal())
            return directionals[0].format(_internal())
        return _internal()

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f'<DeltaSplit {self.to_str(max_number_of_fields=7, directionals=("{}", "{}, is_past=True"), no_time_str="0", include_seconds=True,  granularity_halting_threshold=None)}>'

    def to_dict(self) -> Dict:
        parts = {'largest': self.largest_field_name,
                 'second_largest': self.second_largest_field_name,
                 'is_past': self.is_past,
                 'days': self.days,
                 'hours': self.hours,
                 'minutes': self.minutes,
                 'seconds': self.seconds}
        if self.years:
            parts['years'] = self.years
        if self.months:
            parts['months'] = self.months
        if self.weeks:
            parts['weeks'] = self.weeks
        return parts

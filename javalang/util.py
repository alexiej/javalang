from typing import List
from typing_extensions import LiteralString


def get_source(node, code_lines: List[LiteralString]):
    if node.position is None:
        return ""

    if node.end_position is None:
        return code_lines[node.position.line - 1]

    # Convert to zero-based index for Python lists
    start_line = node.position.line - 1
    end_line = node.end_position.line - 1
    start_column = node.position.column - 1
    end_column = node.end_position.column

    if start_line == end_line:
        # Single line selection
        return code_lines[start_line][start_column:end_column]
    else:
        # Multi-line selection
        lines = []
        # Add the first line from start_column to the end
        lines.append(code_lines[start_line][start_column:])
        # Add all middle lines fully
        lines.extend(code_lines[start_line + 1 : end_line])
        # Add the last line up to end_column
        lines.append(code_lines[end_line][:end_column])

        return "\n".join(lines)


class LookAheadIterator(object):
    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self.look_ahead = list()
        self.markers = list()
        self.default = None
        self.value = None

    def __iter__(self):
        return self

    def set_default(self, value):
        self.default = value

    def next(self):
        return self.__next__()

    def __next__(self):
        if self.look_ahead:
            self.value = self.look_ahead.pop(0)
        else:
            self.value = next(self.iterable)

        if self.markers:
            self.markers[-1].append(self.value)

        return self.value

    def look(self, i=0):
        """Look ahead of the iterable by some number of values with advancing
        past them.

        If the requested look ahead is past the end of the iterable then None is
        returned.

        """

        length = len(self.look_ahead)

        if length <= i:
            try:
                self.look_ahead.extend(
                    [next(self.iterable) for _ in range(length, i + 1)]
                )
            except StopIteration:
                return self.default

        self.value = self.look_ahead[i]
        return self.value

    def last(self):
        return self.value

    def __enter__(self):
        self.push_marker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Reset the iterator if there was an error
        if exc_type or exc_val or exc_tb:
            self.pop_marker(True)
        else:
            self.pop_marker(False)

    def push_marker(self):
        """Push a marker on to the marker stack"""
        self.markers.append(list())

    def pop_marker(self, reset):
        """Pop a marker off of the marker stack. If reset is True then the
        iterator will be returned to the state it was in before the
        corresponding call to push_marker().

        """

        marker = self.markers.pop()

        if reset:
            # Make the values available to be read again
            marker.extend(self.look_ahead)
            self.look_ahead = marker
        elif self.markers:
            # Otherwise, reassign the values to the top marker
            self.markers[-1].extend(marker)
        else:
            # If there are not more markers in the stack then discard the values
            pass


class LookAheadListIterator(object):
    def __init__(self, iterable):
        self.list = list(iterable)

        self.marker = 0
        self.saved_markers = []

        self.default = None
        self.value = None

    def __iter__(self):
        return self

    def set_default(self, value):
        self.default = value

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            self.value = self.list[self.marker]
            self.marker += 1
        except IndexError:
            raise StopIteration()

        return self.value

    def look(self, i=0):
        """Look ahead of the iterable by some number of values with advancing
        past them.

        If the requested look ahead is past the end of the iterable then None is
        returned.

        """

        try:
            self.value = self.list[self.marker + i]
        except IndexError:
            return self.default

        return self.value

    def last(self):
        return self.value

    def __enter__(self):
        self.push_marker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Reset the iterator if there was an error
        if exc_type or exc_val or exc_tb:
            self.pop_marker(True)
        else:
            self.pop_marker(False)

    def push_marker(self):
        """Push a marker on to the marker stack"""
        self.saved_markers.append(self.marker)

    def pop_marker(self, reset):
        """Pop a marker off of the marker stack. If reset is True then the
        iterator will be returned to the state it was in before the
        corresponding call to push_marker().

        """

        saved = self.saved_markers.pop()

        if reset:
            self.marker = saved
        elif self.saved_markers:
            self.saved_markers[-1] = saved

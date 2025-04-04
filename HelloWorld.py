import sys
from pathlib import Path


class Person:
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name
        self.name = f"{first_name} {last_name}"

    @property
    def first_name(self):
        """Get the first name."""
        if (self._first_name is not None) or (self._first_name != ""):
            return self._first_name
        return "No First name"

    @first_name.setter
    def first_name(self, value):
        self._first_name = value
        self.name = f"{self._first_name} {self._last_name}"

    @property
    def last_name(self):
        """Get the last name."""
        if (self._last_name is not None) or (self._last_name != ""):
            return self._last_name
        return "No Last name"

    @last_name.setter
    def last_name(self, value):
        """Set the last name."""
        self._last_name = value
        self.name = f"{self._first_name} {self._last_name}"

    def greet(self):
        print(f"Hello, {self.name}!")

    def farewell(self):
        print(f"Goodbye, {self.name}!")


if __name__ == "__main__":
    #sys.path.append(str(Path(__file__).resolve().parent.parent))
    john = Person("John", "Doe")
    print("First name: " + john.first_name)
    john.greet()
    john.farewell()
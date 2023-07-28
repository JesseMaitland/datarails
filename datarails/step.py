from typing import Callable, Optional

from datarails.databox import DataBox


class StepMeta(type):
    def __new__(cls, name, bases, attrs):
        # Create the class as normal.
        klass = super().__new__(cls, name, bases, attrs)

        # Add a list to the class that contains all the methods starting with 'step_'.
        # We don't include 'self' in these methods yet, because we don't have an instance.
        klass.step_methods = [k for k, v in attrs.items() if callable(v) and k.startswith("step_")]

        return klass


class DataRailsStep(metaclass=StepMeta):
    def __init__(
        self, dbx: DataBox, on_entry_callback: Optional[Callable] = None, on_exit_callback: Optional[Callable] = None
    ) -> None:
        self.dbx = dbx
        self.step_method_name_generator = None
        self.on_entry_callback = on_entry_callback
        self.on_exit_callback = on_exit_callback
        self.reset()

    def __str__(self) -> str:
        return self.__class__.__name__

    def reset(self) -> None:
        self.step_method_name_generator = iter(self.step_methods)

    def run_steps(self) -> DataBox:
        if self.on_entry_callback:
            self.on_entry_callback()

        while True:
            try:
                self.advance(stepper=False)
            except StopIteration:
                if self.on_exit_callback:
                    self.on_exit_callback()

                return self.dbx

    def advance(self, stepper: Optional[bool] = True):
        try:
            method_name = next(self.step_method_name_generator)
            method = getattr(self, method_name)
            method()
        except StopIteration:
            if stepper:
                print("No more steps to execute. Reset and try again.")
            else:
                raise

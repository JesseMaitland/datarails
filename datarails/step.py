from typing import Callable, Optional

from datarails.contexts import DataBox, DataRailsContext


class _StepMeta(type):
    def __new__(cls, name, bases, attrs):
        # Create the class as normal.
        klass = super().__new__(cls, name, bases, attrs)

        # Add a list to the class that contains all the methods starting with 'step_'.
        # We don't include 'self' in these methods yet, because we don't have an instance.
        klass.step_methods = [k for k, v in attrs.items() if callable(v) and k.startswith("step_")]

        return klass


class DataRailsStep(metaclass=_StepMeta):
    """
    Represents a step in a data pipeline process. This class is meant to be inherited from and not used directly.
    All methods that are declared with the prefix 'step_' on the child class will be run in order in which they are
    declared.

    Please check the examples directory of this repo for a more detailed example of how this class can be used.

    Attributes:
        dbx (DataBox): The data box object that stores and handles data for the step.
        on_entry_callback (Callable, optional): The function to call upon entering a step. Default is None.
        on_exit_callback (Callable, optional): The function to call upon exiting a step. Default is None.
        step_method_name_generator (Generator): A generator that yields names of step methods.
    """

    def __init__(
        self,
        dbx: DataBox,
        ctx: DataRailsContext,
        on_entry_callback: Optional[Callable] = None,
        on_exit_callback: Optional[Callable] = None,
    ) -> None:
        """
        Constructs all the necessary attributes for the DataRailsStep object.

        Args:
            dbx (DataBox): The data box object that stores and handles data for the step.
            on_entry_callback (Callable, optional): The function to call upon entering a step. Default is None.
            on_exit_callback (Callable, optional): The function to call upon exiting a step. Default is None.
        """
        self.dbx = dbx
        self.ctx = ctx
        self.step_method_name_generator = None
        self.on_entry_callback = on_entry_callback
        self.on_exit_callback = on_exit_callback
        self.reset()

    def __str__(self) -> str:
        """
        Returns the class name of the instance.

        Returns:
            str: The name of the class.
        """
        return self.__class__.__name__

    def reset(self) -> None:
        """
        Resets the step method name generator to its initial state. This method should be called before running the
        steps if being used as a stepper for debugging.
        """
        self.step_method_name_generator = iter(self.step_methods)

    def run_steps(self) -> DataBox:
        """
        Runs all the steps in the order in which they were passed to the class constructor.
        The order is fixed and cannot be changed.

        Returns:
            DataBox: The updated DataBox after all steps have been run.
        """
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
        """
        Advances to the next method in the pipeline. This is intended to be used as a stepper for debugging purposes.
        Please check the examples directory in this repo for a more detailed example of how this method can be used.

        Args:
            stepper (bool, optional): If set to True, prints a message when no more steps to execute. Default is True.

        Raises:
            StopIteration: If there are no more steps to execute and stepper is False.
        """
        try:
            method_name = next(self.step_method_name_generator)
            method = getattr(self, method_name)
            method()
        except StopIteration:
            if stepper:
                print("No more steps to execute. Reset and try again.")
            else:
                raise

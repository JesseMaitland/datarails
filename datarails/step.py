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
    All methods that are declared with the prefix 'step_' in the child class will be run in the order they are declared.

    Attributes:
        dbx (DataBox): The data box object that stores and handles data for the step.
        ctx (DataRailsContext): The context object that provides additional data and functionality.
        on_entry_callback (Callable, optional): The function to call upon entering a step. Default is None.
        on_exit_callback (Callable, optional): The function to call upon exiting a step. Default is None.
        step_method_name_iterator (Iterator): An iterator that yields names of step methods.
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
            ctx (DataRailsContext): The context object that provides additional data and functionality.
            on_entry_callback (Callable, optional): The function to call upon entering a step. Default is None.
            on_exit_callback (Callable, optional): The function to call upon exiting a step. Default is None.
        """
        self.dbx = dbx
        self.ctx = ctx
        self.on_entry_callback = on_entry_callback
        self.on_exit_callback = on_exit_callback
        self.step_method_name_iterator = None

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the instance, in this case, the class name.

        Returns:
            str: The name of the class.
        """
        return self.__class__.__name__

    def reset(self) -> None:
        """
        Resets the iterator that yields names of step methods, allowing the steps to be run from the beginning.
        """
        self.step_method_name_iterator = None

    def run(self) -> DataBox:
        """
        Runs all the steps in the order they were declared in the child class.
        The order is fixed and cannot be changed. Each 'step_' method is called in turn.

        on_entry_callback is called at the beginning, if provided.
        on_exit_callback is called at the end, if provided.

        Returns:
            DataBox: The updated DataBox after all steps have been run.
        """
        if self.on_entry_callback:
            self.on_entry_callback()

        for method_name in self.step_methods:
            method = getattr(self, method_name)
            method()

        if self.on_exit_callback:
            self.on_exit_callback()

        return self.dbx

    def advance(self) -> None:
        """
        Advances to the next 'step_' method in the pipeline, if available.
        This method can be used to control the execution of steps, for example in debugging scenarios.
        """

        if not self.step_method_name_iterator:
            self.step_method_name_iterator = iter(self.step_methods)

        method_name = next(self.step_method_name_iterator, None)

        if method_name:
            method = getattr(self, method_name)
            method()
        else:
            print("All steps have been executed.")

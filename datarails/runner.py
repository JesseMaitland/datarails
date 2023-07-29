from typing import List, Optional, Type

from datarails.contexts import DataBox, DataRailsContext
from datarails.step import DataRailsStep


class DataRailsStepRunner:
    """
    This class orchestrates the execution of a sequence of DataRailsSteps. It primarily uses
    DataBox as input, advancing through the steps and managing the DataBox state.

    Attributes:
        steps (List[Type[DataRailsStep]]): The ordered list of step classes to be executed.
        dbx (DataBox): The DataBox object for data management.
        ctx (DataRailsContext): The DataRailsContext object for context management.
    """

    def __init__(
        self, steps: List[Type[DataRailsStep]], dbx: Optional[DataBox] = None, ctx: Optional[DataRailsContext] = None
    ) -> None:
        """
        Initializes the StepRunner object with a list of DataRailsStep classes.

        Args:
            steps (List[Type[DataRailsStep]]): The list of step classes to be executed.
            dbx (DataBox, optional): The DataBox object. If not provided, a new one is created.
            ctx (DataRailsContext, optional): The DataRailsContext object. If not provided, a new one is created.
        """
        self.steps = steps
        self.dbx = dbx or DataBox()
        self.ctx = ctx or DataRailsContext()
        self._i = 0

    def reset(self):
        """
        Resets the steps_iterator to its initial state, enabling the step sequence to be run again from the start.
        """
        self._i = 0

    def _i_in_bounds(self) -> bool:
        """
        Checks if the current index is within the bounds of the steps list.

        Returns:
            bool: True if the index is in bounds, False otherwise.
        """
        return 0 <= self._i < len(self.steps)

    def get_current_step(self):
        """
        Retrieves the current step instance based on the index.

        Returns:
            DataRailsStep: The current step instance.
        """
        return self.steps[self._i](self.dbx, self.ctx)

    def print_current_step(self) -> None:
        """
        Prints the details of the current step to standard output.
        """
        step_instance = self.get_current_step()
        print(f"The Current Step : {self._i} : {step_instance}")

    def advance(self) -> None:
        """
        Executes the current step in the steps list and advances the index to the next one.
        Prints a message if there are no more steps to execute.
        """
        if self._i_in_bounds():
            current_step_instance = self.get_current_step()
            self.dbx = current_step_instance.run()
            print(f"Running step: {self._i} : {current_step_instance}")
            self._i += 1
        else:
            print("All Steps Completed.")

    def run(self) -> None:
        """
        Executes all steps in the steps list. If all steps have been completed, it stops the execution.
        """
        while self._i_in_bounds():
            self.advance()

from typing import List, Optional

from datarails.contexts import DataBox, DataRailsContext


class StepRunner:
    """
    Class to facilitate sequential execution of steps, primarily with DataBox as input.

    Attributes:
        steps (list): A list of steps to be executed.
        steps_iterator (iterator): An iterator object to iterate over steps.
        dbx (DataBox): A DataBox object for data management.
    """

    def __init__(self, steps: List, dbx: Optional[DataBox] = None, ctx: Optional[DataRailsContext] = None) -> None:
        """
        Constructs all the necessary attributes for the StepRunner object.

        Args:
            steps (list): A list of steps to be executed.
        """
        self.steps = steps
        self.steps_iterator = iter(self.steps)
        self.dbx = dbx or DataBox()
        self.ctx = ctx or DataRailsContext()

    def reset(self):
        """
        Resets the steps_iterator to its initial state.
        """
        self.steps_iterator = iter(self.steps)

    def advance(self, stepper: Optional[bool] = True) -> None:
        """
        Executes the next step in the steps_iterator. If stepper is set to True (default),
        it prints a message when no more steps are left to execute, otherwise it raises StopIteration.

        Args:
            stepper (Optional[bool], optional): If set to True, prints a message when no more steps to
            execute, otherwise raises StopIteration. Defaults to True.

        Raises:
            StopIteration: If stepper is False and no more steps are left to execute.
        """
        try:
            step = next(self.steps_iterator)
            step_instance = step(self.dbx, self.ctx)
            self.dbx = step_instance.run_steps()
        except StopIteration:
            if stepper:
                print("No more steps to execute. Reset and try again.")
            else:
                raise

    def run(self) -> None:
        """
        Runs all the steps in the steps_iterator until no more steps are left to execute.
        It prints a message and breaks the loop when no more steps are left to execute.
        """
        while True:
            try:
                self.advance(stepper=False)
            except StopIteration:
                print("No more steps to execute. Reset and try again.")
                break

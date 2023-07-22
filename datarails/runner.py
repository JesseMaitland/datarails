from typing import Optional

from datarails.databox import DataBox


class StepRunner:
    def __init__(self, steps: list) -> None:
        self.steps = steps
        self.steps_iterator = iter(self.steps)
        self.dbx = DataBox()

    def reset(self):
        self.steps_iterator = iter(self.steps)

    def advance(self, stepper: Optional[bool] = True) -> None:
        try:
            step = next(self.steps_iterator)
            step_instance = step(self.dbx)
            self.dbx = step_instance.run_steps()
        except StopIteration:
            if stepper:
                print("No more steps to execute. Reset and try again.")
            else:
                raise

    def run(self) -> None:
        while True:
            try:
                self.advance(stepper=False)
            except StopIteration:
                print("No more steps to execute. Reset and try again.")
                break

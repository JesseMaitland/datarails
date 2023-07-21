




class _StepMeta(type):
    def __new__(cls, name, bases, attrs):
        # Create the class as normal.
        klass = super().__new__(cls, name, bases, attrs)

        # Add a list to the class that contains all the methods starting with 'step_'.
        # We don't include 'self' in these methods yet, because we don't have an instance.
        klass.step_methods = [k for k, v in attrs.items() if callable(v) and k.startswith('step_')]

        return klass


# Example usage:
class Step(metaclass=_StepMeta):

    def __init__(self, dbx: DataBox) -> None:
        self.dbx = dbx
        self.step_method_name_generator = None

        self.reset()

    def reset(self):
        self.step_method_name_generator = (n for n in self.step_methods)

    def run_steps(self) -> DataBox:
        while True:
            try:
                self.advance()
            except StopIteration:
                return self.dbx

    def advance(self, stepper=False):
        try:
            method_name = next(self.step_method_name_generator)
            method = getattr(self, method_name)
            method()
        except StopIteration:
            if stepper:
                print('No more steps to execute. Reset and try again.')
            else:
                raise

    class StepRunner:

        def __init__(self, steps: list) -> None:
            self.steps = steps
            self.step_index = 0

        def run(self):
            dbx = DataBox()
            for step in self.steps:
                step_instance = step(dbx)
                dbx = step_instance.run_steps()

This is a description of the `StepRunner` class. It is intended to be used as a container and runner for all ETL DataRailsStep child classes.
Steps are run in the order they are added to the runner. The constructor take a list of step class definitions. 
A DataBox will be created automatically in the constructor and passed to each step as the execution progresses.

To use this class
```python
from datarails.runner import StepRunner
```

::: datarails.runner.StepRunner

This is a description of the `DataRailsSteps` class. It is intended to be used as a base class for all steps in a DataRails ETL workflow. 

When a child class is created, all methods that are declared with the prefix `step_` will be executed in the order that they are declared. 
It is intended that each step will perform a single task, such as loading a file, or transforming data. The smaller the piece of work the better.

Each step has an attribute called `dbx` which is an instance of a ``DataBox``. This is a container for all the data that is being processed and will
be automatically passed to each step as the execution progresses.

To use this class
```python
from datarails.step import DataRailsStep
```

::: datarails.step.DataRailsStep

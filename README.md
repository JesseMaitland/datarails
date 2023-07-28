# datarails -- A Simple Framework for Dataframe ETL
####  -- VERSION 0.2.3 --

Datarails is a simple framework for organizing your in memory Dataframe based ETL jobs. It doesn't matter of you are using `pandas`, `spark`, `glue` or anything else
this library serves as a simple way to structure your ETL jobs so that others don't come along and have to debug your 300 line script by copy / pasting sections of it into
a jupyter notebook.

Steps are defined as classes and then passed to a step runner. All methods in the class that start with `step_` will be run in the order they are defined.
Each step has access to a `DataBox` object that can be used to store dataframes and access them by name in downstream steps.

In addition to the `DataBox` object, each step has access to a `DataRailsContext` object that can be used to store and access variables that are not dataframes.


## Basic Usage

```python
import pandas as pd
from datarails.step import DataRailsStep
from datarails.runner import StepRunner


class LoadDataFromCSV(DataRailsStep):
    
    def step_load_csv(self) -> None:
        print('loading data from csv')
        df = pd.read_csv('data.csv')
        self.dbx.put_df('data', df) # dbx now has an attribute called data that is a dataframe


class TransformData(DataRailsStep):
    
    def step_add_new_column(self) -> None:
        print('adding new column')
        self.dbx.data['new_column'] = self.dbx.data['old_column'] * 2
    
    def step_drop_all_null_rows(self) -> None:
        print('dropping null rows')
        self.dbx.data = self.dbx.data.dropna()

    def rename_columns(self) -> None:
        print('renaming columns')
        self.dbx.data = self.dbx.data.rename(columns={'new_column': 'blue_column'})

        
class SaveData(DataRailsStep):
        
    def step_save_data(self) -> None:
        print('saving data')
        self.dbx.data.to_csv('new_data.csv')


steps = [
    LoadDataFromCSV,
    TransformData,
    SaveData
]        

runner = StepRunner(steps=steps)
runner.run()

```

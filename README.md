[![Release python package](https://github.com/JesseMaitland/datarails/actions/workflows/release.yml/badge.svg)](https://github.com/JesseMaitland/datarails/actions/workflows/release.yml)
# datarails -- A Simple Framework for Dataframe ETL
####  -- VERSION 0.3.1 --


## Official Documentation
The official documentation is hosted on github pages at [jesse.maitland.github.io](https://jessemaitland.github.io/datarails/)

## Example Project
There is an example repo containing some simple ETL jobs, notebooks and commands for building documentation at [jessemaitland/datarails-example](https://github.com/JesseMaitland/datarails_examples)

Datarails is a simple framework for organizing your in memory Dataframe based ETL jobs. It doesn't matter of you are using `pandas`, `spark`, `glue` or anything else
this library serves as a simple way to structure your ETL jobs so that others don't come along and have to debug your 300 line script by copy / pasting sections of it into
a jupyter notebook.

## Basic Usage

Steps are defined as classes and then passed to a step runner. All methods in the class that start with `step_` will be run in the order they are defined.
Each step has access to a `DataBox` object that can be used to store dataframes and access them by name in downstream steps.

In addition to the `DataBox` object, each step has access to a `DataRailsContext` object that can be used to store and access variables that are not dataframes.

```python
import pandas as pd
from datarails.step import DataRailsStep
from datarails.runner import DataRailsStepRunner


class LoadDataFromCSV(DataRailsStep):

    def step_load_csv(self) -> None:
        print('loading data from csv')
        df = pd.read_csv('data.csv')
        self.dbx.put_df('data', df)  # dbx now has an attribute called data that is a dataframe


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


# gather your steps in a list of class definitions. The class instances will be created by the step runner
# while the jobs is being executed.
steps = [
    LoadDataFromCSV,
    TransformData,
    SaveData
]

# pass your steps to the step runner
runner = DataRailsStepRunner(steps=steps)

# Run the job. The steps will be run in the order they are defined in the list. Each method declared in a step will be
# executed in the order they are defined in the class.

if __name__ == '__main__':
    runner.run()

```

## Why Use DataRails?

`datarails` is intended to solve a few simple problems that I have encountered while working with small to medium sized etl scripts in python. It is a very
simple framework for ETL job execution and nothing more. It is not a replacement for `airflow`, `luigi`, `dagster` or any other workflow management tool, but rather
can serve as the "entry point" for your workflow management tool to execute your ETL job.

### 1. Break your ETL Job into Smaller Steps
Quite often what happens with "small" or "medium" sized etl jobs is that they are thrown together as a single script that does everything.
This works ok until the first time your script throws an error. As during the ETL process, your error is likely due to a problem with the data,
and the single script approach makes it difficult to debug.

### 2. Step Through Your ETL Job
In the event you do encounter a problem with your ETL job, with `datarails` you can simply import your runner into a python shell or a jupyter notebook
like this:

```python
from my_etl_job import runner
runner.advance() # run the next step and stop execution
```

This allows you to step through your job and inspect the data at each step. This is especially useful when you are working with a format such a json or csv as
your source data that does not have a schema.


### 3. You Probably Don't Have Big Data
In all likelihood you have some external process fetching data and dumping it into S3 (or some other cloud storage) on a daily bases. The files entering your landing zone 
are in the order of 20MB to 100MB and are stored in some horrible format like `json`, or `json lines` or even `csv`. You need to transform this data into a format that is more useful and 
do a bit of clean up so that the data is available for other teams in your datalake, or data warehouse. You probably have 10s or even 100s of jobs that are similar to this. `datarails` is
a perfect library for these types of jobs.


### 4. Documentation
How often you you get a request from someone non-technical in the company who asks a question about an ETL job that was written 6 months ago? You get a question like,
"Hey, I noticed that the data in the `blue_column` is different than the data in the `red_column`. Can you tell me why that is?" You of course have no idea why that is, and you have to go
back to the code to figure it out. 

`datarails` forces you to break up your ETL job into smaller steps or methods. Since python provides many tools for building documentation from docstrings, you can easily
incorporate documentation using standard python docstrings, which can be published in your CI job. The documentation can then be available to business users, or other technical users
which will save you time from having to answer questions about your ETL jobs.

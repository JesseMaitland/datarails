[![Release python package](https://github.com/JesseMaitland/datarails/actions/workflows/release.yml/badge.svg)](https://github.com/JesseMaitland/datarails/actions/workflows/release.yml)

# datarails -- A Simple, Lightweight Framework for Dataframe ETL
####  -- VERSION 0.3.2 --

Datarails is a simple framework for organizing your in memory Dataframe based ETL jobs. It doesn't matter of you are using `pandas`, `spark`, `glue` or anything else
this library serves as a simple way to structure your ETL jobs. It is not a replacement for `airflow`, `luigi`, `dagster` or any other workflow management tool, but rather
can serve as the "entry point" for your workflow management tool to execute your ETL job.

## Official Documentation
The official documentation is hosted on github pages at [jesse.maitland.github.io](https://jessemaitland.github.io/datarails/)

## Installation
Datarails is available on PyPI and can be installed with pip. It has no dependencies and is written in pure python.
```bash
pip install datarails
```

## Features

Datarails consists of 4 main classes:

**DataBox:** A dynamic data store for DataFrame objects. It can handle any DataFrame type, and offers methods for adding, retrieving, and removing data. It's a bit like a dictionary for DataFrames.

**DataRailsContext:** A companion to DataBox, this class is designed for storing and retrieving additional data that you may need alongside your DataFrame objects. It allows you to associate metadata, configuration details, and other supplementary information with your data.

**DataRailsStepRunner:** This class is responsible for running a sequence of DataRailsStep objects. It takes a DataBox as input and manages the execution of each step, tracking the state of the DataBox as it goes.

**DataRailsStep:** A base class for defining steps in your data pipeline. By inheriting from this class, you can create custom steps that fit your specific needs.

## Simple Example

ETL steps are defined as classes and then passed to a step runner. All methods in the class that start with `step_` will be run in the order they are defined.
Each step has access to a `DataBox` object that can be used to store dataframes and access them by name in downstream steps.

In addition to the `DataBox` object, each step has access to a `DataRailsContext` object that can be used to store and access variables that are not dataframes.

In this below example we are doing some simple procssing using pandas, however any other dataframe library could be used.

```python
import pandas as pd
from datarails.step import DataRailsStep
from datarails.runner import DataRailsStepRunner


class LoadDataFromCSV(DataRailsStep):
    """Loads data from a CSV file into a DataBox."""
    
    def step_load_csv(self) -> None:
        """Loads a DataFrame from a CSV file and stores it in the DataBox under 'data'."""
        print('loading data from csv')
        df = pd.read_csv('data.csv')
        self.dbx.put_df('data', df)


class TransformData(DataRailsStep):
    """Applies transformation operations to a DataFrame stored in a DataBox."""
    
    def step_add_new_column(self) -> None:
        """Adds a new column to the DataFrame which is double the values of the 'old_column'."""
        print('adding new column')
        self.dbx.data['new_column'] = self.dbx.data['old_column'] * 2

    def step_drop_all_null_rows(self) -> None:
        """Removes all rows from the DataFrame that contain any null values."""
        print('dropping null rows')
        self.dbx.data = self.dbx.data.dropna()

    def step_rename_columns(self) -> None:
        """Renames the 'new_column' in the DataFrame to 'blue_column'."""
        print('renaming columns')
        self.dbx.data = self.dbx.data.rename(columns={'new_column': 'blue_column'})


class SaveData(DataRailsStep):
    """Saves the DataFrame from a DataBox to a CSV file."""
    
    def step_save_data(self) -> None:
        """Saves the DataFrame to a CSV file named 'new_data.csv'."""
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

## Example Project
There is an example repo containing some simple ETL jobs, notebooks and commands for building documentation at [jessemaitland/datarails-example](https://github.com/JesseMaitland/datarails_examples)

## Why Use DataRails?

`datarails` addresses several critical issues commonly encountered during the execution of small to medium scale ETL (Extract, Transform, Load) scripts in Python. While simple, it is an effective framework that streamlines ETL tasks, and serves as a robust "entry point" for other workflow management tools, like `airflow`, `luigi`, or `dagster`, to execute your ETL job.

### 1. Segmenting Your ETL Job into Manageable Steps
ETL tasks of small or medium complexity can often transform into a single, monolithic script. While functional, this approach could be challenging to debug when data-related errors occur. `datarails` allows the segmentation of ETL tasks into distinct, manageable steps, enhancing clarity and error-handling.

### 2. Navigating Your ETL Job Step by Step
With `datarails`, it's possible to debug ETL jobs step-by-step. You can import your runner into a Python shell or a Jupyter notebook, advancing through each step individually. This method is particularly beneficial when working with schema-less source data formats like JSON or CSV, enabling precise data inspection at every stage.

```python
from my_etl_job import runner
runner.advance() # run the next step and stop execution

step_to_debug = runner.get_current_step() # get the current step

step_to_debug.dbx.data # inspect the data in the DataBox
step_to_debug.dbx.context # inspect the context in the DataRailsContext

step_to_debug.advance() # run the next step and stop execution. Repeat as needed.
```

### 3. A Practical Solution for Typical Data Sizes
Most often, external processes fetch data and upload it into S3 (or similar cloud storage) on a daily basis. The data, typically in the size range of 20MB to 100MB and in diverse formats like `json`, `json lines`, or `csv`, needs transformation and cleaning before it can be utilized by other teams in your data lake or warehouse. `datarails` is an ideal library for managing and transforming these types of data.

### 4. Simplified Documentation
`datarails` encourages the practice of dividing ETL jobs into smaller methods, thus facilitating the process of documentation. This feature works well with Python's native tools for generating documentation from docstrings, and such documentation can be published through your CI job. This way, it is readily available for business users or other technical users, significantly reducing the time you spend responding to queries about your ETL jobs.

### 5. Facilitating Standardization Across the Organization

In many organizations, ETL processes and data pipelines can be constructed in vastly different ways depending on the preferences and experience of individual developers. This can lead to considerable confusion, difficulty in maintaining code, and barriers to effective collaboration. `datarails` can help overcome these challenges by offering a standard framework for developing ETL jobs.

The use of `datarails` ensures that all ETL scripts follow the same structure and approach, creating a uniform coding style across the organization. This not only makes the codebase easier to understand and maintain, but also encourages effective collaboration between team members. Moreover, the standardized structure can expedite the onboarding process for new team members, as they only need to familiarize themselves with one framework, rather than a multitude of disparate coding styles.

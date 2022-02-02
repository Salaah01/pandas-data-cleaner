# Pandas Data Cleaner
This package is a data cleaning tool for Pandas DataFrames and other objects with a similar structure.

The tool is designed to help clean data by providing a function onto which you can apply various cleaning methods.

The main cleaning function can be found in `pandas_data_cleaner.base.clean_data`.

The app also provides an abstract base class `pandas_data_cleaner.base.CleaningStrategy` which can be used to implement custom cleaning strategies.

## Installation
To install the application, run the following command:
```bash
pip install pandas-data-cleaner
```

## Cleaning Data
In order to clean data, you need:
* Pandas DataFrame
* List of strategies to apply
* Any additional arguments that you may need to pass to the cleaning function.

Let's suppose we have the following DataFrame:

```python
import pandas as pd

dataframe = pd.DataFrame({
    "id": [1, 2, 1],
    "structure_value": ["a", "a", "a"],
    "status": ["ENABLED", "ENABLED", "DISABLED"],
})
```
As a table, this would look like this:

| id  | structure_value | status   |
| --- | --------------- | -------- |
| 1   | a               | ENABLED  |
| 2   | a               | ENABLED  |
| 1   | a               | DISABLED |

In this data frame, we can see that there are two rows with the same id but different values for status.

As part of our cleaning exercise, we want to keep the latest row of data as this is the most up-to-date.

Let's try to apply the RemoveDuplicates cleaning strategy to the data frame:

```python
import pandas as pd
from pandas_data_cleaner.base import clean_data
from pandas_data_cleaner.strategies import RemoveDuplicates

dataframe = pd.DataFrame({
    "id": [1, 2, 1],
    "structure_value": ["a", "a", "a"],
    "status": ["ENABLED", "ENABLED", "DISABLED"],
})

dataframe = clean_data(dataframe, [RemoveDuplicates])
```

Running this will result in the following error:
```bash
pandas_data_cleaner.exceptions.MissingOptionsError: Missing kwargs:
remove_duplicates_subset_fields
remove_duplicates_keep
```

This lets us that we need to provide additional arguments when calling the cleaning function, these are:
* `remove_duplicates_subset_fields`
* `remove_dupplicates_keep`

To find out more information about the additional arguments required, you can run:
```python
RemoveDuplicates.info()
```
This will return some information on how the strategy works as well as additional information on the arguments that are required.

For the `RemoveDuplicates` cleaning strategy, `remove_duplicates_subset_fields` is the fields we should perform the duplicate removal on and `remove_duplicates_keep` indicates given some duplicates are, which row should we keep.

If we now tweak our earlier code:


```python
import pandas as pd
from pandas_data_cleaner.base import clean_data
from pandas_data_cleaner.strategies import RemoveDuplicates

dataframe = pd.DataFrame({
    "id": [1, 2, 1],
    "structure_value": ["a", "a", "a"],
    "status": ["ENABLED", "ENABLED", "DISABLED"],
})

dataframe = clean_data(
    dataframe,
    [RemoveDuplicates],
    remove_duplicates_subset_fields=["id"],
    remove_duplicates_keep="last"
)
```

We will now get the following data frame:

```python
pd.DataFrame({
    "id": [2, 1],
    "structure_value": ["a", "a"],
    "status": ["ENABLED", "DISABLED"],
})
```

As a table:

| id  | structure_value | status   |
| --- | --------------- | -------- |
| 2   | a               | ENABLED  |
| 1   | a               | DISABLED |

As we had set `remove_duplicates_subset_fields=["id"]`, it found that there were two rows with the same ID. As we set `remove_duplicates_keep="last"`, it kept the last row only.

In our example, we used only one cleaning strategy, but we are free to use as many as we like, we simply need to add all the strategies to the list of cleaning strategies to apply.

## Creating Custom Cleaning Strategies
Let's suppose we intend to create a new cleaning strategy that removes certain columns.

We would create a new class inheriting from `base.CleaningStrategy`:

```python
from pandas_data_cleaner.base import CleaningStrategy


class RemoveColumns(CleaningStrategy):
    pass
```

When using this strategy, we need to know which column names to remove. We will therefore decide that, when using this class in the `clean_data` method, we need to provide a `remove_columns` argument.

To do this, we simply create a class attribute called `required_options` and set it to `["remove_columns"]`.

We also will add some documentation to allow the end-user to receive some useful information when they run `RemoveColumns.info()`.

Our new strategy will now look like this:

```python
class RemoveColumns(CleaningStrategy):
    """Removes columns from a dataframe.

    Required options:
        `remove_columns` - (_t.List[str]) A list of columns to remove.
    """

    required_options = ["remove_columns"]
```

Now, we need to create our cleaning method.
Once the cleaning method has been added, the class will look like the following:

```python
class RemoveColumns(CleaningStrategy):
    """Removes columns from a dataframe.

    Required options:
        `remove_columns` - (List[str]) A list of columns to remove.
    """

    required_options = ["remove_columns"]

    def clean(self):
        """Executes the cleaning task."""
        self.dataframe.drop(
            self.remove_columns, axis=1, inplace=True
        )
```

Let's discuss how this cleaning method works.
Firstly, whenever a user would use this strategy may run the following:

```python
clean_data(dataframe, [RemoveColumns], remove_columns=["id", "status"])
```

`clean_data` will instantiate each cleaning strategy, in this case, just `RemoveColumns` providing the data frame as a required initial parameter as well as passing any keyword arguments to the function.

Each strategy would then set both the `dataframe` and each keyword argument to the self object.

This means that within the clean method, we would have access:
* `self.dataframe`
* `self.remove_columns`.

If the command the user ran was instead:
```python
clean_data(dataframe, [RemoveColumns], remove_columns=["id", "status"], foo="bar")
```

Then within the clean method would have access:
* `self.dataframe`
* `self.remove_columns`
* `self.foo`

By adding `remove_columns` to the `required_options` list, once this class is instantiated, we will be able to access `self.remove_columns`.

Now that we have built our cleaning strategy let's run it:

```python
dataframe = pd.DataFrame({
    "id": [1, 2, 3],
    "col1": [1, 2, 3],
    "col2": [1, 2, 3],
    "col3": [1, 2, 3],
})

dataframe = clean_data(
    dataframe,
    [RemoveColumns],
    remove_columns=["col1", "col2"]
)

print(dataframe)

>>> pd.DataFrame({
    "id": [1, 2, 3],
    "col3": [1, 2, 3],
})
```
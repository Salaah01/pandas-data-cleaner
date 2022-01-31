# Data Cleaners

This app contains a number of cleaning strategies for cleaning data. These can be found in `methods.py`. The app also contains a function `base.clean_data` which can be used to clean data applying multiple cleaning strategies.

The app also provides an abstract class `base.CleaningStrategy` which can be used to implement custom cleaning strategies.

## Cleaning Data
To clean data using `base.clean_data` you will need:
* A pandas data frame as the source data.
* A Django model class as a reference (the app will not load data, it needs this information so that it understands how the data should be structured).
* A list of cleaning strategies to apply.

Let's suppose we have the following model class:
```python
from django.db import models

class Campaign(models.Model):
    structure_value = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
```

Let's suppose we have the following pandas data frame:
```python
import pandas as pd

dataframe = pd.DataFrame({
    "id": [1, 2, 1],
    "structure_value": ["a", "a", "a"],
    "status": ["ENABLED", "ENABLED", "DISABLED"],
})
```

As a table, this would look like:
| id  | structure_value | status   |
| --- | --------------- | -------- |
| 1   | a               | ENABLED  |
| 2   | a               | ENABLED  |
| 1   | a               | DISABLED |

In this data frame, we can see that there are two rows with the same `id` but different values for `status`.

As part of our cleaning exercise, we want to keep the latest row of data as this is the most up-to-date.

Let's try to apply the `RemoveDuplicates` cleaning strategy to the data frame:
```python
from data_cleaners.base import clean_data
from data_cleaners.methods import RemoveDuplicates

dataframe = pd.DataFrame({
    "id": [1, 2, 1],
    "structure_value": ["a", "a", "a"],
    "status": ["ENABLED", "ENABLED", "DISABLED"],
})

dataframe = clean_data(dataframe, Campaign, [RemoveDuplicates])
```

This raises a `NotImplementedError` as the cleaning strategies require additional information in our models.

```
NotImplementedError: The model does not have a DataCleaner class.
```

The error suggests that we need to make the following change to our model:

```python
class Campaign(models.Model):
    structure_value = models.CharField(max_length=255)
    status = models.CharField(max_length=100)

    class DataCleaner:
        pass
```
This does not seem to do a lot. However, using cleaning strategies requires this. The `DataCleaner` class is where each strategy looks for some settings relating to that specific strategy.

Running this again will return another error:

```
NotImplementedError: Model missing `DataCleaner.remove_duplicates_subset_fields`  attribute. This attribute is required for to know which fields to remove duplicates from. `remove_duplicates_subset_fields =['field_1', 'field_2']`
```

This now gives us more information about what attributes we need to add and what it is needed for. We can now update our model to the following:

```python
class Campaign(models.Model):
    structure_value = models.CharField(max_length=255)
    status = models.CharField(max_length=100)

    class DataCleaner:
        remove_duplicates_subset_fields = ["id"]
```


This change will ensure that when our cleaning strategy is being applied, it will only remove duplicates based on the `id` field. Without this change, the cleaning strategy would not know which fields to use to remove duplicates.

Please note that most cleaning strategies require additional information in our models. Each strategy has error handling is place to let you know when the `DataCleaner` class is missing an attribute that it needs.

Now when we run the cleaning function, we will get the following data frame:
```python
dataframe = pd.DataFrame({
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

In our example we used only one cleaning strategy, but we are free to use as many as we like, we simply need to add all the strategies to the list of cleaning strategies to apply.

## Creating Custom Cleaning Strategies
Let's suppose we want to create a cleaning strategy that removes all rows with a `status` of `DISABLED` on data that we intend to load into the `Campaign` model.

If the strategy is generic and could possibly be used by other apps, it should be placed in `data_cleaners/methods.py`. Otherwise, it should be placed in a local app directory. This is to prevent `methods.py` for becoming cluttered.

For our example, we will create a new file `campaigns/cleaning_methods.py` with the following code:
```python
# We need to import the abstract base class to create new strategies.
from data_cleaners.base import CleaningStrategy


class RemoveDisabled(CleaningStrategy):  # Need to inherit from CleaningStrategy
    """Remove all rows with a status of DISABLED."""

    # The `clean` method is applied when the cleaning strategy is applied. 
    def clean(self):
        """Executes the cleaning task."""
        self.validate_model()
        self.dataframe.drop(
            self.dataframe[self.dataframe.status == 'DISABLED'].index,
            inplace=True,
        )
```

In the `clean` method, we see that the `self.validate_models()` is called. This will run some validation defined in the `CleaningStrategy` class. The method will call `self.can_use_cleaner` which returns a tuple of `(bool, str)`.

The first element of the tuple is a boolean indicating whether the cleaning strategy can be used. The second element is a message explaining why the cleaning strategy cannot be used.

If the value of the first element is `False`, `self.validate_models` will raise an error with a helpful message. We saw this previously when our model did not include the `DataCleaner` class with the `remove_duplicates_subset_fields` attribute.

If you wish to add your own validations, you can override the `can_use_cleaner` method.

Now with our new cleaning strategy, we can apply it to our data frame:
```python
dataframe = pd.DataFrame({
    "id": [1, 2, 1],
    "structure_value": ["a", "a", "a"],
    "status": ["ENABLED", "ENABLED", "DISABLED"],
})

dataframe = clean_data(dataframe, Campaign, [RemoveDisabled])
```

This will return the following dataframe:
```python
dataframe = pd.DataFrame({
    "id": [1, 1],
    "structure_value": ["a", "a"],
    "status": ["ENABLED", "ENABLED"],
})
```
As a table:
| id  | structure_value | status  |
| --- | --------------- | ------- |
| 1   | a               | Enabled |
| 1   | a               | Enabled |

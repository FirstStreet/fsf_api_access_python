# First Street Foundation API Access Documentation (Python)
The First Street Foundation API Access (Python) is a wrapper used to bulk extract flood data from the First Street Foundation API

## Installation
**NOTE**: This project requires [Python](https://www.python.org/downloads/) 3.6+ to run.
1. Install the source code manager [Git]
2. Clone the [project repository](https://github.com/FirstStreet/api-access-python) to a directory
3. Open a shell and navigate to the new project directory
    ```sh
    cd /path/to/project
    ```
4. [Optional] Create and activate a new virtual environment through cmd/terminal to keep clean environments:
    ```sh
    python -m venv /path/to/new/virtual/environment
   
    cd /path/to/new/virtual/environment
   
    .\venv\Scripts\activate
    ```
5. Run the setup script to install the project requirements
    ```sh
    python setup.py install
    ```
6. The project is now setup and can be ran. See below for details on how to extract flood data products from the API

## Intializing Client
**[Reminder] Keep your API key safe, and do not share it with others!**
```python
# Create a new First Street Foundation API Client in a Python Script. 
import firststreet
fs = firststreet.FirstStreet("api-key")
```

## Products
### Location

The Location API provides `Detail` and `Summary` data for the given FSIDs.

```python
fs.location.<method>
```

* `get_detail`(fsids `list`, location_type `string`, csv `bool`) - Returns an array of `Location Detail` product for the given IDs, and optionally creates a csv file
* `get_summary`(fsids `list`, location_type `string`, csv `bool`) - Returns an array of `Location Summary` product for the given IDs, and optionally creates a csv file

### Probability

The Probability API provides `Depth`, `Chance`, `Cumulative`, `Count` data for the given FSIDs.

```python
fs.probability.<method>
```

* `get_depth`(fsids `list`, csv `bool`) - Returns an array of `Probability Depth` product for the given IDs, and optionally creates a csv file
* `get_chance`(fsids `list`, csv `bool`) - Returns an array of `Probability Chance` product for the given IDs, and optionally creates a csv file
* `get_cumulative`(fsids `list`, csv `bool`) - Returns an array of `Probability Cumulative` product for the given IDs, and optionally creates a csv file
* `get_count`(fsids `list`, location_type `string`, csv `bool`) - Returns an array of `Probability Count` product for the given IDs, and optionally creates a csv file

### Historic

The Historic API provides `Summary` and `Event` data for the given FSIDs.

```python
fs.historic.<method>
```

* `get_event`(fsids `list`, csv `bool`) - Returns an array of `Historic Event` product for the given historic IDs, and optionally creates a csv file
* `get_summary`(fsids `list`, location_type `string`, csv `bool`) - Returns an array of `Historic Summary` product for the given IDs, and optionally creates a csv file

### Adaptation

The Adaptation API provides `Summary` and `Project` data for the given FSIDs.

```python
fs.adaptation.<method>
```

* `get_project`(fsids `list`, csv `bool`) - Returns an array of `Adaptation Project` product for the given adaptation IDs, and optionally creates a csv file
* `get_summary`(fsids `list`, location_type `string`, csv `bool`) - Returns an array of `Adaptation Summary` product for the given IDs, and optionally creates a csv file

### Fema

The Fema API provides `NFIP` data for the given FSIDs.

```python
fs.fema.<method>
```

* `get_nfip`(fsids `list`, location_type `string`, csv `bool`) - Returns an array of `Fema NFIP` product for the given IDs, and optionally creates a csv file

### Environmental

The Environmental API provides `Precipitation` data for the given FSIDs.

```python
fs.environmental.<method>
```

* `get_precipitation`(fsids `list`, csv `bool`) - Returns an array of `Environmental Precipitation` product for the given county IDs, and optionally creates a csv file

## CSV File Output:
Any product above can be additionally exported to a CSV file for further usage if the csv boolean is set during the product call. The extracted can be found in the `data_csv` directory of the project folder (if at least one CSV has been extracted).


### CSV File Name:
The file name will be in the format of `YYYY_MM_DD_HH_mm_SS_product_subtype_lookup.csv`. 

Ex:
- `2020_06_10_17_29_49_adaptation_detail.csv`
- `2020_06_10_17_33_56_adaptation_summary_property.csv`

### CSV File Content
The contents of the CSV file will follow similar formats as the `First Street Foundation API - V1.0 Overview and Dictionary`, but all lists will be expanded to a flat file. For any values that are null or not available, <NA> will be used.

Ex: 
```csv
fsid,year,returnPeriod,bin,low,mid,high
7935,2020,20,20,<NA>,2,<NA>
7935,2020,20,50,<NA>,1,<NA>
7935,2020,20,55,<NA>,2,<NA>
7935,2020,20,65,<NA>,2,<NA>
7935,2020,20,75,<NA>,2,<NA>
7935,2020,20,95,<NA>,1,<NA>
7935,2020,20,100,<NA>,1,<NA>
...
```
   
   
## Examples
**[Reminder] Keep your API key safe, and do not share it with others!**
1. Single FSID Extraction
    ```python
    # Retrieve a Location Detail Product from the API for fsid: 39035103400
    import firststreet
    fs = firststreet.FirstStreet("api-key")
    
    fsids = [39035103400]
    probability = fs.probability.get_count(fsids, "tract")
    
    print(probability[0].fsid)
    print(probability[0].count)
    ```

2. Multiple FSIDs Extraction
    ```python
    # Retrieve a Location Detail Product from the API for fsids: 1912000, 1979140
    import firststreet
    fs = firststreet.FirstStreet("api-key")
    
    fsids = [1912000, 1979140]
    details = fs.location.get_detail(fsids, "property")
    
    print(details[0].fsid)
    print(details[0].route)
    print(details[1].fsid)
    ```
   
2. Adaptation detail Extraction to CSV
    ```python
    # Retrieve an Adaptation Detail Product from the API for adaptationID: 29 and export to a CSV located in data_csv`
    import firststreet
    fs = firststreet.FirstStreet("api-key")
    
    fs.adaptation.get_detail([29], csv=True)
    ```
   
   Output File:
   ```csv
    adaptationId,name,type,scenario,conveyance,returnPeriod
    29,Riverfront Park,bioswale,fluvial,False,500
    29,Riverfront Park,bioswale,pluvial,False,500
    29,Riverfront Park,detention basin,fluvial,False,500
    29,Riverfront Park,detention basin,pluvial,False,500
    29,Riverfront Park,levee,fluvial,False,500
    29,Riverfront Park,levee,pluvial,False,500
    29,Riverfront Park,pervious pavement,fluvial,False,500
    29,Riverfront Park,pervious pavement,pluvial,False,500
    ```

[git]: <https://git-scm.com/downloads>

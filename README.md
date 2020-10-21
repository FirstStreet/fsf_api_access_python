# First Street Foundation API Access Documentation (Python 3.7+)
[![CircleCI](https://img.shields.io/circleci/build/gh/FirstStreet/fsf_api_access_python)](https://circleci.com/gh/FirstStreet/fsf_api_access_python)
![GitHub](https://img.shields.io/github/license/firststreet/fsf_api_access_python)

The First Street Foundation API Access (Python) is a wrapper used to bulk extract flood data from the First Street Foundation API

**Notice:** This API wrapper is subject to change.

<a name="toc"></a>
# Table of contents
- **[Installation](#installation)**
  * [Running the Project - Method 1: Through the Command Line](#method1)
    + [Command Line Argument Details](#commandline)
  * [Running the Project - Method 2: Through the Client](#method2)
      - [Client Initialization Details](#client-init)
      - [Arguments](#client-arguments)
      - [If you are using Jupyter Notebook](#jupyter_setup)
- **[Products](#products)**
  - [Location](#location)
  - [Probability](#probability)
  - [Historic](#historic)
  - [Adaptation](#adaptation)
  - [Fema](#fema)
  - [Environmental](#environmental)
  - [Tile](#tiles)
- **[Examples](#examples)**
- **[CSV File Output:](#csv-output)**
  - [CSV File Name:](#csv-name)
  - [CSV File Content](#csv-content)
- **[Updating the Project to the Newest Version:](#updating)**
- **[License](#license)**

<a name="installation"></a>
# [Installation](#toc)
**NOTE**: This project requires [Python](https://www.python.org/downloads/) 3.7+ to run.

1. Go to the Python page (https://www.python.org/downloads/) and download then install Python version 3. **Make sure that the checkbox is checked for Python to be added to the PATH**

    A more detailed and in-depth guide on how to install Python can be found [here](https://realpython.com/installing-python/)
    
2. [Optional] Open a new `powershell console` / `bash terminal`and create and activate a new virtual environment in the project directory:
    ```sh
    python -m venv /path/to/new/virtual/environment
   
    cd /path/to/project
   
    .\venv\Scripts\activate
    ```
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//1.4.1.png)
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//1.4.2.png)
    
3. Use pip to install the project
    ```sh
    cd /path/to/project
   
    pip install fsf-api-access-python
    ```
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//1.5.2.png)
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//1.5.1.png)
    
7. The project is now setup and can be ran through one of the two methods below. See `Products` for additional details on how to extract flood data products from the API.
    ```sh
    Example File Structure:
    
    .
    ├── venv
    ├── my_script.py

<a name="method1"></a>
## [Running the Project - Method 1: Through the Command Line](#toc)
**[Reminder] Keep your API key safe, and do not share it with others!**

[NOTE] This method will always generate a CSV. 

1.  ## **MacOS or Linux** 
    [Required] Open a `bash terminal` and set an Environmental Variable with the `variable_name` as `FSF_API_KEY` and the `variable_value` with the `API_KEY` with the command
    ```shell script
    export FSF_API_KEY=your personal API key
    ``` 
    
    ## **Windows** 
    [Required] Set an Environmental Variable with the `variable_name` as `FSF_API_KEY` and the `variable_value` with the `API_KEY`.
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//3.1.1.png)
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//3.1.2.png)
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//3.1.3.png)

2. Open/Re-open a `powershell console` / `bash terminal` and navigate to the project directory. Next, call one of the methods described below in the `Products` section through the command line. See the `Examples` section for more examples.
    ```sh
    cd /path/to/project
   
    python -m firststreet -p <product>.<product_subtype> -i <search_item> -f <file_name> -l <lookup_type>
    ```
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//3.2.1.png)
    
<a name="commandline"></a>
### [Command Line Argument Details:](#toc)

- `-p/--product PRODUCT`: [REQUIRED] The product to call from the API

    Example: ```-p location.get_detail```
    
- `[-api_key/--api_key API_KEY]`: [OPTIONAL] If step 1 is skipped or unavailable, this argument can take the `API_KEY` instead.

    Example: ```-a XXXXXXXXXXXXXXXXXXX```
    
- `[-v/--version VERSION]`: [OPTIONAL] The version of the API to call. Defaults to the current version.

    Example: ```-v v1```
    
- `[-i/--search_items SEARCH_ITEM]`: [OPTIONAL] The Search Items to search for with the product. 

    **NOTE** THE LIST MUST BE A SEPRATED WITH A SEMICOLON (;) INSTEAD OF A COMMA

    Example: ```-i 541114211;541229206```
    
- `[-l/--location LOOKUP_TYPE]`: [OPTIONAL] The lookup location type (property, neighborhood, city, zcta, tract, county, cd, state)

    Example: ```-l property```
    
- `[-connection_limit/--connection_limit CONNECTION_LIMIT]`: [OPTIONAL] The max number of concurrent connections to make to the API at the same time. This is does not affect the number of FSIDs that can be pulled. Defaults to 100 connections

    Example: ```-connection_limit 20000```
    
- `[-rate_limit/--rate_limit RATE_LIMIT]`: [OPTIONAL] The max number of requests during the rate limit period. Defaults to 20000 requests

    Example: ```-rate_limit 1```
    
- `[-rate_period/--rate_period RATE_PERIOD]`: [OPTIONAL] The period of time for the rate limit. Defaults to 1 second

    Example: ```-rate_period 20```
    
- `[-log/--log LOG]`: [OPTIONAL] To log info output to the console or not. Defaults to True

    Example: ```-l False```
    
- `[-e/--extra_param EXTRA_PARAM]`: [OPTIONAL] Adds the argument to the end of the endpoint call

    Example: ```-e extra_param```
    
- `[-year/--year YEAR]`: [OPTIONAL] The year to use for the `Probability Depth Tile` product

    Example: ```-year 2050```
    
- `[-return_period/--return_period RETURN_PERIOD]`: [OPTIONAL] The return period to use for the `Probability Depth Tile` product

    Example: ```-return_period 500```
    
- `[-event_id/--event_id EVENT_ID]`: [OPTIONAL] The event id to use for the `Historic Event Tile` product

    Example: ```-event_id 3```
    
- `[-f/--file FILE]`: [OPTIONAL] A file of Search Items (one per line) to search for with the product

    Example: ```-f sample.txt```

    Content of a sample text file. Note that the file must be in the same directory as the project:
    ```text
    541114211
    540456284
    541229206
    540563324
    541262690
    540651172
    ```
  
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//4.4.1.png)
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//4.4.2.png)

<a name="method2"></a>
## [Running the Project - Method 2: Through the Client](#toc)
**[Reminder] Keep your API key safe, and do not share it with others!**

[NOTE] This method will **NOT** generate a CSV by default. An argument must be passed to generate a CSV.

1. Create a new Python script (by using notepad or any other text editor) and initialize a First Street Foundation API Client. 
    ```python
    # Contents of my_script.py
    import firststreet
    fs = firststreet.FirstStreet("api-key")
    ```
    
    <a name="client-init"></a>
    #### [Client Initialization Details](#toc)
    
    ```python
    firststreet.FirstStreet(api_key, [connection_limit], [rate_limit], [rate_period], [version], [log])
    ```
    
    <a name="client-arguments"></a>
    #### [Arguments](#toc)
    * api_key `string`: The assigned API key to access the API.
    * connection_limit `int=100`: The max number of connections to make
    * rate_limit `int=20000`: The max number of requests during the period
    * rate_period `int=1`: The period of time for the limit
    * version `string= v1`: The version of the API to access. Defaults to the current version.
    * log `bool= True`: Setting for whether to log info or not. Defaults to True.

2. Call one of the methods described below in the `Products` section with the required arguments. See the `Examples` section for more examples.
    ```python
    fs.<product>.<product_subtype>(<search_items: list>, <lookup_type: string>, <csv: boolean>)
    ```
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//2.2.1.png)
    
    OR
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//2.2.2.png)
    
    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//2.2.3.png)
    
3. Run the python script.

    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//2.3.1.png)


<a name="jupyter_setup"></a>
### [If you are using Jupyter Notebook](#toc)
1. Add the following to the top of the file before the [client initialization](client-init) to allow the jupyter notebook and download loops to work correctly

    ```python
    # Setup For Notebook only
    import nest_asyncio
    nest_asyncio.apply()
    ```

<a name="products"></a>
# [Products](#toc)

More information on each product can be found at the [First Street Foundation API Data Dictionary](https://docs.firststreet.dev/docs)

<a name="Search Item"></a>
#### [Search Item:](#toc) 

For every product, a list or file of `search items` must be provided to the product call. 
There are 3 types of `search items` corresponding to the 3 types of lookups. 
(More information on the Lookup types can be found on the [Lookups Page on the First Street Foundation API Data Dictionary](https://docs.firststreet.dev/docs/lookups)
)

1. FSID (`int`): The simplest type of lookup is a fsid lookup. If you know the fsid of the specific location, you can navigate directly to the specific product's information using the location's fsid. Example FSID: `18`

2. Lat/Lng (`tuple of int`): Provide a tuple of latitude, longitude pairs will check to see if that point intersects within a boundary of a parcel from the database. Example lat/lng: `(40.7079652311, -74.0021455387)`

3. Address (`string`): Pass the address in your request to retrieve a reverse geocode location lookup. LocationType is required for address lookup. An address can be a city name, home address, or business address. City and State need to be included within the address query. Example Address: `New York, NY`

Example list of `search items`:

```python
lst = [362493883, (40.792505, -73.951949), "1220 5th Ave, New York, NY"]
```

Example file of `search items`:
```text
362493883
(40.792505, -73.951949)
1220 5th Ave, New York, NY
```

<a name="location"></a>
#### [Location](#toc)

The Location API provides `Detail` and `Summary` data for the given SearchItems.
(More information on the Location product can be found on the [Location Page on the First Street Foundation API Data Dictionary](https://docs.firststreet.dev/docs/location-introduction)
)
```python
location.<method>
```

* `get_detail`(search_items `list/file`, location_type `string`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Location Detail` product for the given IDs, location_type, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call
* `get_summary`(search_items `list/file`, location_type `string`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Location Summary` product for the given IDs, location_type, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call

<a name="probability"></a>
#### [Probability](#toc)

The Probability API provides `Depth`, `Chance`, `Cumulative`, `Count` data for the given SearchItems.
(More information on the Probability product can be found on the [Probability Page on the First Street Foundation API Data Dictionary](https://docs.firststreet.dev/docs/probability-depth)
)

```python
probability.<method>
```

* `get_depth`(search_items `list/file`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Probability Depth` product for the given IDs, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call
* `get_chance`(search_items `list/file`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Probability Chance` product for the given IDs, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call
* `get_count_summary`(search_items `list/file`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Probability Count-Summary` product for the given IDs, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call
* `get_cumulative`(search_items `list/file`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Probability Cumulative` product for the given IDs, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call
* `get_count`(search_items `list/file`, location_type `string`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Probability Count` product for the given IDs, location_type, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call

<a name="historic"></a>
#### [Historic](#toc)

The Historic API provides `Summary` and `Event` data for the given SearchItems.
(More information on the Historic product can be found on the [Historic Page on the First Street Foundation API Data Dictionary](https://docs.firststreet.dev/docs/historic-summary)
)

```python
historic.<method>
```

* `get_event`(search_items `list/file`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Historic Event` product for the given historic IDs, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call
* `get_events_by_location`(search_items `list/file`, location_type `string`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Historic Detail` product for the given IDs, location_type, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call
* `get_summary`(search_items `list/file`, location_type `string`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Historic Summary` product for the given IDs, location_type, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call

<a name="adaptation"></a>
#### [Adaptation](#toc)
(More information on the Adaptation product can be found on the [Adaptation Page on the First Street Foundation API Data Dictionary](https://docs.firststreet.dev/docs/adaptation-introduction)
)

The Adaptation API provides `Summary` and `Project` data for the given SearchItems.

```python
adaptation.<method>
```

* `get_project`(search_items `list/file`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Adaptation Project` product for the given adaptation IDs, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call
* `get_details_by_location`(search_items `list/file`, location_type `string`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Adaptation Project` product for the given IDs, location_type, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call
* `get_summary`(search_items `list/file`, location_type `string`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Adaptation Summary` product for the given IDs, location_type, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call

<a name="fema"></a>
#### [Fema](#toc)

The Fema API provides `NFIP` data for the given SearchItems.
(More information on the Fema NFIP product can be found on the [Fema NFIP Page on the First Street Foundation API Data Dictionary](https://docs.firststreet.dev/docs/fema-nfip)
)

```python
fema.<method>
```

* `get_nfip`(search_items `list/file`, location_type `string`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Fema NFIP` product for the given IDs, location_type, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call

<a name="environmental"></a>
#### [Environmental](#toc)

The Environmental API provides `Precipitation` data for the given SearchItems.
(More information on the Environmental Precipitation product can be found on the [Environmental Precipitation Page on the First Street Foundation API Data Dictionary](https://docs.firststreet.dev/docs/environmental-precipitation)
)

```python
environmental.<method>
```

* `get_precipitation`(search_items `list/file`, csv `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Environmental Precipitation` product for the given county IDs, and optionally creates a csv file. Arguments provided to `extra_param` will be appened to the end of the endpoint call
   
<a name="tiles"></a>
#### [Tiles](#toc)

The Flood Tiles product give the ability to customize maps by layering on flood tiles.
(More information on the Tile product can be found on the [Tile Page on the First Street Foundation API Data Dictionary](https://docs.firststreet.dev/docs/tiles-introduction)
)

```python
tile.<method>
```

* `get_probability_depth`(coordinate `list of tuple of int [(z, x, y)]`, year `int`, return_period `int`, image `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Probability Depth Tile` product for the given coordinates, and optionally creates an image file
* `get_historic_event`(coordinate `list of tuple of int [(z, x, y)]`, event_id `int`, image `bool`, [output_dir `str='cwd'`], [extra_param `str=None`]) - Returns an array of `Historic Event Tile` product for the given coordinates, and optionally creates an image file
   
<a name="examples"></a>
# [Examples](#toc)
**[Reminder] Keep your API key safe, and do not share it with others!**
1. Single FSID Extraction Through the Client:
    ```python
    # Contents of sample.py
    import firststreet
    fs = firststreet.FirstStreet("api-key")
    
    fsids = [39035103400]
    probability = fs.probability.get_count(fsids, "tract")
    
    print(probability[0].fsid)
    print(probability[0].count)
    ```

2. Multiple FSIDs Extraction Through the Client:
    ```python
    # Contents of sample.py
    import firststreet
    fs = firststreet.FirstStreet("api-key")
    
    fsids = [1912000, 1979140]
    details = fs.location.get_detail(fsids, "city")
    
    print(details[0].fsid)
    print(details[0].county)
    print(details[1].fsid)
    ```
   
3. Adaptation detail Extraction to CSV Through the Client:
    ```python
    # Contents of sample.py
    import firststreet
    fs = firststreet.FirstStreet("api-key")
    
    adaptation = fs.adaptation.get_detail([29], csv=True)

    print(adaptation[0].adaptationId)
    print(adaptation[0].name)
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
   
4. Multiple FSIDs Extraction Using a File Through the Client:

    Content of sample.txt:
    ```text
    541114211
    540456284
    541229206
    540563324
    541262690
    540651172
    ```
    
    ```python
    # Contents of sample.py
    import firststreet
    fs = firststreet.FirstStreet("api-key")
    
    details = fs.location.get_detail("sample.txt", "property")

    print(details[0].fsid)
    print(details[0].county)
    print(details[1].fsid)
    ```
    
5. Different Location Types Through the Client:
    ```python
    # Contents of sample.py
    import firststreet
    fs = firststreet.FirstStreet("api-key")
    
    lst = [362493883, (40.792505, -73.951949), "1220 5th Ave, New York, NY"]
    location = fs.location.get_detail(lst, location_type="property", csv=True)

    print(location[0].fsid)
    print(location[0].route)
    print(location[1].fsid)
    print(location[1].route)
    print(location[2].fsid)
    print(location[2].route)
    ```

5. Single FSID Extraction to CSV Through the Command Line:
    ```sh
    python -m firststreet -p probability.get_depth -i 390000227
    ```

6. Multiple FSIDs Extraction to CSV Through the Command Line:
    ```sh
    python -m firststreet -p historic.get_summary -i 1912000;1979140 -l property
    ```

7. Bulk FSIDs Extraction From File to CSV Through the Command Line:

    Content of sample.txt:
    ```text
    541114211
    540456284
    541229206
    540563324
    541262690
    540651172
    ```
   
    ```sh
    python -m firststreet -p location.get_summary -f sample.txt -l property
    ```
   
   Output File 2020_06_10_20_33_12_location_summary_property.csv:
    ```csv
    fsid,floodFactor,riskDirection,environmentalRisk,historic,adaptation
    541114211,1,0,1,0,0
    540456284,9,0,1,0,0
    541229206,9,1,1,0,0
    540563324,1,0,1,0,0
    541262690,1,0,1,0,0
    540651172,1,0,1,0,0
    ```

5. Different Location Types Through the Command Line:

   **Note that the separator for each item must be a semicolon `;`**
    ```sh
    python -m firststreet -p location.get_detail -i "362493883;(40.792505,-73.951949);1220 5th Ave, New York, NY" -l property
    ```
    
6. Different Locatio Types From File to CSV Through Command Line:

   Content of sample.txt:
   ```text
   362493883
   (40.792505, -73.951949)
   1220 5th Ave, New York, NY
   ```

   ```sh
   python -m firststreet -p location.get_summary -f sample.txt -l property
   ```

7. Getting a Tile from the API Tile Product Through the Client:
    ```python
    # Contents of sample.py
    import firststreet
    fs = firststreet.FirstStreet("api-key")
    
    fs.tile.get_probability_depth(year=2050, return_period=500, coordinate=[(14, 2633, 5694)], image=True)
    tile_image = fs.tile.get_historic_event(event_id=2, coordinate=[(12, 942, 1715)], image=False)
    ```
    
8. Getting a Tile from the API Tile Product Through the Command Line:

   **Note that the separator for each coordinate must be a semicolon `;`, and the spacing within the coordinates**
   ```sh
   python -m firststreet -p tile.get_probability_depth -i (12,942,1715);(11,942,1715) -year 2050 -return_period 500
   python -m firststreet -p tile.get_historic_event -i (12,942,1715) -event_id 14
   ```
   
    
<a name="csv-output"></a>
# [CSV File Output:](#toc)
Any product above can be additionally exported to a CSV file for further usage if the csv boolean is set during the product call, or any call using the command line. The extracted can be found in the `output_data` directory of the project folder (if at least one CSV has been extracted).

<a name="csv-name"></a>
#### [CSV File Name:](#toc)
The file name will be in the format of `YYYY_MM_DD_HH_mm_SS_product_subtype_lookup.csv`. 

Ex:
- `2020_06_10_17_29_49_adaptation_detail.csv`
- `2020_06_10_17_33_56_adaptation_summary_property.csv`

<a name="csv-content"></a>
#### [CSV File Content](#toc)
The contents of the CSV file will follow similar formats as the `First Street Foundation API - V1.0 Overview and Dictionary`, but all lists will be expanded to a flat file. For any values that are null or not available, `<NA>` will be used.

If any of the input FSIDs are invalid, a `valid_id` column will appear with the invalid FSIDs marked with `False`

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
![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//5.2.1.png)

![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//5.2.2.png)

<a name="updating"></a>
# [Updating the Project to the Newest Version:](#toc)
If an update is made to this project, you will need to upgrade through PyPi

1. Open a new `powershell console` / `bash terminal`, navigate to the project, and run the upgrade command:

    ```shell script
    cd /path/to/project
   
    .\venv\Scripts\activate
   
    pip install --upgrade fsf_api_access_python
    ```

    ![Screenshot](https://raw.githubusercontent.com/FirstStreet/fsf_api_access_python/master/doc/images//6.1.2.png)

3. The project should now be updated to the newest version

<a name="license"></a>
# [License](#toc)
```  
MIT License

Copyright (c) 2020 First Street Foundation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


[git]: <https://git-scm.com/downloads>

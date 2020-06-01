## First Street API Access Documentation (Python)

### Intializing Client

```python
# Create a new First Street Foundation API Client
import firststreet
fs = firststreet.FirstStreet("api-key")
```

### Example

```python
# Create a new First Street Foundation API Client
import firststreet
fs = firststreet.FirstStreet("api-key")

fsids = [1912000, 1979140]
fs.location.get_detail(fsids, "property")
```

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

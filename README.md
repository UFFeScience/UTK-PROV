# UTK-PROV

**UTK-PROV** is a provenance-aware extension of the Urban Toolkit (UTK) that captures, stores, queries, and analyzes the evolution of grammar-based urban visualizations. The system records user operations performed during visualization construction and represents them using the W3C PROV model, enabling workflow reconstruction, auditing, reproducibility analysis, and exploration-pattern discovery.

---

## Overview

Urban visualizations are commonly developed through iterative workflows involving the addition, removal, and modification of visualization components. Traditional visualization systems typically preserve only the final specification, making it difficult to understand how a visualization evolved over time.

UTK-PROV addresses this limitation by automatically recording visualization-development activities and transforming them into provenance records. These records can then be queried to recover information about:

* Contributors involved in a project
* Evolution of visualization specifications
* User interaction histories
* Workflow strategies
* Temporal development patterns
* Unique exploration behaviors

The system integrates provenance capture directly into the visualization-construction process and stores provenance information in a relational database for efficient querying and analysis.

---

## Features

* W3C PROV-compliant provenance model
* Automatic capture of visualization operations
* Tracking of additions, removals, and modifications
* Provenance graph generation
* Workflow reconstruction
* User activity analysis
* Temporal workflow analysis
* Exploration-pattern identification
* SQL-based provenance querying
* Support for grammar-based urban visualizations

---

## Provenance Model

UTK-PROV represents visualization workflows using the three core PROV concepts:

### Agents

Users responsible for creating or modifying visualization specifications.

### Activities

Operations performed during visualization construction, including:

* Add
* Remove
* Modify

### Entities

Artifacts generated or modified during visualization development, such as:

* Visualization specifications
* Layers
* Knots
* Maps
* Plots

The provenance graph captures relationships including:

* `wasGeneratedBy`
* `used`
* `wasAssociatedWith`
* `wasDerivedFrom`

---

## Architecture

```text
User
 │
 ▼
UTK Interface
 │
 ▼
Visualization Specification
 │
 ▼
Change Detection
 │
 ▼
Provenance Capture Layer
 │
 ▼
PROV Representation
 │
 ▼
Database Storage
 │
 ▼
Query Engine
 │
 ▼
Workflow Analysis
```

---

## Software Requirements

UTK-PROV relies on the following Python packages:

```text
pysolar==0.*
geopy==2.*
osmium==3.*
overpass==0.7.*
numpy==1.*
pandas==2.*
scipy==1.*
geopandas==0.13.*
tqdm==4.*
mapbox_earcut==1.0.1
shapely==1.8.*
pyproj==3.*
pytz==2023.*
timezonefinder==6.*
pythonnet==3.*
pygeos==0.14.*
ipywidgets==8.*
geojson==3.*
flask==2.3.*
vedo==2023.*
netCDF4==1.6.*
requests==2.*
psutil==5.9.*
watchdog==3.0.*
```

Install the dependencies using:

```bash
pip install -r requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/UFFeScience/UTK-PROV.git
cd UTK-PROV
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

**Linux/macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Example Provenance Queries

### Identifying Contributors

Returns the users associated with a visualization project.

### Session Intervals

Computes the elapsed time between consecutive specification submissions.

###  Workflow Comparison

Retrieves operations performed by a user and the visualization elements affected by those operations.

###  Project Duration

Calculates the temporal span between the first and last recorded project modifications.

###  Exploration Patterns

Identifies workflow sequences that are unique to a specific user.

---

## Example Use Cases

### Multiple Datasets

This scenario explores the integration of heterogeneous urban datasets, including:

* Water bodies
* Parks
* Noise complaints
* Crime rates
* Schools
* Restaurants
* Taxi routes

The use case demonstrates how provenance records capture the evolution of visualization specifications as additional datasets are incorporated.

### What-If Scenario

This scenario evaluates alternative urban-development configurations involving:

* Water features
* Roads
* Parks
* 3D buildings
* Shadow simulations
* Comparative visual analyses

The use case highlights iterative refinement and alternative workflow paths.

---

## Evaluation

UTK-PROV supports provenance-based analyses including:

* Contributor identification
* Workflow reconstruction
* Strategy comparison
* Temporal evolution analysis
* Exploration-pattern discovery

Experimental results demonstrate that provenance queries remain efficient even as provenance graphs grow in size.

---

## Repository Structure


UTK-PROV/
├── backend/
├── database/
├── queries/
├── examples/
├── requirements.txt
└── README.md

---

## License

See the `LICENSE` file for licensing information.

---

## Acknowledgments

UTK-PROV was developed as part of research on provenance-aware urban visualization systems and extends the Urban Toolkit ecosystem with provenance capture, storage, and analysis capabilities.

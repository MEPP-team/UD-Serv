# UD-Serv

UD-Serv is a collection of server-side tools for converting and analysing urban data.

Note: for the client-side components [refer to UD-Viz](https://github.com/VCityTeam/UD-Viz/).

## Available tools

### City 3DTiles tilers
3DTiles, as
[described by Cesium](https://github.com/CesiumGS/3d-tiles), 
is an open specification for sharing, visualizing, fusing, and interacting 
with massive heterogenous 3D geospatial content across desktop, web, and 
mobile applications.. 

UD-Serv offers different kinds of "3DTiles tilers" that take a set of 
CityGML files (version 2.0, XML format) and processes them to yield
3DTiles tilesets. 
For example
[ComputeLyon3DTilesTemporal](https://github.com/VCityTeam/UD-Reproducibility/tree/master/Computations/ComputeLyon3DTilesTemporal)
is a processing pipeline that yields 3D Tiles tilesets extended 
with the temporal extension and capturing the evolutive range of 
the city of Lyon accross various data snapshot vintages ranging 
from 2009 to 2015.

### ExtractCityData
The [ExtractCityData tool](ExtractCityData) allows to process a 
[3DCityDB](https://www.3dcitydb.org/3dcitydb/3dcitydbhomepage/)
database in order to create a materialized view of buildings (encountered in
the database) constituted by their building id, their geometry and optionnally
their year of construction and year of demolition.

### CityGML utility scripts
Some modest helpers, working at the CityGML (version 2.0) file level like: 
 - [CityGML2Stripper](Utils/CityGML2Stripper/) strips a CityGML (XML)file from
   its "appearences" and generic attributes and serializes the result back
   into a new CityGML (XML) file.
 - [CityGMLBuildingBlender](Utils/CityGMLBuildingBlender/) takes a set 
   of CityGML input files, collects all their buildings and gathers them
   within a single CityGML resulting file.

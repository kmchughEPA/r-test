"""
Project:
C_P33 Industry SLAM v4

Script:
industry_catchment_summary.py

Purpose:
Assign IED loads to WFD Catchments and calculate
total nitrogen (N) and phosphorus (P) loads
per catchment.

Inputs:
- IED_Loads_SLAMv4
- vector.SDE.WFD_Catchments_Cycle2

Outputs:
- IED_SLAMv4_Catchment_Loads

Author:
Keelan McHugh

Date:
August 2026
"""


import arcpy
import os

arcpy.env.overwriteOutput = True

# ------------------------------------------------------------------
# Open ArcGIS Pro Project
# ------------------------------------------------------------------

aprx = arcpy.mp.ArcGISProject(
    r"\\dubcatch\Catchments\Projects\_33_Industry\Maps\C_P33_Industry_SLAMv4\Industry_C_P33_Industry_SLAMv4.aprx"
)

m = aprx.listMaps()[0]

# ------------------------------------------------------------------
# Find Layers
# ------------------------------------------------------------------

catchments = None
industry = None

for lyr in m.listLayers():

    if lyr.name == "vector.SDE.WFD_Catchments_Cycle2":
        catchments = lyr

    if lyr.name == "IED_Loads_SLAMv4":
        industry = lyr

if catchments is None:
    raise Exception("Catchment layer not found")

if industry is None:
    raise Exception("IED layer not found")

print("Layers found")

# ------------------------------------------------------------------
# Output Locations
# ------------------------------------------------------------------

scratch_gdb = arcpy.env.scratchGDB

points_with_catchments = os.path.join(
    scratch_gdb,
    "IED_Loads_SLAMv4_Points_With_Catchments"
)

summary_table = (
    r"\\dubcatch\Catchments\Projects\_33_Industry\Maps\C_P33_Industry_SLAMv4"
    r"\Industry_C_P33_Industry_SLAMv4.gdb\IED_SLAMv4_Catchment_Loads"
)

# ------------------------------------------------------------------
# Spatial Join
# Join each IED point to its catchment
# ------------------------------------------------------------------

arcpy.analysis.SpatialJoin(
    target_features=industry,
    join_features=catchments,
    out_feature_class=points_with_catchments,
    join_operation="JOIN_ONE_TO_ONE",
    join_type="KEEP_ALL",
    match_option="INTERSECT"
)

print("Spatial Join complete")

# ------------------------------------------------------------------
# Check fields
# ------------------------------------------------------------------

print("Fields in joined output:")

for field in arcpy.ListFields(points_with_catchments):
    print(field.name)

# ------------------------------------------------------------------
# Statistics
# Sum N and P by catchment
# ------------------------------------------------------------------

arcpy.analysis.Statistics(
    in_table=points_with_catchments,
    out_table=summary_table,
    statistics_fields=[
        ["N", "SUM"],
        ["P", "SUM"]
    ],
    case_field=[
        "CatchmentI",
        "Name"
    ]
)

print("Summary table created")
print(summary_table)
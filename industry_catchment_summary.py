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
    raise Exception("Industry layer not found")

print("Layers found")

# ------------------------------------------------------------------
# Output Locations
# ------------------------------------------------------------------

scratch_gdb = arcpy.env.scratchGDB

spatial_join_fc = os.path.join(
    scratch_gdb,
    "IED_Catchment_SpatialJoin"
)

summary_table = (
    r"\\dubcatch\Catchments\Projects\_33_Industry\Maps\C_P33_Industry_SLAMv4"
    r"\Industry_C_P33_Industry_SLAMv4.gdb\IED_Catchment_Loads"
)

# ------------------------------------------------------------------
# Spatial Join
# ------------------------------------------------------------------

arcpy.analysis.SpatialJoin(
    target_features=catchments,
    join_features=industry,
    out_feature_class=spatial_join_fc,
    join_operation="JOIN_ONE_TO_ONE",
    join_type="KEEP_ALL",
    match_option="INTERSECT"
)

print("Spatial Join complete")

# ------------------------------------------------------------------
# Statistics
# ------------------------------------------------------------------

arcpy.analysis.Statistics(
    in_table=spatial_join_fc,
    out_table=summary_table,
    statistics_fields=[
        ["N", "SUM"],
        ["P", "SUM"]
    ],
    case_field=[
        "CatchmentID",
        "Name"
    ]
)

print("Summary table created")
print(summary_table)
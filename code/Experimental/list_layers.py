import arcpy

aprx = arcpy.mp.ArcGISProject(
    r"\\dubcatch\Catchments\Projects\_33_Industry\Maps\C_P33_Industry_SLAMv4\Industry_C_P33_Industry_SLAMv4.aprx"
)

for m in aprx.listMaps():
    print(f"\nMAP: {m.name}")

    for lyr in m.listLayers():
        print(f"  {lyr.name}")
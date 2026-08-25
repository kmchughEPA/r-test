import arcpy

aprx = arcpy.mp.ArcGISProject(
    r"\\dubcatch\Catchments\Projects\_33_Industry\Maps\C_P33_Industry_SLAMv4\Industry_C_P33_Industry_SLAMv4.aprx"
)

m = aprx.listMaps()[0]

for lyr in m.listLayers():

    if lyr.name == "vector.SDE.WFD_Catchments_Cycle2":

        print("\nFIELDS\n")

        for f in arcpy.ListFields(lyr):
            print(f.name)
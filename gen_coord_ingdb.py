import arcpy

'''
# 设置工作空间
workspace = r"C:/Users/fresh/Documents/ArcGIS/Projects/test001/test001.gdb"
arcpy.env.workspace = workspace

# 获取所有面要素类
feature_classes = arcpy.ListFeatureClasses(feature_type='Polygon')

# 遍历每个面要素类
for fc in feature_classes:
    # 添加新的字段
    field_name = "GDZB"
    field_alias = "拐点坐标"
    field_type = "TEXT"
    field_length = 8000
    
    if not arcpy.ListFields(fc, field_name):
        arcpy.AddField_management(fc, field_name, field_type, field_length=field_length, field_alias=field_alias)
    
    # 更新字段值
    with arcpy.da.UpdateCursor(fc, ["SHAPE@", field_name]) as cursor:
        for row in cursor:
            geometry = row[0]
            points = geometry.getPart(0)
            coordinates = ["({:.3f}, {:.3f})".format(point.X, point.Y) for point in points]
            row[1] = ", ".join(coordinates)
            cursor.updateRow(row)

print("字段添加和更新完成！")
'''

# 设置工作空间
workspace = r"C:/Users/fresh/Documents/ArcGIS/Projects/test001/test001.gdb"
arcpy.env.workspace = workspace

# 获取所有面要素类
feature_classes = arcpy.ListFeatureClasses(feature_type='Polygon')

# 遍历每个面要素类
for fc in feature_classes:
    # 添加新的字段
    field_name = "GDZBXH"
    field_alias = "拐点坐标(带序号)"
    field_type = "TEXT"
    field_length = 8000
    
    if not arcpy.ListFields(fc, field_name):
        arcpy.AddField_management(fc, field_name, field_type, field_length=field_length, field_alias=field_alias)
    
    # 更新字段值
    with arcpy.da.UpdateCursor(fc, ["SHAPE@", field_name]) as cursor:
        for row in cursor:
            geometry = row[0]
            points = geometry.getPart(0)
            coordinates = ["{}: ({:.3f}, {:.3f})".format(i+1, point.X, point.Y) for i, point in enumerate(points)]
            row[1] = ", ".join(coordinates)
            cursor.updateRow(row)

print("字段添加和更新完成！")

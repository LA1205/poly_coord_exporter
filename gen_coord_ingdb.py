'''
import arcpy


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
            coordinates = []
            for part in geometry:
                for point in part:
                    if point:
                        coordinates.append("({:.3f}, {:.3f})".format(point.X, point.Y))
            row[1] = ", ".join(coordinates)
            cursor.updateRow(row)

print("字段添加和更新完成！")
'''
'''
import arcpy

# 设置工作空间
workspace = r"D:\BaiduSyncdisk\Work_Space\KB\Projetcs\hotan\license\license.gdb"
arcpy.env.workspace = workspace

# 获取所有面要素类
#feature_classes = arcpy.ListFeatureClasses(feature_type='Polygon')
# 或者获取指定名称的要素类
feature_classes = arcpy.ListFeatureClasses(wild_card='HETIANDIQU_V6_topochecked')

# 遍历每个面要素类
for fc in feature_classes:
    # 添加新的字段
    field_name = "GDZBXH"
    field_alias = "拐点坐标(带序号)"
    field_type = "TEXT"
    field_length = 11000
    
    if not arcpy.ListFields(fc, field_name):
        arcpy.AddField_management(fc, field_name, field_type, field_length=field_length, field_alias=field_alias)
    
    # 更新字段值
    with arcpy.da.UpdateCursor(fc, ["SHAPE@", field_name]) as cursor:
        for row in cursor:
            geometry = row[0]
            coordinates = []
            for part in geometry:
                for i, point in enumerate(part):
                    if point:
                        coordinates.append("{}: ({:.1f}, {:.1f})".format(i+1, point.X, point.Y))
                        #格式化坐标保留1位小数#
            row[1] = ", ".join(coordinates)
            cursor.updateRow(row)

print("字段添加和更新完成！")
'''
import arcpy

# 设置工作空间
workspace = r"D:\BaiduSyncdisk\Work_Space\KB\Projetcs\hotan\license\license.gdb"
arcpy.env.workspace = workspace

# 获取所有面要素类
# feature_classes = arcpy.ListFeatureClasses(feature_type='Polygon')
# 或者获取指定名称的要素类
feature_classes = arcpy.ListFeatureClasses(wild_card='HETIANDIQU_V6_topochecked')

# 坐标保留的小数位数（可调整）
decimal_places = 1

# 遍历每个面要素类
for fc in feature_classes:
    # 添加原始字段（不变）
    field_name = "GDZBXH"
    field_alias = "拐点坐标(带序号)"
    field_type = "TEXT"
    field_length = 11000

    if not arcpy.ListFields(fc, field_name):
        arcpy.AddField_management(fc, field_name, field_type, field_length=field_length, field_alias=field_alias)

    # 添加新的四个文本字段（用于存储四个极点的 (x, y) 坐标）
    # 字段长度给到足够冗余（例如 50），避免精度提高时截断
    extreme_fields = [
        ("W_POINT", "至西点坐标", 255),
        ("S_POINT", "至南点坐标", 255),
        ("E_POINT", "至东点坐标", 255),
        ("N_POINT", "至北点坐标", 255),
    ]
    for fname, alias, length in extreme_fields:
        if not arcpy.ListFields(fc, fname):
            arcpy.AddField_management(fc, fname, "TEXT", field_length=length, field_alias=alias)

    # 更新字段值
    with arcpy.da.UpdateCursor(fc, ["SHAPE@", field_name, "W_POINT", "S_POINT", "E_POINT", "N_POINT"]) as cursor:
        for row in cursor:
            geometry = row[0]
            coordinates_texts = []
            all_points = []

            # 收集所有拐点并写入原始文本字段（保留原功能）
            for part in geometry:
                for i, point in enumerate(part):
                    if point:
                        coordinates_texts.append(
                            "{}: ({:.{p}f},{:.{p}f})".format(i + 1, point.X, point.Y, p=decimal_places)
                        )
                        all_points.append(point)

            row[1] = ",".join(coordinates_texts)

            # 计算四个极点，并以文本形式写入 "(x, y)"
            if all_points:
                west_point = min(all_points, key=lambda p: p.X)
                east_point = max(all_points, key=lambda p: p.X)
                south_point = min(all_points, key=lambda p: p.Y)
                north_point = max(all_points, key=lambda p: p.Y)

                # 统一格式化函数
                def fmt_xy(pt):
                    return "{:.{p}f},{:.{p}f}".format(pt.X, pt.Y, p=decimal_places)

                row[2] = fmt_xy(west_point)   # W_POINT
                row[3] = fmt_xy(south_point)  # S_POINT
                row[4] = fmt_xy(east_point)   # E_POINT
                row[5] = fmt_xy(north_point)  # N_POINT
            else:
                # 没有点的情况置为空字符串（或可用 None）
                row[2] = ""
                row[3] = ""
                row[4] = ""
                row[5] = ""

            cursor.updateRow(row)

print("字段添加和更新完成！")


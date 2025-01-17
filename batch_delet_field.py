import arcpy

# 设置工作空间
workspace = r'D:\BaiduSyncdisk\Work_Space\KB\Projetcs\hotan\cele_update1\cele_update1.gdb'
arcpy.env.workspace = workspace

# 获取所有面要素类
feature_classes = arcpy.ListFeatureClasses(feature_type='Polygon')

# 指定要删除的字段名称
field_to_delete = "GDZBXH"

# 遍历每个面要素类
for fc in feature_classes:
    # 检查字段是否存在
    if arcpy.ListFields(fc, field_to_delete):
        # 删除字段
        arcpy.DeleteField_management(fc, field_to_delete)
        print(f"字段 {field_to_delete} 已从 {fc} 中删除")
    else:
        print(f"字段 {field_to_delete} 不存在于 {fc} 中")

print("字段删除完成！")

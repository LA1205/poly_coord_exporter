import arcpy
import pandas as pd
import os

def export_feature_classes_to_excel(gdb_path, output_folder):
    arcpy.env.workspace = gdb_path
    feature_classes = arcpy.ListFeatureClasses()

    for fc in feature_classes:
        # 获取要素类的字段别名
        fields = arcpy.ListFields(fc)
        field_aliases = {field.name: field.aliasName for field in fields}

        # 获取要素类的属性表
        data = []
        with arcpy.da.SearchCursor(fc, [field.name for field in fields]) as cursor:
            for row in cursor:
                data.append(row)

        # 将属性表转换为DataFrame
        df = pd.DataFrame(data, columns=[field.name for field in fields])
        df.rename(columns=field_aliases, inplace=True)

        # 获取第一个几何要素的XMMC字段值作为文件名
        first_feature = next(arcpy.da.SearchCursor(fc, ["XMMC"]))
        file_name = f"{first_feature[0]}.xlsx"

        # 导出为Excel文件
        output_path = os.path.join(output_folder, file_name)
        df.to_excel(output_path, index=False)
        print('表格 -> ' + str(file_name) + '导出完成！')

# 示例用法
gdb_path = r"D:\BaiduSyncdisk\Work_Space\KB\Projetcs\hotan\cele_update1\cele_update1.gdb"
output_folder = r"D:\BaiduSyncdisk\Work_Space\KB\Projetcs\hotan\20250127各县项目小班表\策勒县"
export_feature_classes_to_excel(gdb_path, output_folder)


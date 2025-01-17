import geopandas as gpd
import pandas as pd
import fiona
import os

# 读取GDB文件路径
gdb_path = r'D:\BaiduSyncdisk\Work_Space\KB\Projetcs\hotan\hetian_update1\hetian_集体土地项目合并.gdb'

# 获取所有图层名
layers = fiona.listlayers(gdb_path)

# 创建输出文件夹（如不存在）
output_folder = r"D:\BaiduSyncdisk\Work_Space\KB\Projetcs\hotan\hetian_update1"
os.makedirs(output_folder, exist_ok=True)

# 遍历每个图层
for layer in layers:
    # 读取图层
    gdf = gpd.read_file(gdb_path, layer=layer)

    # 检查图层中是否包含“乡镇”和“村”字段（可以根据具体字段名修改）
    if 'XM' not in gdf.columns or 'QSDWMC' not in gdf.columns or 'QSXZ' not in gdf.columns:
        print(f'图层 {layer} 不包含 "XM" 、 "QSDWMC"或"QSXZ" 字段，跳过...')
        continue

    # 创建一个用于存储拐点和属性的DataFrame
    points_data = []

    # 遍历图层中的所有几何形状
    for idx, row in gdf.iterrows():
        geom = row.geometry
        township = row['XM']  # 读取乡镇字段
        village = row['QSDWMC']  # 读取村字段
        qs = row['QSXZ'] #读取权属性质
        coordinates_str = ""  # 用于存储该图斑的所有坐标字符串

        if geom.geom_type == 'Polygon' or geom.geom_type == 'MultiPolygon':
            # 对于每个Polygon获取其外部边界的所有点
            if geom.geom_type == 'Polygon':
                polygons = [geom]
            else:
                polygons = geom.geoms  # 如果是MultiPolygon，则获取所有子Polygon

            for polygon in polygons:
                exterior_coords = polygon.exterior.coords
                # 将每个拐点的坐标转换为字符串并连接，并限制结果到四位小数
                coordinates_str += "; ".join([f"({coord[0]:.4f}, {coord[1]:.4f})" for coord in exterior_coords])

        # 将该图斑的乡镇、村和坐标存入列表中
        points_data.append({
            'XM': township,
            'QSDWMC': village,
            'QSXZ': qs,
            '图斑编号': idx,
            '拐点坐标': coordinates_str
        })

    # 转换为DataFrame
    points_df = pd.DataFrame(points_data)

    # 输出文件名与图层名相同的Excel文件
    output_excel_path = os.path.join(output_folder, f'{layer}.xlsx')
    points_df.to_excel(output_excel_path, index=False)

    print(f'{layer} 图层的乡镇、村及拐点坐标已导出至 {output_excel_path}')


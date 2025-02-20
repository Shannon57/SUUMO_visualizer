from data_processing import RentDataProcessor
from map_visualizer import RentMapVisualizer

# 賃貸アパート　または　賃貸マンション
rent_type = '賃貸アパート'
# 1DK 1K 1LDK 1LK
room_type = '1K'
# 最大3
transfers = 2
# Trueにするとこの乗り換え回数の駅のみ出力
# Falseにするとこの乗り換え回数以下の駅を出力
transfers_only = False

# 最大60
max_travel_time = 60



# データ処理
processor = RentDataProcessor(rent_type, room_type, transfers, transfers_only, max_travel_time)
processor.rank_rent()
df, rent_ranges = processor.get_data()

# ファイルのラベル作成
transfers_label = ''
if transfers_only:
    transfers_label = f'乗換{transfers}回'
else:
    transfers_label = f'乗換{transfers}回以下'

# 地図作成
visualizer = RentMapVisualizer(df, rent_ranges)
visualizer.generate_map(f'{rent_type}_{room_type}_{transfers_label}_{max_travel_time}分以内.html')

print(f'出力完了【{rent_type}_{room_type}_{transfers_label}_{max_travel_time}分以内.html】')

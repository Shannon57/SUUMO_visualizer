import pandas as pd

class RentDataProcessor:
    def __init__(self, rent_type, room_type, transfers, transfers_only, max_travel_time):
        file_path = f'./data/rent_info_{rent_type}_{room_type}.csv'
        self.df = pd.read_csv(file_path)
        self.transfers = transfers
        self.transfers_only = transfers_only
        self.max_travel_time = max_travel_time
        self.process_data()

    def process_data(self):
        """データの前処理"""
        self.df['乗り換え回数'] = self.df['乗り換え回数'].str.extract('(\d+)').astype(int)
        self.df['所要時間'] = self.df['所要時間'].str.replace("分", "").astype(int)
        # 京急かつ本線なら乗り換え回数を-1する
        mask = (self.df['鉄道会社'] == '京急') & (self.df['路線名'] == '本線')
        self.df.loc[mask, '乗り換え回数'] -= 1

        # 指定されたフィルタ処理
        self.df = self.df[self.df['所要時間'] <= self.max_travel_time]
        if (self.transfers_only):
            self.df = self.df[self.df['乗り換え回数'] == self.transfers]
        else:
            self.df = self.df[self.df['乗り換え回数'] <= self.transfers]


    def rank_rent(self):
        """家賃を5段階にランク付け"""
        rent_bins = pd.qcut(self.df['月額'], 5, retbins=True, labels=[1, 2, 3, 4, 5])
        self.df['家賃ランク'] = rent_bins[0]
        self.rent_ranges = rent_bins[1]

    def get_data(self):
        """処理済みのデータを取得"""
        return self.df, self.rent_ranges

import folium
import json

class RentMapVisualizer:
    def __init__(self, df, rent_ranges):
        self.df = df
        self.rent_ranges = rent_ranges

    def generate_map(self, output_file='map.html'):
        """地図を作成し、マーカーを表示"""
        m = folium.Map(location=[self.df['lat'].mean(), self.df['lon'].mean()], zoom_start=12, tiles="CartoDB positron")

        # タイルレイヤー
        folium.TileLayer('CartoDB dark_matter').add_to(m)
        folium.TileLayer('OpenStreetMap').add_to(m)
        folium.LayerControl().add_to(m)

        # 色の定義
        color_scale = {1: 'lightblue', 2: 'blue', 3: 'green', 4: 'orange', 5: 'red'}

        # マーカー追加
        for _, row in self.df.iterrows():
            popup_html = f"""
            <div style="font-size:12px; white-space: nowrap;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr><td><b>駅名</b></td><td>{row['駅名']}</td></tr>
                    <tr><td><b>鉄道会社</b></td><td>{row['鉄道会社']}</td></tr>
                    <tr><td><b>路線名</b></td><td>{row['路線名']}</td></tr>
                    <tr><td><b>所要時間</b></td><td>{row['所要時間']} 分</td></tr>
                    <tr><td><b>乗り換え回数</b></td><td>{row['乗り換え回数']} 回</td></tr>
                    <tr><td><b>家賃</b></td><td>{row['月額']} 万円</td></tr>
                </table>
            </div>
            """

            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=5,
                color=color_scale[row['家賃ランク']],
                fill=True,
                fill_color=color_scale[row['家賃ランク']],
                fill_opacity=0.7,
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(m)

        # 凡例
        legend_html = f'''
        <div style="
            position: fixed; 
            bottom: 20px; right: 20px; 
            background: white; 
            z-index: 1000;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            font-size: 12px;
        ">
            <b>家賃ランク凡例（万円）</b><br>
            <svg width="10" height="10"><rect width="10" height="10" style="fill:lightblue"/></svg> {self.rent_ranges[0]:.1f}万円 - {self.rent_ranges[1]:.1f}万円<br>
            <svg width="10" height="10"><rect width="10" height="10" style="fill:blue"/></svg> {self.rent_ranges[1]:.1f}万円 - {self.rent_ranges[2]:.1f}万円<br>
            <svg width="10" height="10"><rect width="10" height="10" style="fill:green"/></svg> {self.rent_ranges[2]:.1f}万円 - {self.rent_ranges[3]:.1f}万円<br>
            <svg width="10" height="10"><rect width="10" height="10" style="fill:orange"/></svg> {self.rent_ranges[3]:.1f}万円 - {self.rent_ranges[4]:.1f}万円<br>
            <svg width="10" height="10"><rect width="10" height="10" style="fill:red"/></svg> {self.rent_ranges[4]:.1f}万円 - {self.rent_ranges[5]:.1f}万円
        </div>
        '''

        m.get_root().html.add_child(folium.Element(legend_html))
        m.save(output_file)

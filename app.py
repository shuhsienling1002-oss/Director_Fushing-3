import streamlit as st
import pandas as pd
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定 (System Config)
# ==========================================
st.set_page_config(
    page_title="2026 全國賞櫻地圖 (蘇佐璽嚴選終極版)",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (UI/UX Upgrade)
# ==========================================
st.markdown("""
<style>
/* 全站基礎設定：粉嫩櫻花風 */
.stApp {
    background-color: #FFF0F5;
    font-family: "Microsoft JhengHei", sans-serif;
    color: #333333 !important;
}

/* 隱藏官方雜項 */
header {visibility: hidden;}
footer {display: none !important;}

/* 標題區：增強層次感 */
.header-box {
    background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%);
    padding: 30px 20px;
    border-radius: 0 0 30px 30px;
    color: white !important;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 6px 20px rgba(255, 20, 147, 0.4);
    margin-top: -60px;
}
.header-title { 
    font-size: 28px; font-weight: 800; letter-spacing: 1px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2); color: white !important; 
}

/* 輸入區卡片化 */
.input-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    border: 1px solid #FFC0CB;
    margin-bottom: 20px;
}

/* 按鈕優化 */
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #C71585 0%, #DB7093 100%);
    color: white !important;
    border-radius: 50px;
    border: none;
    padding: 14px 0;
    font-weight: bold;
    font-size: 18px;
    box-shadow: 0 4px 12px rgba(199, 21, 133, 0.3);
    transition: transform 0.1s;
}
.stButton>button:active { transform: scale(0.98); }

/* 行程卡片 */
.day-card {
    background: white;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 15px;
    border-left: 8px solid #FF69B4;
    box-shadow: 0 3px 8px rgba(0,0,0,0.08);
    position: relative;
}

/* 導航按鈕 */
.nav-btn {
    display: inline-block;
    background-color: #4285F4;
    color: white !important;
    padding: 4px 10px;
    border-radius: 15px;
    font-size: 12px;
    text-decoration: none;
    margin-left: 5px;
}

/* 標籤系統 */
.tag { font-size: 11px; padding: 3px 8px; border-radius: 10px; margin-right: 5px; color: white; display: inline-block;}
.tag-must { background: #FF1493; }
.tag-hot { background: #FF8C00; }
.tag-secret { background: #9370DB; }
.tag-city { background: #20B2AA; }

/* 花況燈號 */
.status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }
.status-full { background-color: #FF1493; box-shadow: 0 0 5px #FF1493; }
.status-start { background-color: #32CD32; }
.status-end { background-color: #A9A9A9; }

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (45+ 筆完整版)
# ==========================================
all_spots_db = [
    # === 👑 桃園復興區 (核心推廣) ===
    {"name": "拉拉山恩愛農場", "region": "北部", "county": "桃園", "lat": 24.695, "lon": 121.405, "zone": "深山", "month": [2, 3], "flower": "千島櫻", "status": "🌸 滿開", "desc": "粉紅櫻花與雲海同框的夢幻大景。"},
    {"name": "中巴陵櫻木花道", "region": "北部", "county": "桃園", "lat": 24.680, "lon": 121.395, "zone": "深山", "month": [2], "flower": "昭和櫻", "status": "🌸 滿開", "desc": "北橫公路旁最美的粉紅隧道。"},
    {"name": "角板山行館", "region": "北部", "county": "桃園", "lat": 24.818, "lon": 121.350, "zone": "郊區", "month": [1, 2], "flower": "梅花/山櫻", "status": "🍃 綠葉", "desc": "賞花還能逛戰備隧道，適合全家出遊。"},
    {"name": "東眼山森林遊樂區", "region": "北部", "county": "桃園", "lat": 24.825, "lon": 121.410, "zone": "郊區", "month": [2, 3], "flower": "山櫻花", "status": "🌸 盛開", "desc": "漫步在柳杉林中的粉紅驚喜。"},
    {"name": "翠墨莊園", "region": "北部", "county": "桃園", "lat": 24.830, "lon": 121.360, "zone": "郊區", "month": [1, 2], "flower": "緋寒櫻", "status": "🌸 盛開", "desc": "復興區新興網美打卡點。"},
    {"name": "壽山巖觀音寺", "region": "北部", "county": "桃園", "lat": 25.005, "lon": 121.345, "zone": "市區", "month": [2], "flower": "寒櫻", "status": "🍃 謝花", "desc": "桃園市區最近的賞櫻名所。"},

    # === 北部 (大台北/新竹) ===
    {"name": "淡水天元宮", "region": "北部", "county": "新北", "lat": 25.185, "lon": 121.485, "zone": "郊區", "month": [2, 3], "flower": "吉野櫻", "status": "🌱 含苞", "desc": "無極真元天壇與櫻花交織。"},
    {"name": "陽明山平菁街", "region": "北部", "county": "台北", "lat": 25.135, "lon": 121.560, "zone": "郊區", "month": [1, 2], "flower": "寒櫻", "status": "🍃 謝花", "desc": "台北第一波櫻花，巷弄粉紅圍牆。"},
    {"name": "內湖樂活公園", "region": "北部", "county": "台北", "lat": 25.068, "lon": 121.615, "zone": "市區", "month": [2], "flower": "寒櫻/八重", "status": "🌸 滿開", "desc": "搭捷運就能到的夜櫻勝地。"},
    {"name": "中正紀念堂", "region": "北部", "county": "台北", "lat": 25.035, "lon": 121.519, "zone": "市區", "month": [2, 3], "flower": "大漁櫻", "status": "🌸 盛開", "desc": "市中心最方便的賞櫻點。"},
    {"name": "三峽大熊櫻花林", "region": "北部", "county": "新北", "lat": 24.890, "lon": 121.450, "zone": "郊區", "month": [1, 2, 3], "flower": "三色櫻", "status": "🌸 滿開", "desc": "4000棵櫻花染紅山頭，夜櫻超美。"},
    {"name": "烏來瀑布公園", "region": "北部", "county": "新北", "lat": 24.848, "lon": 121.550, "zone": "郊區", "month": [2], "flower": "山櫻花", "status": "🌸 盛開", "desc": "搭台車看瀑布與櫻花。"},
    {"name": "司馬庫斯", "region": "北部", "county": "新竹", "lat": 24.578, "lon": 121.335, "zone": "深山", "month": [2], "flower": "昭和櫻", "status": "🌸 滿開", "desc": "上帝的部落，需預約通行證。"},
    {"name": "山上人家", "region": "北部", "county": "新竹", "lat": 24.605, "lon": 121.090, "zone": "深山", "month": [2, 3], "flower": "吉野櫻", "status": "🌱 含苞", "desc": "雲端上的茶園與櫻花。"},
    {"name": "新竹公園", "region": "北部", "county": "新竹", "lat": 24.802, "lon": 120.980, "zone": "市區", "month": [2], "flower": "河津櫻", "status": "🌸 盛開", "desc": "玻璃工藝博物館旁的日式櫻花。"},

    # === 中部 (台中/南投/雲林) ===
    {"name": "武陵農場", "region": "中部", "county": "台中", "lat": 24.360, "lon": 121.310, "zone": "深山", "month": [2], "flower": "紅粉佳人", "status": "🌸 滿開", "desc": "台灣賞櫻的代名詞，綿延三公里。"},
    {"name": "福壽山農場", "region": "中部", "county": "台中", "lat": 24.245, "lon": 121.245, "zone": "深山", "month": [2, 3], "flower": "千島櫻", "status": "🌱 含苞", "desc": "全台最高海拔櫻花園。"},
    {"name": "后里泰安派出所", "region": "中部", "county": "台中", "lat": 24.320, "lon": 120.745, "zone": "市區", "month": [2], "flower": "八重櫻", "status": "🌸 盛開", "desc": "全台最美派出所，平地賞櫻首選。"},
    {"name": "新社櫻木花道", "region": "中部", "county": "台中", "lat": 24.205, "lon": 120.805, "zone": "郊區", "month": [2], "flower": "八重櫻", "status": "🌸 盛開", "desc": "區公所旁的粉紅街道。"},
    {"name": "東勢林場", "region": "中部", "county": "台中", "lat": 24.285, "lon": 120.875, "zone": "郊區", "month": [2], "flower": "山櫻花", "status": "🍃 謝花", "desc": "中部陽明山，適合親子健行。"},
    {"name": "九族文化村", "region": "中部", "county": "南投", "lat": 23.870, "lon": 120.950, "zone": "郊區", "month": [2], "flower": "八重櫻", "status": "🌸 滿開", "desc": "日本認證賞櫻名所，夜櫻祭必看。"},
    {"name": "暨南大學", "region": "中部", "county": "南投", "lat": 23.950, "lon": 120.930, "zone": "市區", "month": [2], "flower": "山櫻", "status": "🌸 盛開", "desc": "全台最美校園櫻花季，適合野餐。"},
    {"name": "奧萬大", "region": "中部", "county": "南投", "lat": 23.945, "lon": 121.170, "zone": "深山", "month": [2, 3], "flower": "霧社櫻", "status": "🌱 含苞", "desc": "春天的白色霧社櫻是絕景。"},
    {"name": "杉林溪", "region": "中部", "county": "南投", "lat": 23.635, "lon": 120.795, "zone": "深山", "month": [2, 3], "flower": "椿寒櫻", "status": "🌸 盛開", "desc": "鬱金香與櫻花同時盛開。"},
    {"name": "草嶺石壁", "region": "中部", "county": "雲林", "lat": 23.600, "lon": 120.700, "zone": "深山", "month": [2, 3], "flower": "白花山櫻", "status": "🌸 盛開", "desc": "全台極罕見的白色山櫻花秘境。"},

    # === 南部 (嘉義/台南/高雄/屏東) ===
    {"name": "阿里山森林遊樂區", "region": "南部", "county": "嘉義", "lat": 23.510, "lon": 120.800, "zone": "深山", "month": [3, 4], "flower": "吉野櫻", "status": "🌱 含苞", "desc": "小火車穿梭櫻花林，世界級景觀。"},
    {"name": "隙頂石棹", "region": "南部", "county": "嘉義", "lat": 23.470, "lon": 120.690, "zone": "深山", "month": [2, 3], "flower": "昭和櫻", "status": "🌸 盛開", "desc": "琉璃光與櫻花夜景。"},
    {"name": "寒溪呢森林", "region": "南部", "county": "嘉義", "lat": 23.555, "lon": 120.735, "zone": "深山", "month": [1, 2], "flower": "福爾摩沙櫻", "status": "🍃 謝花", "desc": "周子瑜也去過的白色櫻花隧道。"},
    {"name": "烏山頭水庫", "region": "南部", "county": "台南", "lat": 23.205, "lon": 120.365, "zone": "市區", "month": [3], "flower": "南洋櫻", "status": "🌱 含苞", "desc": "香榭大道，粉紅花瓣飄落如下雪。"},
    {"name": "寶山二集團", "region": "南部", "county": "高雄", "lat": 23.065, "lon": 120.725, "zone": "郊區", "month": [1, 2], "flower": "河津櫻", "status": "🍃 謝花", "desc": "高雄最早盛開的粉紅花海。"},
    {"name": "藤枝森林遊樂區", "region": "南部", "county": "高雄", "lat": 23.070, "lon": 120.755, "zone": "深山", "month": [1, 2], "flower": "山櫻", "status": "🍃 謝花", "desc": "南部小溪頭，森濤中的櫻花。"},
    {"name": "霧台櫻花王", "region": "南部", "county": "屏東", "lat": 22.750, "lon": 120.730, "zone": "深山", "month": [2], "flower": "山櫻", "status": "🍃 謝花", "desc": "一棵樹就開滿整個庭院，魯凱族傳奇。"},

    # === 東部 (宜蘭/花蓮/台東) ===
    {"name": "宜蘭大同櫻花林", "region": "東部", "county": "宜蘭", "lat": 24.600, "lon": 121.500, "zone": "郊區", "month": [2], "flower": "八重櫻", "status": "🌸 盛開", "desc": "台7甲線沿路都是櫻花。"},
    {"name": "明池森林遊樂區", "region": "東部", "county": "宜蘭", "lat": 24.650, "lon": 121.470, "zone": "深山", "month": [2, 3], "flower": "大島櫻", "status": "🌱 含苞", "desc": "高山湖泊與櫻花的空靈之美。"},
    {"name": "羅莊櫻花步道", "region": "東部", "county": "宜蘭", "lat": 24.665, "lon": 121.780, "zone": "市區", "month": [2, 3], "flower": "墨染櫻", "status": "🌱 含苞", "desc": "平地最美櫻花河岸，倒影迷人。"},
    {"name": "玉山神學院", "region": "東部", "county": "花蓮", "lat": 23.885, "lon": 121.515, "zone": "郊區", "month": [2, 3], "flower": "霧社櫻", "status": "🌸 盛開", "desc": "俯瞰鯉魚潭，白色櫻花配湖光山色。"},
    {"name": "太麻里金針山", "region": "東部", "county": "台東", "lat": 22.650, "lon": 120.960, "zone": "深山", "month": [1, 2], "flower": "山櫻", "status": "🍃 謝花", "desc": "雲霧繚繞的東部後花園。"}
]

# ==========================================
# 4. 核心邏輯：地理圍欄行程生成器 (Smart Logic)
# ==========================================
def generate_smart_itinerary(travel_date, days_option, group, target_region):
    m = travel_date.month
    
    # 1. 處理天數
    if "一日" in days_option: total_days = 1
    elif "二日" in days_option: total_days = 2
    else: total_days = 3

    itinerary = {}
    
    # 2. 篩選可用景點
    if target_region == "🌸 全臺環島 (蘇區長特推)":
        candidates = [s for s in all_spots_db if m in s['month']]
    else:
        candidates = [s for s in all_spots_db if s['region'] == target_region and m in s['month']]
    
    # 防呆：如果沒景點，就顯示所有該區景點
    if not candidates:
        candidates = [s for s in all_spots_db if s['region'] == target_region][:3]

    # 3. 智能分組 (避免瞬間移動)
    # 將景點按「縣市」分組
    grouped_spots = {}
    for s in candidates:
        c = s['county']
        if c not in grouped_spots: grouped_spots[c] = []
        grouped_spots[c].append(s)
    
    # 縣市列表
    counties = list(grouped_spots.keys())
    
    # 4. 行程生成
    for d in range(1, total_days + 1):
        day_spots = []
        
        # Day 1 邏輯：北部優先給桃園 (政治正確)，其他地區隨機
        if d == 1 and target_region == "北部" and "桃園" in grouped_spots:
            current_county = "桃園"
        else:
            # 隨機選一個還有景點的縣市
            if not counties: counties = list(grouped_spots.keys()) # 重置
            current_county = counties[d % len(counties)]
        
        # 從該縣市選 1-2 個點
        county_pool = grouped_spots.get(current_county, [])
        if len(county_pool) >= 2:
            day_spots = random.sample(county_pool, 2)
        elif len(county_pool) == 1:
            day_spots = [county_pool[0]]
            # 補一個鄰近的 (簡單處理：隨機補一個同區的)
            backup = [s for s in candidates if s not in day_spots]
            if backup: day_spots.append(backup[0])
        else:
            # 萬一該縣市沒點了，隨機抓
            day_spots = random.sample(candidates, min(2, len(candidates)))
            
        itinerary[d] = day_spots

    return itinerary, candidates

# ==========================================
# 5. UI 呈現 (Mobile First + Map)
# ==========================================
st.markdown("""
<div class="header-box">
<div class="header-title">🌸 2026 全國賞櫻地圖</div>
<div style="color:white; opacity:0.9; margin-top:5px; font-size:14px;">
復興區長 <b>蘇佐璽</b> 祝大家新春愉快．賞花開心 ❤️
</div>
</div>
""", unsafe_allow_html=True)

# --- 1. 輸入區 ---
st.markdown('<div class="input-card">', unsafe_allow_html=True)
c1, c2 = st.columns([2, 1])
with c1:
    target_region = st.selectbox("📍 選擇區域", ["北部", "中部", "南部", "東部", "🌸 全臺環島 (蘇區長特推)"])
with c2:
    days = st.selectbox("📅 天數", ["一日遊", "二日遊", "三日遊"])

c3, c4 = st.columns(2)
with c3:
    travel_date = st.date_input("🚀 出發日", value=date(2026, 2, 20))
with c4:
    group = st.selectbox("👥 夥伴", ["情侶", "親子", "長輩", "獨旅"])

run_btn = st.button("✨ 生成蘇區長推薦行程")
st.markdown('</div>', unsafe_allow_html=True)

# --- 2. 地圖與行程 ---
if run_btn:
    itinerary, all_candidates = generate_smart_itinerary(travel_date, days, group, target_region)
    
    # 準備地圖數據
    map_data = []
    for d, spots in itinerary.items():
        for s in spots:
            map_data.append({"lat": s['lat'], "lon": s['lon'], "name": s['name']})
    df_map = pd.DataFrame(map_data)

    # Tab 分頁
    tab1, tab2 = st.tabs(["🗺️ 地圖模式", "📝 詳細行程"])
    
    with tab1:
        if not df_map.empty:
            st.map(df_map, latitude='lat', longitude='lon', size=20, color='#FF1493')
            st.caption("👆 地圖顯示您行程中的景點分佈")
        else:
            st.warning("查無相關景點數據。")
            
        # 顯示簡易列表
        st.markdown("### 📍 景點快覽")
        for d, spots in itinerary.items():
            for s in spots:
                 badge = "👑" if s['county'] == "桃園" else "🌸"
                 st.markdown(f"{badge} **{s['name']}** ({s['county']})")

    with tab2:
        st.success(f"已為您規劃：{target_region} {days}！")
        
        for d, spots in itinerary.items():
            s1 = spots[0]
            s2 = spots[1] if len(spots) > 1 else s1
            
            # 標籤邏輯
            def get_tags(s):
                tags = ""
                if s['county'] == "桃園": tags += '<span class="tag tag-must">蘇區長推</span>'
                if s['zone'] == "深山": tags += '<span class="tag tag-secret">秘境</span>'
                if s['zone'] == "市區": tags += '<span class="tag tag-city">市區</span>'
                if "滿開" in s['status']: tags += '<span class="tag tag-hot">滿開中</span>'
                return tags

            # Google Maps Link
            def get_nav_link(name):
                return f"https://www.google.com/maps/search/?api=1&query={name}"

            # === 關鍵修復：HTML 字串完全靠左，移除所有縮排 ===
            st.markdown(f"""
<div class="day-card">
<div style="font-size:20px; font-weight:bold; color:#333; margin-bottom:15px; border-bottom:1px dashed #FFB6C1; padding-bottom:10px;">
🗓️ Day {d} <span style="font-size:14px; color:#888; font-weight:normal;">({s1['county']}周邊)</span>
</div>
<div style="margin-bottom:20px;">
<div style="font-weight:bold; font-size:18px; color:#C71585;">
09:30 {s1['name']} 
<a href="{get_nav_link(s1['name'])}" target="_blank" class="nav-btn">➤ 導航</a>
</div>
<div style="margin-top:5px;">{get_tags(s1)}</div>
<div style="color:#555; font-size:14px; margin-top:5px;">
<span class="status-dot status-full"></span>{s1['status']} | {s1['desc']}
</div>
</div>
<div style="background:#FFF0F5; padding:10px; border-radius:8px; font-size:14px; color:#C71585; margin-bottom:20px; text-align:center;">
🍱 午餐推薦：{s1['county']} 在地風味料理
</div>
<div>
<div style="font-weight:bold; font-size:18px; color:#C71585;">
14:30 {s2['name']}
<a href="{get_nav_link(s2['name'])}" target="_blank" class="nav-btn">➤ 導航</a>
</div>
<div style="margin-top:5px;">{get_tags(s2)}</div>
<div style="color:#555; font-size:14px; margin-top:5px;">
<span class="status-dot status-start"></span>{s2['status']} | {s2['desc']}
</div>
</div>
</div>
""", unsafe_allow_html=True)

else:
    # 尚未點擊按鈕時的歡迎畫面
    st.info("👆 請選擇上方條件，開始規劃您的賞櫻之旅！")
    
    # 隨機展示幾個熱門景點
    st.markdown("### 🔥 本週熱門賞櫻點")
    cols = st.columns(2)
    hot_spots = [s for s in all_spots_db if "滿開" in s['status']][:6]
    for i, s in enumerate(hot_spots):
        with cols[i % 2]:
            st.markdown(f"""
<div style="background:white; padding:10px; border-radius:10px; margin-bottom:10px; border:1px solid #eee;">
<b>{s['name']}</b><br>
<span style="font-size:12px; color:#FF1493;">{s['status']}</span>
<span style="font-size:12px; color:#666;">{s['county']}</span>
</div>
""", unsafe_allow_html=True)

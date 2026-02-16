import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定
# ==========================================
st.set_page_config(
    page_title="2026 全國賞櫻環島地圖 (蘇佐璽嚴選版)",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (維持蘇區長粉色系風格)
# ==========================================
st.markdown("""
    <style>
    /* 全站基礎設定 */
    .stApp {
        background-color: #FFF0F5;
        font-family: "Microsoft JhengHei", sans-serif;
        color: #333333 !important;
    }
    p, div, span, h1, h2, h3, h4, h5, h6, label, .stMarkdown, .stText {
        color: #333333 !important;
    }

    /* 輸入元件修復 */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
        color: #333333 !important;
    }
    input { color: #333333 !important; }
    div[data-baseweb="select"] span { color: #333333 !important; }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; }
    li[data-baseweb="option"] { color: #333333 !important; }
    
    /* 隱藏官方元件 */
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 標題區 */
    .header-box {
        background: linear-gradient(135deg, #FF69B4 0%, #C71585 100%);
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
        margin-top: -60px;
    }
    .header-title { font-size: 28px; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.2); color: white !important; }
    .header-subtitle { font-size: 16px; margin-top: 5px; opacity: 0.9; color: white !important; }
    
    /* 輸入卡片 */
    .input-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #FFE4E1;
        margin-bottom: 20px;
    }
    
    /* 按鈕 */
    .stButton>button {
        width: 100%;
        background-color: #FF1493;
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 12px 0;
        font-weight: bold;
        transition: 0.3s;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #C71585;
    }
    
    /* 資訊看板 */
    .info-box {
        background-color: #fffbea;
        border-left: 5px solid #FFD700;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .weather-tag {
        font-weight: bold;
        color: #D48806 !important;
        font-size: 18px;
        margin-bottom: 5px;
    }
    
    /* 時間軸 */
    .timeline-item {
        border-left: 3px solid #FF69B4;
        padding-left: 20px;
        margin-bottom: 25px;
        position: relative;
    }
    .timeline-item::before {
        content: '🌸';
        position: absolute;
        left: -13px;
        top: 0;
        background: #FFF0F5;
        border-radius: 50%;
        font-size: 18px;
    }
    .day-header {
        background: #FFE4E1;
        color: #C71585 !important;
        padding: 8px 20px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 20px;
        margin-top: 10px;
        font-weight: bold;
        font-size: 16px;
    }
    .spot-title { font-weight: bold; color: #C71585 !important; font-size: 18px; }
    .spot-desc { font-size: 14px; color: #555 !important; margin-top: 3px; }
    .spot-tag { 
        font-size: 12px; background: #FFE4E1; color: #D87093 !important; 
        padding: 2px 8px; border-radius: 10px; margin-left: 8px; vertical-align: middle;
    }
    
    /* 桃園特別標記 */
    .taoyuan-badge {
        background: #9370DB; color: white !important; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-left: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (新增桃園重點與環島節點)
# ==========================================
all_spots_db = [
    # --- 桃園 (Taoyuan - Must Have) ---
    {"name": "拉拉山恩愛農場", "region": "北部", "zone": "深山絕景", "month": [2, 3], "type": "賞花", "flower": "千島櫻/富士櫻", "fee": "門票$100", "desc": "【蘇區長力推】桃園復興最高點，櫻花與雲海共舞。"},
    {"name": "復興區角板山行館", "region": "北部", "zone": "市區近郊", "month": [1, 2], "type": "健行", "flower": "梅花/山櫻", "fee": "免門票", "desc": "【蘇區長力推】北橫最美歷史行館，賞花兼遊湖。"},
    {"name": "東眼山森林遊樂區", "region": "北部", "zone": "市區近郊", "month": [2, 3], "type": "健行", "flower": "山櫻花", "fee": "門票$80", "desc": "【蘇區長力推】漫步柳杉林，尋找粉紅驚喜。"},
    {"name": "中巴陵櫻木花道", "region": "北部", "zone": "深山絕景", "month": [2], "type": "秘境", "flower": "昭和櫻", "fee": "免門票", "desc": "北橫公路上的粉紅隧道，攝影師最愛。"},

    # --- 北部 (Other North) ---
    {"name": "淡水天元宮", "region": "北部", "zone": "市區近郊", "month": [2, 3], "type": "網美", "flower": "吉野櫻", "fee": "免門票", "desc": "天壇與夜櫻的絕美構圖。"},
    {"name": "司馬庫斯", "region": "北部", "zone": "深山絕景", "month": [2], "type": "秘境", "flower": "昭和櫻", "fee": "需預約", "desc": "上帝的部落，全台最難抵達的粉紅仙境。"},

    # --- 中部 (Central) ---
    {"name": "武陵農場", "region": "中部", "zone": "深山絕景", "month": [2], "type": "賞花", "flower": "紅粉佳人", "fee": "門票$160", "desc": "台灣賞櫻首選，綿延三公里的粉紅隧道。"},
    {"name": "福壽山農場", "region": "中部", "zone": "深山絕景", "month": [2, 3], "type": "賞花", "flower": "千島櫻", "fee": "門票$100", "desc": "全台最高海拔櫻花園，偽出國感最強。"},
    {"name": "九族文化村", "region": "中部", "zone": "市區近郊", "month": [2, 3], "type": "樂園", "flower": "八重櫻", "fee": "門票$900", "desc": "日本認證賞櫻名所，夜櫻必看。"},
    {"name": "后里泰安派出所", "region": "中部", "zone": "市區近郊", "month": [2], "type": "兜風", "flower": "八重櫻", "fee": "免門票", "desc": "全台最美派出所，平地賞櫻首選。"},

    # --- 南部 (South) ---
    {"name": "阿里山國家森林", "region": "南部", "zone": "深山絕景", "month": [3, 4], "type": "賞花", "flower": "吉野櫻(櫻王)", "fee": "門票$200", "desc": "小火車穿梭櫻花林，經典中的經典。"},
    {"name": "石棹櫻花道", "region": "南部", "zone": "深山絕景", "month": [2, 3], "type": "攝影", "flower": "昭和櫻", "fee": "免門票", "desc": "琉璃光與櫻花夜景。"},
    {"name": "寶山二集團", "region": "南部", "zone": "市區近郊", "month": [1, 2], "type": "健行", "flower": "河津櫻", "fee": "免門票", "desc": "高雄桃源區，南部最早盛開的粉紅花海。"},
    {"name": "霧台櫻花王", "region": "南部", "zone": "深山絕景", "month": [2], "type": "部落", "flower": "山櫻花", "fee": "清潔費", "desc": "魯凱族部落，30年樹齡的櫻花傳奇。"},

    # --- 東部 (East) ---
    {"name": "太麻里金針山", "region": "東部", "zone": "深山絕景", "month": [1, 2, 3], "type": "健行", "flower": "山櫻", "fee": "免門票", "desc": "雲霧繚繞的東部後花園。"},
    {"name": "花蓮玉山神學院", "region": "東部", "zone": "市區近郊", "month": [2, 3], "type": "賞花", "flower": "霧社櫻", "fee": "免門票", "desc": "鯉魚潭旁，俯瞰湖光山色。"},
    {"name": "宜蘭大同櫻花林", "region": "東部", "zone": "市區近郊", "month": [2], "type": "兜風", "flower": "八重櫻", "fee": "免門票", "desc": "台7甲線沿路，通往武陵的前哨站。"}
]

# ==========================================
# 4. 邏輯核心：環島行程生成器
# ==========================================
def generate_itinerary(travel_date, days_option, group, target_region):
    m = travel_date.month
    
    # 提取天數數字
    if "5日" in days_option: total_days = 5
    elif "7日" in days_option: total_days = 7
    elif "10日" in days_option: total_days = 10
    elif "一日" in days_option: total_days = 1
    elif "二日" in days_option: total_days = 2
    else: total_days = 3

    itinerary = {}
    
    # === 模式 A: 環島模式 (Round Island) ===
    if target_region == "🌸 全臺環島 (蘇區長特推)":
        # 邏輯：強制包含桃園，並依序分配 北->中->南->東
        
        # 1. Day 1: 桃園 (Taoyuan Must)
        taoyuan_spots = [s for s in all_spots_db if "復興" in s['name'] or "拉拉山" in s['name'] or "東眼山" in s['name']]
        # 確保該月份有花，若無則選角板山(最保險)
        valid_taoyuan = [s for s in taoyuan_spots if m in s['month']]
        d1_spot1 = valid_taoyuan[0] if valid_taoyuan else taoyuan_spots[1] # 預設角板山
        d1_spot2 = [s for s in taoyuan_spots if s['name'] != d1_spot1['name']][0]
        
        itinerary[1] = [d1_spot1, d1_spot2]
        
        # 2. 其餘天數分配
        # 獲取各地區有效景點
        central = [s for s in all_spots_db if s['region'] == "中部" and m in s['month']]
        south = [s for s in all_spots_db if

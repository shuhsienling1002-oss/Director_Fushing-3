import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定 (改為 Centered 適合手機閱讀)
# ==========================================
st.set_page_config(
    page_title="2026 全國賞櫻地圖 (蘇佐璽嚴選)",
    page_icon="🌸",
    layout="centered", # 手機版推薦用置中單欄
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (手機版優化 + 粉色系)
# ==========================================
st.markdown("""
    <style>
    /* 全站基礎設定 */
    .stApp {
        background-color: #FFF0F5;
        font-family: "Microsoft JhengHei", sans-serif;
        color: #333333 !important;
    }
    
    /* 隱藏漢堡選單與Footer (讓它更像原生App) */
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 輸入元件優化 (手機好點擊) */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
        color: #333333 !important;
        min-height: 45px; /* 加大點擊區域 */
    }
    input { color: #333333 !important; }
    
    /* 標題區 (RWD自適應) */
    .header-box {
        background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%);
        padding: 25px 15px;
        border-radius: 0 0 25px 25px;
        color: white !important;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(255, 20, 147, 0.3);
        margin-top: -60px; /* 頂部滿版 */
    }
    .header-title { 
        font-size: 26px; 
        font-weight: bold; 
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2); 
        color: white !important; 
    }
    
    /* 輸入卡片 (手機版浮動卡片) */
    .input-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #FFC0CB;
        margin-bottom: 20px;
    }
    
    /* 生成按鈕 (滿寬大按鈕) */
    .stButton>button {
        width: 100%;
        background-color: #C71585;
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 15px 0;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 4px 10px rgba(199, 21, 133, 0.4);
        transition: 0.2s;
    }
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    /* 行程卡片 */
    .day-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 6px solid #FF69B4;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .spot-title {
        font-weight: bold;
        color: #C71585;
        font-size: 18px;
    }
    
    /* 標籤 */
    .tag {
        font-size: 12px; 
        padding: 2px 6px; 
        border-radius: 4px; 
        background: #EEE; 
        color: #555;
        margin-right: 5px;
    }
    .tag-hot { background: #FF4500; color: white; }
    .tag-tao { background: #9370DB; color: white; }
    
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (50+ 終極版)
# ==========================================
# zone: 市區/郊區/深山 (影響行程邏輯)
all_spots_db = [
    # === 👑 桃園復興區 (Must Have) ===
    {"name": "拉拉山恩愛農場", "region": "北部", "zone": "深山", "month": [2, 3], "flower": "千島櫻", "desc": "粉紅櫻花與雲海同框的夢幻大景。"},
    {"name": "中巴陵櫻木花道", "region": "北部", "zone": "深山", "month": [2], "flower": "昭和櫻", "desc": "北橫公路旁最美的粉紅隧道。"},
    {"name": "角板山行館", "region": "北部", "zone": "郊區", "month": [1, 2], "flower": "梅花/山櫻", "desc": "賞花還能逛戰備隧道，適合全家出遊。"},
    {"name": "東眼山森林遊樂區", "region": "北部", "zone": "郊區", "month": [2, 3], "flower": "山櫻花", "desc": "漫步在柳杉林中的粉紅驚喜。"},
    {"name": "壽山巖觀音寺", "region": "北部", "zone": "市區", "month": [2], "flower": "寒櫻", "desc": "桃園市區最近的賞櫻名所。"},

    # === 北部 ===
    {"name": "淡水天元宮", "region": "北部", "zone": "郊區", "month": [2, 3], "flower": "吉野櫻", "desc": "無極真元天壇與櫻花交織。"},
    {"name": "陽明山平菁街", "region": "北部", "zone": "郊區", "month": [1, 2], "flower": "寒櫻", "desc": "台北第一波櫻花，圍牆探出的粉紅花海。"},
    {"name": "三峽大熊櫻花林", "region": "北部", "zone": "郊區", "month": [1, 2, 3], "flower": "三色櫻", "desc": "4000棵櫻花染紅山頭，夜櫻超美。"},
    {"name": "司馬庫斯", "region": "北部", "zone": "深山", "month": [2], "flower": "昭和櫻", "desc": "上帝的部落，一生必去的粉紅仙境。"},
    {"name": "新竹公園", "region": "北部", "zone": "市區", "month": [2], "flower": "河津櫻", "desc": "玻璃工藝博物館旁的日式櫻花。"},
    {"name": "觀霧山莊", "region": "北部", "zone": "深山", "month": [3], "flower": "霧社櫻", "desc": "全台最大霧社櫻王，滿樹雪白。"},
    {"name": "內湖樂活公園", "region": "北部", "zone": "市區", "month": [2], "flower": "寒櫻", "desc": "搭捷運就能到，夜櫻非常浪漫。"},
    {"name": "中正紀念堂", "region": "北部", "zone": "市區", "month": [2, 3], "flower": "大漁櫻", "desc": "市中心最方便的賞櫻點。"},

    # === 中部 ===
    {"name": "武陵農場", "region": "中部", "zone": "深山", "month": [2], "flower": "紅粉佳人", "desc": "台灣賞櫻的代名詞，綿延三公里。"},
    {"name": "福壽山農場", "region": "中部", "zone": "深山", "month": [2, 3], "flower": "千島櫻", "desc": "全台最高海拔櫻花園。"},
    {"name": "后里泰安派出所", "region": "中部", "zone": "市區", "month": [2], "flower": "八重櫻", "desc": "全台最美派出所，平地賞櫻首選。"},
    {"name": "九族文化村", "region": "中部", "zone": "郊區", "month": [2], "flower": "八重櫻", "desc": "日本認證賞櫻名所，夜櫻祭必看。"},
    {"name": "草嶺石壁", "region": "中部", "zone": "深山", "month": [2, 3], "flower": "白花山櫻", "desc": "全台極罕見的白色山櫻花秘境。"},
    {"name": "暨南大學", "region": "中部", "zone": "市區", "month": [2], "flower": "山櫻", "desc": "全台最美校園櫻花季，適合野餐。"},
    {"name": "奧萬大", "region": "中部", "zone": "深山", "month": [1, 2, 3], "flower": "霧社櫻", "desc": "春天的奧萬大是櫻花與鳥類天堂。"},
    {"name": "新社櫻木花道", "region": "中部", "zone": "郊區", "month": [2], "flower": "八重櫻", "desc": "區公所旁的粉紅街道。"},

    # === 南部 ===
    {"name": "阿里山森林遊樂區", "region": "南部", "zone": "深山", "month": [3, 4], "flower": "吉野櫻", "desc": "小火車穿梭櫻花林，世界級景觀。"},
    {"name": "隙頂石棹", "region": "南部", "zone": "深山", "month": [2, 3], "flower": "昭和櫻", "desc": "琉璃光與櫻花夜景。"},
    {"name": "寒溪呢", "region": "南部", "zone": "深山", "month": [1, 2], "flower": "福爾摩沙櫻", "desc": "周子瑜也去過的白色櫻花隧道。"},
    {"name": "寶山二集團", "region": "南部", "zone": "郊區", "month": [1, 2], "flower": "河津櫻", "desc": "高雄最早盛開的粉紅花海。"},
    {"name": "霧台櫻花王", "region": "南部", "zone": "深山", "month": [2], "flower": "山櫻", "desc": "一棵樹就開滿整個庭院，魯凱族傳奇。"},
    {"name": "烏山頭水庫", "region": "南部", "zone": "市區", "month": [3], "flower": "南洋櫻", "desc": "香榭大道，粉紅花瓣飄落如下雪。"},
    {"name": "藤枝森林遊樂區", "region": "南部", "zone": "深山", "month": [1, 2], "flower": "山櫻", "desc": "南部小溪頭，森濤中的櫻花。"},

    # === 東部 ===
    {"name": "宜蘭大同櫻花林", "region": "東部", "zone": "郊區", "month": [2], "flower": "八重櫻", "desc": "台7甲線沿路都是櫻花。"},
    {"name": "明池森林遊樂區", "region": "東部", "zone": "深山", "month": [2, 3], "flower": "大島櫻", "desc": "高山湖泊與櫻花的空靈之美。"},
    {"name": "太麻里金針山", "region": "東部", "zone": "深山", "month": [1, 2], "flower": "山櫻", "desc": "雲霧繚繞的東部後花園。"},
    {"name": "羅莊櫻花步道", "region": "東部", "zone": "市區", "month": [2, 3], "flower": "墨染櫻", "desc": "平地最美櫻花河岸，倒影迷人。"},
    {"name": "玉山神學院", "region": "東部", "zone": "郊區", "month": [2, 3], "flower": "霧社櫻", "desc": "俯瞰鯉魚潭，白色櫻花配湖光山色。"}
]

# ==========================================
# 4. 核心邏輯：AI 行程生成器
# ==========================================
def generate_itinerary(travel_date, days_option, group, target_region):
    m = travel_date.month
    
    # 1. 處理天數
    if "5日" in days_option: total_days = 5
    elif "7日" in days_option: total_days = 7
    elif "10日" in days_option: total_days = 10
    elif "一日" in days_option: total_days = 1
    elif "二日" in days_option: total_days = 2
    else: total_days = 3

    itinerary = {}
    
    # 2. 篩選可用景點
    if target_region == "🌸 全臺環島 (蘇區長特推)":
        candidates = [s for s in all_spots_db if m in s['month']]
        pool = candidates
    else:
        # 單一地區
        candidates = [s for s in all_spots_db if s['region'] == target_region and m in s['month']]
        pool = candidates
        
        # 桃園強制置頂 (北部時)
        if target_region == "北部":
             taoyuan_must = [s for s in all_spots_db if ("拉拉山" in s['name'] or "角板山" in s['name']) and m in s['month']]
             for t in taoyuan_must:
                 if t not in pool: pool.insert(0, t)

    if not pool:
        pool = [s for s in all_spots_db if s['region'] == target_region][:3] # 防呆

    # 3. 排程邏輯 (簡單輪播)
    for d in range(1, total_days + 1):
        if d == 1 and target_region in ["北部", "🌸 全臺環島 (蘇區長特推)"]:
             # Day 1 桃園優先
             taoyuan_available = [s for s in pool if "桃園" in s['name'] or "拉拉山" in s['name'] or "角板山" in s['name']]
             if taoyuan_available:
                 s1 = taoyuan_available[0]
                 s2 = taoyuan_available[1] if len(taoyuan_available) > 1 else (pool[0] if pool[0]!=s1 else pool[1])
             else:
                 s1 = pool[0]; s2 = pool[1] if len(pool)>1 else pool[0]
        else:
            idx1 = (d * 2) % len(pool)
            idx2 = (d * 2 + 1) % len(pool)
            s1 = pool[idx1]
            s2 = pool[idx2]
            
        itinerary[d] = [s1, s2]

    return itinerary

# ==========================================
# 5. UI 呈現 (Mobile First Design)
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌸 2026 全國賞櫻地圖</div>
        <div style="color:white; opacity:0.9; margin-top:5px; font-size:14px;">
            復興區長 <b>蘇佐璽</b> 嚴選．手機版 ❤️
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 1. 輸入區 (手機版浮動卡片) ---
st.markdown('<div class="input-card">', unsafe_allow_html=True)

# 第一行：地區
c1, c2 = st.columns([2, 1])
with c1:
    target_region = st.selectbox("📍 想去哪裡？", ["🌸 全臺環島 (蘇區長特推)", "北部", "中部", "南部", "東部"])
with c2:
    days = st.selectbox("📅 天數", ["一日遊", "二日遊", "三日遊", "5日遊", "7日遊", "10日遊"])

# 第二行：日期與夥伴
c3, c4 = st.columns(2)
with c3:
    travel_date = st.date_input("🗓 出發日", value=date(2026, 2, 20))
with c4:
    group = st.selectbox("👥 夥伴", ["情侶", "親子", "長輩", "獨旅"])

# 按鈕
run_btn = st.button("🚀 生成推薦行程")

st.markdown('</div>', unsafe_allow_html=True)

# --- 2. 結果區 (Tabs) ---
tab1, tab2 = st.tabs(["🗺️ 我的行程", "📚 景點總表"])

# Tab 1: AI 行程
with tab1:
    if run_btn:
        itinerary = generate_itinerary(travel_date, days, group, target_region)
        st.success(f"已為您規劃：{target_region} {days}！")
        
        for d, spots in itinerary.items():
            s1, s2 = spots[0], spots[1]
            
            # 徽章邏輯
            t1 = '<span class="tag tag-tao">蘇區長推</span>' if "拉拉山" in s1['name'] or "角板山" in s1['name'] else ('<span class="tag tag-hot">熱門</span>' if s1['zone']=="深山" else "")
            t2 = '<span class="tag tag-tao">蘇區長推</span>' if "拉拉山" in s2['name'] or "角板山" in s2['name'] else ('<span class="tag tag-hot">熱門</span>' if s2['zone']=="深山" else "")

            st.markdown(f"""
            <div class="day-card">
                <div style="font-size:20px; font-weight:bold; color:#333; margin-bottom:10px;">🗓️ Day {d}</div>
                
                <div style="margin-bottom:15px;">
                    <div class="spot-title">09:00 {s1['name']} {t1}</div>
                    <div style="color:#666; font-size:14px; margin-left:5px;">🌸 {s1['flower']} | {s1['desc']}</div>
                </div>
                
                <div style="background:#FFF0F5; padding:8px; border-radius:5px; font-size:13px; color:#C71585; margin-bottom:15px;">
                    🍱 午餐：{("山上原民風味餐" if s1['zone']=="深山" else "在地人氣美食")}
                </div>

                <div style="margin-bottom:15px;">
                    <div class="spot-title">14:30 {s2['name']} {t2}</div>
                    <div style="color:#666; font-size:14px; margin-left:5px;">🌸 {s2['flower']} | {s2['desc']}</div>
                </div>

                <hr style="border-top:1px dashed #FFB6C1;">
                <div style="font-size:14px; color:#555;">
                    🛏️ <b>住宿</b>：{("優質民宿或農場" if s2['zone']=="深山" else "市區飯店商旅")}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👆 請點擊上方 **「生成推薦行程」** 按鈕開始規劃！")

# Tab 2: 景點總表 (手機版列表)
with tab2:
    filter_reg_list = st.selectbox("🌏 篩選地區", ["全部", "北部", "中部", "南部", "東部"])
    
    filtered_list = [s for s in all_spots_db if filter_reg_list == "全部" or s['region'] == filter_reg_list]
    
    for spot in filtered_list:
        badge = '<span class="tag tag-tao">蘇區長推</span>' if "拉拉山" in spot['name'] or "角板山" in spot['name'] else ""
        
        st.markdown(f"""
        <div style="background:white; padding:15px; border-bottom:1px solid #eee;">
            <div style="font-weight:bold; font-size:16px; color:#333;">{spot['name']} {badge}</div>
            <div style="font-size:13px; color:#999; margin:3px 0;">📍 {spot['region']} {spot['zone']} | 🌸 {spot['flower']}</div>
            <div style="font-size:14px; color:#555;">{spot['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

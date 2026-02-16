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
    
    /* 新增：秘境標記 */
    .secret-badge {
        background: #FF4500; color: white !important; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-left: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (擴充秘境版)
# ==========================================
all_spots_db = [
    # --- 桃園 (Taoyuan - Must Have) ---
    {"name": "拉拉山恩愛農場", "region": "北部", "zone": "深山絕景", "month": [2, 3], "type": "賞花", "flower": "千島櫻/富士櫻", "fee": "門票$100", "desc": "【蘇區長力推】桃園復興最高點，櫻花與雲海共舞。"},
    {"name": "復興區角板山行館", "region": "北部", "zone": "市區近郊", "month": [1, 2], "type": "健行", "flower": "梅花/山櫻", "fee": "免門票", "desc": "【蘇區長力推】北橫最美歷史行館，賞花兼遊湖。"},
    {"name": "東眼山森林遊樂區", "region": "北部", "zone": "市區近郊", "month": [2, 3], "type": "健行", "flower": "山櫻花", "fee": "門票$80", "desc": "【蘇區長力推】漫步柳杉林，尋找粉紅驚喜。"},
    {"name": "中巴陵櫻木花道", "region": "北部", "zone": "深山絕景", "month": [2], "type": "秘境", "flower": "昭和櫻", "fee": "免門票", "desc": "北橫公路上的粉紅隧道，攝影師最愛。"},

    # --- 北部 (Other North) ---
    {"name": "三峽大熊櫻花林", "region": "北部", "zone": "市區近郊", "month": [1, 2, 3], "type": "網美", "flower": "三色櫻/八重櫻", "fee": "門票$250", "desc": "【新北必去】4000棵櫻花林，夜櫻拍攝聖地。"},
    {"name": "淡水天元宮", "region": "北部", "zone": "市區近郊", "month": [2, 3], "type": "網美", "flower": "吉野櫻", "fee": "免門票", "desc": "天壇與夜櫻的絕美構圖。"},
    {"name": "司馬庫斯", "region": "北部", "zone": "深山絕景", "month": [2], "type": "秘境", "flower": "昭和櫻", "fee": "需預約", "desc": "上帝的部落，全台最難抵達的粉紅仙境。"},
    {"name": "新竹觀霧山莊", "region": "北部", "zone": "深山絕景", "month": [3], "type": "秘境", "flower": "霧社櫻王", "fee": "免門票", "desc": "【雪霸秘境】全台最大霧社櫻王，雪白如雲。"},

    # --- 中部 (Central) ---
    {"name": "武陵農場", "region": "中部", "zone": "深山絕景", "month": [2], "type": "賞花", "flower": "紅粉佳人", "fee": "門票$160", "desc": "台灣賞櫻首選，綿延三公里的粉紅隧道。"},
    {"name": "福壽山農場", "region": "中部", "zone": "深山絕景", "month": [2, 3], "type": "賞花", "flower": "千島櫻", "fee": "門票$100", "desc": "全台最高海拔櫻花園，偽出國感最強。"},
    {"name": "雲林草嶺石壁", "region": "中部", "zone": "深山絕景", "month": [2, 3], "type": "秘境", "flower": "白花山櫻/杏花", "fee": "免門票", "desc": "【近年爆紅】全台絕無僅有的白色山櫻花秘境。"},
    {"name": "九族文化村", "region": "中部", "zone": "市區近郊", "month": [2, 3], "type": "樂園", "flower": "八重櫻", "fee": "門票$900", "desc": "日本認證賞櫻名所，夜櫻必看。"},
    {"name": "后里泰安派出所", "region": "中部", "zone": "市區近郊", "month": [2], "type": "兜風", "flower": "八重櫻", "fee": "免門票", "desc": "全台最美派出所，平地賞櫻首選。"},

    # --- 南部 (South) ---
    {"name": "阿里山國家森林", "region": "南部", "zone": "深山絕景", "month": [3, 4], "type": "賞花", "flower": "吉野櫻(櫻王)", "fee": "門票$200", "desc": "小火車穿梭櫻花林，經典中的經典。"},
    {"name": "石棹櫻花道", "region": "南部", "zone": "深山絕景", "month": [2, 3], "type": "攝影", "flower": "昭和櫻", "fee": "免門票", "desc": "琉璃光與櫻花夜景。"},
    {"name": "高雄藤枝森林遊樂區", "region": "南部", "zone": "深山絕景", "month": [1, 2], "type": "健行", "flower": "山櫻花", "fee": "門票$120", "desc": "【南部小溪頭】森濤與櫻花的合奏。"},
    {"name": "寶山二集團", "region": "南部", "zone": "市區近郊", "month": [1, 2], "type": "健行", "flower": "河津櫻", "fee": "免門票", "desc": "高雄桃源區，南部最早盛開的粉紅花海。"},
    {"name": "霧台櫻花王", "region": "南部", "zone": "深山絕景", "month": [2], "type": "部落", "flower": "山櫻花", "fee": "清潔費", "desc": "魯凱族部落，30年樹齡的櫻花傳奇。"},

    # --- 東部 (East) ---
    {"name": "宜蘭明池森林遊樂區", "region": "東部", "zone": "深山絕景", "month": [2, 3], "type": "景觀", "flower": "大島櫻/山櫻", "fee": "門票$120", "desc": "【北橫明珠】高山湖泊與櫻花的空靈之美。"},
    {"name": "太麻里金針山", "region": "東部", "zone": "深山絕景", "month": [1, 2, 3], "type": "健行", "flower": "山櫻", "fee": "免門票", "desc": "雲霧繚繞的東部後花園。"},
    {"name": "花蓮玉山神學院", "region": "東部", "zone": "市區近郊", "month": [2, 3], "type": "賞花", "flower": "霧社櫻", "fee": "免門票", "desc": "鯉魚潭旁，俯瞰湖光山色。"},
    {"name": "宜蘭大同櫻花林", "region": "東部", "zone": "市區近郊", "month": [2], "type": "兜風", "flower": "八重櫻", "fee": "免門票", "desc": "台7甲線沿路，通往武陵的前哨站。"}
]

# ==========================================
# 4. 邏輯核心：環島行程生成器
# ==========================================
def generate_itinerary(travel_date, days_option, group, target_region):
    m = travel_date.month
    
    # 提取天數數字 (Robust parsing)
    if "5日" in days_option: total_days = 5
    elif "7日" in days_option: total_days = 7
    elif "10日" in days_option: total_days = 10
    elif "一日" in days_option: total_days = 1
    elif "二日" in days_option: total_days = 2
    else: total_days = 3

    itinerary = {}
    
    # === 模式 A: 環島模式 (Round Island) ===
    if target_region == "🌸 全臺環島 (蘇區長特推)":
        # 1. Day 1: 桃園 (Taoyuan Must)
        taoyuan_spots = [s for s in all_spots_db if "復興" in s['name'] or "拉拉山" in s['name'] or "東眼山" in s['name']]
        # 確保該月份有花，若無則選角板山(最保險)
        valid_taoyuan = [s for s in taoyuan_spots if m in s['month']]
        
        if not valid_taoyuan:
            d1_spot1 = taoyuan_spots[1] # 預設角板山
        else:
            d1_spot1 = valid_taoyuan[0]
            
        remaining_taoyuan = [s for s in taoyuan_spots if s['name'] != d1_spot1['name']]
        d1_spot2 = remaining_taoyuan[0] if remaining_taoyuan else d1_spot1
        
        itinerary[1] = [d1_spot1, d1_spot2]
        
        # 2. 其餘天數分配
        central = [s for s in all_spots_db if s['region'] == "中部" and m in s['month']]
        south = [s for s in all_spots_db if s['region'] == "南部" and m in s['month']]
        east = [s for s in all_spots_db if s['region'] == "東部" and m in s['month']]
        north_others = [s for s in all_spots_db if s['region'] == "北部" and "復興" not in s['name'] and m in s['month']]
        
        # 補充清單 (防呆)
        if not central: central = [s for s in all_spots_db if s['region'] == "中部"][:2]
        if not south: south = [s for s in all_spots_db if s['region'] == "南部"][:2]
        if not east: east = [s for s in all_spots_db if s['region'] == "東部"][:2]
        
        # 動態填入 (根據天數延展)
        current_day = 2
        
        # Day 2-3: 中部
        if current_day <= total_days:
            # 優先推薦草嶺石壁(如果有花)
            if any("草嶺" in s['name'] for s in central):
                c_spot = next(s for s in central if "草嶺" in s['name'])
                itinerary[current_day] = [c_spot, central[0] if central[0]!=c_spot else central[1]]
            else:
                itinerary[current_day] = [central[0], central[1] if len(central)>1 else central[0]]
            current_day += 1
            
        if total_days >= 5 and current_day <= total_days:
             s_extra = central[-1] if len(central) > 2 else {"name": "清境農場", "region": "中部", "zone": "順遊", "desc": "雲端上的綿羊城堡", "flower": "草原"}
             itinerary[current_day] = [s_extra, {"name": "日月潭環湖", "region": "中部", "zone": "順遊", "desc": "全球最美自行車道", "flower": "湖景"}]
             current_day += 1
             
        # Day 4-5: 南部
        if current_day <= total_days:
            itinerary[current_day] = [south[0], south[1] if len(south)>1 else south[0]]
            current_day += 1
        if total_days >= 7 and current_day <= total_days:
             s_extra_s = south[-1] if len(south) > 2 else {"name": "台南赤崁樓", "region": "南部", "zone": "順遊", "desc": "古蹟美食巡禮", "flower": "人文"}
             itinerary[current_day] = [s_extra_s, {"name": "高雄駁二", "region": "南部", "zone": "順遊", "desc": "港都藝術特區", "flower": "海景"}]
             current_day += 1

        # Day 6-7: 東部
        if current_day <= total_days:
            itinerary[current_day] = [east[0], east[1] if len(east)>1 else east[0]]
            current_day += 1
        if total_days >= 7 and current_day <= total_days:
             s_extra_e = east[-1] if len(east) > 2 else {"name": "花東縱谷", "region": "東部", "zone": "順遊", "desc": "縱谷花海畫布", "flower": "油菜花"}
             itinerary[current_day] = [s_extra_e, {"name": "池上伯朗大道", "region": "東部", "zone": "順遊", "desc": "金城武樹下乘涼", "flower": "稻浪"}]
             current_day += 1
             
        # Day 8+: 回北部/收尾
        while current_day <= total_days:
            leftover = north_others if north_others else taoyuan_spots
            s_end = leftover[0] if leftover else {"name": "台北101", "region": "北部", "desc": "都會繁華", "flower": "夜景"}
            itinerary[current_day] = [s_end, {"name": "快樂賦歸", "region": "全台", "zone": "市區", "desc": "購買伴手禮", "flower": "回憶"}]
            current_day += 1

        title = f"🌸 {total_days}天環島賞櫻大縱走 (桃園出發)"

    # === 模式 B: 單一區域深度遊 ===
    else:
        # 篩選邏輯
        region_spots = [s for s in all_spots_db if s['region'] == target_region]
        available_spots = [s for s in region_spots if m in s['month']]
        if not available_spots: available_spots = region_spots[:3]
        
        # 確保若選北部，桃園一定在其中
        if target_region == "北部":
             taoyuan_must = [s for s in all_spots_db if "復興" in s['name'] or "拉拉山" in s['name']]
             for t in taoyuan_must:
                 is_in_list = any(s['name'] == t['name'] for s in available_spots)
                 if not is_in_list and m in t['month']:
                     available_spots.insert(0, t)

        # 簡單分配
        for d in range(1, total_days + 1):
            idx1 = (d - 1) * 2 % len(available_spots)
            idx2 = ((d - 1) * 2 + 1) % len(available_spots)
            
            s1 = available_spots[idx1]
            s2 = available_spots[idx2]
            
            # 若天數很多，避免景點重複
            if d > 3 and s1['name'] == available_spots[0]['name']:
                s1 = {"name": f"{target_region}私房秘境", "region": target_region, "zone": "秘境", "desc": "在地人推薦的隱藏版", "flower": "驚喜"}
            
            itinerary[d] = [s1, s2]

        title = f"🌸 {target_region} {total_days}日深度賞櫻"

    return title, itinerary

# ==========================================
# 5. 頁面內容 (UI)
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌸 2026 全國賞櫻環島地圖</div>
        <div class="header-subtitle">復興區長 <b>蘇佐璽</b> 嚴選．桃園出發．遊遍全臺 ❤️</div>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        # 地區選擇：包含環島選項
        target_region = st.selectbox(
            "想去哪裡賞櫻？", 
            ["🌸 全臺環島 (蘇區長特推)", "北部", "中部", "南部", "東部"]
        )
        travel_date = st.date_input("預計出發日期", value=date(2026, 2, 20), min_value=date(2026, 1, 1), max_value=date(2026, 4, 30))
    with col2:
        # 天數選擇：包含長天數
        days_options = ["5日遊 (半島精華)", "7日遊 (全島大縱走)", "10日遊 (慢活深度)", "一日遊 (快閃)", "二日遊 (輕旅)", "三日遊 (經典)"]
        days = st.selectbox("行程天數", days_options)
        group = st.selectbox("出遊夥伴", ["情侶/夫妻", "親子家庭", "長輩樂齡", "熱血獨旅"])
    
    generate_btn = st.button("🚀 生成蘇區長推薦行程")
    st.markdown('</div>', unsafe_allow_html=True)

if generate_btn:
    status_title, itinerary = generate_itinerary(travel_date, days, group, target_region)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="weather-tag">{status_title}</div>
        <div>根據您選擇的 <b>{days}</b>，蘇區長為 <b>{group}</b> 規劃了包含 <b>桃園復興區</b> 在內的最佳賞花路徑。</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🗓️ 每日行程細節", "💰 預算與住宿", "🚗 交通建議"])

    # --- Tab 1: 動態行程 ---
    with tab1:
        for day_num, spots in itinerary.items():
            st.markdown(f'<div class="day-header">Day {day_num}</div>', unsafe_allow_html=True)
            
            # 第一個景點
            s1 = spots[0]
            # 判斷標記
            badge = ""
            if "復興" in s1['name'] or "拉拉山" in s1['name']:
                badge = '<span class="taoyuan-badge">蘇區長大推</span>'
            elif "秘境" in s1.get('desc', '') or "爆紅" in s1.get('desc', ''):
                badge = '<span class="secret-badge">隱藏版</span>'
            
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">09:00 {s1['name']} {badge} <span class="spot-tag">{s1.get('zone','')}</span></div>
                <div class="spot-desc">{s1['desc']} ({s1.get('flower','')})</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 午餐
            lunch_loc = "復興區原民風味餐" if "復興" in s1['name'] else "當地特色美食"
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">12:30 午餐時間</div>
                <div class="spot-desc">推薦品嚐：{lunch_loc}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 第二個景點
            s2 = spots[1]
            badge2 = ""
            if "復興" in s2['name'] or "拉拉山" in s2['name']:
                badge2 = '<span class="taoyuan-badge">蘇區長大推</span>'
            elif "秘境" in s2.get('desc', '') or "爆紅" in s2.get('desc', ''):
                badge2 = '<span class="secret-badge">隱藏版</span>'
            
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">14:30 {s2['name']} {badge2} <span class="spot-tag">{s2.get('zone','')}</span></div>
                <div class="spot-desc">{s2['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 住宿建議
            region_stay = s2.get('region', target_region)
            if region_stay == "全台": region_stay = "溫暖的家"
            
            st.markdown(f"""
            <div class="timeline-item" style="border-color:#9370DB;">
                <div class="spot-title" style="color:#9370DB !important;">18:00 夜宿：{region_stay}</div>
                <div class="spot-desc">建議選擇該區域特色民宿或飯店。</div>
            </div>
            """, unsafe_allow_html=True)

    # --- Tab 2: 預算 ---
    with tab2:
        days_num = len(itinerary)
        est_cost = days_num * 3500 # 概抓每天花費
        st.subheader(f"💵 {days} 預算預估")
        st.metric("每人預估費用 (含食宿行)", f"NT$ {est_cost:,}")
        st.info("💡 蘇區長貼心提醒：環島長天數行程建議提早預訂「拉拉山」與「武陵農場」的住宿，通常需半年前搶訂！")

    # --- Tab 3: 交通 ---
    with tab3:
        st.subheader("🚗 環島交通策略")
        if target_region == "🌸 全臺環島 (蘇區長特推)":
            st.success("**建議逆時針環島**：桃園出發 -> 新竹 -> 台中 -> 高雄 -> 台東 -> 花蓮 -> 宜蘭 -> 台北。")
            st.warning("⚠️ **北橫公路 (台7線)**：若要從桃園復興直接前往宜蘭，請務必先查詢路況，櫻花季期間車流量大且偶有管制。")
        else:
            st.info(f"前往 **{target_region}** 建議搭乘高鐵至主要城市後租車，機動性最高。")

else:
    st.info("👆 請在上方選擇「全臺環島」並設定天數 (5-10天)，開始您的粉紅大冒險！")

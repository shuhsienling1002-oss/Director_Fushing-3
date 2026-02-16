import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定 (System Config)
# ==========================================
st.set_page_config(
    page_title="2026 全國賞櫻地圖 (蘇佐璽嚴選版)",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (完全繼承原版設計)
# ==========================================
st.markdown("""
    <style>
    /* 1. 強制全站背景為粉色，字體為深色 */
    .stApp {
        background-color: #FFF0F5;
        font-family: "Microsoft JhengHei", sans-serif;
        color: #333333 !important;
    }
    
    /* 2. 強制所有一般文字元素為深色 */
    p, div, span, h1, h2, h3, h4, h5, h6, label, .stMarkdown {
        color: #333333 !important;
    }

    /* === 3. 核心修復：強制輸入框與選單在深色模式下維持「白底黑字」 === */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important; /* 強制白底 */
        border: 1px solid #cccccc !important;
        color: #333333 !important; /* 強制黑字 */
    }
    
    input { color: #333333 !important; }
    div[data-baseweb="select"] span { color: #333333 !important; }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; }
    li[data-baseweb="option"] { color: #333333 !important; }
    svg { fill: #333333 !important; color: #333333 !important; }

    /* 隱藏官方元件 */
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 標題區 */
    .header-box {
        background: linear-gradient(135deg, #FF69B4 0%, #FFB7C5 100%);
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
        margin-top: -60px;
    }
    .header-box h1, .header-box div, .header-box span { color: white !important; }
    .header-title { font-size: 28px; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.2); }
    
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
    
    /* 資訊看板 */
    .info-box {
        background-color: #fffbea;
        border-left: 5px solid #FFD700;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    
    /* 時間軸 */
    .timeline-item {
        border-left: 3px solid #FF69B4;
        padding-left: 20px;
        margin-bottom: 20px;
        position: relative;
    }
    .timeline-item::before {
        content: '🌸';
        position: absolute;
        left: -13px;
        top: 0;
        background: #FFF0F5;
        border-radius: 50%;
    }
    .day-header {
        background: #FFE4E1;
        color: #C71585 !important;
        padding: 5px 15px;
        border-radius: 15px;
        display: inline-block;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .spot-title { font-weight: bold; color: #C71585 !important; font-size: 18px; }
    .spot-tag { 
        font-size: 12px; background: #FFE4E1; color: #D87093 !important; 
        padding: 2px 8px; border-radius: 10px; margin-right: 5px;
    }
    
    /* 住宿卡片 */
    .hotel-card {
        background: #F8F8FF;
        border-left: 5px solid #9370DB;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    
    /* 景點名錄小卡 */
    .mini-card {
        background: white;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #eee;
        font-size: 14px;
        margin-bottom: 8px;
        border-left: 3px solid #FF69B4;
    }
    .flower-badge {
        background: #FF69B4; color: white !important; padding: 1px 5px; border-radius: 4px; font-size: 11px; margin-left: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (全國版擴充)
# ==========================================
# 邏輯映射：
# region: 北部/中部/南部/東部
# zone: 市區近郊 (對應原架構的前山/易達) / 深山絕景 (對應原架構的後山/需過夜)

all_spots_db = [
    # --- 北部 (North) ---
    {"name": "淡水天元宮", "region": "北部", "zone": "市區近郊", "month": [1, 2, 3], "type": "網美", "flower": "吉野櫻/三色櫻", "fee": "免門票", "desc": "新北地標，天壇與櫻花交織的絕景。"},
    {"name": "陽明山平菁街42巷", "region": "北部", "zone": "市區近郊", "month": [1, 2], "type": "賞花", "flower": "寒櫻", "fee": "免門票", "desc": "台北最早開花的櫻花巷，粉紅圍牆。"},
    {"name": "三峽大熊櫻花林", "region": "北部", "zone": "市區近郊", "month": [1, 2, 3], "type": "健行", "flower": "三色櫻/八重櫻", "fee": "門票$150", "desc": "4000棵櫻花染紅山頭，夜櫻著名。"},
    {"name": "司馬庫斯 (上帝部落)", "region": "北部", "zone": "深山絕景", "month": [2], "type": "秘境", "flower": "昭和櫻/霧社櫻", "fee": "需預約", "desc": "新竹尖石深山，全台最難抵達的粉紅仙境。"},
    {"name": "拉拉山恩愛農場", "region": "北部", "zone": "深山絕景", "month": [2, 3], "type": "賞花", "flower": "千島櫻/富士櫻", "fee": "門票$100", "desc": "桃園復興最高點，櫻花與雲海共舞。"},
    {"name": "山上人家森林農場", "region": "北部", "zone": "深山絕景", "month": [2, 3], "type": "景觀", "flower": "吉野櫻", "fee": "門票$200", "desc": "新竹五峰，茶園與櫻花的夢幻構圖。"},

    # --- 中部 (Central) ---
    {"name": "武陵農場", "region": "中部", "zone": "深山絕景", "month": [2], "type": "賞花", "flower": "紅粉佳人", "fee": "門票$160", "desc": "台灣賞櫻首選，綿延三公里的粉紅隧道。"},
    {"name": "福壽山農場千櫻園", "region": "中部", "zone": "深山絕景", "month": [2, 3], "type": "賞花", "flower": "富士櫻/昭和櫻", "fee": "門票$100", "desc": "全台最高海拔櫻花園，偽出國感最強。"},
    {"name": "九族文化村", "region": "中部", "zone": "市區近郊", "month": [2, 3], "type": "樂園", "flower": "八重櫻/吉野櫻", "fee": "門票$900", "desc": "台灣唯一日本認證賞櫻名所，夜櫻必看。"},
    {"name": "后里泰安派出所", "region": "中部", "zone": "市區近郊", "month": [2], "type": "兜風", "flower": "八重櫻", "fee": "免門票", "desc": "全台最美派出所，平地賞櫻首選。"},
    {"name": "奧萬大森林遊樂區", "region": "中部", "zone": "深山絕景", "month": [1, 2, 3], "type": "健行", "flower": "山櫻/霧社櫻", "fee": "門票$200", "desc": "不只賞楓，春天的白色霧社櫻更是絕美。"},
    {"name": "古坑草嶺櫻花季", "region": "中部", "zone": "市區近郊", "month": [2], "type": "秘境", "flower": "寒櫻/白花山櫻", "fee": "免門票", "desc": "雲林石壁部落，沿著149甲線的粉紅公路。"},

    # --- 南部 (South) ---
    {"name": "阿里山國家森林遊樂區", "region": "南部", "zone": "深山絕景", "month": [3, 4], "type": "賞花", "flower": "吉野櫻(櫻王)", "fee": "門票$200", "desc": "小火車穿梭櫻花林，經典中的經典。"},
    {"name": "隙頂/石棹櫻花道", "region": "南部", "zone": "深山絕景", "month": [2, 3], "type": "攝影", "flower": "昭和櫻", "fee": "免門票", "desc": "阿里山公路旁，琉璃光與櫻花夜景。"},
    {"name": "屏東霧台櫻花王", "region": "南部", "zone": "深山絕景", "month": [2], "type": "部落", "flower": "山櫻花", "fee": "清潔費", "desc": "魯凱族部落，一棵樹開滿整座庭院的傳奇。"},
    {"name": "寶山二集團櫻花公園", "region": "南部", "zone": "市區近郊", "month": [1, 2], "type": "健行", "flower": "河津櫻", "fee": "免門票", "desc": "高雄桃源區，南部最早盛開的粉紅花海。"},
    
    # --- 東部 (East) ---
    {"name": "宜蘭大同櫻花林", "region": "東部", "zone": "市區近郊", "month": [2], "type": "兜風", "flower": "八重櫻", "fee": "免門票", "desc": "台7甲線沿路，通往武陵的前哨站。"},
    {"name": "太麻里金針山", "region": "東部", "zone": "深山絕景", "month": [1, 2, 3], "type": "健行", "flower": "山櫻/八重櫻", "fee": "免門票", "desc": "台東賞花秘境，雲霧繚繞的山徑。"},
    {"name": "花蓮玉山神學院", "region": "東部", "zone": "市區近郊", "month": [2, 3], "type": "賞花", "flower": "霧社櫻/山櫻", "fee": "免門票", "desc": "鯉魚潭旁，俯瞰湖光山色的櫻花步道。"}
]

# 住宿資料庫 (全國精選)
hotels_db = [
    # 北部
    {"name": "淡水福容大飯店", "region": "北部", "tag": "奢華", "price": 6000, "desc": "近天元宮，漁人碼頭夕陽。"},
    {"name": "新竹老爺行旅", "region": "北部", "tag": "設計", "price": 3500, "desc": "前往司馬庫斯的中繼站。"},
    # 中部
    {"name": "武陵富野渡假村", "region": "中部", "tag": "搶手", "price": 5000, "desc": "就在武陵農場內，需半年前預訂。"},
    {"name": "日月潭雲品酒店", "region": "中部", "tag": "湖景", "price": 12000, "desc": "九族賞櫻後的頂級享受。"},
    {"name": "台中林酒店", "region": "中部", "tag": "市區", "price": 4800, "desc": "泰安派出所賞櫻首選住宿。"},
    # 南部
    {"name": "阿里山賓館", "region": "南部", "tag": "歷史", "price": 8000, "desc": "住在森林遊樂區內，看日出最方便。"},
    {"name": "嘉義承億文旅", "region": "南部", "tag": "文青", "price": 2800, "desc": "高CP值，前往阿里山的起點。"},
    # 東部
    {"name": "礁溪老爺酒店", "region": "東部", "tag": "溫泉", "price": 9000, "desc": "賞櫻兼泡湯，極致享受。"},
    {"name": "花蓮理想大地", "region": "東部", "tag": "渡假", "price": 5500, "desc": "歐式運河風情。"}
]

# ==========================================
# 4. 邏輯核心：全國動態行程生成演算法
# ==========================================
def generate_dynamic_itinerary(travel_date, days_str, group, target_region):
    m = travel_date.month
    
    # 1. 篩選：地區 + 月份
    region_spots = [s for s in all_spots_db if s['region'] == target_region]
    available_spots = [s for s in region_spots if m in s['month']]
    
    # 防呆：若該月無花，塞入該區所有景點
    if not available_spots:
        available_spots = region_spots if region_spots else all_spots_db[:3]

    # 2. 分區邏輯 (Mapping): 
    # zone="市區近郊" 類似原架構的 "前山" (易達)
    # zone="深山絕景" 類似原架構的 "後山" (需跋涉)
    easy_spots = [s for s in available_spots if s['zone'] == "市區近郊"]
    deep_spots = [s for s in available_spots if s['zone'] == "深山絕景"]
    
    # 確保列表不為空
    if not easy_spots: easy_spots = available_spots
    if not deep_spots: deep_spots = available_spots
    
    if "一日" in days_str: day_count = 1
    elif "二日" in days_str: day_count = 2
    else: day_count = 3
    
    itinerary = {}
    
    # --- Day 1: 輕鬆抵達的熱點 (市區/近郊) ---
    # 邏輯：第一天通常體力好但不想太累，或者剛抵達
    d1_spot1 = easy_spots[0]
    remaining = [s for s in easy_spots if s['name'] != d1_spot1['name']]
    d1_spot2 = remaining[0] if remaining else (deep_spots[0] if deep_spots else d1_spot1)
    
    itinerary[1] = [d1_spot1, d1_spot2]
    
    # --- Day 2: 深入秘境 (深山/絕景) ---
    if day_count >= 2:
        # Day 2 上午：直攻最難抵達的深山大景
        d2_spot1 = deep_spots[0] # 通常是該區最強景點 (如武陵、司馬庫斯)
        
        # Day 2 下午：附近的次要景點
        used_names = [s['name'] for s in itinerary[1]] + [d2_spot1['name']]
        d2_pool = [s for s in available_spots if s['name'] not in used_names]
        d2_spot2 = d2_pool[0] if d2_pool else easy_spots[-1]
            
        itinerary[2] = [d2_spot1, d2_spot2]

    # --- Day 3: 漫遊與回程 ---
    if day_count == 3:
        used_names = [s['name'] for day in itinerary.values() for s in day]
        d3_pool = [s for s in available_spots if s['name'] not in used_names]
        
        d3_spot1 = d3_pool[0] if d3_pool else itinerary[1][0]
        # Day 3 下午固定為採買行程
        souvenir_map = {
            "北部": "淡水老街/台北101", "中部": "台中歌劇院/宮原眼科", 
            "南部": "檜意森活村/駁二", "東部": "花蓮東大門/宜蘭傳藝"
        }
        d3_spot2 = {"name": souvenir_map.get(target_region, "市區商圈"), "region": target_region, "flower": "人文", "type": "採買", "fee": "免門票", "desc": "快樂賦歸，購買伴手禮。"}
        
        itinerary[3] = [d3_spot1, d3_spot2]

    titles = {1: "❄️ 早春寒櫻序曲", 2: "🌸 粉紅風暴大爆發", 3: "🍑 吉野櫻與桃花雨", 4: "🌲 高山晚櫻與新綠"}
    status_title = titles.get(m, "🌲 四季寶島森呼吸")
    
    return status_title, itinerary

# ==========================================
# 5. 頁面內容 (UI)
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌸 2026 全國賞櫻攻略地圖</div>
        <div class="header-subtitle">復興區長 <b>蘇佐璽</b> 帶您遊遍全台灣 ❤️</div>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        # 新增：地區選擇器
        target_region = st.selectbox("想去哪裡賞櫻？", ["北部", "中部", "南部", "東部"])
        travel_date = st.date_input("預計出發日期", value=date(2026, 2, 20), min_value=date(2026, 1, 1), max_value=date(2026, 4, 30))
    with col2:
        days = st.selectbox("行程天數", ["一日遊", "二日遊", "三日遊"])
        group = st.selectbox("出遊夥伴", ["情侶/夫妻", "親子家庭", "長輩樂齡", "熱血獨旅"])
        transport = st.selectbox("交通方式", ["自行開車", "大眾運輸 (高鐵/客運)", "機車/單車"])
    
    generate_btn = st.button("🚀 生成蘇區長推薦行程")
    st.markdown('</div>', unsafe_allow_html=True)

if generate_btn:
    status_title, itinerary = generate_dynamic_itinerary(travel_date, days, group, target_region)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="weather-tag">{status_title}</div>
        <div>根據您選擇的 <b>{target_region} {days}</b>，我們為 <b>{group}</b> 規劃了最佳賞花路徑。</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🗓️ 詳細行程", "💰 精準預算", "🚗 交通住宿", "🌸 景點名錄"])

    # --- Tab 1: 動態行程 ---
    with tab1:
        for day_num, spots in itinerary.items():
            st.markdown(f'<div class="day-header">Day {day_num}</div>', unsafe_allow_html=True)
            
            s1 = spots[0]
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">09:30 {s1['name']} <span class="spot-tag">{s1['zone']}</span></div>
                <div class="spot-desc">{s1['desc']} ({s1['flower']})</div>
            </div>
            """, unsafe_allow_html=True)
            
            lunch_text = "當地特色風味餐 (甕仔雞/山產)" if s1['zone'] == "深山絕景" else "市區人氣美食或老街小吃"
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">12:30 午餐時間</div>
                <div class="spot-desc">{lunch_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
            s2 = spots[1]
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">14:30 {s2['name']} <span class="spot-tag">{s2['zone']}</span></div>
                <div class="spot-desc">{s2['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if day_num < len(itinerary):
                 st.markdown(f"""
                <div class="timeline-item" style="border-color:#9370DB;">
                    <div class="spot-title" style="color:#9370DB;">18:00 入住 {target_region} 精選旅宿</div>
                    <div class="spot-desc">建議選擇下方「交通住宿」頁籤中的推薦飯店。</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                 st.markdown(f"""
                <div class="timeline-item" style="border-color:#4CAF50;">
                    <div class="spot-title" style="color:#4CAF50;">17:00 快樂賦歸</div>
                    <div class="spot-desc">帶著滿滿的照片與回憶回家。</div>
                </div>
                """, unsafe_allow_html=True)

    # --- Tab 2: 經費 ---
    with tab2:
        day_count = len(itinerary)
        person_count = 2 if "情侶" in group else (4 if "親子" in group or "長輩" in group else 1)
        
        # 全國版預算稍微調高
        food_cost = 1000 * day_count
        stay_cost = 0
        if day_count > 1:
            avg_room_price = 4500 # 全國平均房價較高
            nights = day_count - 1
            rooms = (person_count + 1) // 2
            total_stay = avg_room_price * nights * rooms
            stay_cost = total_stay / person_count
            
        trans_cost = 1500 if "大眾" in transport else (500 if "機車" in transport else 1200) # 油錢/高鐵票
        total_est = food_cost + stay_cost + trans_cost
        
        c1, c2, c3 = st.columns(3)
        c1.metric("餐飲預算(人)", f"${food_cost}")
        c2.metric("住宿預算(人)", f"${int(stay_cost)}")
        c3.metric("交通/雜支(人)", f"${trans_cost}")
        
        st.divider()
        st.subheader(f"💵 總預算預估：${int(total_est)} /人")
        st.info(f"計算基礎：{target_region} {day_count}天行程，{person_count}人同行，{transport}。")

    # --- Tab 3: 交通與住宿 ---
    with tab3:
        st.subheader("🚗 交通策略")
        if "自行開車" in transport:
            st.warning(f"⚠️ **賞櫻熱點管制**：{target_region} 熱門景點 (如武陵、阿里山、天元宮) 櫻花季期間皆有交通管制，請務必申請通行證或轉乘接駁車。")
        elif "大眾運輸" in transport:
            st.success("🚄 **高鐵+客運**：推薦搭乘高鐵至主要城市 (台北/台中/嘉義)，再轉乘「台灣好行」賞花專車，省去塞車煩惱。")
        else:
            st.info("🏍️ **機車漫遊**：適合短程市區近郊 (如陽明山、大坑)，長途跨縣市請注意安全。")

        st.divider()
        st.subheader("🛌 嚴選住宿推薦")
        
        filtered_hotels = [h for h in hotels_db if h['region'] == target_region]
        if not filtered_hotels: filtered_hotels = hotels_db[:4]
        
        st.caption(f"根據您的目的地 **{target_region}**，蘇區長推薦以下優質旅宿：")
        
        cols = st.columns(2)
        for i, h in enumerate(filtered_hotels):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="hotel-card">
                    <div style="font-weight:bold;">{h['name']} <span style="font-size:12px; color:#666;">({h['price']}元起)</span></div>
                    <div style="font-size:12px; margin-top:5px;">🏷️ {h['tag']} | {h['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- Tab 4: 完整景點名錄 ---
    with tab4:
        st.markdown(f"### 🌸 {target_region} 賞櫻名所全收錄")
        search = st.text_input("🔍 搜尋全台景點", placeholder="輸入關鍵字 (如：武陵、阿里山)...")
        
        # 預設顯示選定區域，若有搜尋則搜尋全庫
        filtered = [s for s in all_spots_db if s['region'] == target_region]
        if search:
            filtered = [s for s in all_spots_db if search in s['name'] or search in s['desc']]
            
        for s in filtered:
            fee_info = s.get('fee', '詳見說明')
            st.markdown(f"""
            <div class="mini-card">
                <b>{s['name']}</b> <span class="flower-badge">{s['flower']}</span>
                <span style="font-size:12px; color:#666 !important; float:right;">💰 {fee_info}</span><br>
                <span style="font-size:12px; color:#666 !important;">📍 {s['region']} {s['zone']} | {s['desc']}</span>
            </div>
            """, unsafe_allow_html=True)

else:
    st.info("👆 請選擇想去的區域 (北/中/南/東)，我們將為您生成全國級的賞櫻攻略。")

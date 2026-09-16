import streamlit as st
import random
import pandas as pd
import time

# ==============================
# 기본 설정
# ==============================

st.set_page_config(
    page_title="STOCK TYCOON : 5-TURN SPEED GAME",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS - 디자인 & 색상 맞춤 설정
# ==============================

st.markdown("""
<style>
/* 기본 배경 및 글자색 */
.stApp {
    background-color: #f8fafc;
    color: #1e293b;
}

.block-container {
    max-width: 1200px;
    padding: 25px 35px 50px 35px;
}

/* 상단 제목 */
.title-box {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    padding: 28px;
    border-radius: 22px;
    color: #ffffff;
    margin-bottom: 20px;
}

.title {
    font-size: 38px;
    font-weight: 900;
    color: #ffffff !important;
}

.subtitle {
    font-size: 16px;
    font-weight: 600;
    color: #e2e8f0 !important;
}

.section-title {
    font-size: 22px;
    font-weight: 900;
    color: #0f172a;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* 대시보드 카드 */
.metric-card {
    background: white;
    border: 2px solid #cbd5e1;
    border-radius: 18px;
    padding: 20px;
    min-height: 110px;
}

.metric-label {
    color: #475569;
    font-size: 15px;
    font-weight: 800;
}

.metric-value {
    font-size: 24px;
    font-weight: 900;
    color: #0f172a;
    margin-top: 6px;
    white-space: nowrap;
}

/* 타이머 박스 */
.timer-card {
    background: #fef2f2;
    border: 2px solid #ef4444;
    border-radius: 18px;
    padding: 20px;
    min-height: 110px;
}

.timer-value {
    font-size: 26px;
    font-weight: 900;
    color: #dc2626;
    margin-top: 4px;
}

/* 돌발 특수 이벤트 대형 박스 */
.flash-event-box-crash {
    background: #fff1f2;
    border: 2px solid #f43f5e;
    border-radius: 20px;
    padding: 22px 28px;
    margin-top: 15px;
    margin-bottom: 20px;
}

.flash-badge-crash {
    display: inline-block;
    background: #e11d48;
    color: #ffffff !important;
    font-size: 13px;
    font-weight: 900;
    padding: 5px 12px;
    border-radius: 6px;
    margin-bottom: 10px;
}

.flash-title-crash {
    font-size: 22px;
    font-weight: 900;
    color: #881337;
    margin-bottom: 8px;
}

.flash-text-crash {
    font-size: 16px;
    color: #4c0519;
    font-weight: 700;
    line-height: 1.6;
}

/* 지문 박스 */
.news-card-large {
    background: #ffffff;
    border: 2px solid #0f172a;
    border-radius: 20px;
    padding: 30px 35px;
    margin-top: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.news-badge {
    display: inline-block;
    background: #0f172a;
    color: #ffffff !important;
    font-size: 14px;
    font-weight: 900;
    padding: 6px 14px;
    border-radius: 6px;
    margin-bottom: 15px;
}

.news-title-large {
    font-size: 23px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.4;
    margin-bottom: 15px;
}

.news-text-large {
    font-size: 16px;
    color: #1e293b;
    font-weight: 700;
    line-height: 1.8;
    background: #f1f5f9;
    padding: 20px;
    border-left: 6px solid #0f172a;
    border-radius: 8px;
    white-space: pre-line;
}

/* 주식 카드 */
.stock-card {
    background: white;
    border-radius: 20px;
    border: 2px solid #cbd5e1;
    padding: 22px;
    min-height: 230px;
    margin-bottom: 10px;
}

.stock-name {
    font-size: 22px;
    font-weight: 900;
    color: #0f172a;
}

.stock-price {
    font-size: 26px;
    font-weight: 900;
    margin-top: 8px;
    color: #0f172a;
}

.stock-info {
    color: #475569;
    font-size: 15px;
    font-weight: 700;
    margin-top: 5px;
}

/* 일반 버튼 (수량, 매수, 매도 등) - 검은 배경 & 흰 글씨 */
.stButton > button {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: 2px solid #ffffff !important;
    min-height: 48px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 900;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #262626 !important;
    color: #ffffff !important;
}

/* 다음 턴 버튼 - 빨간색 배경 */
div[data-testid="stButton"] > button[kind="primary"] {
    background-color: #dc2626 !important;
    color: #ffffff !important;
    border: 2px solid #b91c1c !important;
}

div[data-testid="stButton"] > button[kind="primary"]:hover {
    background-color: #b91c1c !important;
}

.stNumberInput input {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: 2px solid #000000 !important;
    min-height: 45px;
    font-size: 16px;
    font-weight: 900;
    border-radius: 10px;
}

.stNumberInput label {
    color: #000000 !important;
    font-weight: 900 !important;
    font-size: 15px !important;
}

/* 결과 화면 - 하얀색 바탕 & 검은색 글씨 */
.result-card-white {
    background-color: #ffffff;
    border: 3px solid #0f172a;
    border-radius: 22px;
    padding: 40px;
    text-align: center;
    color: #000000 !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.result-card-white h1 { 
    color: #000000 !important; 
    font-size: 32px; 
    font-weight: 900; 
    margin-bottom: 10px; 
}

.result-card-white h2 { 
    color: #0284c7 !important; 
    font-size: 34px; 
    font-weight: 900; 
    margin: 15px 0; 
}

.result-card-white h3 { 
    color: #475569 !important; 
    font-size: 20px; 
    font-weight: 800; 
    margin-top: 20px; 
}

.result-card-white .final-asset { 
    color: #0f172a !important; 
    font-size: 40px; 
    font-weight: 900; 
}

/* 시작 화면 카드 스타일 */
.start-card {
    background: white;
    border: 2px solid #0f172a;
    border-radius: 22px;
    padding: 40px;
    max-width: 600px;
    margin: 40px auto;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)


# ==============================
# 게임 데이터 (수익률 변동 폭 대폭 상향 🔥)
# ==============================

TOTAL_TURNS = 5
TURN_TIME_LIMIT = 30

STOCKS = {
    "삼성전자": 70000,
    "SK하이닉스": 120000,
    "카카오": 50000,
    "테슬라": 300000,
    "엔비디아": 180000
}

EXAM_NEWS_POOL = [
    {
        "code": "HARD-01 (유동성 재편)",
        "title": "[분석 지문] 기준금리 인하 기조 속 시중 유동성 흡수와 대체 투자 재편",
        "text": """중앙은행이 경기 진작을 위해 기준금리 인하를 발표했으나, 통화당국은 물가 상방 압력을 통제하고자 역레포 금리를 상향 조정하여 시중 단기 유동성을 강하게 흡수하는 상반된 정책을 동시 집행하였다.

이로 인해 금융권 자금이 위험자산인 IT·플랫폼 부문에서 이탈하여 고정 채권형 자산으로 이동하고 있다. 한편, 완성차/배터리 제조 단가 둔화 세는 소폭 완화되는 반사이익이 발생하고 있다.""",
        # 🚀 이전보다 2~3배 확장된 변동률 범위
        "effects": {"삼성전자": (-35, -15), "SK하이닉스": (-40, -20), "카카오": (-45, -25), "테슬라": (15, 45)}
    },
    {
        "code": "HARD-02 (기술 패러다임)",
        "title": "[분석 지문] AI CAPEX 과잉 투자 회의론과 ASIC 맞춤형 칩 대체 전환",
        "text": """빅테크 기업들의 AI 인프라 투자 대비 실질 수익성 창출 시점이 연기됨에 따라 비싼 범용 GPU 구매를 급격히 줄이고, 자체 설계한 주문형 반도체(ASIC) 생산 비율을 확대하기로 선회하였다.

범용 GPU 공급망을 독점하던 기업에 악재로 작용하나, 맞춤형 ASIC 반도체 위탁 생산(Foundry) 대기업에게는 대체 수주 기회가 열리고 있다.""",
        "effects": {"엔비디아": (-50, -20), "삼성전자": (20, 50), "SK하이닉스": (-25, 25)}
    },
    {
        "code": "HARD-03 (통화 및 무역)",
        "title": "[분석 지문] 강달러 환율 오버슈팅 및 반덤핑 상계관세 부과 조치",
        "text": """원/달러 환율이 오버슈팅 현상으로 급등하는 가운데, 미 통상무역위원회가 한국산 반도체 부품 및 플랫폼 소프트웨어 수출 품목에 반덤핑 상계관세를 부과하였다.

반면 환차익이 극대화되는 해외 본사 소재 빅테크 기업으로 외국인 순매수가 강하게 쏠리고 있다.""",
        "effects": {"삼성전자": (-30, -10), "카카오": (-40, -15), "테슬라": (20, 55), "엔비디아": (15, 45)}
    },
    {
        "code": "HARD-04 (안보 및 규제)",
        "title": "[분석 지문] 자율주행 데이터 안보법 제정과 희토류 수출 통제 보복 조치",
        "text": """주요 원자재 수출국이 차량용 핵심 희토류 수출 제한령을 발효하고, 자국의 도로 주행 데이터 해외 서버 이전을 엄격히 금지하였다.

이로 인해 글로벌 자율주행 완성차 기업은 데이터 유입 마비와 생산 원가 상승이라는 이중고에 직면하였다.""",
        "effects": {"테슬라": (-50, -25), "엔비디아": (-25, -5), "카카오": (10, 35)}
    },
    {
        "code": "HARD-05 (재고 및 기저효과)",
        "title": "[분석 지문] 메모리 반도체 덤핑 재고 소진 완료와 착시 효과",
        "text": """장기 불황을 이끌었던 메모리 반도체 재고가 감산 정책으로 소진되며 고정 거래가가 반등하였다. 다만 이는 소비 폭증이 아닌 공급 통제에 따른 수급 개선 효과이다.""",
        "effects": {"SK하이닉스": (25, 60), "삼성전자": (15, 40), "엔비디아": (-25, -5)}
    }
]

FLASH_EVENTS = [
    {
        "title": "💥 [돌발 대폭락] 지정학적 리스크 및 원자재 수송 차질",
        "text": "주요 수송로 봉쇄 우려로 금융 시장 매수세가 완전히 실종되며 전 종목 주가가 궤멸적인 하락 압력을 받습니다.",
        "effects": {"삼성전자": (-45, -20), "SK하이닉스": (-45, -20), "카카오": (-50, -25), "테슬라": (-35, -15), "엔비디아": (-40, -20)}
    },
    {
        "title": "📉 [돌발 악재] 글로벌 투자은행 자산 매각 공시",
        "text": "대형 운용사의 자금 회수용 강제 매물이 쏟아지며 주요 종목 주가가 폭락합니다.",
        "effects": {"삼성전자": (-30, -10), "SK하이닉스": (-35, -15), "카카오": (-40, -15), "테슬라": (-30, -10), "엔비디아": (-35, -15)}
    },
    {
        "title": "🚀 [돌발 대떡상] 중동 국부펀드 글로벌 테크 수급 폭풍 유입",
        "text": "대규모 자산 재배분 결정으로 보유 종목 전반에 상한가 기세를 이끄는 강력한 매수세가 들어옵니다.",
        "effects": {"삼성전자": (20, 50), "SK하이닉스": (25, 55), "카카오": (15, 45), "테슬라": (30, 60), "엔비디아": (35, 65)}
    }
]


# ==============================
# 게임 초기화 함수
# ==============================

def start_game(start_cash):
    st.session_state.game_started = True
    st.session_state.start_cash = start_cash
    st.session_state.cash = start_cash
    st.session_state.prices = STOCKS.copy()
    st.session_state.holdings = {stock: 0 for stock in STOCKS}
    st.session_state.buy_costs = {stock: 0 for stock in STOCKS}
    st.session_state.turn = 1
    st.session_state.history = []
    st.session_state.trade_history = []
    st.session_state.game_over = False
    st.session_state.last_changes = {stock: 0 for stock in STOCKS}
    st.session_state.price_history = [STOCKS.copy()]
    
    st.session_state.turn_start_time = time.time()
    
    news_deck = EXAM_NEWS_POOL.copy()
    random.shuffle(news_deck)
    st.session_state.news_deck = news_deck
    st.session_state.current_news = st.session_state.news_deck.pop()
    st.session_state.flash_event = None


# 시작 자산 입력 화면
if "game_started" not in st.session_state or not st.session_state.game_started:
    st.markdown('<div class="title-box"><div class="title">STOCK TYCOON</div><div class="subtitle">5턴 스피드 트레이딩 레이스</div></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="start-card">
        <h2 style="color:#0f172a; font-weight:900; margin-bottom:20px;">🎮 게임 시작 설정</h2>
        <p style="color:#475569; font-weight:700; font-size:16px;">투자를 시작할 초기 자산을 설정해주세요.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        init_cash = st.number_input("시작 자산 (원)", min_value=100_000, value=1_000_000, step=100_000, format="%d")
        st.write("")
        if st.button("🚀 게임 시작하기", type="primary", use_container_width=True):
            start_game(init_cash)
            st.rerun()
    st.stop()


# ==============================
# 계산 및 매매 함수
# ==============================

def total_asset():
    stock_value = sum(
        st.session_state.prices[stock] * st.session_state.holdings[stock]
        for stock in STOCKS
    )
    return st.session_state.cash + stock_value


def profit_rate():
    start = st.session_state.get("start_cash", 1_000_000)
    if start == 0:
        return 0.0
    return (total_asset() - start) / start * 100


def buy_stock(stock, amount):
    price = st.session_state.prices[stock]
    cost = price * amount

    if amount <= 0:
        st.warning("수량을 1개 이상 입력하세요.")
        return

    if cost > st.session_state.cash:
        st.error("현금이 부족합니다.")
        return

    st.session_state.cash -= cost
    st.session_state.holdings[stock] += amount
    st.session_state.buy_costs[stock] += cost
    st.session_state.trade_history.insert(0, f"매수 | {stock} {amount:,}주 | ₩{cost:,}")


def sell_stock(stock, amount):
    price = st.session_state.prices[stock]

    if amount <= 0:
        st.warning("수량을 1개 이상 입력하세요.")
        return

    if amount > st.session_state.holdings[stock]:
        st.error("보유 주식보다 많이 팔 수 없습니다.")
        return

    revenue = price * amount
    avg_price = st.session_state.buy_costs[stock] / st.session_state.holdings[stock]
    st.session_state.buy_costs[stock] -= int(avg_price * amount)
    
    st.session_state.cash += revenue
    st.session_state.holdings[stock] -= amount
    st.session_state.trade_history.insert(0, f"매도 | {stock} {amount:,}주 | ₩{revenue:,}")


# ==============================
# 턴 진행 로직 (수익률 변동 강화 적용)
# ==============================

def next_turn():
    st.session_state.history.append(total_asset())
    
    if st.session_state.turn >= TOTAL_TURNS:
        st.session_state.game_over = True
        return

    current_effects = st.session_state.current_news["effects"]
    
    is_flash_triggered = random.random() < 0.25
    flash_data = random.choice(FLASH_EVENTS) if is_flash_triggered else None
    st.session_state.flash_event = flash_data

    changes = {}

    for stock in STOCKS:
        # 뉴스 영향 기반 계산
        if stock in current_effects:
            min_p, max_p = current_effects[stock]
            base_change = random.randint(min_p, max_p)
            # 10% 확률로 예상과 반대로 튀는 반전 노이즈
            if random.random() < 0.10:
                base_change = -base_change
        else:
            base_change = random.randint(-15, 15)
        
        # 돌발 이벤트 영향 추가
        flash_change = 0
        if flash_data and stock in flash_data["effects"]:
            f_min, f_max = flash_data["effects"][stock]
            flash_change = random.randint(f_min, f_max)
        
        # 시장 기본 변동 노이즈 확대 (-5% ~ +5%)
        noise = random.randint(-5, 5)
        
        total_change = base_change + flash_change + noise
        
        old_price = st.session_state.prices[stock]
        new_price = max(1000, int(old_price * (1 + total_change / 100)))
        st.session_state.prices[stock] = new_price
        changes[stock] = total_change

    st.session_state.last_changes = changes
    st.session_state.price_history.append(st.session_state.prices.copy())
    st.session_state.turn += 1
    
    st.session_state.turn_start_time = time.time()

    if not st.session_state.news_deck:
        st.session_state.news_deck = EXAM_NEWS_POOL.copy()
        random.shuffle(st.session_state.news_deck)
    st.session_state.current_news = st.session_state.news_deck.pop()


# ==============================
# 결과 화면 (하얀색 바탕 & 검은색 타이틀)
# ==============================

if st.session_state.game_over:
    asset = total_asset()
    profit = profit_rate()

    if profit >= 50:
        grade = "S (스피드 타짜 - 신의 손)"
    elif profit >= 25:
        grade = "A (1등급 - 성공한 트레이더)"
    elif profit >= 10:
        grade = "B (2등급 - 우수)"
    elif profit >= 0:
        grade = "C (3등급 - 원금 보존)"
    else:
        grade = "D (4등급 이하 - 깡통)"

    profit_color = "#ef4444" if profit >= 0 else "#2563eb"

    st.markdown('<div class="title-box"><div class="title">STOCK TYCOON</div><div class="subtitle">5턴 스피드 레이스 결과</div></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="result-card-white">
        <h1>🏆 최종 투자 평가 완료</h1>
        <h2>{grade}</h2>
        <h3>최종 자산</h3>
        <div class="final-asset">₩{asset:,}</div>
        <p style="font-weight:900; font-size:22px; color:{profit_color}; margin-top:15px;">
            수익률 {profit:+.2f}%
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.session_state.history:
        st.markdown('<div class="section-title">자산 변화 추이</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({"자산": st.session_state.history})
        chart_data.index = [f"{i+1}턴" for i in range(len(st.session_state.history))]
        st.line_chart(chart_data, use_container_width=True)

    if st.button("다시 도전하기", use_container_width=True):
        st.session_state.game_started = False
        st.rerun()

    st.stop()


# ==============================
# 메인 UI
# ==============================

st.markdown('<div class="title-box"><div class="title">STOCK TYCOON</div><div class="subtitle">5턴 스피드 레이스 - 턴당 제한시간 30초! 시간 종료 시 자동 진행됩니다.</div></div>', unsafe_allow_html=True)

elapsed_time = time.time() - st.session_state.get("turn_start_time", time.time())
remaining_time = max(0, int(TURN_TIME_LIMIT - elapsed_time))

if remaining_time <= 0:
    next_turn()
    st.rerun()

asset = total_asset()
profit = profit_rate()

profit_style = "color:#ef4444;" if profit >= 0 else "color:#2563eb;"

c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 2])

with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">보유 현금</div><div class="metric-value">₩{st.session_state.cash:,}</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">총 자산</div><div class="metric-value">₩{asset:,}</div></div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">수익률</div><div class="metric-value" style="{profit_style}">{profit:+.2f}%</div></div>', unsafe_allow_html=True)

with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">현재 턴</div><div class="metric-value">{min(st.session_state.turn, TOTAL_TURNS)} / {TOTAL_TURNS}</div></div>', unsafe_allow_html=True)

with c5:
    st.markdown(f'<div class="timer-card"><div class="metric-label" style="color:#dc2626; font-weight:800;">⏱️ 남은 시간</div><div class="timer-value">{remaining_time}초</div></div>', unsafe_allow_html=True)

st.write("")
st.progress(min(st.session_state.turn / TOTAL_TURNS, 1.0))


# ==============================
# 돌발 특수 이벤트
# ==============================

if st.session_state.flash_event:
    fe = st.session_state.flash_event
    st.markdown(f"""
    <div class="flash-event-box-crash">
        <div class="flash-badge-crash">FLASH EVENT - 돌발 변수 발생!</div>
        <div class="flash-title-crash">{fe['title']}</div>
        <div class="flash-text-crash">{fe['text']}</div>
    </div>
    """, unsafe_allow_html=True)


# ==============================
# 뉴스 지문
# ==============================

st.markdown('<div class="section-title">오늘의 분석 지문 (다음 턴 반영)</div>', unsafe_allow_html=True)

news = st.session_state.current_news

st.markdown(f"""
<div class="news-card-large">
    <div class="news-badge">{news['code']}</div>
    <div class="news-title-large">{news['title']}</div>
    <div class="news-text-large">{news['text']}</div>
</div>
""", unsafe_allow_html=True)


# ==============================
# 주식 시장
# ==============================

st.markdown('<div class="section-title">주식 시장</div>', unsafe_allow_html=True)

stock_items = list(STOCKS.keys())
rows = [stock_items[i:i + 3] for i in range(0, len(stock_items), 3)]

for row in rows:
    cols = st.columns(len(row))
    for idx, stock in enumerate(row):
        price = st.session_state.prices[stock]
        change = st.session_state.last_changes[stock]
        holding = st.session_state.holdings[stock]
        buy_cost = st.session_state.buy_costs[stock]
        
        change_color = "#ef4444" if change >= 0 else "#2563eb"
        change_sign = "+" if change >= 0 else ""
        
        if holding > 0:
            avg_price = int(buy_cost / holding)
            stock_profit = ((price - avg_price) / avg_price) * 100
            stock_profit_color = "#ef4444" if stock_profit >= 0 else "#2563eb"
            profit_text = f"수익률: {stock_profit:+.1f}%"
            avg_text = f"평단가: ₩{avg_price:,}"
        else:
            stock_profit_color = "#64748b"
            profit_text = "수익률: - %"
            avg_text = "평단가: - 원"

        with cols[idx]:
            st.markdown(f"""
            <div class="stock-card">
                <div class="stock-name">{stock}</div>
                <div class="stock-price">₩{price:,}</div>
                <div class="stock-info" style="color:{change_color}; font-weight:800;">
                    직전 변동률 {change_sign}{change}%
                </div>
                <hr style="margin: 10px 0; border:none; border-top:1px solid #cbd5e1;">
                <div class="stock-info"><b>보유량:</b> {holding:,}주</div>
                <div class="stock-info"><b>{avg_text}</b></div>
                <div class="stock-info" style="color:{stock_profit_color}; font-weight:800;">{profit_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
            amount = st.number_input("수량", min_value=1, value=1, step=1, key=f"amount_{stock}")

            buy_col, sell_col = st.columns(2)
            with buy_col:
                if st.button("매수", key=f"buy_{stock}", use_container_width=True):
                    buy_stock(stock, amount)
                    st.rerun()

            with sell_col:
                if st.button("매도", key=f"sell_{stock}", use_container_width=True):
                    sell_stock(stock, amount)
                    st.rerun()

# 차트
st.markdown('<div class="section-title">주가 변동 추이</div>', unsafe_allow_html=True)

history_df = pd.DataFrame(st.session_state.price_history)
history_df.index = [f"{i}턴" for i in range(len(history_df))]
st.line_chart(history_df, use_container_width=True)

# 최근 거래
st.markdown('<div class="section-title">최근 거래 기록</div>', unsafe_allow_html=True)

if st.session_state.trade_history:
    for trade in st.session_state.trade_history[:5]:
        st.info(trade)
else:
    st.caption("아직 거래 기록이 없습니다.")

# 다음 턴 진행 버튼 (빨간색 배경)
st.write("")

if st.button("지문 분석 완료 ➔ 즉시 다음 턴 진행", type="primary", use_container_width=True):
    next_turn()
    st.rerun()

# 게임 진행 중일 때 1초마다 자동 새로고침
if not st.session_state.game_over:
    time.sleep(1)
    st.rerun()

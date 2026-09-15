import streamlit as st
import random
import pandas as pd

# ==============================
# 기본 설정
# ==============================

st.set_page_config(
    page_title="STOCK TYCOON : REALISTIC MARKET",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS - 모의고사 & 돌발 이벤트 전용 스타일
# ==============================

st.markdown("""
<style>
.stApp {
    background-color: #f4f6fa;
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
    color: white;
    margin-bottom: 20px;
}

.title {
    font-size: 38px;
    font-weight: 800;
}

.subtitle {
    font-size: 16px;
    opacity: 0.8;
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* 대시보드 카드 */
.metric-card {
    background: white;
    border: 1px solid #cbd5e1;
    border-radius: 18px;
    padding: 20px;
    min-height: 110px;
}

.metric-label {
    color: #64748b;
    font-size: 14px;
}

.metric-value {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 6px;
    white-space: nowrap;
}

/* 돌발 특수 이벤트 대형 박스 */
.flash-event-box {
    background: #fff1f2;
    border: 3px solid #e11d48;
    border-radius: 20px;
    padding: 25px 30px;
    margin-top: 15px;
    margin-bottom: 20px;
    box-shadow: 0 10px 25px rgba(225, 29, 72, 0.15);
}

.flash-badge {
    display: inline-block;
    background: #e11d48;
    color: #ffffff;
    font-size: 14px;
    font-weight: 900;
    padding: 6px 14px;
    border-radius: 6px;
    margin-bottom: 12px;
    letter-spacing: 1px;
}

.flash-title {
    font-size: 26px;
    font-weight: 900;
    color: #881337;
    margin-bottom: 10px;
}

.flash-text {
    font-size: 16px;
    color: #9f1239;
    font-weight: 600;
    line-height: 1.6;
}

/* 모의고사형 불수능 지문 박스 */
.news-card-large {
    background: #ffffff;
    border: 2px solid #0f172a;
    border-radius: 20px;
    padding: 30px 35px;
    margin-top: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
}

.news-badge {
    display: inline-block;
    background: #0f172a;
    color: #ffffff;
    font-size: 13px;
    font-weight: 800;
    padding: 5px 12px;
    border-radius: 6px;
    margin-bottom: 15px;
}

.news-title-large {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.4;
    margin-bottom: 15px;
}

.news-text-large {
    font-size: 15px;
    color: #1e293b;
    line-height: 1.8;
    background: #f8fafc;
    padding: 22px;
    border-left: 5px solid #0f172a;
    border-radius: 8px;
    white-space: pre-line;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
}

/* 주식 카드 */
.stock-card {
    background: white;
    border-radius: 20px;
    border: 1px solid #cbd5e1;
    padding: 22px;
    min-height: 240px;
    margin-bottom: 10px;
}

.stock-name {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    white-space: nowrap;
}

.stock-price {
    font-size: 26px;
    font-weight: 800;
    margin-top: 8px;
    color: #0f172a;
    white-space: nowrap;
}

.stock-info {
    color: #64748b;
    font-size: 14px;
    margin-top: 4px;
    white-space: nowrap;
}

.result-card {
    background: white;
    border-radius: 22px;
    padding: 30px;
    border: 1px solid #cbd5e1;
    text-align: center;
}

.stButton > button {
    min-height: 48px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 700;
}

.stNumberInput input {
    min-height: 45px;
    font-size: 16px;
}

@media (max-width: 800px) {
    .block-container { padding: 15px; }
    .title { font-size: 28px; }
    .news-title-large { font-size: 19px; }
    .news-text-large { font-size: 14px; }
}
</style>
""", unsafe_allow_html=True)


# ==============================
# 게임 데이터 및 돌발 이벤트 정의
# ==============================

STOCKS = {
    "삼성전자": 70000,
    "SK하이닉스": 120000,
    "카카오": 50000,
    "테슬라": 300000,
    "엔비디아": 180000
}

EXAM_NEWS = [
    {
        "code": "HARD-01 (유동성 재편)",
        "title": "[분석 지문] 기준금리 인하 기조 속 시중 유동성 흡수와 대체 투자 재편",
        "text": """중앙은행이 경기 진작을 위해 기준금리 인하를 발표했으나, 통화당국은 물가 상방 압력을 통제하고자 역레포 금리를 상향 조정하여 시중 단기 유동성을 강하게 흡수하는 상반된 정책을 동시 집행하였다.

이로 인해 금융권 자금이 위험자산인 IT·플랫폼 부문에서 이탈하여 고정 채권형 자산으로 이동하고 있다. 한편, 완성차/배터리 제조 단가 둔화 세는 소폭 완화되는 반사이익이 발생하고 있다.""",
        "effects": {"삼성전자": (-25, -10), "SK하이닉스": (-30, -15), "카카오": (-40, -20), "테슬라": (15, 30)}
    },
    {
        "code": "HARD-02 (기술 패러다임)",
        "title": "[분석 지문] AI CAPEX 과잉 투자 회의론과 ASIC 맞춤형 칩 대체 전환",
        "text": """빅테크 기업들의 AI 인프라 투자 대비 실질 수익성 창출 시점이 연기됨에 따라 비싼 범용 GPU 구매를 급격히 줄이고, 자체 설계한 주문형 반도체(ASIC) 생산 비율을 확대하기로 선회하였다.

범용 GPU 공급망을 독점하던 기업에 극심한 악재로 작용하나, 맞춤형 ASIC 반도체 위탁 생산(Foundry) 대기업에게는 대규모 대체 수주 기회가 열리고 있다.""",
        "effects": {"엔비디아": (-45, -25), "삼성전자": (20, 40), "SK하이닉스": (-10, 10)}
    },
    {
        "code": "HARD-03 (통화 및 무역)",
        "title": "[분석 지문] 강달러 환율 오버슈팅 및 반덤핑 상계관세 부과 조치",
        "text": """원/달러 환율이 오버슈팅 현상으로 급등하는 가운데, 미 통상무역위원회가 한국산 반도체 부품 및 플랫폼 소프트웨어 수출 품목에 30%에 달하는 기습적 반덤핑 상계관세를 부과하였다.

반면 환차익이 극대화되는 해외 본사 소재 빅테크 기업으로 외국인 순매수가 강하게 쏠리고 있다.""",
        "effects": {"삼성전자": (-25, -10), "카카오": (-30, -15), "테슬라": (25, 45), "엔비디아": (20, 40)}
    },
    {
        "code": "HARD-04 (안보 및 규제)",
        "title": "[분석 지문] 자율주행 데이터 안보법 제정과 희토류 수출 통제 보복 조치",
        "text": """주요 원자재 수출국이 차량용 핵심 희토류 수출 제한령을 발효하고, 자국의 도로 주행 데이터 해외 서버 이전을 엄격히 금지하였다.

이로 인해 글로벌 자율주행 완성차 기업은 데이터 유입 마비와 생산 원가 폭등이라는 이중고에 직면하였다.""",
        "effects": {"테슬라": (-50, -30), "엔비디아": (-15, -5), "카카오": (15, 30)}
    }
]

FLASH_EVENTS = [
    {
        "title": "🚨 [급락 서프라이즈] 글로벌 뱅크런 사태 & 숏퀴즈 폭발!",
        "text": "해외 대형 투자은행의 기습 파산 신청으로 전 세계 금융 시장에 뱅크런 공포가 집어삼켰습니다! 전체 주가가 사태 진정 전까지 미친 듯이 급락합니다.",
        "effects": {"삼성전자": -40, "SK하이닉스": -45, "카카오": -50, "테슬라": -35, "엔비디아": -40}
    },
    {
        "title": "🚀 [급등 서프라이즈] 오일 머니 100조 원 테크펀드 기습 집행!",
        "text": "중동 국부펀드가 자산 재배분을 통해 보유 전 종목을 장중 시가로 쓸어담기 시작했습니다! 전 종목이 폭발적으로 급등합니다.",
        "effects": {"삼성전자": 50, "SK하이닉스": 55, "카카오": 40, "테슬라": 60, "엔비디아": 65}
    }
]


# ==============================
# 게임 초기화
# ==============================

def new_game(start_cash=1_000_000):
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
    
    st.session_state.current_news = random.choice(EXAM_NEWS)
    st.session_state.flash_event = None


if "cash" not in st.session_state:
    new_game(1_000_000)


# ==============================
# 계산 및 매매
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
# 턴 진행 (불확실성 및 비언급 종목 변동 로직 적용)
# ==============================

def next_turn():
    st.session_state.history.append(total_asset())
    
    current_effects = st.session_state.current_news["effects"]
    
    # 1. 15% 확률로 돌발 특수 이벤트
    is_flash_triggered = random.random() < 0.15
    flash_data = None
    if is_flash_triggered:
        flash_data = random.choice(FLASH_EVENTS)
        st.session_state.flash_event = flash_data
    else:
        st.session_state.flash_event = None

    changes = {}

    for stock in STOCKS:
        # 지문에 언급된 종목인지 확인
        if stock in current_effects:
            min_p, max_p = current_effects[stock]
            base_change = random.randint(min_p, max_p)
            
            # [수정] 20% 확률로 지문 해석과 반대로 움직이는 역발상 장세(차익실현 등)
            if random.random() < 0.20:
                base_change = -base_change
        else:
            # [수정] 지문에 나오지 않은 종목도 독립적으로 ±15% 내외 무작위 변동
            base_change = random.randint(-15, 15)
        
        # 돌발 이벤트 합산
        flash_change = flash_data["effects"].get(stock, 0) if flash_data else 0
        
        # 시장의 예측 불가능한 잡음(노이즈) ±5% 추가
        noise = random.randint(-5, 5)
        
        total_change = base_change + flash_change + noise
        
        old_price = st.session_state.prices[stock]
        new_price = max(1000, int(old_price * (1 + total_change / 100)))
        st.session_state.prices[stock] = new_price
        changes[stock] = total_change

    st.session_state.last_changes = changes
    st.session_state.price_history.append(st.session_state.prices.copy())
    st.session_state.turn += 1

    if st.session_state.turn > 10:
        st.session_state.game_over = True
    else:
        st.session_state.current_news = random.choice(EXAM_NEWS)


# ==============================
# 게임 종료 화면
# ==============================

if st.session_state.game_over:
    asset = total_asset()
    profit = profit_rate()

    if profit >= 70:
        grade = "S (전설의 타짜)"
    elif profit >= 30:
        grade = "A (1등급 - 성공한 트레이더)"
    elif profit >= 10:
        grade = "B (2등급 - 우수)"
    elif profit >= 0:
        grade = "C (3등급 - 원금 보존)"
    else:
        grade = "D (4등급 이하 - 깡통)"

    st.markdown('<div class="title-box"><div class="title">STOCK TYCOON</div><div class="subtitle">최종 시뮬레이션 결과</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-card"><h1>평가 완료</h1><h2>{grade}</h2><h3>최종 자산</h3><h2>₩{asset:,}</h2><p>수익률 {profit:+.2f}%</p></div>', unsafe_allow_html=True)

    st.write("")

    if st.session_state.history:
        st.markdown('<div class="section-title">자산 변화 추이</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({"자산": st.session_state.history})
        chart_data.index = [f"{i+1}턴" for i in range(len(st.session_state.history))]
        st.line_chart(chart_data, use_container_width=True)

    if st.button("재시험 시작", use_container_width=True):
        new_game(st.session_state.start_cash)
        st.rerun()

    st.stop()


# ==============================
# 메인 UI
# ==============================

st.markdown('<div class="title-box"><div class="title">STOCK TYCOON : REALISTIC MARKET</div><div class="subtitle">지문 분석뿐만 아니라 시장의 불확실성과 무작위 수급 변동까지 예측해 보세요.</div></div>', unsafe_allow_html=True)

# 대시보드
asset = total_asset()
profit = profit_rate()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">보유 현금</div><div class="metric-value">₩{st.session_state.cash:,}</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">총 자산</div><div class="metric-value">₩{asset:,}</div></div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">수익률</div><div class="metric-value">{profit:+.2f}%</div></div>', unsafe_allow_html=True)

with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">현재 턴</div><div class="metric-value">{min(st.session_state.turn, 10)} / 10</div></div>', unsafe_allow_html=True)

st.write("")
st.progress(min(st.session_state.turn / 10, 1.0))


# ==============================
# 돌발 특수 이벤트 발생 표시
# ==============================

if st.session_state.flash_event:
    fe = st.session_state.flash_event
    st.markdown(f"""
    <div class="flash-event-box">
        <div class="flash-badge">FLASH EVENT - 돌발 이슈 발생!</div>
        <div class="flash-title">{fe['title']}</div>
        <div class="flash-text">{fe['text']}</div>
    </div>
    """, unsafe_allow_html=True)


# ==============================
# 고난도 모의고사 지문
# ==============================

st.markdown('<div class="section-title">오늘의 심화 분석 지문 (다음 턴 기본 반영)</div>', unsafe_allow_html=True)

news = st.session_state.current_news

st.markdown(f"""
<div class="news-card-large">
    <div class="news-badge">고난도 문항 : {news['code']}</div>
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
        
        if holding > 0:
            avg_price = int(buy_cost / holding)
            stock_profit = ((price - avg_price) / avg_price) * 100
            profit_text = f"수익률: {stock_profit:+.1f}%"
            avg_text = f"평단가: ₩{avg_price:,}"
        else:
            profit_text = "수익률: - %"
            avg_text = "평단가: - 원"

        with cols[idx]:
            st.markdown(f"""
            <div class="stock-card">
                <div class="stock-name">{stock}</div>
                <div class="stock-price">₩{price:,}</div>
                <div class="stock-info">직전 변동률 {change:+d}%</div>
                <hr style="margin: 10px 0; border:none; border-top:1px solid #eee;">
                <div class="stock-info"><b>보유량:</b> {holding:,}주</div>
                <div class="stock-info"><b>{avg_text}</b></div>
                <div class="stock-info" style="color: {'#e11d48' if '수익률: +' in profit_text else ('#2563eb' if '수익률: -' in profit_text and '-%' not in profit_text else '#788396')}; font-weight:700;">{profit_text}</div>
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
st.markdown('<div class="section-title">최근 거래</div>', unsafe_allow_html=True)

if st.session_state.trade_history:
    for trade in st.session_state.trade_history[:5]:
        st.info(trade)
else:
    st.caption("아직 거래 기록이 없습니다.")

# 턴 진행
st.write("")

if st.button("지문 분석 제출 ➔ 다음 턴 결과 반영", type="primary", use_container_width=True):
    if st.session_state.turn <= 10:
        next_turn()
        st.rerun()

st.write("")

# 설정 영역
st.markdown('<div class="section-title">게임 설정</div>', unsafe_allow_html=True)

reset_col1, reset_col2 = st.columns([2, 1])

with reset_col1:
    init_cash = st.number_input("시작 소지금 설정 (원)", min_value=1000, value=st.session_state.get("start_cash", 1_000_000), step=100_000)

with reset_col2:
    st.write("")
    st.write("")
    if st.button("게임 초기화 / 적용", use_container_width=True):
        new_game(init_cash)
        st.rerun()

st.caption("※ 지문 해석과 달리 20% 확률로 역발상 차익실현 장세가 펼쳐지거나, 미언급 종목도 독립적으로 변동합니다.")

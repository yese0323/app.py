import streamlit as st
import random
import pandas as pd

# ==============================
# 기본 설정
# ==============================

st.set_page_config(
    page_title="STOCK TYCOON : HARDCORE MARKET",
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

/* 돌발 특수 이벤트 대형 박스 (폭락 전용) */
.flash-event-box-crash {
    background: #fef2f2;
    border: 3px solid #dc2626;
    border-radius: 20px;
    padding: 25px 30px;
    margin-top: 15px;
    margin-bottom: 20px;
    box-shadow: 0 10px 25px rgba(220, 38, 38, 0.2);
}

.flash-badge-crash {
    display: inline-block;
    background: #dc2626;
    color: #ffffff;
    font-size: 14px;
    font-weight: 900;
    padding: 6px 14px;
    border-radius: 6px;
    margin-bottom: 12px;
    letter-spacing: 1px;
}

.flash-title-crash {
    font-size: 26px;
    font-weight: 900;
    color: #991b1b;
    margin-bottom: 10px;
}

.flash-text-crash {
    font-size: 16px;
    color: #7f1d1d;
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
# 게임 데이터 정의
# ==============================

STOCKS = {
    "삼성전자": 70000,
    "SK하이닉스": 120000,
    "카카오": 50000,
    "테슬라": 300000,
    "엔비디아": 180000
}

# 뉴스 데이터베이스 (중복 없이 순차 추출)
EXAM_NEWS_POOL = [
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
    },
    {
        "code": "HARD-05 (재고 및 기저효과)",
        "title": "[분석 지문] 메모리 반도체 덤핑 재고 소진 완료와 착시 효과",
        "text": """장기 불황을 이끌었던 메모리 반도체 재고가 감산 정책으로 완전 소진되며 고정 거래가가 반등하였다. 그러나 이는 실제 완제품 소비 증가가 아닌 공급 통제에 따른 착시 효과이다.""",
        "effects": {"SK하이닉스": (30, 50), "삼성전자": (10, 25), "엔비디아": (-20, -5)}
    },
    {
        "code": "HARD-06 (망사용료 법안)",
        "title": "[분석 지문] 초거대 AI 망사용료 의무화 통과 및 IDC 차별화",
        "text": """국회 본회의에서 트래픽 다량 발생 기업 대상 고율의 망 이용 대가 부과 법안이 통과되었다. 자체 IDC 국산화율이 높은 국내 플랫폼만 비용을 방어할 것으로 전망된다.""",
        "effects": {"카카오": (30, 50), "엔비디아": (-20, -5), "테슬라": (-10, 0)}
    }
]

# 💥 무조건 폭락하는 재앙급 악재 이벤트 3종 포함!
FLASH_EVENTS = [
    {
        "title": "💥 [지정학적 재앙] 제3차 세계대전 발발 및 중동 원유 공급 완전 봉쇄!",
        "text": "주요 원유 수송로가 기습 봉쇄되며 유가가 400% 폭등하고 국제 수송망이 완전 마비되었습니다! 금융 시장에 매수세가 완전히 사라지고 전 종목이 궤멸 수준으로 무조건 폭락합니다.",
        "effects": {"삼성전자": -50, "SK하이닉스": -55, "카카오": -60, "테슬라": -45, "엔비디아": -50}
    },
    {
        "title": "📉 [금융 시스템 마비] 글로벌 대형 자산운용사 연쇄 파산 & 뱅크런 사태!",
        "text": "월가 초대형 자산운용사의 기습 파산 선언으로 금융권 유동성이 완전 마비되었습니다. 자금 회수를 위한 전 세계적 강제 청산 매물이 쏟아지며 전 종목 무조건 폭락합니다.",
        "effects": {"삼성전자": -35, "SK하이닉스": -40, "카카오": -55, "테슬라": -40, "엔비디아": -45}
    },
    {
        "title": "⚠️ [기술 패러다임 붕괴] 글로벌 데이터센터 초대형 사이버 테러 발생!",
        "text": "전 세계 클라우드 infrastructure가 무력화되며 빅테크/반도체 기업들의 핵심 데이터가 영구 멸실되었습니다. 기술주 전체에 사상 최대 규모의 무조건 폭락이 몰아칩니다.",
        "effects": {"삼성전자": -40, "SK하이닉스": -45, "카카오": -50, "테슬라": -50, "엔비디아": -65}
    },
    {
        "title": "🚀 [호재 서프라이즈] 중동 오일머니 100조 원 기습 유입!",
        "text": "국부펀드의 자산 재배분 결정으로 전 종목 시가 매수 주문이 쏟아지며 전 종목 폭발적 상승을 기록합니다.",
        "effects": {"삼성전자": 45, "SK하이닉스": 50, "카카오": 40, "테슬라": 55, "엔비디아": 60}
    }
]


# ==============================
# 게임 초기화 (뉴스 덱 셔플 적용)
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
    
    # 중복 방지를 위해 뉴스 덱을 새로 섞음
    news_deck = EXAM_NEWS_POOL.copy()
    random.shuffle(news_deck)
    st.session_state.news_deck = news_deck
    
    st.session_state.current_news = st.session_state.news_deck.pop()
    st.session_state.flash_event = None


if "cash" not in st.session_state:
    new_game(1_000_000)


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
# 턴 진행 로직
# ==============================

def next_turn():
    st.session_state.history.append(total_asset())
    
    current_effects = st.session_state.current_news["effects"]
    
    # 20% 확률로 돌발 특수 이벤트(폭락/급등) 발동
    is_flash_triggered = random.random() < 0.20
    flash_data = None
    if is_flash_triggered:
        flash_data = random.choice(FLASH_EVENTS)
        st.session_state.flash_event = flash_data
    else:
        st.session_state.flash_event = None

    changes = {}

    for stock in STOCKS:
        # 1. 지문 언급 종목 분석
        if stock in current_effects:
            min_p, max_p = current_effects[stock]
            base_change = random.randint(min_p, max_p)
            
            # 20% 확률로 역발상 차익실현 장세 (지문과 반대 변동)
            if random.random() < 0.20:
                base_change = -base_change
        else:
            # 지문 미언급 종목 무작위 독립 변동 (±15%)
            base_change = random.randint(-15, 15)
        
        # 돌발 이벤트 변동 합산
        flash_change = flash_data["effects"].get(stock, 0) if flash_data else 0
        
        # 시장 무작위 잡음 (±5%)
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
        # 남은 뉴스 덱에서 중복 없이 꺼내기 (부족할 경우 다시 리필)
        if not st.session_state.news_deck:
            st.session_state.news_deck = EXAM_NEWS_POOL.copy()
            random.shuffle(st.session_state.news_deck)
        st.session_state.current_news = st.session_state.news_deck.pop()


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

st.markdown('<div class="title-box"><div class="title">STOCK TYCOON : HARDCORE</div><div class="subtitle">돌발 폭락 재앙과 예측불허 시황 속에서 자산을 지켜내세요!</div></div>', unsafe_allow_html=True)

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
# 돌발 특수 이벤트 표출
# ==============================

if st.session_state.flash_event:
    fe = st.session_state.flash_event
    st.markdown(f"""
    <div class="flash-event-box-crash">
        <div class="flash-badge-crash">FLASH EVENT - 돌발 악재/이슈 발생!</div>
        <div class="flash-title-crash">{fe['title']}</div>
        <div class="flash-text-crash">{fe['text']}</div>
    </div>
    """, unsafe_allow_html=True)


# ==============================
# 뉴스 지문 표출
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
st.markdown('<div class="section-title">최근 거래 기록</div>', unsafe_allow_html=True)

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

st.caption("※ 20% 확률로 전 종목 폭락 등의 무서운 돌발 악재 이벤트가 발동할 수 있습니다.")

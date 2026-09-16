import streamlit as st
import random
import pandas as pd

# ==============================
# 기본 설정 (가로 와이드 레이아웃)
# ==============================

st.set_page_config(
    page_title="STOCK TYCOON : WIDE DASHBOARD",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS - 가로형 대시보드 전용 스타일
# ==============================

st.markdown("""
<style>
.stApp { background-color: #f8fafc; }
.block-container { max-width: 100%; padding: 15px 25px; }

/* 상단 매직 바 */
.top-bar {
    background: #0f172a;
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* 대시보드 카드 */
.dash-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 15px;
    margin-bottom: 12px;
}

.card-title {
    font-size: 15px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 8px;
}

/* 돌발 폭락/급등 이벤트 박스 */
.flash-card-crash {
    background: #fef2f2;
    border: 2px solid #ef4444;
    border-radius: 12px;
    padding: 12px 15px;
    margin-bottom: 12px;
}
.flash-title-crash { color: #991b1b; font-weight: 800; font-size: 15px; }
.flash-text-crash { color: #7f1d1d; font-size: 13px; margin-top: 4px; }

/* 지문 박스 */
.news-box {
    background: white;
    border-left: 4px solid #0f172a;
    border-radius: 8px;
    padding: 12px 15px;
    font-size: 13px;
    color: #334155;
    line-height: 1.6;
    white-space: pre-line;
}

/* 주식 세로/가로 리스트 */
.stock-row {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
}

.stButton > button { min-height: 38px; border-radius: 8px; font-weight: 700; }
.stNumberInput input { min-height: 38px; }
</style>
""", unsafe_allow_html=True)


# ==============================
# 게임 데이터 (완화된 변동 범위 적용)
# ==============================

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
        "title": "[분석 지문] 기준금리 인하 기조 속 시중 유동성 흡수",
        "text": "중앙은행이 금리를 인하했으나 역레포 금리를 상향하여 유동성을 흡수함. 자금이 IT/플랫폼에서 채권형 자산으로 이동하는 반면 완성차 제조 단가 부담은 완화됨.",
        "effects": {"삼성전자": (-12, -4), "SK하이닉스": (-15, -5), "카카오": (-18, -6), "테슬라": (5, 15)}
    },
    {
        "code": "HARD-02 (기술 패러다임)",
        "title": "[분석 지문] AI CAPEX 과잉 투자 회의론과 ASIC 전환",
        "text": "빅테크 기업들이 범용 GPU 구매를 줄이고 자체 ASIC 반도체 생산을 확대함. 독점 기업에는 악재이나 위탁 생산 대기업에는 대체 수주 기회가 열림.",
        "effects": {"엔비디아": (-20, -8), "삼성전자": (8, 20), "SK하이닉스": (-5, 5)}
    },
    {
        "code": "HARD-03 (통화 및 무역)",
        "title": "[분석 지문] 강달러 오버슈팅 및 반덤핑 상계관세 부과",
        "text": "환율 급등 속 한국산 반도체/소프트웨어에 30% 상계관세 부과. 국장 테크주는 타격을 입으나 외화 자산 비율이 높은 해외 빅테크로 수급이 쏠림.",
        "effects": {"삼성전자": (-12, -4), "카카오": (-15, -5), "테슬라": (10, 22), "엔비디아": (8, 18)}
    },
    {
        "code": "HARD-04 (안보 및 규제)",
        "title": "[분석 지문] 자율주행 데이터 안보법 및 희토류 수출 통제",
        "text": "원자재 수출 국가의 희토류 제한과 자율주행 데이터 반출 금지로 완성차 기업의 생산 원가 폭등 및 주행 학습 마비가 우려됨.",
        "effects": {"테슬라": (-22, -10), "엔비디아": (-8, -2), "카카오": (5, 12)}
    }
]

# 돌발 이벤트 (고정값이 아닌 범위 지정)
FLASH_EVENTS = [
    {
        "title": "💥 [돌발 악재] 지정학적 리스크 및 원자재 수송 차질",
        "text": "주요 수송로 봉쇄 우려로 금융 시장 매수세가 감소하며 시장 전체가 약세를 보입니다.",
        "effects": {"삼성전자": (-20, -8), "SK하이닉스": (-22, -10), "카카오": (-25, -12), "테슬라": (-18, -6), "엔비디아": (-20, -8)}
    },
    {
        "title": "📉 [돌발 악재] 글로벌 투자은행 자산 매각 공시",
        "text": "대형 운용사의 자금 회수용 강제 매물이 쏟아지며 주요 종목 주가가 일시 하락합니다.",
        "effects": {"삼성전자": (-15, -5), "SK하이닉스": (-18, -6), "카카오": (-20, -8), "테슬라": (-15, -5), "엔비디아": (-18, -6)}
    },
    {
        "title": "🚀 [돌발 호재] 중동 국부펀드 글로벌 테크 수급 유입",
        "text": "대규모 자산 재배분으로 기술주 매수 주문이 유입되어 주가가 일시 상승합니다.",
        "effects": {"삼성전자": (8, 20), "SK하이닉스": (10, 22), "카카오": (6, 18), "테슬라": (12, 25), "엔비디아": (15, 28)}
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
    
    news_deck = EXAM_NEWS_POOL.copy()
    random.shuffle(news_deck)
    st.session_state.news_deck = news_deck
    st.session_state.current_news = st.session_state.news_deck.pop()
    st.session_state.flash_event = None


if "cash" not in st.session_state:
    new_game(1_000_000)


def total_asset():
    stock_value = sum(st.session_state.prices[stock] * st.session_state.holdings[stock] for stock in STOCKS)
    return st.session_state.cash + stock_value


def profit_rate():
    start = st.session_state.get("start_cash", 1_000_000)
    return ((total_asset() - start) / start * 100) if start > 0 else 0.0


def buy_stock(stock, amount):
    cost = st.session_state.prices[stock] * amount
    if amount <= 0: return
    if cost > st.session_state.cash:
        st.error("현금이 부족합니다.")
        return
    st.session_state.cash -= cost
    st.session_state.holdings[stock] += amount
    st.session_state.buy_costs[stock] += cost
    st.session_state.trade_history.insert(0, f"매수 | {stock} {amount}주 | ₩{cost:,}")


def sell_stock(stock, amount):
    if amount <= 0 or amount > st.session_state.holdings[stock]:
        st.error("수량이 올바르지 않습니다.")
        return
    price = st.session_state.prices[stock]
    revenue = price * amount
    avg_price = st.session_state.buy_costs[stock] / st.session_state.holdings[stock]
    st.session_state.buy_costs[stock] -= int(avg_price * amount)
    st.session_state.cash += revenue
    st.session_state.holdings[stock] -= amount
    st.session_state.trade_history.insert(0, f"매도 | {stock} {amount}주 | ₩{revenue:,}")


# ==============================
# 턴 진행 로직 (랜덤 수치 반영)
# ==============================

def next_turn():
    st.session_state.history.append(total_asset())
    current_effects = st.session_state.current_news["effects"]
    
    # 20% 확률로 돌발 이벤트
    is_flash = random.random() < 0.20
    flash_data = random.choice(FLASH_EVENTS) if is_flash else None
    st.session_state.flash_event = flash_data

    changes = {}
    for stock in STOCKS:
        # 1. 지문 기본 영향범위에서 무작위 퍼센트 추출
        if stock in current_effects:
            min_p, max_p = current_effects[stock]
            base_change = random.randint(min_p, max_p)
            if random.random() < 0.15: # 15% 역발상
                base_change = -base_change
        else:
            base_change = random.randint(-6, 6) # 미언급 종목 소폭 무작위 변동
        
        # 2. 돌발 이벤트 범위에서 무작위 퍼센트 추출
        flash_change = 0
        if flash_data and stock in flash_data["effects"]:
            f_min, f_max = flash_data["effects"][stock]
            flash_change = random.randint(f_min, f_max)
            
        noise = random.randint(-2, 2) # 시장 소음 완화 (±2%)
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
        if not st.session_state.news_deck:
            st.session_state.news_deck = EXAM_NEWS_POOL.copy()
            random.shuffle(st.session_state.news_deck)
        st.session_state.current_news = st.session_state.news_deck.pop()


# ==============================
# 게임 종료
# ==============================

if st.session_state.game_over:
    st.balloons()
    st.title("🏆 최종 투자 결과")
    st.metric("최종 총 자산", f"₩{total_asset():,}", f"{profit_rate():+.2f}%")
    if st.button("다시 도전하기"):
        new_game(st.session_state.start_cash)
        st.rerun()
    st.stop()


# ==============================
# 메인 가로형 2-Column 대시보드 UI
# ==============================

asset = total_asset()
profit = profit_rate()

# 상단 대시보드 상태바
st.markdown(f"""
<div class="top-bar">
    <span style="font-size:20px; font-weight:800;">📈 STOCK TYCOON DASHBOARD</span>
    <span><b>턴:</b> {min(st.session_state.turn, 10)} / 10 | <b>현금:</b> ₩{st.session_state.cash:,} | <b>총 자산:</b> ₩{asset:,} ({profit:+.2f}%)</span>
</div>
""", unsafe_allow_html=True)

# 좌/우 가로 레이아웃 분할 (왼쪽 5 : 오른쪽 7)
left_col, right_col = st.columns([5, 7])

# --- [왼쪽 컬럼: 지문 분석 & 차트 & 이벤트] ---
with left_col:
    # 돌발 이벤트 표출
    if st.session_state.flash_event:
        fe = st.session_state.flash_event
        st.markdown(f"""
        <div class="flash-card-crash">
            <div class="flash-title-crash">⚡ {fe['title']}</div>
            <div class="flash-text-crash">{fe['text']}</div>
        </div>
        """, unsafe_allow_html=True)

    # 지문 카드
    news = st.session_state.current_news
    st.markdown(f"""
    <div class="dash-card">
        <div class="card-title">📄 시장 분석 지문 ({news['code']})</div>
        <div style="font-weight:700; color:#0f172a; margin-bottom:6px;">{news['title']}</div>
        <div class="news-box">{news['text']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 턴 진행 버튼
    if st.button("지문 분석 완료 ➔ 다음 턴 결과 반영", type="primary", use_container_width=True):
        if st.session_state.turn <= 10:
            next_turn()
            st.rerun()

    # 주가 추이 차트
    st.markdown('<div class="dash-card"><div class="card-title">📊 주가 변동 추이</div>', unsafe_allow_html=True)
    history_df = pd.DataFrame(st.session_state.price_history)
    history_df.index = [f"{i}턴" for i in range(len(history_df))]
    st.line_chart(history_df, height=220, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --- [오른쪽 컬럼: 주식 시장 & 매매 컨트롤] ---
with right_col:
    st.markdown('<div class="card-title" style="font-size:17px;">🏪 주식 거래소</div>', unsafe_allow_html=True)
    
    # 5개 종목 가로/세로 통합 리스트
    for stock in STOCKS:
        price = st.session_state.prices[stock]
        change = st.session_state.last_changes[stock]
        holding = st.session_state.holdings[stock]
        buy_cost = st.session_state.buy_costs[stock]
        
        if holding > 0:
            avg_price = int(buy_cost / holding)
            s_profit = ((price - avg_price) / avg_price) * 100
            p_color = "#e11d48" if s_profit > 0 else ("#2563eb" if s_profit < 0 else "#64748b")
            p_str = f"평단 ₩{avg_price:,} ({s_profit:+.1f}%)"
        else:
            p_color = "#64748b"
            p_str = "미보유"

        # 가로형 종목 행 구성 (종목정보 | 보유 현황 | 수량 입력 | 매수/매도 버튼)
        st_c1, st_c2, st_c3, st_c4, st_c5 = st.columns([3, 3, 2, 1.5, 1.5])
        
        with st_c1:
            st.markdown(f"**{stock}**  \n₩{price:,} ({change:+d}%)")
        with st_c2:
            st.markdown(f"보유: **{holding:,}주**  \n<span style='color:{p_color}; font-size:12px;'>{p_str}</span>", unsafe_allow_html=True)
        with st_c3:
            amount = st.number_input("수량", min_value=1, value=1, key=f"amt_{stock}", label_visibility="collapsed")
        with st_c4:
            if st.button("매수", key=f"b_{stock}", use_container_width=True):
                buy_stock(stock, amount)
                st.rerun()
        with st_c5:
            if st.button("매도", key=f"s_{stock}", use_container_width=True):
                sell_stock(stock, amount)
                st.rerun()
        
        st.divider()

    # 최근 거래 기록 요약
    if st.session_state.trade_history:
        st.caption(f"최근 거래: {st.session_state.trade_history[0]}")

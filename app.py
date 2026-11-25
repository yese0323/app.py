import streamlit as st
import random
import pandas as pd

# ==========================================
# 1. 기본 설정
# ==========================================

st.set_page_config(
    page_title="STOCK TYCOON",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DEFAULT_STARTING_CASH = 1_000_000
MAX_TURNS = 5

MAX_LOAN = 500_000

STOCKS = {
    "엔비디아": 70000,
    "테슬라": 120000,
    "삼성": 50000
}

DOGECOIN = "도지코인"
DOGECOIN_START_PRICE = 1000
DOGECOIN_DELIST_PROBABILITY = 0.10

ALL_ASSETS = list(STOCKS.keys()) + [DOGECOIN]


# ==========================================
# 2. 화면 디자인
# ==========================================

st.markdown("""
<style>
header, footer, #MainMenu { visibility: hidden; }
.block-container {
    padding: 0.25rem 0.55rem 0.2rem 0.55rem !important;
    max-width: 100% !important;
}
h1 { font-size: 21px !important; margin: 0 0 2px 0 !important; }
h2 { font-size: 15px !important; margin: 2px 0 !important; }
h3 { font-size: 12px !important; margin: 1px 0 !important; }
p, label, .stCaption, [data-testid="stMarkdownContainer"] { font-size: 10px !important; }
div[data-testid="stVerticalBlock"] { gap: 0.12rem !important; }
div[data-testid="stHorizontalBlock"] { gap: 0.35rem !important; }
div[data-testid="stMetric"] {
    padding: 2px 5px !important;
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 7px;
}
div[data-testid="stMetricValue"] { font-size: 14px !important; }
div[data-testid="stMetricLabel"] { font-size: 9px !important; }
.stButton button { min-height: 24px !important; padding: 0 4px !important; font-size: 9px !important; }
.stNumberInput input { height: 27px !important; font-size: 10px !important; }
.doge-panel {
    background: linear-gradient(115deg, #fff3a6 0%, #ffd84d 48%, #f5b800 100%) !important;
    border: 2px solid #d99a00 !important;
    color: #352600 !important;
    padding: 6px 9px !important; margin: 2px 0 !important;
    border-radius: 9px;
    box-shadow: 0 2px 10px rgba(218, 160, 0, 0.28);
}
.doge-dead {
    background: linear-gradient(115deg, #350909, #790d0d, #a51c1c) !important;
    border: 2px solid #ff5252 !important;
    color: white !important;
    padding: 6px 9px !important; margin: 2px 0 !important;
    border-radius: 9px;
}
.doge-title { font-size: 15px !important; font-weight: 900 !important; color: #4a3500 !important; }
.doge-price { font-size: 20px !important; margin-top: 0 !important; color: #2d2100 !important; font-weight: 900 !important; }
.doge-sub, .doge-warning { font-size: 9px !important; margin-top: 2px !important; padding: 3px 5px !important; color: #3d2c00 !important; }
.doge-warning {
    background: rgba(255,255,255,0.38) !important;
    border: 1px solid rgba(110,75,0,0.22) !important;
    border-radius: 5px;
}
.stock-card { padding: 4px 6px !important; margin-bottom: 1px !important; border-radius: 7px; }
.news-card { padding: 4px 6px !important; margin-bottom: 2px !important; }
.loan-panel { padding: 6px 8px !important; margin: 2px 0 !important; }
hr { margin: 3px 0 !important; }
[data-testid="stProgress"] { height: 5px !important; }
[data-testid="stAlert"] { padding: 5px 8px !important; }
[data-testid="stExpander"] details { padding: 2px 6px !important; }
@media screen and (orientation: landscape) and (min-width: 700px) {
    .block-container { padding: 0.15rem 0.4rem 0.1rem 0.4rem !important; }
}
@media screen and (max-height: 800px) and (orientation: landscape) {
    .block-container { padding-top: 0.05rem !important; padding-bottom: 0.05rem !important; }
    h1 { font-size: 18px !important; }
    h2 { font-size: 13px !important; }
    p, label, .stCaption, [data-testid="stMarkdownContainer"] { font-size: 9px !important; }
    div[data-testid="stMetricValue"] { font-size: 12px !important; }
    .doge-panel, .doge-dead { padding: 4px 7px !important; }
    .doge-price { font-size: 17px !important; }
    .stButton button { min-height: 21px !important; }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. 게임 초기화
# ==========================================

def initialize_game(starting_cash=DEFAULT_STARTING_CASH):
    starting_cash = max(1, int(starting_cash))
    st.session_state.starting_cash = starting_cash
    st.session_state.game_started = True
    st.session_state.cash = starting_cash

    st.session_state.prices = {
        **STOCKS,
        DOGECOIN: DOGECOIN_START_PRICE
    }

    st.session_state.holdings = {
        asset: 0 for asset in ALL_ASSETS
    }

    st.session_state.turn = 1
    st.session_state.history = []
    st.session_state.price_history = []

    st.session_state.market_news = (
        "시장 개장 전. 첫 번째 시장 동향을 확인하세요."
    )
    st.session_state.pending_news_event = None

    st.session_state.doge_notice = (
        "도지코인은 매 턴 독립적으로 변동합니다."
    )

    st.session_state.doge_last_change = 0
    st.session_state.dogecoin_delisted = False
    st.session_state.game_over = False

    # 대출 관련 데이터
    st.session_state.loan_debt = 0
    st.session_state.loan_prompt_open = False

    st.session_state.price_history.append({
        asset: st.session_state.prices[asset]
        for asset in ALL_ASSETS
    })


if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.starting_cash = DEFAULT_STARTING_CASH
    st.session_state.pending_news_event = None


# ==========================================
# 4. 계산 함수
# ==========================================

def get_gross_asset():
    total = st.session_state.cash

    for asset in ALL_ASSETS:
        total += (
            st.session_state.holdings[asset]
            * st.session_state.prices[asset]
        )

    return total


def get_total_asset():
    # 대출금은 빚이므로 순자산에서 차감
    return get_gross_asset() - st.session_state.loan_debt


def format_money(value):
    return f"{int(value):,}원"


def add_history(message):
    st.session_state.history.insert(0, message)
    st.session_state.history = st.session_state.history[:8]


# ==========================================
# 5. 매수 함수
# ==========================================

def buy_stock(asset, quantity):
    if st.session_state.game_over:
        return

    if asset == DOGECOIN and st.session_state.dogecoin_delisted:
        st.error("상장폐지된 도지코인은 거래할 수 없습니다.")
        return

    if quantity <= 0:
        st.warning("수량을 확인하세요.")
        return

    price = st.session_state.prices[asset]
    total = price * quantity

    if total > st.session_state.cash:
        st.warning("보유 현금이 부족합니다.")
        return

    st.session_state.cash -= total
    st.session_state.holdings[asset] += quantity

    add_history(
        f"{asset} {quantity}개 매수 | -{format_money(total)}"
    )

    st.rerun()


# ==========================================
# 6. 매도 함수
# ==========================================

def sell_stock(asset, quantity):
    if st.session_state.game_over:
        return

    if asset == DOGECOIN and st.session_state.dogecoin_delisted:
        st.error("상장폐지된 도지코인은 거래할 수 없습니다.")
        return

    if quantity <= 0:
        st.warning("수량을 확인하세요.")
        return

    if quantity > st.session_state.holdings[asset]:
        st.warning("보유 수량이 부족합니다.")
        return

    price = st.session_state.prices[asset]
    total = price * quantity

    st.session_state.cash += total
    st.session_state.holdings[asset] -= quantity

    add_history(
        f"{asset} {quantity}개 매도 | +{format_money(total)}"
    )

    st.rerun()


# ==========================================
# 7. 풀매수 함수
# ==========================================

def buy_all(asset):
    if st.session_state.game_over:
        return

    if asset == DOGECOIN and st.session_state.dogecoin_delisted:
        st.error("상장폐지된 도지코인은 거래할 수 없습니다.")
        return

    price = st.session_state.prices[asset]

    if price <= 0:
        st.warning("현재 거래할 수 없는 종목입니다.")
        return

    max_quantity = st.session_state.cash // price

    if max_quantity <= 0:
        st.warning("매수할 현금이 부족합니다.")
        return

    buy_stock(asset, max_quantity)


# ==========================================
# 8. 풀매도 함수
# ==========================================

def sell_all(asset):
    if st.session_state.game_over:
        return

    if asset == DOGECOIN and st.session_state.dogecoin_delisted:
        st.error("상장폐지된 도지코인은 거래할 수 없습니다.")
        return

    quantity = st.session_state.holdings[asset]

    if quantity <= 0:
        st.warning("매도할 보유 수량이 없습니다.")
        return

    sell_stock(asset, quantity)


# ==========================================
# 9. 대출 시스템
# ==========================================

def get_remaining_loan():
    return MAX_LOAN - st.session_state.loan_debt


def take_loan(amount):
    if st.session_state.game_over:
        return

    remaining = get_remaining_loan()

    if amount <= 0:
        st.warning("대출 금액을 확인하세요.")
        return

    if amount > remaining:
        st.warning("대출 가능 한도를 초과했습니다.")
        return

    st.session_state.cash += amount
    st.session_state.loan_debt += amount

    st.session_state.loan_prompt_open = False

    add_history(
        f"대출 실행 | +{format_money(amount)}"
    )

    st.success(
        f"{format_money(amount)} 대출이 완료되었습니다."
    )

    st.rerun()


# ==========================================
# 10. 뉴스 이벤트
# ==========================================

NEWS_EVENTS = [
    # 엔비디아 - 기존 호재 및 악재
    {"asset": "엔비디아", "news": "가속기 수요, 공급능력 상회", "min_change": 0.03, "max_change": 0.10},
    {"asset": "엔비디아", "news": "핵심 경영진 복귀설 재부상", "min_change": 0.05, "max_change": 0.15},
    {"asset": "엔비디아", "news": "차세대 칩 수율, 시장 기대 하회", "min_change": -0.12, "max_change": -0.05},
    {"asset": "엔비디아", "news": "대형 고객사 CAPEX 재검토", "min_change": -0.20, "max_change": -0.10},

    # 엔비디아 - 추가된 복합 변수 뉴스
    {"asset": "엔비디아", "news": "클라우드 사업자, AI 인프라 투자 집행 시점 조정", "min_change": -0.18, "max_change": 0.20},
    {"asset": "엔비디아", "news": "차세대 가속기 공급 확대…수익성 검증은 미완", "min_change": -0.17, "max_change": 0.19},
    {"asset": "엔비디아", "news": "수출 규정 재검토 속 중국향 제품 전략 수정", "min_change": -0.20, "max_change": 0.17},
    {"asset": "엔비디아", "news": "대형 고객사 자체 칩 개발과 외부 조달 병행", "min_change": -0.19, "max_change": 0.18},

    # 테슬라 - 기존 호재 및 악재
    {"asset": "테슬라", "news": "전기차 수요 둔화 우려 완화", "min_change": 0.03, "max_change": 0.10},
    {"asset": "테슬라", "news": "차세대 로드스터 양산 가시화", "min_change": 0.05, "max_change": 0.15},
    {"asset": "테슬라", "news": "우주사업 규제 변수 확대", "min_change": -0.12, "max_change": -0.05},
    {"asset": "테슬라", "news": "수입차 관세 부담 급증", "min_change": -0.20, "max_change": -0.10},

    # 테슬라 - 추가된 복합 변수 뉴스
    {"asset": "테슬라", "news": "차량 인도량 반등에도 평균 판매단가 하락 지속", "min_change": -0.19, "max_change": 0.22},
    {"asset": "테슬라", "news": "자율주행 규제 완화 논의…책임 기준은 불확실", "min_change": -0.18, "max_change": 0.22},
    {"asset": "테슬라", "news": "에너지저장장치 수주 증가와 원가 부담 동반", "min_change": -0.12, "max_change": 0.19},
    {"asset": "테슬라", "news": "신공장 가동률 개선 전망 속 초기 비용 확대", "min_change": -0.15, "max_change": 0.19},

    # 삼성 - 기존 호재 및 악재
    {"asset": "삼성", "news": "차세대 메모리 공급계약 확대", "min_change": 0.03, "max_change": 0.10},
    {"asset": "삼성", "news": "경쟁사 신제품 품질 논란 확산", "min_change": 0.05, "max_change": 0.15},
    {"asset": "삼성", "news": "반도체 정책 리스크 재부각", "min_change": -0.12, "max_change": -0.05},
    {"asset": "삼성", "news": "모바일 품질 신뢰도 타격", "min_change": -0.20, "max_change": -0.10},

    # 삼성 - 추가된 복합 변수 뉴스
    {"asset": "삼성", "news": "HBM 공급 승인 임박설…양산 수율은 미확인", "min_change": -0.18, "max_change": 0.22},
    {"asset": "삼성", "news": "파운드리 수주 회복 조짐과 고정비 부담 공존", "min_change": -0.14, "max_change": 0.18},
    {"asset": "삼성", "news": "메모리 가격 반등 전망…재고 정상화 속도 변수", "min_change": -0.17, "max_change": 0.19},
    {"asset": "삼성", "news": "대규모 설비투자 계획 공개, 현금흐름 전망 엇갈려", "min_change": -0.20, "max_change": 0.27}

]


def prepare_market_news():
    # 다음 턴에 반영될 뉴스를 미리 선정해 공개
    event = random.choice(NEWS_EVENTS)
    st.session_state.pending_news_event = event
    st.session_state.market_news = (
        f"[{event['asset']}] {event['news']}"
    )


# 첫 게임 시작 또는 초기화 직후 첫 번째 뉴스를 준비
if st.session_state.pending_news_event is None:
    prepare_market_news()

# ==========================================
# 11. 다음 턴 진행
# ==========================================

def next_turn():
    if st.session_state.game_over:
        return

    if st.session_state.turn >= MAX_TURNS:
        st.session_state.game_over = True
        st.rerun()

    # 일반 주식 기본 가격 변동: 상승보다 하락 폭을 조금 더 크게 설정
    for asset in STOCKS:
        if random.random() < 0.5:
            random_change = random.uniform(0.01, 0.05)
        else:
            random_change = random.uniform(-0.07, -0.02)

        new_price = int(
            st.session_state.prices[asset] * (1 + random_change)
        )
        st.session_state.prices[asset] = max(1, new_price)

    # 미리 공개된 뉴스를 이번 턴의 주가에 반영
    event = st.session_state.pending_news_event
    news_asset = event["asset"]
    news_change = random.uniform(event["min_change"], event["max_change"])
    news_base_price = st.session_state.prices[news_asset]
    news_new_price = int(news_base_price * (1 + news_change))
    st.session_state.prices[news_asset] = max(1, news_new_price)

    # 도지코인 독립 이벤트
    if not st.session_state.dogecoin_delisted:

        if random.random() < DOGECOIN_DELIST_PROBABILITY:

            st.session_state.dogecoin_delisted = True
            st.session_state.prices[DOGECOIN] = 0
            st.session_state.doge_last_change = -100

            st.session_state.doge_notice = (
                "상장폐지 발생! 도지코인 거래가 영구 중단되었습니다."
            )

            add_history("도지코인 상장폐지 발생!")

        else:
            change = random.uniform(-0.50, 0.50)

            old_price = st.session_state.prices[DOGECOIN]

            new_price = max(
                1,
                int(old_price * (1 + change))
            )

            st.session_state.prices[DOGECOIN] = new_price
            st.session_state.doge_last_change = change * 100

            st.session_state.doge_notice = (
                f"이번 턴 가격 변동: {change * 100:+.1f}%"
            )

    else:
        st.session_state.doge_notice = (
            "이미 상장폐지된 종목입니다."
        )

    # 턴 증가
    st.session_state.turn += 1

    # 가격 기록
    st.session_state.price_history.append({
        asset: st.session_state.prices[asset]
        for asset in ALL_ASSETS
    })

    # 게임 종료가 아니라면 다음 턴에 분석할 뉴스를 미리 공개
    if st.session_state.turn >= MAX_TURNS:
        st.session_state.game_over = True
    else:
        prepare_market_news()

    st.rerun()


# ==========================================
# 12. 제목
# ==========================================

st.title("STOCK TYCOON")
st.caption(
    f"가상의 주식 투자 시뮬레이션 | 시작 자금 {format_money(st.session_state.starting_cash)}"
    if st.session_state.game_started
    else "가상의 주식 투자 시뮬레이션 | 시작 자금을 설정하세요"
)

# 게임 시작 전 초기 자본 설정 화면
if not st.session_state.game_started:
    st.markdown("## 투자 시작 설정")
    st.write("이번 게임에서 사용할 초기 보유 금액을 입력하세요.")
    with st.form("start_game_form"):
        starting_cash_input = st.number_input(
            "초기 보유 금액 (원)",
            min_value=100_000,
            max_value=100_000_000,
            value=DEFAULT_STARTING_CASH,
            step=100_000,
            format="%d"
        )
        st.caption("최소 10만 원 · 최대 1억 원 · 5턴 동안 투자")
        start_submitted = st.form_submit_button(
            "게임 시작", type="primary", use_container_width=True
        )
        if start_submitted:
            initialize_game(starting_cash_input)
            st.rerun()
    st.stop()

# ==========================================
# 13. 게임 종료 화면
# ==========================================

if st.session_state.game_over:

    total = get_total_asset()
    profit = total - st.session_state.starting_cash
    rate = profit / st.session_state.starting_cash * 100

    st.subheader("투자 종료")

    a, b, c = st.columns(3)

    a.metric("최종 순자산", format_money(total))
    b.metric("수익", format_money(profit))
    c.metric("수익률", f"{rate:+.2f}%")

    if rate >= 80:
        grade = "S"
    elif rate >= 50:
        grade = "A"
    elif rate >= 20:
        grade = "B"
    elif rate >= -20:
        grade = "C"
    else:
        grade = "F"

    st.markdown(f"## 최종 등급: {grade}")

    if st.session_state.dogecoin_delisted:
        st.error("도지코인은 상장폐지되었습니다.")

    st.write(
        f"누적 대출금: {format_money(st.session_state.loan_debt)}"
    )

    st.subheader("최종 보유 자산")

    for asset in ALL_ASSETS:
        quantity = st.session_state.holdings[asset]
        value = quantity * st.session_state.prices[asset]

        st.write(
            f"**{asset}** | {quantity}개 | {format_money(value)}"
        )

    st.subheader("가격 변화 그래프")

    st.line_chart(
        pd.DataFrame(st.session_state.price_history)
    )

    if st.button("새 게임 시작", use_container_width=True):
        initialize_game(st.session_state.starting_cash)
        st.rerun()

    st.stop()


# ==========================================
# 14. 한 화면 대시보드 (태블릿 가로형)
# ==========================================

total_asset = get_total_asset()
profit = total_asset - st.session_state.starting_cash

# 상단 자산 요약
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("보유 현금", format_money(st.session_state.cash))
m2.metric("총 순자산", format_money(total_asset))
m3.metric("수익", format_money(profit))
m4.metric("진행 턴", f"{st.session_state.turn}/{MAX_TURNS}")
held = sum(1 for q in st.session_state.holdings.values() if q > 0)
m5.metric("보유 종목", f"{held}개")
m6.metric("누적 대출", format_money(st.session_state.loan_debt))
st.progress(st.session_state.turn / MAX_TURNS)

# 가로 화면을 좌측(거래)과 우측(뉴스/진행)으로 분리
trade_area, info_area = st.columns([2.25, 1], gap="small")

with trade_area:
    # 도지코인 패널
    st.markdown("### SPECIAL ASSET · DOGECOIN")
    doge_price = st.session_state.prices[DOGECOIN]
    doge_quantity = st.session_state.holdings[DOGECOIN]
    doge_value = doge_price * doge_quantity

    if st.session_state.dogecoin_delisted:
        st.markdown(
            f'''<div class="doge-dead">
                <b>DOGECOIN | 상장폐지</b>　<strong style="font-size:19px">0원</strong><br>
                <span>거래 영구 중단 · 보유 {doge_quantity}개 · 평가 {format_money(doge_value)}</span>
            </div>''', unsafe_allow_html=True
        )
    else:
        change = st.session_state.doge_last_change
        st.markdown(
            f'''<div class="doge-panel">
                <span class="doge-title">DOGECOIN</span>
                <span class="doge-price" style="margin-left:12px">{format_money(doge_price)}</span>
                <div class="doge-sub">이번 턴 변동률 {change:+.1f}%　|　보유 {doge_quantity}개　|　평가 {format_money(doge_value)}</div>
                <div class="doge-warning">상장폐지 위험: 매 턴 10%　|　일반 뉴스와 독립적으로 변동</div>
            </div>''', unsafe_allow_html=True
        )
        d1, d2, d3, d4, d5 = st.columns([1.2, 1, 1, 1, 1])
        with d1:
            doge_buy_quantity = st.number_input("도지 수량", min_value=1, value=1, key="doge_buy_quantity")
        with d2:
            if st.button("매수", key="doge_buy", use_container_width=True):
                buy_stock(DOGECOIN, doge_buy_quantity)
        with d3:
            if st.button("매도", key="doge_sell", use_container_width=True, disabled=doge_quantity <= 0):
                sell_stock(DOGECOIN, min(doge_buy_quantity, doge_quantity))
        with d4:
            if st.button("풀매수", key="doge_full_buy", use_container_width=True):
                buy_all(DOGECOIN)
        with d5:
            if st.button("풀매도", key="doge_full_sell", use_container_width=True, disabled=doge_quantity <= 0):
                sell_all(DOGECOIN)

    # 일반 주식 3종목을 가로 카드로 배치
    st.markdown("### 일반 주식")
    stock_columns = st.columns(3, gap="small")
    for index, asset in enumerate(STOCKS):
        with stock_columns[index]:
            price = st.session_state.prices[asset]
            owned = st.session_state.holdings[asset]
            st.markdown(
                f'''<div class="stock-card"><b>{asset}</b><br>
                <strong style="font-size:16px">{format_money(price)}</strong><br>
                <span>보유: {owned}주</span></div>''',
                unsafe_allow_html=True
            )
            quantity = st.number_input("수량", min_value=1, value=1, key=f"stock_quantity_{index}")
            b1, b2 = st.columns(2, gap="small")
            with b1:
                if st.button("매수", key=f"stock_buy_{index}", use_container_width=True):
                    buy_stock(asset, quantity)
                if st.button("풀매수", key=f"stock_full_buy_{index}", use_container_width=True):
                    buy_all(asset)
            with b2:
                if st.button("매도", key=f"stock_sell_{index}", use_container_width=True, disabled=owned <= 0):
                    sell_stock(asset, min(quantity, owned))
                if st.button("풀매도", key=f"stock_full_sell_{index}", use_container_width=True, disabled=owned <= 0):
                    sell_all(asset)

with info_area:
    # 순자산 0원 이하일 때만 대출 UI 표시
    loan_condition = get_total_asset() <= 0
    remaining_loan = get_remaining_loan()
    if loan_condition:
        st.markdown("### 자금 부족 · 대출")
        st.warning("순자산이 0원 이하입니다. 대출을 이용할 수 있습니다.")
        if remaining_loan > 0:
            if not st.session_state.loan_prompt_open:
                if st.button("대출 신청", type="primary", use_container_width=True):
                    st.session_state.loan_prompt_open = True
                    st.rerun()
            else:
                loan_amount = st.number_input(
                    "대출 금액", min_value=1, max_value=remaining_loan,
                    value=min(100000, remaining_loan), step=10000,
                    key="loan_amount_input"
                )
                lc1, lc2 = st.columns(2)
                with lc1:
                    if st.button("대출 확정", type="primary", use_container_width=True):
                        take_loan(loan_amount)
                with lc2:
                    if st.button("취소", use_container_width=True):
                        st.session_state.loan_prompt_open = False
                        st.rerun()
        else:
            st.error("대출 한도 500,000원을 모두 사용했습니다.")

    st.markdown("### 다음 턴 시장 뉴스")
    st.caption("뉴스를 분석한 뒤 턴을 진행하세요. 가격 변동은 다음 턴에 반영됩니다.")
    st.info(st.session_state.market_news)

    st.markdown("### 최근 거래")
    if st.session_state.history:
        for item in st.session_state.history[:4]:
            st.caption(item)
    else:
        st.caption("거래 내역 없음")

    st.markdown("### 게임 진행")
    if st.button("다음 턴 진행", type="primary", use_container_width=True):
        next_turn()
    if st.button("게임 초기화", use_container_width=True):
        initialize_game(st.session_state.starting_cash)
        st.rerun()

# 그래프는 기본 화면 공간을 차지하지 않도록 접어 둠
with st.expander("가격 변화 그래프", expanded=False):
    chart_df = pd.DataFrame(st.session_state.price_history)
    st.line_chart(chart_df, height=120)

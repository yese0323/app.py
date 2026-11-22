
import streamlit as st
import random
import pandas as pd

st.set_page_config(
    page_title="STOCK TYCOON",
    layout="wide",
    initial_sidebar_state="collapsed"
)

STARTING_CASH = 1_000_000
MAX_TURNS = 10

STOCKS = {
    "삼성전자": 70000,
    "SK하이닉스": 120000,
    "카카오": 50000
}

DOGECOIN = "도지코인"
DOGECOIN_START_PRICE = 1000
DOGECOIN_DELIST_PROBABILITY = 0.10
ALL_ASSETS = list(STOCKS.keys()) + [DOGECOIN]

# =========================
# CSS
# =========================

st.markdown("""
<style>
header, footer, #MainMenu {
    visibility: hidden;
}

.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0.3rem;
    padding-left: 1.2rem;
    padding-right: 1.2rem;
    max-width: 100%;
}

h1 {
    font-size: 25px !important;
    margin-bottom: 2px !important;
}

h2 {
    font-size: 19px !important;
}

h3 {
    font-size: 16px !important;
}

div[data-testid="stMetric"] {
    padding: 7px 10px;
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 9px;
}

div[data-testid="stMetricValue"] {
    font-size: 20px;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.35rem;
}

.stButton button {
    min-height: 34px;
    font-size: 12px;
}

.doge-panel {
    background: linear-gradient(115deg, #34270b, #76500d, #b77a13);
    border: 2px solid #e5ad35;
    border-radius: 16px;
    padding: 18px 20px;
    color: white;
    margin: 8px 0 10px 0;
    box-shadow: 0 4px 16px rgba(190,130,20,0.22);
}

.doge-title {
    font-size: 23px;
    font-weight: 900;
    letter-spacing: 1px;
}

.doge-price {
    font-size: 35px;
    font-weight: 900;
    margin-top: 5px;
    line-height: 1.2;
}

.doge-sub {
    font-size: 12px;
    opacity: 0.9;
    margin-top: 5px;
}

.doge-warning {
    background: rgba(0,0,0,0.22);
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 9px;
    padding: 8px 10px;
    font-size: 12px;
    margin-top: 10px;
}

.doge-dead {
    background: linear-gradient(115deg, #350909, #790d0d, #a51c1c);
    border: 2px solid #ff5252;
    border-radius: 16px;
    padding: 18px 20px;
    color: white;
    margin: 8px 0 10px 0;
}

.stock-card {
    border: 1px solid rgba(128,128,128,0.35);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 5px;
}

.news-card {
    border: 1px solid rgba(128,128,128,0.3);
    border-radius: 9px;
    padding: 9px 12px;
    margin-bottom: 8px;
}

hr {
    margin: 6px 0 !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# 초기화
# =========================

def initialize_game():
    st.session_state.cash = STARTING_CASH

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

    st.session_state.market_news = "시장이 개장했습니다. 투자를 시작하세요."
    st.session_state.doge_notice = "도지코인은 매 턴 독립적으로 변동합니다."
    st.session_state.doge_last_change = 0

    st.session_state.dogecoin_delisted = False
    st.session_state.game_over = False

    st.session_state.price_history.append({
        asset: st.session_state.prices[asset]
        for asset in ALL_ASSETS
    })


if "cash" not in st.session_state:
    initialize_game()


# =========================
# 계산
# =========================

def get_total_asset():
    total = st.session_state.cash

    for asset in ALL_ASSETS:
        total += (
            st.session_state.holdings[asset]
            * st.session_state.prices[asset]
        )

    return total


def format_money(value):
    return f"{int(value):,}원"


def add_history(message):
    st.session_state.history.insert(0, message)
    st.session_state.history = st.session_state.history[:6]


# =========================
# 거래
# =========================

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
        f"{asset} {quantity}주 매수 | -{format_money(total)}"
    )

    st.rerun()


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
        f"{asset} {quantity}주 매도 | +{format_money(total)}"
    )

    st.rerun()


# =========================
# 뉴스
# =========================

NEWS_EVENTS = [
    {
        "news": "반도체 산업 호황! 관련 기업 주가 상승",
        "effects": {
            "삼성전자": 1.10,
            "SK하이닉스": 1.15,
            "카카오": 0.98
        }
    },
    {
        "news": "IT 기업 투자 심리 악화! 기술주 하락",
        "effects": {
            "삼성전자": 0.97,
            "SK하이닉스": 0.94,
            "카카오": 0.90
        }
    },
    {
        "news": "국내 증시 상승세! 투자자들의 기대감 증가",
        "effects": {
            "삼성전자": 1.08,
            "SK하이닉스": 1.07,
            "카카오": 1.09
        }
    },
    {
        "news": "경기 침체 우려 확산! 시장 전반 하락",
        "effects": {
            "삼성전자": 0.92,
            "SK하이닉스": 0.91,
            "카카오": 0.93
        }
    },
    {
        "news": "특별한 시장 이슈 없음. 주가 소폭 변동",
        "effects": {
            "삼성전자": 1.00,
            "SK하이닉스": 1.00,
            "카카오": 1.00
        }
    }
]


# =========================
# 턴 진행
# =========================

def next_turn():
    if st.session_state.game_over:
        return

    if st.session_state.turn >= MAX_TURNS:
        st.session_state.game_over = True
        st.rerun()

    # 일반 주식
    event = random.choice(NEWS_EVENTS)
    st.session_state.market_news = event["news"]

    for asset in STOCKS:
        random_change = random.uniform(-0.05, 0.05)

        new_price = int(
            st.session_state.prices[asset]
            * (1 + random_change)
            * event["effects"][asset]
        )

        st.session_state.prices[asset] = max(1, new_price)

    # 도지코인: 뉴스와 완전히 독립
    if not st.session_state.dogecoin_delisted:

        if random.random() < DOGECOIN_DELIST_PROBABILITY:
            st.session_state.dogecoin_delisted = True
            st.session_state.prices[DOGECOIN] = 0
            st.session_state.doge_last_change = -100

            st.session_state.doge_notice = (
                "상장폐지 발생! 도지코인의 거래가 영구 중단되었습니다."
            )

            add_history("도지코인 상장폐지 발생!")

        else:
            change = random.uniform(-0.50, 0.50)

            old_price = st.session_state.prices[DOGECOIN]
            new_price = max(1, int(old_price * (1 + change)))

            st.session_state.prices[DOGECOIN] = new_price
            st.session_state.doge_last_change = change * 100

            st.session_state.doge_notice = (
                f"이번 턴 가격 변동: {change * 100:+.1f}%"
            )

    else:
        st.session_state.doge_notice = "이미 상장폐지된 종목입니다."

    st.session_state.turn += 1

    st.session_state.price_history.append({
        asset: st.session_state.prices[asset]
        for asset in ALL_ASSETS
    })

    if st.session_state.turn >= MAX_TURNS:
        st.session_state.game_over = True

    st.rerun()


# =========================
# 제목
# =========================

st.title("STOCK TYCOON")
st.caption("가상의 주식 투자 시뮬레이션 | 시작 자금 1,000,000원")


# =========================
# 게임 종료
# =========================

if st.session_state.game_over:
    total = get_total_asset()
    profit = total - STARTING_CASH
    rate = profit / STARTING_CASH * 100

    st.subheader("투자 종료")

    a, b, c = st.columns(3)
    a.metric("최종 자산", format_money(total))
    b.metric("수익", format_money(profit))
    c.metric("수익률", f"{rate:+.2f}%")

    if rate >= 50:
        grade = "S"
    elif rate >= 20:
        grade = "A"
    elif rate >= 0:
        grade = "B"
    elif rate >= -20:
        grade = "C"
    else:
        grade = "F"

    st.markdown(f"## 최종 등급: {grade}")

    if st.session_state.dogecoin_delisted:
        st.error("도지코인은 상장폐지되었습니다.")

    st.subheader("최종 보유 자산")

    for asset in ALL_ASSETS:
        quantity = st.session_state.holdings[asset]
        value = quantity * st.session_state.prices[asset]
        st.write(
            f"**{asset}** | {quantity}주 | {format_money(value)}"
        )

    st.line_chart(pd.DataFrame(st.session_state.price_history))

    if st.button("새 게임 시작", use_container_width=True):
        initialize_game()
        st.rerun()

    st.stop()


# =========================
# 상단 자산 정보
# =========================

total_asset = get_total_asset()
profit = total_asset - STARTING_CASH

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("보유 현금", format_money(st.session_state.cash))
m2.metric("총 자산", format_money(total_asset))
m3.metric("수익", format_money(profit))
m4.metric("진행 턴", f"{st.session_state.turn}/{MAX_TURNS}")

held = sum(
    1 for q in st.session_state.holdings.values() if q > 0
)

m5.metric("보유 종목", f"{held}개")

st.progress(st.session_state.turn / MAX_TURNS)


# =========================
# 도지코인 메인 패널
# =========================

st.markdown("## SPECIAL ASSET")

doge_price = st.session_state.prices[DOGECOIN]
doge_quantity = st.session_state.holdings[DOGECOIN]
doge_value = doge_price * doge_quantity

if st.session_state.dogecoin_delisted:

    st.markdown(
        f"""
        <div class="doge-dead">
            <div class="doge-title">DOGECOIN | 상장폐지</div>
            <div class="doge-price">0원</div>
            <div class="doge-sub">
                거래가 영구 중단되었습니다.
            </div>
            <div class="doge-warning">
                보유 수량: {doge_quantity}개 |
                평가 금액: 0원<br>
                이 게임에서는 도지코인을 다시 거래할 수 없습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    change = st.session_state.doge_last_change

    st.markdown(
        f"""
        <div class="doge-panel">
            <div class="doge-title">DOGECOIN</div>
            <div class="doge-price">{format_money(doge_price)}</div>
            <div class="doge-sub">
                이번 턴 변동률: {change:+.1f}%
                &nbsp; | &nbsp;
                보유 수량: {doge_quantity}개
                &nbsp; | &nbsp;
                평가 금액: {format_money(doge_value)}
            </div>
            <div class="doge-warning">
                상장폐지 위험: 매 턴 10% 확률
                &nbsp; | &nbsp;
                일반 뉴스와 무관하게 독립적으로 가격 변동
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 도지코인 전용 거래 영역
if not st.session_state.dogecoin_delisted:

    d1, d2, d3, d4 = st.columns([1, 1, 1, 2])

    with d1:
        doge_buy_quantity = st.number_input(
            "도지코인 매수 수량",
            min_value=1,
            value=1,
            key="doge_buy_quantity"
        )

    with d2:
        if st.button(
            "도지코인 매수",
            use_container_width=True,
            type="primary"
        ):
            buy_stock(DOGECOIN, doge_buy_quantity)

    with d3:
        if st.button(
            "도지코인 매도",
            use_container_width=True,
            disabled=doge_quantity <= 0
        ):
            sell_stock(DOGECOIN, min(doge_buy_quantity, doge_quantity))

    with d4:
        st.caption(
            "주의: 상장폐지 시 보유 중인 도지코인의 평가 금액은 0원이 됩니다."
        )


# =========================
# 일반 주식
# =========================

st.divider()
st.subheader("일반 주식")

stock_columns = st.columns(3)

for index, asset in enumerate(STOCKS):

    with stock_columns[index]:

        price = st.session_state.prices[asset]
        owned = st.session_state.holdings[asset]

        st.markdown(
            f"""
            <div class="stock-card">
                <b>{asset}</b><br>
                <span style="font-size:20px;font-weight:bold;">
                    {format_money(price)}
                </span><br>
                <span style="font-size:12px;">
                    보유: {owned}주
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        quantity = st.number_input(
            "거래 수량",
            min_value=1,
            value=1,
            key=f"stock_quantity_{index}"
        )

        b1, b2 = st.columns(2)

        with b1:
            if st.button(
                "매수",
                key=f"stock_buy_{index}",
                use_container_width=True
            ):
                buy_stock(asset, quantity)

        with b2:
            if st.button(
                "매도",
                key=f"stock_sell_{index}",
                use_container_width=True,
                disabled=owned <= 0
            ):
                sell_stock(asset, min(quantity, owned))


# =========================
# 뉴스와 하단 정보
# =========================

st.divider()

left, middle, right = st.columns([1.2, 1, 0.8])

with left:
    st.subheader("시장 뉴스")
    st.info(st.session_state.market_news)

with middle:
    st.subheader("최근 거래")

    if st.session_state.history:
        for item in st.session_state.history[:5]:
            st.caption(item)
    else:
        st.caption("거래 내역이 없습니다.")

with right:
    st.subheader("게임 진행")

    st.write(f"현재 턴: {st.session_state.turn}/{MAX_TURNS}")

    if st.button(
        "다음 턴 진행",
        type="primary",
        use_container_width=True
    ):
        next_turn()

    if st.button("게임 초기화", use_container_width=True):
        initialize_game()
        st.rerun()


# =========================
# 가격 그래프
# =========================

st.divider()
st.subheader("가격 변화 그래프")

chart_df = pd.DataFrame(st.session_state.price_history)

st.line_chart(chart_df, height=170)

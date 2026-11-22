
import streamlit as st
import random
import pandas as pd

# =========================
# 기본 설정
# =========================

st.set_page_config(
    page_title="STOCK TYCOON",
    page_icon="",
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
# 화면 CSS
# =========================

st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}

.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0.3rem;
    padding-left: 1.2rem;
    padding-right: 1.2rem;
    max-width: 100%;
}

h1 {
    font-size: 25px !important;
    margin-bottom: 3px !important;
}

h2 {
    font-size: 19px !important;
}

h3 {
    font-size: 16px !important;
}

p {
    font-size: 13px !important;
}

div[data-testid="stMetric"] {
    padding: 7px 10px;
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 9px;
}

div[data-testid="stMetricValue"] {
    font-size: 21px;
}

div[data-testid="stMetricLabel"] {
    font-size: 12px;
}

.asset-card {
    border: 1px solid rgba(128,128,128,0.35);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 4px;
    min-height: 95px;
}

.news-card {
    border: 1px solid rgba(128,128,128,0.35);
    border-radius: 9px;
    padding: 9px 12px;
    margin-bottom: 8px;
}

.doge-card {
    border: 1px solid rgba(220,160,40,0.65);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 4px;
    min-height: 95px;
}

.stButton button {
    min-height: 32px;
    padding: 2px 5px;
    font-size: 12px;
}

.stNumberInput input {
    font-size: 13px;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.35rem;
}

hr {
    margin: 5px 0 !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# 게임 초기화
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
    st.session_state.doge_notice = "도지코인은 매 턴 독립적으로 가격이 변동합니다."

    st.session_state.dogecoin_delisted = False
    st.session_state.game_over = False

    st.session_state.price_history.append({
        asset: st.session_state.prices[asset]
        for asset in ALL_ASSETS
    })


if "cash" not in st.session_state:
    initialize_game()


# =========================
# 계산 함수
# =========================

def get_total_asset():
    total = st.session_state.cash

    for asset in ALL_ASSETS:
        total += (
            st.session_state.holdings[asset]
            * st.session_state.prices[asset]
        )

    return total


def get_profit():
    return get_total_asset() - STARTING_CASH


def format_money(value):
    return f"{int(value):,}원"


def add_history(message):
    st.session_state.history.insert(0, message)
    st.session_state.history = st.session_state.history[:5]


# =========================
# 매수
# =========================

def buy_stock(asset, quantity):
    if st.session_state.game_over:
        return

    if asset == DOGECOIN and st.session_state.dogecoin_delisted:
        st.warning("상장폐지된 도지코인은 거래할 수 없습니다.")
        return

    if quantity <= 0:
        st.warning("매수 수량을 확인하세요.")
        return

    price = st.session_state.prices[asset]
    total_price = price * quantity

    if total_price > st.session_state.cash:
        st.warning("보유 현금이 부족합니다.")
        return

    st.session_state.cash -= total_price
    st.session_state.holdings[asset] += quantity

    add_history(
        f"{asset} {quantity}주 매수 | -{format_money(total_price)}"
    )

    st.rerun()


# =========================
# 매도
# =========================

def sell_stock(asset, quantity):
    if st.session_state.game_over:
        return

    if asset == DOGECOIN and st.session_state.dogecoin_delisted:
        st.warning("상장폐지된 도지코인은 거래할 수 없습니다.")
        return

    if quantity <= 0:
        st.warning("매도 수량을 확인하세요.")
        return

    if quantity > st.session_state.holdings[asset]:
        st.warning("보유 수량이 부족합니다.")
        return

    price = st.session_state.prices[asset]
    total_price = price * quantity

    st.session_state.cash += total_price
    st.session_state.holdings[asset] -= quantity

    add_history(
        f"{asset} {quantity}주 매도 | +{format_money(total_price)}"
    )

    st.rerun()


# =========================
# 일반 주식 뉴스 이벤트
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
# 다음 턴 진행
# =========================

def next_turn():
    if st.session_state.game_over:
        return

    if st.session_state.turn >= MAX_TURNS:
        st.session_state.game_over = True
        return

    # 1. 일반 주식 뉴스 이벤트
    event = random.choice(NEWS_EVENTS)

    st.session_state.market_news = event["news"]

    for asset in STOCKS:
        base_change = random.uniform(-0.05, 0.05)
        event_effect = event["effects"][asset]

        new_price = int(
            st.session_state.prices[asset]
            * (1 + base_change)
            * event_effect
        )

        st.session_state.prices[asset] = max(1, new_price)

    # 2. 도지코인 독립 이벤트
    # 일반 뉴스와 무관하게 별도로 확률 계산

    if not st.session_state.dogecoin_delisted:

        if random.random() < DOGECOIN_DELIST_PROBABILITY:

            st.session_state.dogecoin_delisted = True
            st.session_state.prices[DOGECOIN] = 0

            st.session_state.doge_notice = (
                "도지코인 상장폐지! 보유한 도지코인의 가치가 0원이 되었습니다."
            )

            add_history("도지코인 상장폐지 발생!")

        else:
            doge_change = random.uniform(-0.50, 0.50)

            old_price = st.session_state.prices[DOGECOIN]

            new_price = int(
                old_price * (1 + doge_change)
            )

            st.session_state.prices[DOGECOIN] = max(1, new_price)

            percentage = doge_change * 100

            st.session_state.doge_notice = (
                f"도지코인 가격 변동: {percentage:+.1f}%"
            )

    else:
        st.session_state.doge_notice = (
            "도지코인은 이미 상장폐지되어 거래가 중단되었습니다."
        )

    # 3. 턴 증가
    st.session_state.turn += 1

    # 4. 가격 기록
    st.session_state.price_history.append({
        asset: st.session_state.prices[asset]
        for asset in ALL_ASSETS
    })

    # 5. 마지막 턴 종료
    if st.session_state.turn >= MAX_TURNS:
        st.session_state.game_over = True

    st.rerun()


# =========================
# 게임 제목
# =========================

st.title("STOCK TYCOON")

st.caption("가상의 주식 투자 시뮬레이션 | 시작 자금 1,000,000원")


# =========================
# 게임 종료 화면
# =========================

if st.session_state.game_over:

    total = get_total_asset()
    profit = total - STARTING_CASH
    rate = profit / STARTING_CASH * 100

    st.subheader("투자 종료")

    c1, c2, c3 = st.columns(3)

    c1.metric("최종 자산", format_money(total))
    c2.metric("수익", format_money(profit))
    c3.metric("수익률", f"{rate:+.2f}%")

    if rate >= 50:
        grade = "S"
        comment = "놀라운 투자 실력입니다!"
    elif rate >= 20:
        grade = "A"
        comment = "훌륭한 투자 성과입니다."
    elif rate >= 0:
        grade = "B"
        comment = "안정적인 투자였습니다."
    elif rate >= -20:
        grade = "C"
        comment = "아쉬운 투자였습니다."
    else:
        grade = "F"
        comment = "투자에 실패했습니다."

    st.markdown(f"## 최종 등급: {grade}")
    st.write(comment)

    if st.session_state.dogecoin_delisted:
        st.error("도지코인은 상장폐지되었습니다.")

    st.subheader("최종 보유 자산")

    for asset in ALL_ASSETS:
        quantity = st.session_state.holdings[asset]
        value = quantity * st.session_state.prices[asset]

        st.write(
            f"**{asset}** | {quantity}주 | {format_money(value)}"
        )

    st.subheader("자산 변화")

    df = pd.DataFrame(st.session_state.price_history)
    df.index = range(1, len(df) + 1)

    st.line_chart(df)

    if st.button("새 게임 시작", use_container_width=True):
        initialize_game()
        st.rerun()

    st.stop()


# =========================
# 상단 자산 정보
# =========================

total_asset = get_total_asset()
profit = get_profit()

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric(
    "보유 현금",
    format_money(st.session_state.cash)
)

m2.metric(
    "총 자산",
    format_money(total_asset)
)

m3.metric(
    "수익",
    format_money(profit),
    delta=format_money(profit)
)

m4.metric(
    "진행 턴",
    f"{st.session_state.turn} / {MAX_TURNS}"
)

held_count = sum(
    1 for quantity in st.session_state.holdings.values()
    if quantity > 0
)

m5.metric(
    "보유 종목",
    f"{held_count}개"
)

st.progress(
    st.session_state.turn / MAX_TURNS
)


# =========================
# 뉴스 영역
# =========================

left_news, right_news = st.columns(2)

with left_news:
    st.markdown(
        f"""
        <div class="news-card">
            <b>시장 뉴스</b><br>
            {st.session_state.market_news}
        </div>
        """,
        unsafe_allow_html=True
    )

with right_news:
    if st.session_state.dogecoin_delisted:
        st.error(st.session_state.doge_notice)
    else:
        st.markdown(
            f"""
            <div class="news-card">
                <b>도지코인 독립 이벤트</b><br>
                {st.session_state.doge_notice}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================
# 주식 거래 화면
# =========================

st.subheader("주식 거래")

columns = st.columns(4)

for index, asset in enumerate(ALL_ASSETS):

    with columns[index]:

        price = st.session_state.prices[asset]
        quantity_owned = st.session_state.holdings[asset]

        is_doge = asset == DOGECOIN
        is_delisted = (
            is_doge and st.session_state.dogecoin_delisted
        )

        card_class = "doge-card" if is_doge else "asset-card"

        if is_delisted:
            status = "상장폐지"
        elif is_doge:
            status = "독립 변동 종목"
        else:
            status = "거래 가능"

        st.markdown(
            f"""
            <div class="{card_class}">
                <b>{asset}</b><br>
                <span style="font-size:19px;font-weight:bold;">
                    {format_money(price)}
                </span><br>
                <span style="font-size:12px;">
                    보유: {quantity_owned}주 | {status}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        input_key = f"quantity_{index}"

        quantity = st.number_input(
            "거래 수량",
            min_value=1,
            max_value=100000,
            value=1,
            step=1,
            key=input_key
        )

        buy_disabled = is_delisted or st.session_state.cash < price

        b1, b2 = st.columns(2)

        with b1:
            if st.button(
                "매수",
                key=f"buy_{index}",
                use_container_width=True,
                disabled=buy_disabled
            ):
                buy_stock(asset, quantity)

        with b2:
            if st.button(
                "매도",
                key=f"sell_{index}",
                use_container_width=True,
                disabled=(
                    is_delisted
                    or quantity_owned <= 0
                )
            ):
                sell_stock(asset, quantity)

        if is_delisted:
            st.caption("거래 불가능")


# =========================
# 하단 정보 영역
# =========================

st.divider()

left, middle, right = st.columns([1.2, 1, 0.8])

# 자산 그래프
with left:
    st.subheader("자산 가격 변화")

    df = pd.DataFrame(st.session_state.price_history)

    df.index = range(1, len(df) + 1)

    st.line_chart(
        df,
        height=150
    )

# 거래 내역
with middle:
    st.subheader("최근 거래 내역")

    if st.session_state.history:
        for item in st.session_state.history[:5]:
            st.caption(item)
    else:
        st.caption("아직 거래 내역이 없습니다.")

# 턴 진행
with right:
    st.subheader("게임 진행")

    st.write(
        f"현재 {st.session_state.turn}번째 턴"
    )

    st.write(
        f"남은 턴: {MAX_TURNS - st.session_state.turn}"
    )

    if st.button(
        "다음 턴 진행",
        use_container_width=True,
        type="primary"
    ):
        next_turn()

    if st.button(
        "게임 초기화",
        use_container_width=True
    ):
        initialize_game()
        st.rerun()

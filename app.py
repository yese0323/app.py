
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

STARTING_CASH = 1_000_000
MAX_TURNS = 10

MAX_LOAN = 500_000

STOCKS = {
    "삼성전자": 70000,
    "SK하이닉스": 120000,
    "카카오": 50000
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

.loan-panel {
    border: 2px solid #d69b32;
    border-radius: 12px;
    padding: 14px;
    margin: 10px 0;
}

hr {
    margin: 6px 0 !important;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. 게임 초기화
# ==========================================

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

    st.session_state.market_news = (
        "시장이 개장했습니다. 투자를 시작하세요."
    )

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


if "cash" not in st.session_state:
    initialize_game()


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


# ==========================================
# 11. 다음 턴 진행
# ==========================================

def next_turn():
    if st.session_state.game_over:
        return

    if st.session_state.turn >= MAX_TURNS:
        st.session_state.game_over = True
        st.rerun()

    # 일반 주식 뉴스
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

    # 게임 종료
    if st.session_state.turn >= MAX_TURNS:
        st.session_state.game_over = True

    st.rerun()


# ==========================================
# 12. 제목
# ==========================================

st.title("STOCK TYCOON")
st.caption(
    "가상의 주식 투자 시뮬레이션 | 시작 자금 1,000,000원"
)


# ==========================================
# 13. 게임 종료 화면
# ==========================================

if st.session_state.game_over:

    total = get_total_asset()
    profit = total - STARTING_CASH
    rate = profit / STARTING_CASH * 100

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
        initialize_game()
        st.rerun()

    st.stop()


# ==========================================
# 14. 상단 자산 정보
# ==========================================

total_asset = get_total_asset()
profit = total_asset - STARTING_CASH

m1, m2, m3, m4, m5, m6 = st.columns(6)

m1.metric(
    "보유 현금",
    format_money(st.session_state.cash)
)

m2.metric(
    "총 순자산",
    format_money(total_asset)
)

m3.metric(
    "수익",
    format_money(profit)
)

m4.metric(
    "진행 턴",
    f"{st.session_state.turn}/{MAX_TURNS}"
)

held = sum(
    1 for q in st.session_state.holdings.values()
    if q > 0
)

m5.metric("보유 종목", f"{held}개")

m6.metric(
    "누적 대출",
    format_money(st.session_state.loan_debt)
)

st.progress(st.session_state.turn / MAX_TURNS)


# ==========================================
# 15. 대출 안내 화면
# ==========================================

# 현금이 0원이거나 순자산이 0원 이하일 때 표시
loan_condition = get_total_asset() <= 0

remaining_loan = get_remaining_loan()

if loan_condition:

    st.markdown("""
    <div class="loan-panel">
        <h3>자금 부족!</h3>
        <p>
            현재 투자 자금이 부족합니다.<br>
            추가 자금이 필요하다면 대출을 이용할 수 있습니다.
        </p>
        <h3>대출하시겠습니까?</h3>
        <p>최대 대출 가능 금액: 500,000원</p>
    </div>
    """, unsafe_allow_html=True)

    if remaining_loan > 0:

        if not st.session_state.loan_prompt_open:

            if st.button(
                "대출 신청하기",
                type="primary",
                use_container_width=True
            ):
                st.session_state.loan_prompt_open = True
                st.rerun()

        else:

            st.subheader("대출 금액 선택")

            loan_amount = st.number_input(
                "대출받을 금액",
                min_value=1,
                max_value=remaining_loan,
                value=min(100000, remaining_loan),
                step=10000,
                key="loan_amount_input"
            )

            st.caption(
                f"남은 대출 한도: {format_money(remaining_loan)}"
            )

            loan_col1, loan_col2 = st.columns(2)

            with loan_col1:
                if st.button(
                    "대출 확정",
                    type="primary",
                    use_container_width=True
                ):
                    take_loan(loan_amount)

            with loan_col2:
                if st.button(
                    "취소",
                    use_container_width=True
                ):
                    st.session_state.loan_prompt_open = False
                    st.rerun()

    else:
        st.error(
            "대출 한도 500,000원을 모두 사용했습니다. "
            "추가 대출은 불가능합니다."
        )


# ==========================================
# 16. 도지코인 메인 패널
# ==========================================

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


# ==========================================
# 17. 도지코인 거래 버튼
# ==========================================

if not st.session_state.dogecoin_delisted:

    d1, d2, d3, d4, d5 = st.columns([1.2, 1, 1, 1, 1])

    with d1:
        doge_buy_quantity = st.number_input(
            "도지코인 거래 수량",
            min_value=1,
            value=1,
            key="doge_buy_quantity"
        )

    with d2:
        if st.button(
            "매수",
            key="doge_buy",
            use_container_width=True
        ):
            buy_stock(DOGECOIN, doge_buy_quantity)

    with d3:
        if st.button(
            "매도",
            key="doge_sell",
            use_container_width=True,
            disabled=doge_quantity <= 0
        ):
            sell_stock(
                DOGECOIN,
                min(doge_buy_quantity, doge_quantity)
            )

    with d4:
        if st.button(
            "풀매수",
            key="doge_full_buy",
            use_container_width=True
        ):
            buy_all(DOGECOIN)

    with d5:
        if st.button(
            "풀매도",
            key="doge_full_sell",
            use_container_width=True,
            disabled=doge_quantity <= 0
        ):
            sell_all(DOGECOIN)

else:
    st.error("도지코인은 상장폐지되어 모든 거래가 중단되었습니다.")


# ==========================================
# 18. 일반 주식 거래
# ==========================================

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

        b1, b2, b3, b4 = st.columns(4)

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

        with b3:
            if st.button(
                "풀매수",
                key=f"stock_full_buy_{index}",
                use_container_width=True
            ):
                buy_all(asset)

        with b4:
            if st.button(
                "풀매도",
                key=f"stock_full_sell_{index}",
                use_container_width=True,
                disabled=owned <= 0
            ):
                sell_all(asset)


# ==========================================
# 19. 하단 정보
# ==========================================

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

    st.write(
        f"현재 턴: {st.session_state.turn}/{MAX_TURNS}"
    )

    if st.button(
        "다음 턴 진행",
        type="primary",
        use_container_width=True
    ):
        next_turn()

    if st.button(
        "게임 초기화",
        use_container_width=True
    ):
        initialize_game()
        st.rerun()


# ==========================================
# 20. 가격 변화 그래프
# ==========================================

st.divider()
st.subheader("가격 변화 그래프")

chart_df = pd.DataFrame(
    st.session_state.price_history
)

st.line_chart(
    chart_df,
    height=170
)

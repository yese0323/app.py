
import streamlit as st
import random
import pandas as pd

# =====================================
# 1. 기본 설정
# =====================================

st.set_page_config(
    page_title="STOCK TYCOON",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp {
    background: #eef1f6;
}

.block-container {
    max-width: 1600px;
    padding: 0.7rem 1.2rem 0.5rem 1.2rem;
}

header, footer, #MainMenu {
    visibility: hidden;
}

h1, h2, h3, p {
    margin-top: 0;
}

.title-box {
    background: linear-gradient(110deg, #17243b, #344e77);
    color: white;
    padding: 13px 22px;
    border-radius: 15px;
    margin-bottom: 10px;
}

.title {
    font-size: 27px;
    font-weight: 900;
}

.subtitle {
    font-size: 12px;
    opacity: .75;
}

.metric {
    background: white;
    border: 1px solid #dfe4ed;
    border-radius: 12px;
    padding: 10px 13px;
    min-height: 73px;
}

.metric-label {
    font-size: 11px;
    color: #778196;
}

.metric-value {
    font-size: 19px;
    font-weight: 850;
    color: #1b2940;
    margin-top: 4px;
}

.news {
    background: white;
    border: 1px solid #dfe4ed;
    border-radius: 12px;
    padding: 12px 16px;
    min-height: 78px;
}

.news-heading {
    font-size: 15px;
    font-weight: 800;
    color: #263955;
}

.news-text {
    font-size: 12px;
    color: #68758a;
    margin-top: 5px;
}

.stock {
    background: white;
    border: 1px solid #dfe4ed;
    border-radius: 13px;
    padding: 12px;
    min-height: 100px;
}

.stock-name {
    font-size: 16px;
    font-weight: 850;
    color: #263955;
}

.stock-price {
    font-size: 21px;
    font-weight: 900;
    color: #17243b;
    margin-top: 5px;
}

.stock-info {
    font-size: 11px;
    color: #7b8495;
}

.doge {
    background: #fff8e8;
    border: 2px solid #e5bb54;
    border-radius: 13px;
    padding: 11px;
    min-height: 100px;
}

.doge .stock-name {
    color: #94670d;
}

.doge .stock-price {
    color: #8a5c00;
}

.section {
    font-size: 15px;
    font-weight: 850;
    color: #253650;
    margin: 8px 0 5px 2px;
}

.stButton > button {
    min-height: 34px;
    height: 34px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 750;
    padding: 0 5px;
}

div[data-testid="stNumberInput"] input {
    min-height: 32px;
    height: 32px;
    font-size: 12px;
}

div[data-testid="stNumberInput"] label {
    font-size: 11px;
}

.bottom-box {
    background: white;
    border: 1px solid #dfe4ed;
    border-radius: 12px;
    padding: 10px;
    min-height: 125px;
}

.small-text {
    font-size: 11px;
    color: #778196;
}

div[data-testid="stProgress"] {
    margin-top: -8px;
    margin-bottom: 5px;
}

@media (max-width: 900px) {
    .block-container {
        padding: 0.5rem;
    }

    .title {
        font-size: 21px;
    }

    .metric-value {
        font-size: 15px;
    }

    .stock-price {
        font-size: 16px;
    }
}
</style>
""", unsafe_allow_html=True)


# =====================================
# 2. 종목 및 뉴스
# =====================================

STOCKS = {
    "삼성전자": 70000,
    "SK하이닉스": 120000,
    "카카오": 50000
}

DOGE = "도지코인"
ASSETS = list(STOCKS.keys()) + [DOGE]

NEWS = [
    {
        "type": "positive_stock",
        "title": "삼성전자 신제품 출시",
        "text": "신제품이 시장에서 좋은 반응을 얻고 있습니다.",
        "stock": "삼성전자"
    },
    {
        "type": "positive_stock",
        "title": "SK하이닉스 반도체 수요 증가",
        "text": "반도체 수요가 증가하며 기대감이 높아졌습니다.",
        "stock": "SK하이닉스"
    },
    {
        "type": "positive_stock",
        "title": "카카오 신규 서비스 인기",
        "text": "신규 서비스가 많은 이용자를 확보했습니다.",
        "stock": "카카오"
    },
    {
        "type": "negative_stock",
        "title": "삼성전자 실적 전망 하락",
        "text": "실적에 대한 시장의 우려가 커지고 있습니다.",
        "stock": "삼성전자"
    },
    {
        "type": "negative_stock",
        "title": "SK하이닉스 공급 문제",
        "text": "반도체 공급 문제로 불안감이 커졌습니다.",
        "stock": "SK하이닉스"
    },
    {
        "type": "negative_stock",
        "title": "카카오 규제 우려",
        "text": "새로운 규제 가능성이 제기되었습니다.",
        "stock": "카카오"
    },
    {
        "type": "general_positive",
        "title": "국내 증시 상승",
        "text": "투자 심리가 좋아지며 시장이 상승했습니다.",
        "stock": None
    },
    {
        "type": "general_negative",
        "title": "국내 증시 하락",
        "text": "경제 불안감으로 시장이 하락했습니다.",
        "stock": None
    },
    {
        "type": "surge",
        "title": "시장 급등",
        "text": "강한 매수세가 나타났습니다.",
        "stock": None
    },
    {
        "type": "crash",
        "title": "시장 급락",
        "text": "갑작스러운 악재가 발생했습니다.",
        "stock": None
    }
]


# =====================================
# 3. 게임 초기화
# =====================================

def new_game():
    st.session_state.cash = 1_000_000
    st.session_state.prices = STOCKS.copy()
    st.session_state.prices[DOGE] = 1000

    st.session_state.holdings = {
        asset: 0 for asset in ASSETS
    }

    st.session_state.turn = 1
    st.session_state.history = [1_000_000]
    st.session_state.trade_history = []
    st.session_state.news = None
    st.session_state.game_over = False

    st.session_state.last_changes = {
        asset: 0 for asset in ASSETS
    }


if "cash" not in st.session_state:
    new_game()


# =====================================
# 4. 자산 계산
# =====================================

def total_asset():
    value = sum(
        st.session_state.prices[a] *
        st.session_state.holdings[a]
        for a in ASSETS
    )
    return st.session_state.cash + value


def profit_rate():
    return (total_asset() - 1_000_000) / 1_000_000 * 100


# =====================================
# 5. 뉴스 생성
# =====================================

def generate_news():
    st.session_state.news = random.choices(
        NEWS,
        weights=[4, 4, 4, 5, 5, 5, 3, 5, 3, 5]
    )[0]


# =====================================
# 6. 일반 주식 변동
# =====================================

def apply_news():
    news = st.session_state.news

    if not news:
        return

    for stock in STOCKS:
        kind = news["type"]
        affected = news["stock"]

        if kind == "positive_stock":
            change = (
                random.randint(20, 40)
                if stock == affected
                else random.randint(-25, 25)
            )

        elif kind == "negative_stock":
            change = (
                random.randint(-40, -20)
                if stock == affected
                else random.randint(-25, 25)
            )

        elif kind == "general_positive":
            change = random.randint(10, 30)

        elif kind == "general_negative":
            change = random.randint(-30, -10)

        elif kind == "surge":
            change = random.randint(40, 60)

        elif kind == "crash":
            change = random.randint(-60, -40)

        else:
            change = random.randint(-25, 25)

        old = st.session_state.prices[stock]
        new = int(old * (1 + change / 100))

        st.session_state.prices[stock] = max(1000, new)
        st.session_state.last_changes[stock] = change


# =====================================
# 7. 도지코인 독립 변동
# =====================================

def apply_dogecoin():
    old = st.session_state.prices[DOGE]

    # 뉴스와 완전히 독립적인 랜덤 변동
    change = random.uniform(-50, 50)

    new = int(old * (1 + change / 100))

    st.session_state.prices[DOGE] = max(1, new)
    st.session_state.last_changes[DOGE] = round(change, 1)


# =====================================
# 8. 매수 및 매도
# =====================================

def buy(asset, amount):
    price = st.session_state.prices[asset]
    cost = price * amount

    if amount <= 0:
        st.warning("수량을 확인하세요.")
        return

    if cost > st.session_state.cash:
        st.warning("현금이 부족합니다.")
        return

    st.session_state.cash -= cost
    st.session_state.holdings[asset] += amount

    st.session_state.trade_history.insert(
        0, f"매수 {asset} {amount:,}개"
    )


def sell(asset, amount):
    if amount <= 0:
        st.warning("수량을 확인하세요.")
        return

    if amount > st.session_state.holdings[asset]:
        st.warning("보유 수량이 부족합니다.")
        return

    revenue = st.session_state.prices[asset] * amount

    st.session_state.cash += revenue
    st.session_state.holdings[asset] -= amount

    st.session_state.trade_history.insert(
        0, f"매도 {asset} {amount:,}개"
    )


# =====================================
# 9. 턴 진행
# =====================================

def next_turn():
    generate_news()
    apply_news()
    apply_dogecoin()

    st.session_state.history.append(total_asset())
    st.session_state.turn += 1

    if st.session_state.turn > 10:
        st.session_state.game_over = True


# =====================================
# 10. 게임 종료
# =====================================

if st.session_state.game_over:
    asset = total_asset()
    profit = profit_rate()

    grade = (
        "S" if profit >= 50 else
        "A" if profit >= 25 else
        "B" if profit >= 10 else
        "C" if profit >= 0 else
        "D"
    )

    st.markdown("""
    <div class="title-box">
        <div class="title">STOCK TYCOON</div>
        GAME RESULT
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="news">
            <div class="news-heading">게임 종료 · 등급 {grade}</div>
            <div class="stock-price">₩{asset:,}</div>
            <div class="news-text">최종 수익률 {profit:+.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.line_chart(
        pd.DataFrame({"총 자산": st.session_state.history}),
        height=250
    )

    if st.button("새 게임 시작", use_container_width=True):
        new_game()
        st.rerun()

    st.stop()


# =====================================
# 11. 상단 헤더
# =====================================

st.markdown("""
<div class="title-box">
    <div class="title">STOCK TYCOON</div>
    <div class="subtitle">THE MARKET IS YOURS</div>
</div>
""", unsafe_allow_html=True)


# =====================================
# 12. 자산 대시보드
# =====================================

asset = total_asset()
profit = profit_rate()

metrics = st.columns(5)

values = [
    ("보유 현금", f"₩{st.session_state.cash:,}"),
    ("총 자산", f"₩{asset:,}"),
    ("수익률", f"{profit:+.2f}%"),
    ("현재 턴", f"{min(st.session_state.turn, 10)} / 10"),
    ("보유 종목", f"{sum(1 for a in ASSETS if st.session_state.holdings[a] > 0)}개")
]

for col, (label, value) in zip(metrics, values):
    with col:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.progress(min(st.session_state.turn / 10, 1.0))


# =====================================
# 13. 뉴스
# =====================================

st.markdown('<div class="section">오늘의 뉴스</div>', unsafe_allow_html=True)

if st.session_state.news:
    news = st.session_state.news
    news_title = news["title"]
    news_text = news["text"]
else:
    news_title = "시장 개장 준비"
    news_text = "다음 턴을 진행하면 새로운 뉴스가 발표됩니다."

st.markdown(
    f"""
    <div class="news">
        <div class="news-heading">{news_title}</div>
        <div class="news-text">{news_text}</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =====================================
# 14. 종목 카드 4개
# =====================================

st.markdown('<div class="section">주식 및 코인 거래</div>', unsafe_allow_html=True)

cols = st.columns(4)

for index, name in enumerate(ASSETS):
    price = st.session_state.prices[name]
    change = st.session_state.last_changes[name]
    holding = st.session_state.holdings[name]

    with cols[index]:

        card_class = "doge" if name == DOGE else "stock"

        display_name = "DOGECOIN" if name == DOGE else name

        st.markdown(
            f"""
            <div class="{card_class}">
                <div class="stock-name">{display_name}</div>
                <div class="stock-price">₩{price:,}</div>
                <div class="stock-info">변동 {change:+.1f}%</div>
                <div class="stock-info">보유 {holding:,}개</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        amount = st.number_input(
            "수량",
            min_value=1,
            value=1,
            step=1,
            key=f"amount_{name}"
        )

        b1, b2 = st.columns(2)

        with b1:
            if st.button(
                "매수",
                key=f"buy_{name}",
                use_container_width=True
            ):
                buy(name, amount)
                st.rerun()

        with b2:
            if st.button(
                "매도",
                key=f"sell_{name}",
                use_container_width=True
            ):
                sell(name, amount)
                st.rerun()


# =====================================
# 15. 하단 정보
# =====================================

st.markdown("---")

left, middle, right = st.columns([1.2, 1.2, 1])

with left:
    st.markdown('<div class="section">자산 변화</div>', unsafe_allow_html=True)

    st.line_chart(
        pd.DataFrame({"자산": st.session_state.history}),
        height=145
    )

with middle:
    st.markdown('<div class="section">최근 거래</div>', unsafe_allow_html=True)

    if st.session_state.trade_history:
        for item in st.session_state.trade_history[:5]:
            st.markdown(
                f'<div class="small-text">{item}</div>',
                unsafe_allow_html=True
            )
    else:
        st.caption("거래 기록이 없습니다.")

with right:
    st.markdown('<div class="section">게임 진행</div>', unsafe_allow_html=True)

    st.write(f"현재 자산: ₩{total_asset():,}")

    if st.button(
        "다음 턴 진행",
        type="primary",
        use_container_width=True
    ):
        next_turn()
        st.rerun()

    if st.button(
        "게임 초기화",
        use_container_width=True
    ):
        new_game()
        st.rerun()

st.caption("도지코인은 일반 뉴스와 무관하게 매 턴 독립적으로 랜덤 변동합니다.")

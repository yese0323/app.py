import streamlit as st
import random
import pandas as pd

# ==============================
# 기본 설정
# ==============================

st.set_page_config(
    page_title="STOCK TYCOON",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS - 태블릿 최적화
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

/* 제목 */
.title-box {
    background: linear-gradient(135deg, #18243a, #304b76);
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

/* 섹션 타이틀 */
.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #18243a;
    margin-top: 20px;
    margin-bottom: 10px;
}

/* 대시보드 */
.metric-card {
    background: white;
    border: 1px solid #e3e7ee;
    border-radius: 18px;
    padding: 20px;
    min-height: 110px;
}

.metric-label {
    color: #7b8495;
    font-size: 14px;
}

.metric-value {
    font-size: 25px;
    font-weight: 800;
    color: #18243a;
    margin-top: 6px;
}

/* 뉴스 */
.news-card {
    background: white;
    border-radius: 20px;
    border: 1px solid #e3e7ee;
    padding: 25px;
    margin-top: 10px;
}

.news-title {
    font-size: 23px;
    font-weight: 800;
    color: #18243a;
}

.news-text {
    font-size: 16px;
    color: #5f6878;
    margin-top: 8px;
}

/* 주식 카드 */
.stock-card {
    background: white;
    border-radius: 20px;
    border: 1px solid #e3e7ee;
    padding: 22px;
    min-height: 220px;
}

.stock-name {
    font-size: 22px;
    font-weight: 800;
    color: #18243a;
}

.stock-price {
    font-size: 28px;
    font-weight: 800;
    margin-top: 8px;
    color: #18243a;
}

.stock-info {
    color: #788396;
    font-size: 14px;
    margin-top: 4px;
}

/* 버튼 */
.stButton > button {
    min-height: 48px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 700;
}

/* 입력 */
.stNumberInput input {
    min-height: 45px;
    font-size: 16px;
}

/* 결과 */
.result-card {
    background: white;
    border-radius: 22px;
    padding: 30px;
    border: 1px solid #e3e7ee;
    text-align: center;
}

/* 모바일 */
@media (max-width: 800px) {
    .block-container {
        padding: 15px;
    }
    .title {
        font-size: 30px;
    }
    .stock-card {
        min-height: auto;
    }
}
</style>
""", unsafe_allow_html=True)


# ==============================
# 게임 데이터
# ==============================

STOCKS = {
    "삼성전자": 70000,
    "SK하이닉스": 120000,
    "카카오": 50000
}

NEWS = [
    {
        "type": "positive_stock",
        "title": "삼성전자 신제품 출시 소식",
        "text": "삼성전자의 새로운 제품이 시장에서 좋은 반응을 얻고 있습니다.",
        "stock": "삼성전자"
    },
    {
        "type": "positive_stock",
        "title": "SK하이닉스 반도체 수요 증가",
        "text": "반도체 시장의 수요가 증가하면서 SK하이닉스에 대한 기대가 높아졌습니다.",
        "stock": "SK하이닉스"
    },
    {
        "type": "positive_stock",
        "title": "카카오 신규 서비스 인기",
        "text": "카카오의 새로운 서비스가 많은 이용자를 확보했습니다.",
        "stock": "카카오"
    },
    {
        "type": "negative_stock",
        "title": "삼성전자 실적 전망 하락",
        "text": "삼성전자의 실적에 대한 시장의 우려가 커지고 있습니다.",
        "stock": "삼성전자"
    },
    {
        "type": "negative_stock",
        "title": "SK하이닉스 공급 문제",
        "text": "반도체 공급 문제로 인해 시장의 불안감이 커지고 있습니다.",
        "stock": "SK하이닉스"
    },
    {
        "type": "negative_stock",
        "title": "카카오 규제 우려",
        "text": "새로운 규제 가능성이 제기되면서 투자자들이 조심스러운 모습을 보이고 있습니다.",
        "stock": "카카오"
    },
    {
        "type": "general_positive",
        "title": "국내 증시 상승",
        "text": "투자 심리가 좋아지면서 전체적인 시장 분위기가 상승세를 보이고 있습니다.",
        "stock": None
    },
    {
        "type": "general_negative",
        "title": "국내 증시 하락",
        "text": "경제에 대한 불안감이 커지면서 전체적인 시장이 하락했습니다.",
        "stock": None
    },
    {
        "type": "surge",
        "title": "시장 급등",
        "text": "강한 매수세가 나타나면서 관련 종목의 주가가 크게 상승했습니다.",
        "stock": None
    },
    {
        "type": "crash",
        "title": "시장 급락",
        "text": "갑작스러운 악재로 시장이 큰 폭으로 하락했습니다.",
        "stock": None
    }
]


# ==============================
# 게임 초기화
# ==============================

def new_game():
    st.session_state.cash = 1_000_000
    st.session_state.prices = STOCKS.copy()
    st.session_state.holdings = {stock: 0 for stock in STOCKS}
    st.session_state.turn = 1
    st.session_state.history = []
    st.session_state.trade_history = []
    st.session_state.news = None
    st.session_state.game_over = False
    st.session_state.last_changes = {stock: 0 for stock in STOCKS}


# 처음 실행
if "cash" not in st.session_state:
    new_game()


# ==============================
# 계산
# ==============================

def total_asset():
    stock_value = sum(
        st.session_state.prices[stock] * st.session_state.holdings[stock]
        for stock in STOCKS
    )
    return st.session_state.cash + stock_value


def profit_rate():
    return (total_asset() - 1_000_000) / 1_000_000 * 100


# ==============================
# 뉴스 생성 및 주가 적용
# ==============================

def generate_news():
    news = random.choices(
        NEWS,
        weights=[4, 4, 4, 5, 5, 5, 3, 5, 3, 5]
    )[0]
    st.session_state.news = news


def apply_news():
    news = st.session_state.news
    if not news:
        return

    news_type = news["type"]
    affected = news["stock"]
    changes = {}

    for stock in STOCKS:
        if news_type == "positive_stock":
            change = random.randint(20, 40) if stock == affected else random.randint(-25, 25)
        elif news_type == "negative_stock":
            change = random.randint(-40, -20) if stock == affected else random.randint(-25, 25)
        elif news_type == "general_positive":
            change = random.randint(10, 30)
        elif news_type == "general_negative":
            change = random.randint(-30, -10)
        elif news_type == "surge":
            change = random.randint(40, 60)
        elif news_type == "crash":
            change = random.randint(-60, -40)
        else:
            change = random.randint(-25, 25)

        old_price = st.session_state.prices[stock]
        new_price = max(1000, int(old_price * (1 + change / 100)))
        st.session_state.prices[stock] = new_price
        changes[stock] = change

    st.session_state.last_changes = changes


# ==============================
# 매수 / 매도
# ==============================

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
    st.session_state.cash += revenue
    st.session_state.holdings[stock] -= amount
    st.session_state.trade_history.insert(0, f"매도 | {stock} {amount:,}주 | ₩{revenue:,}")


# ==============================
# 턴 진행
# ==============================

def next_turn():
    st.session_state.history.append(total_asset())
    generate_news()
    apply_news()
    st.session_state.turn += 1

    if st.session_state.turn > 10:
        st.session_state.game_over = True


# ==============================
# 게임 종료 화면
# ==============================

if st.session_state.game_over:
    asset = total_asset()
    profit = profit_rate()

    if profit >= 50:
        grade = "S"
    elif profit >= 25:
        grade = "A"
    elif profit >= 10:
        grade = "B"
    elif profit >= 0:
        grade = "C"
    else:
        grade = "D"

    st.markdown('<div class="title-box"><div class="title">STOCK TYCOON</div><div class="subtitle">게임 결과</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-card"><h1>게임 종료</h1><h2>등급 {grade}</h2><h3>최종 자산</h3><h2>₩{asset:,}</h2><p>수익률 {profit:+.2f}%</p></div>', unsafe_allow_html=True)

    st.write("")

    if st.session_state.history:
        chart_data = pd.DataFrame({"자산": st.session_state.history})
        st.line_chart(chart_data, use_container_width=True)

    if st.button("새 게임 시작", use_container_width=True):
        new_game()
        st.rerun()

    st.stop()


# ==============================
# 메인 UI
# ==============================

# 상단 제목
st.markdown('<div class="title-box"><div class="title">STOCK TYCOON</div><div class="subtitle">뉴스와 시장의 변화를 이용해 최고의 투자자가 되어보세요.</div></div>', unsafe_allow_html=True)

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

# 뉴스
st.markdown('<div class="section-title">오늘의 뉴스</div>', unsafe_allow_html=True)

if st.session_state.news:
    news = st.session_state.news
    st.markdown(f'<div class="news-card"><div class="news-title">{news["title"]}</div><div class="news-text">{news["text"]}</div></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="news-card"><div class="news-title">아직 뉴스가 없습니다.</div><div class="news-text">첫 번째 턴을 진행해보세요.</div></div>', unsafe_allow_html=True)

# 주식 시장
st.markdown('<div class="section-title">주식 시장</div>', unsafe_allow_html=True)

columns = st.columns(3)

for index, stock in enumerate(STOCKS):
    price = st.session_state.prices[stock]
    change = st.session_state.last_changes[stock]
    holding = st.session_state.holdings[stock]

    with columns[index]:
        st.markdown(f'<div class="stock-card"><div class="stock-name">{stock}</div><div class="stock-price">₩{price:,}</div><div class="stock-info">변동률 {change:+d}%</div><div class="stock-info" style="margin-top: 15px;">보유량 : {holding:,}주</div></div>', unsafe_allow_html=True)
        
        st.write("")
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

# 시장 현황
st.markdown('<div class="section-title">시장 현황</div>', unsafe_allow_html=True)
price_df = pd.DataFrame(st.session_state.prices, index=["현재가"]).T
st.bar_chart(price_df, use_container_width=True)

# 거래 기록
st.markdown('<div class="section-title">최근 거래</div>', unsafe_allow_html=True)

if st.session_state.trade_history:
    for trade in st.session_state.trade_history[:8]:
        st.info(trade)
else:
    st.caption("아직 거래 기록이 없습니다.")

# 턴 진행 및 리셋
st.write("")

if st.button("다음 턴 진행", type="primary", use_container_width=True):
    if st.session_state.turn <= 10:
        next_turn()
        st.rerun()

st.write("")

if st.button("게임 초기화", use_container_width=True):
    new_game()
    st.rerun()

st.caption("※ 이 게임의 주가는 실제 주식 가격이 아닌 랜덤 시뮬레이션입니다.")

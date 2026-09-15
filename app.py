import streamlit as st
import random
import pandas as pd

# ==============================
# 기본 설정
# ==============================

st.set_page_config(
    page_title="STOCK TYCOON : MOCK TEST",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS - 모의고사 스타일 & 대형 뉴스 박스
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
    background: linear-gradient(135deg, #18243a, #2b3d5b);
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
    color: #18243a;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* 대시보드 카드 */
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
    font-size: 24px;
    font-weight: 800;
    color: #18243a;
    margin-top: 6px;
    white-space: nowrap;
}

/* 모의고사형 대형 뉴스 카운트다운 박스 */
.news-card-large {
    background: #ffffff;
    border: 2px solid #2b3d5b;
    border-radius: 20px;
    padding: 30px 35px;
    margin-top: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.news-badge {
    display: inline-block;
    background: #18243a;
    color: #ffffff;
    font-size: 13px;
    font-weight: 700;
    padding: 5px 12px;
    border-radius: 6px;
    margin-bottom: 15px;
}

.news-title-large {
    font-size: 26px;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.4;
    margin-bottom: 15px;
}

.news-text-large {
    font-size: 16px;
    color: #334155;
    line-height: 1.75;
    background: #f8fafc;
    padding: 20px;
    border-left: 4px solid #3b82f6;
    border-radius: 8px;
    white-space: pre-line;
    font-family: 'Malgun Gothic', sans-serif;
}

/* 주식 카드 */
.stock-card {
    background: white;
    border-radius: 20px;
    border: 1px solid #e3e7ee;
    padding: 22px;
    min-height: 240px;
    margin-bottom: 10px;
}

.stock-name {
    font-size: 22px;
    font-weight: 800;
    color: #18243a;
    white-space: nowrap;
    word-break: keep-all;
}

.stock-price {
    font-size: 26px;
    font-weight: 800;
    margin-top: 8px;
    color: #18243a;
    white-space: nowrap;
}

.stock-info {
    color: #788396;
    font-size: 14px;
    margin-top: 4px;
    white-space: nowrap;
}

.result-card {
    background: white;
    border-radius: 22px;
    padding: 30px;
    border: 1px solid #e3e7ee;
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
    .news-title-large { font-size: 20px; }
    .news-text-large { font-size: 14px; }
}
</style>
""", unsafe_allow_html=True)


# ==============================
# 모의고사형 고난도 경제 지문 데이터
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
        "code": "MOCK-01",
        "title": "[분석 지문] 중앙은행의 빅컷 단행과 고대역폭 메모리(HBM) 수급 불균형 현상 분석",
        "text": """미국 연방준비제도(Fed)가 경기 연착륙을 목적으로 시중 기준금리를 50bp 인하하는 '빅컷'을 기습적으로 단행하였다. 이에 따라 시장 전반의 기술주 수급 환경이 개선되는 가운데, 반도체 산업군에서는 차세대 AI 연산 처리에 필수적인 고대역폭 메모리(HBM3E) 공급 부족 사태가 장기화되는 양상이다.

특히 주요 AI 서버 제조업체들의 차세대 GPU 출하 스케줄이 당초 계획보다 앞당겨짐에 따라, 글로벌 메모리 반도체 공급망을 전담하고 있는 SK하이닉스의 수혜 폭이 극대화될 것이라는 분석이 지배적이다. 반면 상방 압력을 받던 기타 IT 대형주들은 공급망 유동성 확대에도 불구하고 개별 악재로 상쇄되고 있다.""",
        "effects": {"SK하이닉스": (25, 45), "삼성전자": (-10, 10), "엔비디아": (15, 30), "카카오": (5, 15), "테슬라": (0, 10)}
    },
    {
        "code": "MOCK-02",
        "title": "[분석 지문] 글로벌 반도체 대중국 수출 규제안 개정과 GPU 파운드리 병목",
        "text": """미 상무부가 첨단 반도체 기술의 지정학적 리스크 완화를 이유로 대중국 컴퓨팅 파워 연산력 규제 기준(TPP/PD)을 한층 더 강화하였다. 이에 따라 고성능 데이터센터용 AI 가속기의 글로벌 유통 경로가 엄격히 제한될 위기에 직면하였다.

이로 인해 텐서 코어 기반 GPU 시장을 독점하다시피 하고 있는 엔비디아의 주요 라인업 출하량이 급감할 것으로 추정되며, 단기 영업이익률 하락이 불가피해졌다. 이와 반대로 반도체 섹터의 전반적 위축 신호는 대체 안전자산 및 플랫폼 관련주로의 단기 수급 이탈 현상을 부추기고 있다.""",
        "effects": {"엔비디아": (-45, -25), "SK하이닉스": (-20, -5), "카카오": (10, 25), "삼성전자": (-10, 5), "테슬라": (-5, 5)}
    },
    {
        "code": "MOCK-03",
        "title": "[분석 지문] 자율주행 알고리즘 안전성 심사 승인과 독자 수퍼컴퓨터 데이터센터 가동",
        "text": """글로벌 주요 연방도로교통안전국(NHTSA)이 라이다(LiDAR) 센서에 의존하지 않는 비전(Vision) 기반 신경망 알고리즘의 완전자율주행(FSD) 상용화 안건을 최종 승인하였다. 이와 더불어 차세대 AI 수퍼컴퓨터 인프라 조성을 위한 자체 서버 가동이 공식적으로 본격화되었다.

자체 플랫폼의 수직 계열화 성공을 발판 삼아 테슬라의 소프트웨어 구독 모델 매출 성장성이 시장 예상치를 대폭 상회할 것으로 진단된다. 해당 호재는 타 전기차/소프트웨어 테마주 대비 해당 기업으로의 폭발적인 매수 쏠림 현상을 유발하고 있다.""",
        "effects": {"테슬라": (35, 55), "엔비디아": (10, 20), "삼성전자": (-5, 5), "SK하이닉스": (0, 10), "카카오": (-10, 5)}
    },
    {
        "code": "MOCK-04",
        "title": "[분석 지문] 독점규제 및 공정거래에 관한 법률 개정안 및 독점적 플랫폼 과징금 부과",
        "text": """공정거래위원회가 국내 거대 IT 플랫폼 사업자의 시장지배적 지위 남용 및 자사 우대 행위에 대한 제재 방안으로 집행 가능한 최대 규모의 징벌적 과징금을 부과하고 법적 제재 절차에 착수하였다.

이번 법적 리스크는 단기적 비용 증가를 넘어 플랫폼 알고리즘 개편 및 핵심 서비스 수익 모델 훼손이라는 불확실성을 키우고 있다. 이에 따라 카카오를 포함한 국내 주요 IT 플랫폼 상장사 전반에 걸쳐 중장기 밸류에이션 하향 조정(Rerating) 조치가 이어지는 중이다.""",
        "effects": {"카카오": (-50, -30), "삼성전자": (-5, 5), "SK하이닉스": (-5, 5), "테슬라": (0, 5), "엔비디아": (0, 5)}
    },
    {
        "code": "MOCK-05",
        "title": "[분석 지문] 파운드리 수율 정상화 진통 및 차세대 2nm 공정 양산 스케줄 지연 이슈",
        "text": """메모리 사업부의 실적 반등에도 불구하고 글로벌 탑티어 시스템 반도체 파운드리 라인의 수율 개선 속도가 시장의 기대치를 크게 밑돌고 있다. 특히 GAA(Gate-All-Around) 기반 2nm 공정의 테스트 수율 확보 지연으로 빅테크 칩 수주 전선에 경고등이 켜졌다.

이로 인해 종합 반도체 기업(IDM) 구조를 지닌 삼성전자의 시스템 LSI 및 파운드리 부문 적자 폭 확대가 장기화될 위험이 고조되었다. 동종 업계 경쟁사들 대비 상대적 주가 디스카운트 폭이 가파르게 넓어지고 있다.""",
        "effects": {"삼성전자": (-35, -15), "SK하이닉스": (5, 20), "엔비디아": (-10, 0), "테슬라": (-5, 5), "카카오": (-5, 5)}
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
    st.session_state.buy_costs = {stock: 0 for stock in STOCKS}  # 평단가용
    st.session_state.turn = 1
    st.session_state.history = []
    st.session_state.trade_history = []
    st.session_state.game_over = False
    st.session_state.last_changes = {stock: 0 for stock in STOCKS}
    st.session_state.price_history = [STOCKS.copy()]
    
    # 첫 턴 지문 미리 뽑기
    st.session_state.current_news = random.choice(EXAM_NEWS)


if "cash" not in st.session_state:
    new_game(1_000_000)


# ==============================
# 계산 함수
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
    
    # 평단가 비율 차감
    avg_price = st.session_state.buy_costs[stock] / st.session_state.holdings[stock]
    st.session_state.buy_costs[stock] -= int(avg_price * amount)
    
    st.session_state.cash += revenue
    st.session_state.holdings[stock] -= amount
    st.session_state.trade_history.insert(0, f"매도 | {stock} {amount:,}주 | ₩{revenue:,}")


# ==============================
# 턴 진행 (지문 효과 반영 후 새 지문)
# ==============================

def next_turn():
    st.session_state.history.append(total_asset())
    
    # 현재 읽은 모의고사 지문의 주가 영향 반영
    current_effects = st.session_state.current_news["effects"]
    changes = {}

    for stock in STOCKS:
        min_p, max_p = current_effects.get(stock, (-10, 10))
        change = random.randint(min_p, max_p)
        
        old_price = st.session_state.prices[stock]
        new_price = max(1000, int(old_price * (1 + change / 100)))
        st.session_state.prices[stock] = new_price
        changes[stock] = change

    st.session_state.last_changes = changes
    st.session_state.price_history.append(st.session_state.prices.copy())
    st.session_state.turn += 1

    if st.session_state.turn > 10:
        st.session_state.game_over = True
    else:
        # 다음 턴 모의고사 지문 뽑기
        st.session_state.current_news = random.choice(EXAM_NEWS)


# ==============================
# 게임 종료 화면
# ==============================

if st.session_state.game_over:
    asset = total_asset()
    profit = profit_rate()

    if profit >= 50:
        grade = "S (1등급 - 수석)"
    elif profit >= 25:
        grade = "A (2등급 - 우수)"
    elif profit >= 10:
        grade = "B (3등급 - 보통)"
    elif profit >= 0:
        grade = "C (4등급 - 미달)"
    else:
        grade = "D (5등급 - 과락)"

    st.markdown('<div class="title-box"><div class="title">STOCK TYCOON</div><div class="subtitle">금융/경제 모의고사 결과</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-card"><h1>수능 모의고사 평가 완료</h1><h2>{grade}</h2><h3>최종 자산</h3><h2>₩{asset:,}</h2><p>수익률 {profit:+.2f}%</p></div>', unsafe_allow_html=True)

    st.write("")

    if st.session_state.history:
        st.markdown('<div class="section-title">자산 변화 추이</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({"자산": st.session_state.history})
        chart_data.index = [f"{i+1}턴" for i in range(len(st.session_state.history))]
        st.line_chart(chart_data, use_container_width=True)

    if st.button("새 시험 시작", use_container_width=True):
        new_game(st.session_state.start_cash)
        st.rerun()

    st.stop()


# ==============================
# 메인 UI
# ==============================

# 상단 제목
st.markdown('<div class="title-box"><div class="title">STOCK TYCOON : MOCK TEST</div><div class="subtitle">지문을 정밀 분석하여 시장의 변화를 예측하고 투자하세요.</div></div>', unsafe_allow_html=True)

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
    st.markdown(f'<div class="metric-card"><div class="metric-label">현재 문항</div><div class="metric-value">{min(st.session_state.turn, 10)} / 10</div></div>', unsafe_allow_html=True)

st.write("")
st.progress(min(st.session_state.turn / 10, 1.0))


# ==============================
# 모의고사 지문 영역 (대형 박스)
# ==============================

st.markdown('<div class="section-title">오늘의 분석 지문 (다음 턴 주가에 반영)</div>', unsafe_allow_html=True)

news = st.session_state.current_news

st.markdown(f"""
<div class="news-card-large">
    <div class="news-badge">문항 코드: {news['code']}</div>
    <div class="news-title-large">{news['title']}</div>
    <div class="news-text-large">{news['text']}</div>
</div>
""", unsafe_allow_html=True)


# ==============================
# 주식 시장 UI (평단가 및 평가 손익 표기)
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
        
        # 평단가 및 수익률 계산
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

# 주가 변동 추이 차트
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

if st.button("지문 분석 완료 ➔ 다음 턴으로 주가 반영", type="primary", use_container_width=True):
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

st.caption("※ 이 게임의 주가는 모의고사 지문 분석에 따라 확률적으로 달라집니다.")

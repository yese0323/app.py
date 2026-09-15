import streamlit as st
import random
import pandas as pd

# ==============================
# 기본 설정
# ==============================

st.set_page_config(
    page_title="STOCK TYCOON : HARDCORE EXAM",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS - 고난도 모의고사 스타일
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
    background: #dc2626;
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
# 고난도(불수능) 모의고사 지문 데이터베이스 (트릭 함정 다수)
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
        "code": "HARD-01 (역발상 고난도)",
        "title": "[분석 지문] 기준금리 인하 기조 속 시중 유동성 흡수와 대체 투자 재편",
        "text": """중앙은행이 경기 진작을 위해 기준금리 인하를 발표했으나, 통화당국은 물가 상방 압력을 통제하고자 역레포(Reverse Repo) 금리를 상향 조정하여 시중 단기 유동성을 강하게 흡수하는 상반된 정책을 동시 집행하였다.

이로 인해 시장 전반에는 금리 인하로 인한 수혜 기대감보다는, 금융권 자금이 위험자산인 IT·플랫폼 부문에서 이탈하여 확실한 고정 채권형 자산으로 이동하는 기이현상이 관측된다. 한편, 고유가 지속으로 리튬·니켈 등 이차전지 원자재 조달 수입 원가가 상쇄된 덕분에 완성차/배터리 제조 단가 둔화 세는 소폭 완화되는 반사이익이 발생하고 있다.""",
        # 금리인하 호재 착시가 있으나 IT/플랫폼 폭락, 완성차(테슬라) 방어/상승
        "effects": {"삼성전자": (-25, -10), "SK하이닉스": (-30, -15), "카카오": (-40, -20), "테슬라": (15, 30), "엔비디아": (-20, -5)}
    },
    {
        "code": "HARD-02 (기술 패러다임)",
        "title": "[분석 지문] AI 캐펙스(CAPEX) 과잉 투자 회의론과 ASIC 맞춤형 칩 대체 전환",
        "text": """빅테크 기업들의 AI 인프라 투자(CAPEX) 대비 실질 수익성(ROI) 창출 시점이 연기됨에 따라 글로벌 벤처캐피털을 중심으로 AI 거품론이 제기되었다. 이에 빅테크 기업들은 비싼 범용 GPU 구매를 급격히 줄이고, 자체 설계한 주문형 반도체(ASIC) 생산 비율을 확대하기로 방침을 선회하였다.

이러한 전환은 범용 GPU 공급망을 독점하던 기업에 극심한 악재로 작용하나, 맞춤형 ASIC 반도체의 위탁 생산(Foundry) 및 메모리 유통을 전담하는 레거시 및 파운드리 대기업에게는 오히려 대규모 대체 수주 기회가 열리고 있다.""",
        # 엔비디아 급락, 파운드리/레거시 반도체(삼성전자) 급등, 하이닉스 혼조, 테슬라/카카오 영향 소폭
        "effects": {"엔비디아": (-45, -25), "삼성전자": (20, 40), "SK하이닉스": (-10, 10), "테슬라": (5, 15), "카카오": (-5, 5)}
    },
    {
        "code": "HARD-03 (통화 및 환율 함정)",
        "title": "[분석 지문] 강달러 환율 오버슈팅 및 반덤핑 상계관세 부과 조치",
        "text": """원/달러 환율이 거시경제 불확실성으로 인해 단기적 오버슈팅 현상을 보이며 급등하였다. 일반적으로 환율 상승은 수출 기업의 가격 경쟁력을 높여 호재로 작용하지만, 미 통상무역위원회(ITC)가 한국산 반도체 부품 및 플랫폼 소프트웨어 수출 품목에 30%에 달하는 기습적 반덤핑 상계관세를 부과하면서 상황이 반전되었다.

반면 환차익으로 인한 매출 착시가 극대화되는 해외 본사 소재 빅테크 기업 및 외화 자산 보유 비율이 높은 글로벌 기업으로 외국인 순매수가 강하게 쏠리는 현상이 나타나고 있다.""",
        # 국장(삼성, 하이닉스, 카카오) 관세 폭탄 하락, 미장(테슬라, 엔비디아) 환차익 및 쏠림 급등
        "effects": {"삼성전자": (-25, -10), "SK하이닉스": (-20, -5), "카카오": (-30, -15), "테슬라": (25, 45), "엔비디아": (20, 40)}
    },
    {
        "code": "HARD-04 (플랫폼 및 서비스)",
        "title": "[분석 지문] 생성형 AI 서비스 망사용료 법안 통과 및 망 중립성 완화",
        "text": """국회 본회의에서 거대 글로벌 콘텐츠 사업자 및 국내 초거대 AI 플랫폼 트래픽 발생 주체에게 고율의 '망 이용 대가' 부담을 의무화하는 법안이 통과되었다. 이번 법안으로 AI 모델 운영에 막대한 서버 데이터 비용이 추가 발생하게 되었다.

그러나 대형 플랫폼사 중 유일하게 자체 IDC 국산화율이 높은 기업은 망 비용 절감 효과를 입어 독점적 시장 지위를 구축할 것으로 전망된다. 반면 글로벌 빅테크 및 해외 라이벌 기업들은 국내 서비스 운영 비용의 폭발적 증가로 당분간 한국 시장 내 마케팅을 축소할 예정이다.""",
        # 카카오 반사이익 급등, 글로벌 테크/반도체 단기 위축
        "effects": {"카카오": (30, 50), "삼성전자": (-5, 5), "SK하이닉스": (-5, 5), "엔비디아": (-20, -5), "테슬라": (-10, 0)}
    },
    {
        "code": "HARD-05 (공급망 규제)",
        "title": "[분석 지문] 자율주행 데이터 안보법 제정과 희토류 수출 통제 보복 조치",
        "text": """지정학적 갈등 심화로 주요 원자재 수출국이 차량용 핵심 희토류 및 영구자석 수출 제한령을 발효하였다. 이와 함께 글로벌 주요국은 자국 내 도로 주행 데이터의 해외 서버 이전을 엄격히 금지하는 법안을 신설하였다.

이로 인해 센서 기반 주행 데이터를 글로벌 서버로 수집·학습해야 하는 해외 자율주행 완성차 기업은 데이터 유입 마비와 생산 원가 폭등이라는 이중고에 직면하였다. 한편, 차량용 반도체 대체 수혜 및 내수 플랫폼 기반 데이터 교환 기업은 안전지대로 평가받고 있다.""",
        # 테슬라 폭락, 엔비디아 하락, 카카오/삼성전자 상대적 반사이익
        "effects": {"테슬라": (-50, -30), "엔비디아": (-15, -5), "카카오": (15, 30), "삼성전자": (10, 20), "SK하이닉스": (-5, 5)}
    },
    {
        "code": "HARD-06 (기저효과 및 재고)",
        "title": "[분석 지문] 메모리 반도체 덤핑 재고 소진 완료 및 기저효과 착시",
        "text": """메모리 반도체 시장의 장기 불황을 이끌었던 악성 재고가 완전 소진되며 DRAM 및 NAND 고정 거래가가 반등하기 시작했다. 그러나 시장 전문가들은 이번 가격 상승이 수요의 폭발적 증가에 의한 것이 아니라, 제조사들의 극단적 감산에 따른 '기저효과'일 뿐이라고 경고한다.

재무구조 개선 효과로 메모리 전업 기업의 주가는 일시적 오버슈팅이 예상되나, 실제 완제품 교체 수요가 뒷받침되지 않아 빅테크 및 시스템 반도체 설계사들의 실적 추정치는 하향 조정되고 있다.""",
        # SK하이닉스 급등, 삼성전자 상승, 엔비디아/테슬라 하락
        "effects": {"SK하이닉스": (30, 50), "삼성전자": (10, 25), "엔비디아": (-20, -5), "테슬라": (-15, -5), "카카오": (-5, 5)}
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
    avg_price = st.session_state.buy_costs[stock] / st.session_state.holdings[stock]
    st.session_state.buy_costs[stock] -= int(avg_price * amount)
    
    st.session_state.cash += revenue
    st.session_state.holdings[stock] -= amount
    st.session_state.trade_history.insert(0, f"매도 | {stock} {amount:,}주 | ₩{revenue:,}")


# ==============================
# 턴 진행
# ==============================

def next_turn():
    st.session_state.history.append(total_asset())
    
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
        st.session_state.current_news = random.choice(EXAM_NEWS)


# ==============================
# 게임 종료 화면
# ==============================

if st.session_state.game_over:
    asset = total_asset()
    profit = profit_rate()

    if profit >= 60:
        grade = "S (상위 0.1% 수능 만점자)"
    elif profit >= 30:
        grade = "A (1등급 - 경제 전문가)"
    elif profit >= 10:
        grade = "B (2등급 - 우수)"
    elif profit >= 0:
        grade = "C (3등급 - 보통)"
    else:
        grade = "D (4등급 이하 - 원금 손실)"

    st.markdown('<div class="title-box"><div class="title">STOCK TYCOON</div><div class="subtitle">불수능 경제 지문 모의고사 최종 결과</div></div>', unsafe_allow_html=True)
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

st.markdown('<div class="title-box"><div class="title">STOCK TYCOON : HARDCORE EXAM</div><div class="subtitle">지문의 숨겨진 맹점과 트릭을 파악해 실질 수혜 종목을 예측하세요.</div></div>', unsafe_allow_html=True)

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
# 고난도 모의고사 지문
# ==============================

st.markdown('<div class="section-title">오늘의 심화 경제 지문 (분석 후 다음 턴 주가 반영)</div>', unsafe_allow_html=True)

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

st.caption("※ 본 시뮬레이션 지문은 다중 유동성/무역 규제 변수가 복합 적용되어 있습니다.")

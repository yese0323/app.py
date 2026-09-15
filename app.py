import streamlit as st
import random
import pandas as pd

st.set_page_config(
    page_title="STOCK TYCOON : UNPREDICTABLE MARKET",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp {
    background-color: #0b0f19;
    color: #f1f5f9;
}

.block-container {
    max-width: 1250px;
    padding: 20px 30px 40px 30px;
}

/* Header Banner */
.title-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    border: 1px solid #312e81;
    padding: 26px 32px;
    border-radius: 20px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.title {
    font-size: 34px;
    font-weight: 900;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    font-size: 15px;
    color: #94a3b8;
    margin-top: 6px;
}

.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 24px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Dashboard Metric Cards */
.metric-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 18px 22px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.metric-label {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-value {
    font-size: 26px;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 6px;
    white-space: nowrap;
}

/* Flash Event Display Banner */
.flash-event-box {
    background: linear-gradient(135deg, #450a0a 0%, #881337 100%);
    border: 2px solid #f43f5e;
    border-radius: 18px;
    padding: 22px 28px;
    margin-top: 15px;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px rgba(244, 63, 94, 0.25);
    animation: pulse 2s infinite;
}

.flash-badge {
    display: inline-block;
    background: #f43f5e;
    color: #ffffff;
    font-size: 12px;
    font-weight: 900;
    padding: 4px 12px;
    border-radius: 6px;
    margin-bottom: 10px;
    letter-spacing: 1px;
}

.flash-title {
    font-size: 22px;
    font-weight: 900;
    color: #ffe4e6;
    margin-bottom: 8px;
}

.flash-text {
    font-size: 15px;
    color: #fecdd3;
    font-weight: 500;
    line-height: 1.6;
}

/* Market News Exam Card */
.news-card-large {
    background: #1e293b;
    border: 1px solid #475569;
    border-radius: 18px;
    padding: 26px 30px;
    margin-top: 10px;
    margin-bottom: 20px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.news-badge {
    display: inline-block;
    background: #3b82f6;
    color: #ffffff;
    font-size: 12px;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 6px;
    margin-bottom: 12px;
}

.news-title-large {
    font-size: 22px;
    font-weight: 800;
    color: #f8fafc;
    line-height: 1.4;
    margin-bottom: 14px;
}

.news-text-large {
    font-size: 15px;
    color: #cbd5e1;
    line-height: 1.8;
    background: #0f172a;
    padding: 20px;
    border-left: 4px solid #3b82f6;
    border-radius: 10px;
    white-space: pre-line;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
}

/* Stock Component Cards */
.stock-card {
    background: #1e293b;
    border-radius: 18px;
    border: 1px solid #334155;
    padding: 20px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.stock-name {
    font-size: 20px;
    font-weight: 800;
    color: #f8fafc;
}

.stock-price {
    font-size: 24px;
    font-weight: 800;
    margin-top: 6px;
    color: #38bdf8;
}

.stock-info {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 4px;
}

/* Evaluation Score Card */
.result-card {
    background: #1e293b;
    border-radius: 24px;
    padding: 40px;
    border: 2px solid #6366f1;
    text-align: center;
    box-shadow: 0 12px 36px rgba(99, 102, 241, 0.2);
}

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

STOCKS = {
    "삼성전자": 70000,
    "SK하이닉스": 120000,
    "카카오": 50000,
    "테슬라": 300000,
    "엔비디아": 180000
}

EXAM_NEWS = [
    {
        "id": "NEWS-01",
        "title": "[분석 지문] 글로벌 마이크로칩 관세 격상 및 반도체 공급망 규제 발효",
        "text": """동아시아산 첨단 메모리 반도체 및 로직 칩 품목에 대해 25%의 수입 관세가 기습 발효되었습니다.
이로 인해 글로벌 공급망 정체 우려가 커지는 반면, 파운드리와 서버 인프라 중심의 기존 빅테크 기업은 수출 비용 증대로 직접 타격을 받을 위험에 직면했습니다.""",
        "effects": {"삼성전자": (-25, -10), "SK하이닉스": (-30, -15), "엔비디아": (-20, -5)}
    },
    {
        "id": "NEWS-02",
        "title": "[분석 지문] AI CAPEX 과잉 투자 회의론과 ASIC 맞춤형 칩 대체 전환",
        "text": """빅테크 기업들의 AI 인프라 투자 대비 실질 수익성 창출 시점이 연기됨에 따라 비싼 범용 GPU 구매를 급격히 줄이고, 자체 설계한 주문형 반도체(ASIC) 생산 비율을 확대하기로 선회하였습니다.

범용 GPU 공급망을 독점하던 기업에 극심한 악재로 작용하나, 맞춤형 ASIC 반도체 위탁 생산(Foundry) 대기업에게는 대규모 대체 수주 기회가 열리고 있습니다.""",
        "effects": {"엔비디아": (-45, -25), "삼성전자": (20, 40), "SK하이닉스": (-10, 10)}
    },
    {
        "id": "NEWS-03",
        "title": "[분석 지문] 기준금리 기습 인하와 역레포 유동성 기조 교차",
        "text": """중앙은행이 경기 진작을 위해 기준금리 인하를 발표했으나, 통화당국은 물가 상방 압력을 통제하고자 역레포 금리를 상향 조정하여 시중 단기 유동성을 흡수하였습니다.

자금 대출 접근성이 높아진 고부채 플랫폼 기술 기업 및 차량 구매 금융 수혜를 받는 자율주행 완성차 부문으로 매수세가 쏠리고 있습니다.""",
        "effects": {"카카오": (20, 35), "테슬라": (15, 30), "삼성전자": (-15, -5)}
    },
    {
        "id": "NEWS-04",
        "title": "[분석 지문] 양자 컴퓨팅 암호 해독 브레이크스루 및 초전도체 기술 발표",
        "text": """연구소 결합 파트너십을 통해 10,000 큐비트급 양자 컴퓨터 상용화 단계가 공표되었습니다.
기존 데이터센터 및 GPU 가속 시스템의 비효율성이 지적받는 반면, 첨단 반도체 소재 공급 기업과 차세대 양자 알고리즘 플랫폼 기업이 급부상하고 있습니다.""",
        "effects": {"엔비디아": (-30, -15), "SK하이닉스": (25, 45), "카카오": (15, 30)}
    },
    {
        "id": "NEWS-05",
        "title": "[분석 지문] 자율주행 차 데이터 안보 법안 제정과 희토류 수출 통제",
        "text": """주요 원자재 수출국이 차량용 핵심 희토류 수출 제한령을 발효하고 자국 내 도로 주행 데이터 해외 전송을 완전 금지하였습니다.
글로벌 전기차 제조기업은 데이터 유입 마비와 원가 폭등이라는 이중고에 직면하고, 국내 플랫폼/내수 IT는 상대적 안도감을 얻었습니다.""",
        "effects": {"테슬라": (-45, -25), "엔비디아": (-15, -5), "카카오": (15, 25)}
    },
    {
        "id": "NEWS-06",
        "title": "[분석 지문] 법인세 감면 개혁안 및 자사주 소각 이득세 면제 촉진",
        "text": """의회에서 기업 자사주 매입 후 소각 시 상당한 법인세 세제 혜택을 제공하는 주주환원 촉진법이 통과되었습니다.
현금 보유량이 압도적이고 주주환원 여력이 충분한 대형 IT 제조사와 플랫폼 거대 기업에 막대한 혜택이 집중되고 있습니다.""",
        "effects": {"삼성전자": (20, 35), "카카오": (15, 30), "SK하이닉스": (10, 25)}
    },
    {
        "id": "NEWS-07",
        "title": "[분석 지문] 리튬 및 배터리 핵심 원자재 수급 불균형 폭등",
        "text": """광산 채굴 차질 및 국유화 조치로 리튬 및 니켈 가격이 장중 40% 이상 폭등하였습니다.
전기차 생산업체의 영업이익률 절하 우려가 거세지고 있는 반면, 전력 효율성을 극대화하는 반도체 설계사로 투심이 이동 중입니다.""",
        "effects": {"테슬라": (-40, -20), "엔비디아": (15, 30), "삼성전자": (-10, 5)}
    },
    {
        "id": "NEWS-08",
        "title": "[분석 지문] 클라우드 IT 플랫폼 반독점 규제 및 독점 부문 분할 명령",
        "text": """공정거래위원회가 빅테크 플랫폼의 자사 서비스 우대 행위에 대해 고강도 제재 및 독점 사업 부문 분할 소송을 제기하였습니다.
빅테크 및 플랫폼 대기업의 사업 확장에 급동결 조치가 내려졌으나, 반도체 및 하드웨어 제조 중심 기업은 여파를 비켜섰습니다.""",
        "effects": {"카카오": (-45, -25), "테슬라": (-20, -5), "SK하이닉스": (5, 20)}
    },
    {
        "id": "NEWS-09",
        "title": "[분석 지문] 데이터센터 전력망 셧다운 및 친환경 에너지 그리드 의무화",
        "text": """폭증하는 AI 데이터센터 전력 소비로 인해 주요 지방 정부가 신규 센터 승인을 전면 동결하고 친환경 전력 100% 사용을 의무화했습니다.
전력 효율성 인프라 칩 기술을 보유한 반도체 기업에 대한 수요가 기하급수적으로 폭증하고 있습니다.""",
        "effects": {"엔비디아": (25, 50), "SK하이닉스": (20, 35), "테슬라": (-15, 0)}
    },
    {
        "id": "NEWS-10",
        "title": "[분석 지문] 글로벌 메모리 반도체 공급 과잉 및 감산 합의 진통",
        "text": """메모리 반도체 재고가 역대 최고치를 기록한 가운데 주요 제조사 간 감산 합의가 결렬되며 가격 하락 경쟁이 촉발되었습니다.
메모리 비중이 절대적인 기업의 적자 전환 우려가 커지고 있으며 비메모리 및 파운드리 중심 기업의 가치가 상대적으로 조명을 받습니다.""",
        "effects": {"SK하이닉스": (-40, -20), "삼성전자": (-15, 5), "엔비디아": (10, 25)}
    },
    {
        "id": "NEWS-11",
        "title": "[분석 지문] 환율 오버슈팅 급등 및 고관세 상계 조치",
        "text": """외환 시장에서 달러 가치가 폭등함과 동시에 주요 수입국에서 첨단 품목 대상 기습적 보복 관세를 시행했습니다.
해외 매출 비중이 절대적인 글로벌 테크 기업의 환차익과 비용 증가 우려가 동시 교차하고 내수 위주 기업은 방어력을 상실했습니다.""",
        "effects": {"카카오": (-35, -15), "테슬라": (20, 40), "엔비디아": (15, 30)}
    },
    {
        "id": "NEWS-12",
        "title": "[분석 지문] 글로벌 클라우드 서버 기습 사이버 침해 사태",
        "text": """글로벌 대형 클라우드 서버 망에 사상 최대 규모의 취약점 공격이 감지되어 주요 서비스가 전면 마비되었습니다.
플랫폼 기업의 신뢰도가 크게 실추된 반면 보안 네트워크 고도화를 위한 차세대 칩셋 및 하드웨어 교체 수요가 폭증했습니다.""",
        "effects": {"카카오": (-40, -20), "테슬라": (-25, -10), "삼성전자": (15, 30), "SK하이닉스": (20, 35)}
    }
]

FLASH_EVENTS = [
    {
        "title": "🚨 [블랙스완] 글로벌 대형 자산운용사 뱅크런 및 숏스퀴즈 파산 사태!",
        "text": "해외 유수 헤지펀드의 기습 청산 소식으로 전 세계 자본 시장에 파니셀 공포가 집어삼켰습니다! 전체 주가가 사태 진정 전까지 미친 듯이 급락합니다.",
        "effects": {"삼성전자": -45, "SK하이닉스": -50, "카카오": -55, "테슬라": -40, "엔비디아": -45}
    },
    {
        "title": "🚀 [오일머니 서프라이즈] 국부펀드의 150조 원 테크 매수 집행!",
        "text": "중동 국부펀드가 자산 재배분을 통해 보유 상장 주식을 장중 시가로 쓸어담기 시작했습니다! 시장 전체 종목이 폭발적으로 급등합니다.",
        "effects": {"삼성전자": 50, "SK하이닉스": 55, "카카오": 40, "테슬라": 60, "엔비디아": 65}
    },
    {
        "title": "⚡ [급등락 돌발] 연준(Fed) 긴급 100bp 금리 변경 긴급성명 발표!",
        "text": "거시 경제 이상 징후로 긴급 금리조정이 발표되었습니다. 극심한 변동성과 함께 종목별로 수급이 극단적으로 갈립니다.",
        "effects": {"삼성전자": 25, "SK하이닉스": -30, "카카오": 45, "테슬라": -35, "엔비디아": 30}
    }
]

def init_game(start_cash=1_000_000):
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
    
    # Non-repeating news engine initialization
    news_deck = EXAM_NEWS.copy()
    random.shuffle(news_deck)
    st.session_state.news_deck = news_deck
    st.session_state.current_news = st.session_state.news_deck.pop()
    st.session_state.flash_event = None


if "cash" not in st.session_state:
    init_game(1_000_000)


def total_asset():
    stock_val = sum(st.session_state.prices[s] * st.session_state.holdings[s] for s in STOCKS)
    return st.session_state.cash + stock_val

def profit_rate():
    start = st.session_state.get("start_cash", 1_000_000)
    if start == 0: return 0.0
    return ((total_asset() - start) / start) * 100

def buy_stock(stock, amount):
    price = st.session_state.prices[stock]
    cost = price * amount
    if amount <= 0:
        st.warning("1주 이상 매수 가능합니다.")
        return
    if cost > st.session_state.cash:
        st.error("보유 현금이 부족합니다.")
        return
    st.session_state.cash -= cost
    st.session_state.holdings[stock] += amount
    st.session_state.buy_costs[stock] += cost
    st.session_state.trade_history.insert(0, f"매수 | {stock} {amount:,}주 | ₩{cost:,}")

def sell_stock(stock, amount):
    price = st.session_state.prices[stock]
    if amount <= 0:
        st.warning("1주 이상 매도 가능합니다.")
        return
    if amount > st.session_state.holdings[stock]:
        st.error("보유한 수량보다 더 많이 매도할 수 없습니다.")
        return
    revenue = price * amount
    avg_p = st.session_state.buy_costs[stock] / st.session_state.holdings[stock]
    st.session_state.buy_costs[stock] -= int(avg_p * amount)
    st.session_state.cash += revenue
    st.session_state.holdings[stock] -= amount
    st.session_state.trade_history.insert(0, f"매도 | {stock} {amount:,}주 | ₩{revenue:,}")

def next_turn():
    st.session_state.history.append(total_asset())
    current_effects = st.session_state.current_news["effects"]
    
    # 1. Flash Event Check (18% trigger rate)
    is_flash = random.random() < 0.18
    flash_data = random.choice(FLASH_EVENTS) if is_flash else None
    st.session_state.flash_event = flash_data

    # 2. Market Reaction Dynamics
    # 25% chance of "Sell the News" (contrarian market reaction)
    is_contrarian = random.random() < 0.25
    changes = {}

    for stock in STOCKS:
        if stock in current_effects:
            min_p, max_p = current_effects[stock]
            base_change = random.randint(min_p, max_p)
            if is_contrarian:
                base_change = -base_change
        else:
            # Unmentioned stocks drift randomly (-15% to +15%)
            base_change = random.randint(-15, 15)
        
        flash_change = flash_data["effects"].get(stock, 0) if flash_data else 0
        
        # Unpredictable market noise (-8% to +8%)
        noise = random.randint(-8, 8)
        
        total_change = base_change + flash_change + noise
        old_price = st.session_state.prices[stock]
        new_price = max(1000, int(old_price * (1 + total_change / 100)))
        st.session_state.prices[stock] = new_price
        changes[stock] = total_change

    st.session_state.last_changes = changes
    st.session_state.price_history.append(st.session_state.prices.copy())
    st.session_state.turn += 1

    # End game or fetch next UNSEEN news item
    if st.session_state.turn > 10:
        st.session_state.game_over = True
    else:
        if st.session_state.news_deck:
            st.session_state.current_news = st.session_state.news_deck.pop()
        else:
            # Fallback if deck runs empty
            st.session_state.current_news = random.choice(EXAM_NEWS)

if st.session_state.game_over:
    asset = total_asset()
    profit = profit_rate()

    if profit >= 80:
        grade = "S (전설의 월가 타짜)"
    elif profit >= 40:
        grade = "A (1등급 - 수석 트레이더)"
    elif profit >= 15:
        grade = "B (2등급 - 우수 투자자)"
    elif profit >= 0:
        grade = "C (3등급 - 원금 방어)"
    else:
        grade = "D (4등급 이하 - 깡통)"

    st.markdown('<div class="title-box"><div class="title">STOCK TYCOON</div><div class="subtitle">최종 트레이딩 결과 리포트</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-card"><h1>평가 완료</h1><h2>등급: {grade}</h2><h3>최종 평가 자산</h3><h2>₩{asset:,}</h2><p style="font-size:20px; font-weight:700; color: {"#34d399" if profit >= 0 else "#f87171"};">총 수익률: {profit:+.2f}%</p></div>', unsafe_allow_html=True)
    st.write("")

    if st.session_state.history:
        st.markdown('<div class="section-title">📊 포트폴리오 자산 추이</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({"자산 평가액": st.session_state.history})
        chart_data.index = [f"{i+1}턴" for i in range(len(st.session_state.history))]
        st.line_chart(chart_data, use_container_width=True)

    if st.button("🔄 새 게임 시작 (뉴스 덱 재설정)", use_container_width=True):
        init_game(st.session_state.start_cash)
        st.rerun()

    st.stop()

st.markdown('<div class="title-box"><div class="title">STOCK TYCOON : UNPREDICTABLE MARKET</div><div class="subtitle">지문 분석만으로는 완벽히 예측할 수 없는 노이즈와 역발상 시장을 돌파하세요.</div></div>', unsafe_allow_html=True)

# Metric Dashboard
asset = total_asset()
profit = profit_rate()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">보유 현금</div><div class="metric-value">₩{st.session_state.cash:,}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">총 평가 자산</div><div class="metric-value">₩{asset:,}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">수익률</div><div class="metric-value" style="color: {"#34d399" if profit >= 0 else "#f87171"};">{profit:+.2f}%</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">현재 턴</div><div class="metric-value">{min(st.session_state.turn, 10)} / 10</div></div>', unsafe_allow_html=True)

st.write("")
st.progress(min(st.session_state.turn / 10, 1.0))

# Flash Event Display
if st.session_state.flash_event:
    fe = st.session_state.flash_event
    st.markdown(f"""
    <div class="flash-event-box">
        <div class="flash-badge">FLASH EVENT - 돌발 변수 발생!</div>
        <div class="flash-title">{fe['title']}</div>
        <div class="flash-text">{fe['text']}</div>
    </div>
    """, unsafe_allow_html=True)

# Exam News Card
st.markdown('<div class="section-title">📰 오늘의 심화 분석 지문 (중복 출제 없음)</div>', unsafe_allow_html=True)
news = st.session_state.current_news

st.markdown(f"""
<div class="news-card-large">
    <div class="news-badge">문항 번호 : {news['id']}</div>
    <div class="news-title-large">{news['title']}</div>
    <div class="news-text-large">{news['text']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">📈 종목 매매 센터</div>', unsafe_allow_html=True)

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
            change_color = "#34d399" if change > 0 else ("#f87171" if change < 0 else "#94a3b8")
            st.markdown(f"""
            <div class="stock-card">
                <div class="stock-name">{stock}</div>
                <div class="stock-price">₩{price:,}</div>
                <div class="stock-info" style="color: {change_color}; font-weight: 700;">직전 변동률: {change:+d}%</div>
                <hr style="margin: 10px 0; border:none; border-top:1px solid #334155;">
                <div class="stock-info"><b>보유량:</b> {holding:,}주</div>
                <div class="stock-info"><b>{avg_text}</b></div>
                <div class="stock-info" style="font-weight:700;">{profit_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
            amount = st.number_input("수량 설정", min_value=1, value=1, step=1, key=f"amount_{stock}")

            buy_col, sell_col = st.columns(2)
            with buy_col:
                if st.button("매수", key=f"buy_{stock}", use_container_width=True):
                    buy_stock(stock, amount)
                    st.rerun()

            with sell_col:
                if st.button("매도", key=f"sell_{stock}", use_container_width=True):
                    sell_stock(stock, amount)
                    st.rerun()

st.markdown('<div class="section-title">📉 종목별 주가 변동 추이</div>', unsafe_allow_html=True)
history_df = pd.DataFrame(st.session_state.price_history)
history_df.index = [f"{i}턴" for i in range(len(history_df))]
st.line_chart(history_df, use_container_width=True)

st.markdown('<div class="section-title">📋 최근 거래 내역</div>', unsafe_allow_html=True)
if st.session_state.trade_history:
    for trade in st.session_state.trade_history[:5]:
        st.info(trade)
else:
    st.caption("아직 수행된 거래가 없습니다.")

st.write("")
if st.button("🚀 지문 분석 제출 ➔ 다음 턴 진행", type="primary", use_container_width=True):
    if st.session_state.turn <= 10:
        next_turn()
        st.rerun()

st.write("")
st.markdown('<div class="section-title">⚙️ 게임 설정</div>', unsafe_allow_html=True)
reset_col1, reset_col2 = st.columns([2, 1])

with reset_col1:
    init_cash = st.number_input("시작 소지금 (원)", min_value=1000, value=st.session_state.get("start_cash", 1_000_000), step=100_000)

with reset_col2:
    st.write("")
    st.write("")
    if st.button("게임 초기화", use_container_width=True):
        init_game(init_cash)
        st.rerun()

st.caption("※ 뉴스 덱은 중복 출제되지 않도록 셔플 덱 방식으로 작동하며, 25%의 역발상 반응 및 지문 미언급 종목 무작위 노이즈 변동이 적용됩니다.")

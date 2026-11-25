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
    # 엔비디아
    {"asset": "엔비디아", "news": "젠슨황의 기분이 좋습니다", "min_change": 0.01, "max_change": 0.20},
    {"asset": "엔비디아", "news": "젠슨황이 복귀했습니다", "min_change": 0.01, "max_change": 0.25},
    {"asset": "엔비디아", "news": "젠슨황의 기분이 좋을까요?", "min_change": -0.30, "max_change": -0.10},
    {"asset": "엔비디아", "news": "젠슨황이 잘 하고 있습니다", "min_change": -0.30, "max_change": -0.10},

    # 테슬라
    {"asset": "테슬라", "news": "일론머스크가 기분이 좋습니다", "min_change": 0.01, "max_change": 0.20},
    {"asset": "테슬라", "news": "테슬라가 로드스터를 출시했습니다", "min_change": 0.01, "max_change": 0.30},
    {"asset": "테슬라", "news": "스페이스X의 로켓이 미사일이 되었습니다", "min_change": -0.30, "max_change": -0.10},
    {"asset": "테슬라", "news": "테슬라가 관세 200%를 받습니다", "min_change": -0.40, "max_change": -0.10},

    # 삼성
    {"asset": "삼성", "news": "삼성이 갤럭시S28을 출시했습니다", "min_change": 0.01, "max_change": 0.20},
    {"asset": "삼성", "news": "아이폰의 아이폰 듀오에 내구성 문제가 생겼습니다", "min_change": 0.01, "max_change": 0.15},
    {"asset": "삼성", "news": "이재용이 이재명의 견제를 받습니다", "min_change": -0.30, "max_change": -0.10},
    {"asset": "삼성", "news": "삼성의 휴대폰이 폭발했습니다", "min_change": -0.30, "max_change": -0.10}
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

    # 일반 주식 기본 가격 변동을 먼저 적용
    for asset in STOCKS:
        random_change = random.uniform(-0.05, 0.05)
        new_price = int(
            st.session_state.prices[asset] * (1 + random_change)
        )
        st.session_state.prices[asset] = max(1, new_price)

    # 기본 가격 변동이 끝난 뒤 뉴스 효과를 적용하고, 가격 변경 후 뉴스를 공개
    event = random.choice(NEWS_EVENTS)
    news_asset = event["asset"]
    news_change = random.uniform(event["min_change"], event["max_change"])
    news_base_price = st.session_state.prices[news_asset]
    news_new_price = int(news_base_price * (1 + news_change))
    st.session_state.prices[news_asset] = max(1, news_new_price)

    st.session_state.market_news = (
        f"[{news_asset}] {event['news']} "
        f"(주가 변동: {news_change * 100:+.1f}%)"
    )

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

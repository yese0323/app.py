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

    if st.session_state.market_news_asset:
        news_change = st.session_state.market_news_change

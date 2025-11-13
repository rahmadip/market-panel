import streamlit as st
import streamlit_app as app

st.set_page_config(
    page_title='Stock Panel',
    page_icon=':material/docs:',
    layout='wide',
    initial_sidebar_state='expanded'
)

head = app.headComp(
    icon='docs',
    title='Stock Market IDX',
    typeKey='default',
    placeholder='Enter your code here',
    info='Designed for Indonesian Currency. Only works with IDX Ticker/Code. To check IDX Ticker list, please visit [IDX Stocklist](https://www.idx.co.id/en/market-data/stocks-data/stock-list). Data source from yfinance, data differences may occur. DYOR.'
)

if len(head) == 0:
    st.info('Please enter valid code to access.')
elif len(head) == 4:
    pageStatus = st.progress(0)
    
    data = app.code(head)
        
    c4,c5 = st.columns([3,4])
    with c4:
        mrktPriceContainer = st.container(border=True)
        with mrktPriceContainer:
            mpc1, mpc2 = st.columns([1,7])
            with mpc1:
                st.image(
                    data['logo'],
                    width='stretch'
                )
            with mpc2:
                st.metric(
                    label=data['name'],
                    value=f'Rp {data['price']:,.2f}',
                )
            tabs = st.tabs(app.mrktPriceSetup.keys())
            for tab, name in zip(tabs, app.mrktPriceSetup.keys()):
                with tab:
                    setting = app.mrktPriceSetup[name]
                    try:
                        df = data['ticker'].history(
                            period=setting['period'],
                            interval=setting['interval']
                        )
                        if df is None or df.empty or 'Volume' not in df.columns:
                            st.warning('data not available')
                        else:
                            df = df[df['Volume'] > 0]
                            if df.empty:
                                st.warning('data not available')
                            else:
                                st.plotly_chart(
                                    app.mrktPriceGraph(df),
                                    width='stretch',
                                    config=app.chart
                                )
                    except Exception as e:
                        st.warning('data not available')

    with c5:
        with st.container(border=True):
            incomestmtC,balanceSheetC = st.tabs(['Income Statement','Balance Sheet'])
            with incomestmtC:
                annualIS,quarterIS = st.tabs(['Annual', 'Quarter'])
                with annualIS:
                    incomestmtYDF = app.dfIncomeStmt(
                        data['incomestmtY'],
                        data['shares'],
                        data['price'],
                        'Y'
                    )
                    st.plotly_chart(
                        app.barGraph(
                            incomestmtYDF.T,
                            incomestmtYDF.loc['Total Revenue'],
                            incomestmtYDF.loc['Net Income'],
                            'Revenue',
                            'Net Income'
                        ),
                        width='stretch',
                        config=app.chart
                    )
                    st.table(
                        data=incomestmtYDF.map(app.formatNumber),
                        border='horizontal'
                    )

                with quarterIS:
                    incomestmtQDF = app.dfIncomeStmt(
                        data['incomestmtQ'],
                        data['shares'],
                        data['price'],
                        'Q'
                    )
                    st.plotly_chart(
                        app.barGraph(
                            incomestmtQDF.T,
                            incomestmtQDF.loc['Total Revenue'],
                            incomestmtQDF.loc['Net Income'],
                            'Revenue',
                            'Net Income'
                        ),
                        width='stretch',
                        config=app.chart
                    )
                    st.table(
                        data=incomestmtQDF.map(app.formatNumber),
                        border='horizontal'
                    )

            with balanceSheetC:
                annualBS,quarterBS = st.tabs(['Annual','Quarter'])
                with annualBS:
                    balanceSheetYDF = app.dfBalanceSheet(
                        data['balanceSheetY'],
                        data['shares'],
                        data['price'],
                        'Y'
                    )
                    st.plotly_chart(
                        app.barGraph(
                            balanceSheetYDF.T,
                            balanceSheetYDF.loc['Total Assets'],
                            balanceSheetYDF.loc['Total Liabilities Net Minority Interest'],
                            'Assets',
                            'Liabilities'
                        ),
                        width='stretch',
                        config=app.chart
                    )
                    st.table(
                        data=balanceSheetYDF.map(app.formatNumber),
                        border='horizontal'
                    )

                with quarterBS:
                    balanceSheetQDF = app.dfBalanceSheet(
                        data['balanceSheetQ'],
                        data['shares'],
                        data['price'],
                        'Q'
                    )
                    st.plotly_chart(
                        app.barGraph(
                            balanceSheetQDF.T,
                            balanceSheetQDF.loc['Total Assets'],
                            balanceSheetQDF.loc['Total Liabilities Net Minority Interest'],
                            'Assets',
                            'Liabilities'
                        ),
                        width='stretch',
                        config=app.chart
                    )
                    st.table(
                        data=balanceSheetQDF.map(app.formatNumber),
                        border='horizontal'
                    )

    pageStatus.progress(100)
else:
    st.error('Incorrect code, please try again.')
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
    title='Stock Market [IDX]',
    typeKey='default',
    placeholder='Enter your code here',
    info='Designed for Indonesian Currency. Only works with IDX Ticker/Code. To check IDX Ticker list, please visit [IDX Stocklist](https://www.idx.co.id/en/market-data/stocks-data/stock-list). Data source from yfinance, data differences may occur. DYOR.'
)

if len(head) == 0:
    st.info('Please enter valid code to access.')
elif len(head) == 4:
    pageStatus = st.progress(0)
    
    data = app.code(head)
        
    c4,c5,c6 = st.columns([2,1,1])
    with c4:
        mrktPriceContainer = st.container(border=True)
        with mrktPriceContainer:
            mpc1, mpc2 = st.columns([1,9])
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
                                    use_container_width=True,
                                    config=app.chart
                                )
                    except Exception as e:
                        st.warning('data not available')

        with st.expander(f'Summary', expanded=False):
            summary1,summary2 = st.columns([1,9])
            with summary1:
                st.image(data['logo'])
            with summary2:
                st.metric(
                    label=f':orange[{data['name']}]',
                    value=head.upper()
                )
            infoC,aboutC = st.tabs(['More Information','About Company'])
            with infoC:
                st.write(f':orange[Ticker]: {head}')
                st.write(f':orange[Company]: {data['name']}')
                st.write(f':orange[Sector]: {data['sector']}')
                st.write(f':orange[Market Cap]: Rp {app.formatNumber(data['marketCap'])}')
                st.write(f':orange[Shares]: {data['shares']:,.0f}')
                st.info('under development')
            with aboutC:
                st.write(data['info'])

    with c5:
        incomestmtC = st.container(border=True)
        with incomestmtC:
            st.subheader('Income Statement.')
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
                    use_container_width=True,
                    config=app.chart
                )
                annualISDetails = st.expander(
                    'Annual Report',
                    expanded=False,
                )
                with annualISDetails:
                    annualISTabs = st.tabs(
                        incomestmtYDF
                        .columns
                        .astype(str)
                        .tolist()
                    )
                    for i, tab in enumerate(annualISTabs):
                        with tab:
                            annualISTabsC1,annualISTabsC2 = st.columns([2,1])
                            with annualISTabsC1:
                                st.write('Revenue (Rp)')
                                st.write('Net Income (Rp)')
                                st.write('EPS (Rp/Share)')
                                st.write('PER')
                            with annualISTabsC2:
                                st.write(
                                    app.formatNumber(
                                        incomestmtYDF
                                        .loc['Total Revenue']
                                        .iloc[i]
                                    )
                                )
                                st.write(
                                    app.formatNumber(
                                        incomestmtYDF
                                        .loc['Net Income']
                                        .iloc[i]
                                    )
                                )
                                st.write(
                                    app.formatNumber(
                                        incomestmtYDF
                                        .loc['EPS']
                                        .iloc[i]
                                    )
                                )
                                st.write(
                                    app.formatNumber(
                                        incomestmtYDF
                                        .loc['PER']
                                        .iloc[i]
                                    )
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
                    use_container_width=True,
                    config=app.chart
                )
                quarterISDetails = st.expander(
                    'Quarter Report',
                    expanded=False,
                )
                with quarterISDetails:
                    quarterISTabs = st.tabs(
                        incomestmtQDF
                        .columns
                        .astype(str)
                        .tolist()
                    )
                    for i, tab in enumerate(quarterISTabs):
                        with tab:
                            quarterISTabsC1,quarterISTabsC2 = st.columns([2,1])
                            with quarterISTabsC1:
                                st.write('Revenue (Rp)')
                                st.write('Net Income (Rp)')
                                st.write('EPS (Rp/Share)')
                                st.write('PER')
                            with quarterISTabsC2:
                                st.write(
                                    app.formatNumber(
                                        incomestmtQDF
                                        .loc['Total Revenue']
                                        .iloc[i]
                                    )
                                )
                                st.write(
                                    app.formatNumber(
                                        incomestmtQDF
                                        .loc['Net Income']
                                        .iloc[i]
                                    )
                                )
                                st.write(
                                    app.formatNumber(
                                        incomestmtQDF
                                        .loc['EPS']
                                        .iloc[i]
                                    )
                                )
                                st.write(
                                    app.formatNumber(
                                        incomestmtQDF
                                        .loc['PER']
                                        .iloc[i]
                                    )
                                )

    with c6:
        balanceSheetC = st.container(border=True)
        with balanceSheetC:
            st.subheader('Balance Sheet.')
            annualBS,quarterBS = st.tabs(['Annual','Quarter'])
            st.info('under development')
    
    pageStatus.progress(100)
else:
    st.error('Incorrect code, please try again.')
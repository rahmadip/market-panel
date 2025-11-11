import streamlit as st
import yfinance as yf
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
    
    dataTicker = app.code(head)
        
    c4,c5,c6 = st.columns([2,1,1])
    with c4:
        mrktPriceContainer = st.container(border=True)
        with mrktPriceContainer:
            st.subheader('Market Price')
            tabs= st.tabs(['1D','7D'])
            st.info('under development')
        with st.expander(f'Summary {head}', expanded=True):
            summary1,summary2,summary3 = st.columns([0.65,2,2])
            with summary1:
                st.image({dataTicker['logo']})
            with summary2:
                st.write(f':orange[Ticker]: {head}')
                st.write(f':orange[Company]: {dataTicker['name']}')
                st.write(f':orange[Sector]: {dataTicker['sector']}')
            with summary3:
                st.write(f':orange[Market Cap]: Rp {app.formatNumber(dataTicker['marketCap'])}')
                st.write(f':orange[Shares]: {dataTicker['shares']:,.0f}')
    with c5:
        incomestmtC = st.container(border=True)
        with incomestmtC:
            st.subheader('Income Statement')
            annualIS,quarterIS = st.tabs(['Annual', 'Quarter'])
            st.info('under development')
    with c6:
        balanceSheetC = st.container(border=True)
        with balanceSheetC:
            st.subheader('Balance Sheet')
            annualBS,quarterBS = st.tabs(['Annual','Quarter'])
            st.info('under development')
    
    pageStatus.progress(100)
else:
    st.error('Incorrect code, please try again.')
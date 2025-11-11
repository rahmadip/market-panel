import streamlit as st
import pandas as pd
import yfinance as yf
from urllib.parse import urlparse

# LOGIC
def formatNumber(value):
    if pd.isna(value):
        return ''
    elif abs(value) >= 1_000_000_000:
        return (
            f'{value/1_000_000_000:,.0f} B'
            if value >= 0 else
            f'({abs(value)/1_000_000_000:,.0f}) B'
        )
    elif abs(value) >= 1_000_000:
        return (
            f'{value/1_000_000:,.0f} M'
            if value >= 0 else
            f'({abs(value)/1_000_000:,.0f}) M'
        )
    else:
        return (
            f'{value:,.2f}'
            if value >= 0 else
            f'({abs(value):,.2f})'
        )

def code(code):
    ticker = yf.Ticker(f'{code}.JK')
    website = ticker.info.get('website')
    websiteParse = urlparse(website).netloc.replace('www.','')
    logo = f"https://logo.clearbit.com/{websiteParse}"
    price = ticker.info.get('currentPrice')
    shares = ticker.info.get('sharesOutstanding')
    
    incomestmtY = ticker.income_stmt
    incomestmtQ = ticker.quarterly_income_stmt
    balanceSheetY = ticker.balance_sheet
    balanceSheetQ = ticker.quarterly_balance_sheet
    return {
        'ticker': ticker,
        'name': ticker.info.get('shortName'),
        'sector' : ticker.info.get('sector'),
        'logo' : logo,
        'price' : price,
        'shares' : shares,
        'marketCap' : price*shares,
        'incomestmtY' : incomestmtY,
        'incomestmtQ' : incomestmtQ,
        'balanceSheetY' : balanceSheetY,
        'balanceSheetQ' : balanceSheetQ
    }

# COMPONENT
def headComp(
    icon:str,
    title:str,
    typeKey:str,
    placeholder:str,
    info:str = None
):
    c1,c2,c3 = st.columns(
        spec=[0.7,4,3],
        border=True
    )
    with c2:
        st.subheader(
            body=f':material/{icon}: {title}',
            divider='orange'
        )
        key = st.text_input(
            label= 'key',
            label_visibility='collapsed',
            type=typeKey,
            placeholder=placeholder,
            max_chars=4
        )
    with c3:
        st.write(':orange[_Information:_]')
        st.write(info)
    return key

pages = {
    'Market': [
        st.Page(
            page='pages/stock.py',
            title='Stock',
            icon=':material/docs:'
        ),
        st.Page(
            page='pages/crypto.py',
            title='Crypto',
            icon=':material/docs:'
        )
    ]
}

st.navigation(
    pages=pages,
    position='sidebar',
    expanded=True
).run()
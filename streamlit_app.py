import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
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
        'logo' : logo,
        'price' : price,
        'shares' : shares,
        'marketCap' : price*shares,
        'incomestmtY' : incomestmtY,
        'incomestmtQ' : incomestmtQ,
        'balanceSheetY' : balanceSheetY,
        'balanceSheetQ' : balanceSheetQ
    }

def dfIncomeStmt(
    dataframe,
    shares,
    currentPrice,
    period:str
):
    df = dataframe.loc[
        [
            'Total Revenue',
            'Net Income'
        ]
    ]
    df = df.dropna(
        how='all',
        axis=1
    )
    df.loc['EPS'] = (
        df.loc['Net Income'].fillna(0) / shares
    )
    df.loc['PER'] = (
        currentPrice / df.loc['EPS'].fillna(0)
    )
    if period == 'Y':
        df.columns = df.columns.year
    elif period == 'Q':
        df.columns = pd.to_datetime(df.columns)
        df.columns = [f"Q{(d.month - 1)//3 + 1} {d.year}" for d in df.columns]
    return df

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

def mrktPriceGraph(df):
    startPrice = df['Close'].iloc[0]
    endPrice = df['Close'].iloc[-1]
    minClose = float(df['Close'].min())
    maxClose = float(df['Close'].max())
    minDate = df['Close'].idxmin()
    maxDate = df['Close'].idxmax()
    color = 'green' if endPrice > startPrice else 'red'
    
    fig = px.area(df, x=df.index, y='Close', height=325)
    fig.update_traces(
        line=dict(color=color),
        hovertemplate='%{x|%Y/%m/%d - %H:%M}<br>Rp %{y:,.0f}<extra></extra>'
    )
    fig.update_xaxes(
        title=None,
        showticklabels=False,
        type='category'
    )
    fig.update_yaxes(
        title=None,
        side='right',
        showgrid=False,
        zeroline=False,
        showline=False,
        range=[minClose, maxClose]
        )
    fig.add_hline(
        y=startPrice,
        line_dash='dot',
        line_color='#eaeaea',
    )
    fig.add_annotation(
        x=maxDate,
        y=maxClose,
        text=f'{maxClose:,.0f}',
        yshift=20,
        font=dict(color=color, size=12),
        showarrow=False,
    )
    fig.add_annotation(
        x=minDate,
        y=minClose,
        text=f'{minClose:,.0f}',
        yshift=-20,
        font=dict(color=color, size=12),
        showarrow=False,
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=30),
        hovermode='closest',
        xaxis=dict(
            showspikes=True,
            spikemode='across',
            spikecolor='#eaeaea',
            spikethickness=0.7
        ),
        hoverlabel=dict(
            bgcolor='rgba(0,0,0,0.7)',
            font_color='white',
            font_size=11
        )
    )
    return fig

def barGraph(df,v1,v2,n1,n2):
    years = [str(d) for d in df.index]
    quarter = any("Q" in str(x) for x in years)
    
    if quarter:
        df = df.copy()
        df["__order__"] = df.index.to_series().apply(
            lambda x: int(x.split(" ")[1]) * 10 + int(x.split("Q")[1].split(" ")[0])
        )
        df = df.sort_values("__order__")
        df = df.drop(columns="__order__")
        v1 = v1.reindex(df.index)
        v2 = v2.reindex(df.index)
        indexX = list(df.index)
    else:
        df = df.sort_index(ascending=True)
        v1 = v1.reindex(df.index)
        v2 = v2.reindex(df.index)
        indexX = [str(d) for d in df.index]
        
    fig = px.bar(
        x=indexX,
        y=[v1, v2],
        barmode='group',
        color_discrete_sequence=['#730000', '#ffa200'],
        height=300
    )
    
    for trace in fig.data:
        trace.hovertemplate = 'Rp %{y:,.0f}<extra></extra>'
    
    fig.update_xaxes(title=None)
    fig.update_yaxes(
        title=None,
        side='right',
        exponentformat='SI',
        showexponent='all',
        tickformat='~s'
    )
    fig.data[0].name = n1
    fig.data[1].name = n2
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=30),
        legend_title=None,
        legend=dict(orientation='h', y=-0.15, x=0),
    )
    return fig

# CONFIG
mrktPriceSetup = {
    '1D': {'period':'1d','interval':'1m'},
    '7D': {'period':'7d','interval':'1h'},
    '1M': {'period':'1mo','interval':'1d'},
    '3M': {'period':'3mo','interval': '1d'},
    '6M': {'period':'6mo','interval': '1d'},
    'YTD': {'period':'ytd','interval': '1d'},
    '1Y': {'period':'1y','interval':'1d'},
    '3Y': {'period':'3y','interval': '1d'},
    '5Y': {'period':'5y','interval':'1d'},
    'All': {'period':'max','interval':'1d'}
}

chart = {
    'displayModeBar': False,
    'scrollZoom': False,
    'doubleClick':'reset',
    'dragmode': False
    }

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
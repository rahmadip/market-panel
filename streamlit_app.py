import streamlit as st

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
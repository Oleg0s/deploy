import streamlit as st

from frontend.components.backtesting import backtesting_section
from frontend.components.config_loader import get_default_config_loader
from frontend.components.save_config import render_save_config

# Import submodules
from frontend.pages.config.spread_maker.user_inputs import user_inputs
from frontend.st_utils import get_backend_api_client, initialize_st_page
from frontend.visualization.backtesting_metrics import render_accuracy_metrics, render_backtesting_metrics, render_close_types
from frontend.visualization.executors_distribution import create_executors_distribution_traces

# Initialize the Streamlit page
initialize_st_page(title="Spread Market Maker", icon="👼")
backend_api_client = get_backend_api_client()

# Page content
st.text("This tool will let you create a config for Spread Market Maker.")
get_default_config_loader("spread_maker")

inputs = user_inputs()

st.session_state["default_config"].update(inputs)
with st.expander("Executor Distribution:", expanded=True):
    fig = create_executors_distribution_traces(inputs["buy_spreads"], inputs["sell_spreads"], inputs["buy_amounts_pct"],
                                               inputs["sell_amounts_pct"], inputs["total_amount_quote"])
    st.plotly_chart(fig, use_container_width=True)

st.write("---")
render_save_config(st.session_state["default_config"]["id"], st.session_state["default_config"])

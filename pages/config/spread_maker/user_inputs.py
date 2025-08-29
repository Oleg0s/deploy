import streamlit as st

from frontend.components.executors_distribution import get_executors_distribution_inputs
from frontend.components.config_loader import get_controller_config


def get_spread_market_making_inputs(custom_candles=False, controller_name: str = None):
    with st.expander("General Settings", expanded=True):
        c1, c2, c3, c4, c5, c6 = st.columns(7)
        if controller_name:
            default_config = get_controller_config(controller_name)
        else:
            # Fallback for backward compatibility
            default_config = st.session_state.get("default_config", {})
        connector_name = default_config.get("connector_name", "kraken")
        trading_pair = default_config.get("trading_pair", "ETH-USD")
        leverage = default_config.get("leverage", 1)
        total_amount_quote = default_config.get("total_amount_quote", 100)
        profit_waiting_time = default_config.get("profit_waiting_time", 60 * 60) / 60
        executor_refresh_time = default_config.get("executor_refresh_time", 5 * 60) / 60
        candles_connector = None
        candles_trading_pair = None
        interval = None
        with c1:
            connector_name = st.text_input("Connector", value=connector_name,
                                           help="Enter the name of the exchange to trade on (e.g., binance_perpetual).")
        with c2:
            trading_pair = st.text_input("Trading Pair", value=trading_pair,
                                         help="Enter the trading pair to trade on (e.g., WLD-USDT).")
        with c3:
            leverage = st.number_input("Leverage", value=leverage,
                                       min_value=1,
                                       help="Set the leverage to use for trading (e.g., 20 for 20x leverage). "
                                            "Set it to 1 for spot trading. Value must be greater than 0.")
        with c4:
            total_amount_quote = st.number_input("Total amount of quote", value=total_amount_quote,
                                                 help="Enter the total amount in quote asset to use for "
                                                      "trading (e.g., 1000).")
        with c5:
            profit_waiting_time = st.number_input("Profit waiting Time (minutes)", value=profit_waiting_time,
                                            help="Specify profit waiting time in minutes (e.g., 60).") * 60
        with c6:
            executor_refresh_time = st.number_input("Executor Refresh Time (minutes)", value=executor_refresh_time,
                                                    help="Enter the refresh time in minutes for executors (e.g., 60).") * 60
        if custom_candles:
            candles_connector = default_config.get("candles_connector", "kucoin")
            candles_trading_pair = default_config.get("candles_trading_pair", "WLD-USDT")
            interval = default_config.get("interval", "3m")
            intervals = ["1m", "3m", "5m", "15m", "1h", "4h", "1d"]
            interval_index = intervals.index(interval)
            with c1:
                candles_connector = st.text_input("Candles Connector", value=candles_connector,
                                                  help="Enter the name of the exchange to get candles from"
                                                       "(e.g., binance_perpetual).")
            with c2:
                candles_trading_pair = st.text_input("Candles Trading Pair", value=candles_trading_pair,
                                                     help="Enter the trading pair to get candles for (e.g., WLD-USDT).")
            with c3:
                interval = st.selectbox("Candles Interval", intervals, index=interval_index,
                                        help="Enter the interval for candles (e.g., 1m).")
    return connector_name, trading_pair, leverage, total_amount_quote, profit_waiting_time, \
        executor_refresh_time, candles_connector, candles_trading_pair, interval

def user_inputs():
    connector_name, trading_pair, leverage, total_amount_quote, profit_waiting_time, \
        executor_refresh_time, _, _, _ = get_spread_market_making_inputs()
    buy_spread_distributions, sell_spread_distributions, buy_order_amounts_pct, \
        sell_order_amounts_pct = get_executors_distribution_inputs()

    # Create the config
    config = {
        "controller_name": "spread_maker",
        "controller_type": "market_making",
        "manual_kill_switch": False,
        "candles_config": [],
        "connector_name": connector_name,
        "trading_pair": trading_pair,
        "total_amount_quote": total_amount_quote,
        "buy_spreads": buy_spread_distributions,
        "sell_spreads": sell_spread_distributions,
        "buy_amounts_pct": buy_order_amounts_pct,
        "sell_amounts_pct": sell_order_amounts_pct,
        "executor_refresh_time": executor_refresh_time,
        "profit_waiting_time": profit_waiting_time,
        "leverage": leverage,
    }
    return config

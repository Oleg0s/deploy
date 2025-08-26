from datetime import datetime, timedelta
from decimal import Decimal
from typing import List

from pydantic import Field

from hummingbot.core.data_type.common import PriceType, TradeType
from hummingbot.data_feed.candles_feed.data_types import CandlesConfig
from hummingbot.strategy_v2.controllers.market_making_controller_base import (
    MarketMakingControllerBase,
    MarketMakingControllerConfigBase,
)
from hummingbot.strategy_v2.executors.position_executor.data_types import PositionExecutorConfig


class PMMCatConfig(MarketMakingControllerConfigBase):
    controller_name: str = "pmm_cat"
    # As this controller is a simple version of the PMM, we are not using the candles feed
    candles_config: List[CandlesConfig] = Field(default=[])


class MarketPricePositionExecutorConfig(PositionExecutorConfig):
    """
    Custom PositionExecutorConfig that calculates take profit based on current market price
    """

    def __init__(
            self,
            timestamp: float,
            level_id: str,
            connector_name: str,
            trading_pair: str,
            entry_price: Decimal,
            amount: Decimal,
            triple_barrier_config,
            leverage: int,
            side: TradeType,
    ):
        super().__init__(
            timestamp=timestamp,
            level_id=level_id,
            connector_name=connector_name,
            trading_pair=trading_pair,
            entry_price=entry_price,
            amount=amount,
            triple_barrier_config=triple_barrier_config,
            leverage=leverage,
            side=side,
        )
        self.price_profit_from: Decimal = None
        self.time_profit_from = datetime.now()
        self.time_delta = 5


    def get_take_profit_price(self, current_market_price: Decimal) -> Decimal:
        """
        Calculate take profit price based on current market price instead of entry price
        """
        if not self.triple_barrier_config or not self.triple_barrier_config.take_profit:
            return None

        if self.price_profit_from is None or self.time_profit_from + timedelta(minutes=self.time_delta) < datetime.now():
            self.time_profit_from = datetime.now()
            self.price_profit_from = current_market_price

        if self.side == TradeType.BUY:
            return self.price_profit_from * (1 + self.triple_barrier_config.take_profit)
        else:
            return self.price_profit_from * (1 - self.triple_barrier_config.take_profit)


class PMMCatController(MarketMakingControllerBase):
    def __init__(self, config: PMMCatConfig, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.config = config

    def get_executor_config(self, level_id: str, price: Decimal, amount: Decimal):
        trade_type = self.get_trade_type_from_level_id(level_id)
        return MarketPricePositionExecutorConfig(
            timestamp=self.market_data_provider.time(),
            level_id=level_id,
            connector_name=self.config.connector_name,
            trading_pair=self.config.trading_pair,
            entry_price=price,
            amount=amount,
            triple_barrier_config=self.config.triple_barrier_config,
            leverage=self.config.leverage,
            side=trade_type,
        )

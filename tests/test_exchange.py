import pytest

from jesse.exceptions import NegativeBalance, InsufficientMargin
from .utils import single_route_backtest


def test_negative_balance_validation_for_spot_market():
    """
    The initial account balance for USDT is 10_000. So trying to spend 10_001
    should throw NegativeBalance exception
    """
    with pytest.raises(NegativeBalance):
        single_route_backtest('TestSpotNegativeBalance', is_futures_trading=False)


def test_negative_balance_validation_for_futures_market():
    """
    The initial account balance for USDT is 10_000. So trying to spend 10_001
    should throw InsufficientMargin exception
    """
    # (MARKET order)
    with pytest.raises(InsufficientMargin):
        single_route_backtest('TestInsufficientMargin1', is_futures_trading=True, leverage=1)
    # but with more leverage, it should work
    single_route_backtest('TestInsufficientMargin1', is_futures_trading=True, leverage=2)

    # (LIMIT order)
    with pytest.raises(InsufficientMargin):
        single_route_backtest('TestInsufficientMargin2', is_futures_trading=True, leverage=1)
    # but with more leverage, it should work
    single_route_backtest('TestInsufficientMargin2', is_futures_trading=True, leverage=2)

    # short-version (STOP order)
    with pytest.raises(InsufficientMargin):
        single_route_backtest('TestInsufficientMargin3', is_futures_trading=True, leverage=1)
    # but with more leverage, it should work
    single_route_backtest('TestInsufficientMargin3', is_futures_trading=True, leverage=2)


def test_wallet_balance_and_available_margin_for_futures_market():
    """
    Works the same way as Binance Futures'es wallet balance does.
    It is only changed at commission charges and after realized PNL is added.
    """
    single_route_backtest('TestWalletBalance', is_futures_trading=True, leverage=2)


# TODO: test_wallet_balance_and_available_margin_for_spot_market

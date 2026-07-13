"""Unit tests for Black-Scholes model."""

import math
import pytest
from black_scholes import BlackScholes


class TestBlackScholesInitialization:
    """Test Black-Scholes initialization."""
    
    def test_valid_initialization(self):
        """Test valid parameter initialization."""
        bs = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        assert bs.spot_price == 100
        assert bs.strike_price == 100
        assert bs.time_to_expiry == 1
        assert bs.risk_free_rate == 0.05
        assert bs.volatility == 0.2
    
    def test_invalid_spot_price(self):
        """Test invalid spot price."""
        with pytest.raises(ValueError, match="Spot price must be positive"):
            BlackScholes(
                spot_price=-100,
                strike_price=100,
                time_to_expiry=1,
                risk_free_rate=0.05,
                volatility=0.2
            )
    
    def test_invalid_strike_price(self):
        """Test invalid strike price."""
        with pytest.raises(ValueError, match="Strike price must be positive"):
            BlackScholes(
                spot_price=100,
                strike_price=0,
                time_to_expiry=1,
                risk_free_rate=0.05,
                volatility=0.2
            )
    
    def test_invalid_time_to_expiry(self):
        """Test invalid time to expiry."""
        with pytest.raises(ValueError, match="Time to expiry must be positive"):
            BlackScholes(
                spot_price=100,
                strike_price=100,
                time_to_expiry=-1,
                risk_free_rate=0.05,
                volatility=0.2
            )
    
    def test_invalid_volatility(self):
        """Test invalid volatility."""
        with pytest.raises(ValueError, match="Volatility must be positive"):
            BlackScholes(
                spot_price=100,
                strike_price=100,
                time_to_expiry=1,
                risk_free_rate=0.05,
                volatility=0
            )


class TestBlackScholesOptionPricing:
    """Test option pricing calculations."""
    
    def test_call_price_at_the_money(self):
        """Test call price for at-the-money option."""
        bs = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        call_price = bs.call_price()
        assert isinstance(call_price, float)
        assert call_price > 0
    
    def test_put_price_at_the_money(self):
        """Test put price for at-the-money option."""
        bs = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        put_price = bs.put_price()
        assert isinstance(put_price, float)
        assert put_price > 0
    
    def test_put_call_parity(self):
        """Test put-call parity: C - P = S - Ke^(-rT)."""
        bs = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        call_price = bs.call_price()
        put_price = bs.put_price()
        
        left_side = call_price - put_price
        right_side = bs.spot_price - bs.strike_price * math.exp(-bs.risk_free_rate * bs.time_to_expiry)
        
        assert abs(left_side - right_side) < 1e-10
    
    def test_call_price_in_the_money(self):
        """Test call price is higher for in-the-money options."""
        bs_itm = BlackScholes(
            spot_price=110,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        bs_atm = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        assert bs_itm.call_price() > bs_atm.call_price()
    
    def test_call_price_out_of_money(self):
        """Test call price is lower for out-of-the-money options."""
        bs_otm = BlackScholes(
            spot_price=90,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        bs_atm = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        assert bs_otm.call_price() < bs_atm.call_price()


class TestBlackScholesGreeks:
    """Test Greeks calculations."""
    
    def test_greeks_return_dict(self):
        """Test that greeks() returns a dictionary."""
        bs = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        greeks = bs.greeks()
        assert isinstance(greeks, dict)
    
    def test_greeks_keys(self):
        """Test that greeks() contains all required keys."""
        bs = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        greeks = bs.greeks()
        required_keys = ['call_delta', 'put_delta', 'gamma', 'vega', 
                        'call_theta', 'put_theta', 'call_rho', 'put_rho']
        for key in required_keys:
            assert key in greeks
    
    def test_call_delta_bounds(self):
        """Test that call delta is between 0 and 1."""
        bs = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        greeks = bs.greeks()
        assert 0 <= greeks['call_delta'] <= 1
    
    def test_put_delta_bounds(self):
        """Test that put delta is between -1 and 0."""
        bs = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        greeks = bs.greeks()
        assert -1 <= greeks['put_delta'] <= 0
    
    def test_gamma_positive(self):
        """Test that gamma is always positive."""
        bs = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        greeks = bs.greeks()
        assert greeks['gamma'] > 0
    
    def test_vega_positive(self):
        """Test that vega is positive."""
        bs = BlackScholes(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2
        )
        greeks = bs.greeks()
        assert greeks['vega'] > 0

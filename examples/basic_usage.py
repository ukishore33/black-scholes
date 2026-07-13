"""Basic usage example of Black-Scholes model."""

from black_scholes import BlackScholes


def main():
    """Run basic example."""
    print("Black-Scholes Option Pricing Model")
    print("=" * 40)
    
    # Create Black-Scholes instance
    options = BlackScholes(
        spot_price=100,           # Current stock price
        strike_price=100,         # Strike price
        time_to_expiry=1,         # 1 year to expiration
        risk_free_rate=0.05,      # 5% risk-free rate
        volatility=0.2            # 20% volatility
    )
    
    # Calculate option prices
    call_price = options.call_price()
    put_price = options.put_price()
    
    print(f"\nOption Prices:")
    print(f"  Call Price: ${call_price:.4f}")
    print(f"  Put Price:  ${put_price:.4f}")
    
    # Calculate Greeks
    greeks = options.greeks()
    
    print(f"\nGreeks (Call):")
    print(f"  Delta: {greeks['call_delta']:.6f}")
    print(f"  Gamma: {greeks['gamma']:.6f}")
    print(f"  Vega:  {greeks['vega']:.6f}")
    print(f"  Theta: {greeks['call_theta']:.6f}")
    print(f"  Rho:   {greeks['call_rho']:.6f}")
    
    print(f"\nGreeks (Put):")
    print(f"  Delta: {greeks['put_delta']:.6f}")
    print(f"  Gamma: {greeks['gamma']:.6f}")
    print(f"  Vega:  {greeks['vega']:.6f}")
    print(f"  Theta: {greeks['put_theta']:.6f}")
    print(f"  Rho:   {greeks['put_rho']:.6f}")
    
    # Verify Put-Call Parity
    import math
    theoretical_put = call_price - options.spot_price + options.strike_price * math.exp(-options.risk_free_rate * options.time_to_expiry)
    print(f"\nPut-Call Parity Check:")
    print(f"  Calculated Put Price: ${put_price:.4f}")
    print(f"  Theoretical Put (C - S + Ke^-rT): ${theoretical_put:.4f}")
    print(f"  Difference: ${abs(put_price - theoretical_put):.10f}")


if __name__ == "__main__":
    main()

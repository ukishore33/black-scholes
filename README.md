# Black-Scholes Option Pricing Model

A Python implementation of the Black-Scholes option pricing model for calculating European option prices and Greeks.

## Overview

The Black-Scholes model is a mathematical model for pricing European-style options. This project provides:

- **Option Pricing**: Calculate call and put option prices
- **Greeks Calculation**: Compute Delta, Gamma, Vega, Theta, and Rho
- **Visualization**: Graphical representation of option prices and Greeks
- **Analysis Tools**: Sensitivity analysis and scenario modeling

## Features

- Pure Python implementation with NumPy and SciPy
- Support for call and put options
- Calculation of all five Greeks
- Input validation and error handling
- Comprehensive documentation
- Unit tests

## Installation

```bash
git clone https://github.com/ukishore33/black-scholes.git
cd black-scholes
pip install -r requirements.txt
```

## Quick Start

```python
from black_scholes import BlackScholes

# Initialize with option parameters
options = BlackScholes(
    spot_price=100,           # Current stock price
    strike_price=100,         # Strike price
    time_to_expiry=1,         # Time to expiration in years
    risk_free_rate=0.05,      # Risk-free rate
    volatility=0.2            # Volatility (sigma)
)

# Calculate option prices
call_price = options.call_price()
put_price = options.put_price()

print(f"Call Price: ${call_price:.2f}")
print(f"Put Price: ${put_price:.2f}")

# Calculate Greeks
greeks = options.greeks()
print(f"Delta: {greeks['delta']:.4f}")
print(f"Gamma: {greeks['gamma']:.4f}")
print(f"Vega: {greeks['vega']:.4f}")
print(f"Theta: {greeks['theta']:.4f}")
print(f"Rho: {greeks['rho']:.4f}")
```

## Black-Scholes Formula

### Call Option Price
```
C = S₀*N(d₁) - K*e^(-rT)*N(d₂)
```

### Put Option Price
```
P = K*e^(-rT)*N(-d₂) - S₀*N(-d₁)
```

Where:
- `d₁ = [ln(S₀/K) + (r + σ²/2)*T] / (σ*√T)`
- `d₂ = d₁ - σ*√T`
- `S₀` = Current stock price
- `K` = Strike price
- `r` = Risk-free rate
- `T` = Time to expiration
- `σ` = Volatility
- `N()` = Cumulative standard normal distribution

## Project Structure

```
black-scholes/
├── README.md
├── requirements.txt
├── black_scholes/
│   ├── __init__.py
│   ├── model.py           # Core Black-Scholes implementation
│   └── greeks.py          # Greeks calculations
├── tests/
│   ├── __init__.py
│   └── test_model.py      # Unit tests
└── examples/
    └── basic_usage.py     # Example usage
```

## Parameters

- **spot_price**: Current price of the underlying asset
- **strike_price**: Strike (exercise) price of the option
- **time_to_expiry**: Time until option expiration (in years)
- **risk_free_rate**: Risk-free interest rate (e.g., 0.05 for 5%)
- **volatility**: Annualized volatility/standard deviation of returns

## Requirements

- Python 3.7+
- NumPy
- SciPy
- Pandas (optional, for data analysis)
- Matplotlib (optional, for visualization)

## References

- Black, F., & Scholes, M. (1973). The pricing of options and corporate liabilities.
- Hull, J. C. (2012). Options, Futures, and Other Derivatives.

## License

MIT

## Author

ukishore33

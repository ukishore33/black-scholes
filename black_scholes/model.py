"""Black-Scholes option pricing model."""

import math
from scipy.stats import norm


class BlackScholes:
    """Black-Scholes option pricing model.
    
    A mathematical model for pricing European-style options.
    
    Attributes:
        spot_price (float): Current price of the underlying asset
        strike_price (float): Strike (exercise) price
        time_to_expiry (float): Time to expiration in years
        risk_free_rate (float): Risk-free interest rate
        volatility (float): Annualized volatility (sigma)
    """
    
    def __init__(self, spot_price, strike_price, time_to_expiry, 
                 risk_free_rate, volatility):
        """Initialize Black-Scholes model.
        
        Args:
            spot_price (float): Current stock price
            strike_price (float): Strike price
            time_to_expiry (float): Time to expiration in years
            risk_free_rate (float): Risk-free rate (e.g., 0.05 for 5%)
            volatility (float): Volatility (sigma)
            
        Raises:
            ValueError: If any parameter is invalid
        """
        self._validate_parameters(spot_price, strike_price, time_to_expiry,
                                 risk_free_rate, volatility)
        
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.time_to_expiry = time_to_expiry
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
    
    @staticmethod
    def _validate_parameters(spot_price, strike_price, time_to_expiry,
                            risk_free_rate, volatility):
        """Validate input parameters.
        
        Args:
            spot_price (float): Current stock price
            strike_price (float): Strike price
            time_to_expiry (float): Time to expiration
            risk_free_rate (float): Risk-free rate
            volatility (float): Volatility
            
        Raises:
            ValueError: If any parameter is invalid
        """
        if spot_price <= 0:
            raise ValueError("Spot price must be positive")
        if strike_price <= 0:
            raise ValueError("Strike price must be positive")
        if time_to_expiry <= 0:
            raise ValueError("Time to expiry must be positive")
        if volatility <= 0:
            raise ValueError("Volatility must be positive")
    
    def _calculate_d1_d2(self):
        """Calculate d1 and d2 parameters.
        
        Returns:
            tuple: (d1, d2)
        """
        numerator = math.log(self.spot_price / self.strike_price) + \
                    (self.risk_free_rate + 0.5 * self.volatility ** 2) * self.time_to_expiry
        denominator = self.volatility * math.sqrt(self.time_to_expiry)
        
        d1 = numerator / denominator
        d2 = d1 - denominator
        
        return d1, d2
    
    def call_price(self):
        """Calculate European call option price.
        
        Returns:
            float: Call option price
        """
        d1, d2 = self._calculate_d1_d2()
        
        call = (self.spot_price * norm.cdf(d1) - 
                self.strike_price * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(d2))
        
        return call
    
    def put_price(self):
        """Calculate European put option price.
        
        Returns:
            float: Put option price
        """
        d1, d2 = self._calculate_d1_d2()
        
        put = (self.strike_price * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(-d2) - 
               self.spot_price * norm.cdf(-d1))
        
        return put
    
    def greeks(self):
        """Calculate option Greeks.
        
        Returns:
            dict: Dictionary containing Delta, Gamma, Vega, Theta, and Rho
        """
        d1, d2 = self._calculate_d1_d2()
        
        # Delta
        call_delta = norm.cdf(d1)
        put_delta = norm.cdf(d1) - 1
        
        # Gamma
        gamma = norm.pdf(d1) / (self.spot_price * self.volatility * math.sqrt(self.time_to_expiry))
        
        # Vega
        vega = self.spot_price * norm.pdf(d1) * math.sqrt(self.time_to_expiry) / 100  # Per 1% change
        
        # Theta
        call_theta = (-self.spot_price * norm.pdf(d1) * self.volatility / (2 * math.sqrt(self.time_to_expiry)) -
                      self.risk_free_rate * self.strike_price * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(d2)) / 365
        put_theta = (-self.spot_price * norm.pdf(d1) * self.volatility / (2 * math.sqrt(self.time_to_expiry)) +
                     self.risk_free_rate * self.strike_price * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(-d2)) / 365
        
        # Rho
        call_rho = self.strike_price * self.time_to_expiry * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(d2) / 100  # Per 1% change
        put_rho = -self.strike_price * self.time_to_expiry * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(-d2) / 100
        
        return {
            'call_delta': call_delta,
            'put_delta': put_delta,
            'gamma': gamma,
            'vega': vega,
            'call_theta': call_theta,
            'put_theta': put_theta,
            'call_rho': call_rho,
            'put_rho': put_rho
        }

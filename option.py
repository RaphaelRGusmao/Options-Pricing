################################################################################
#                               Options Pricing                                #
#                              Raphael R. Gusmão                               #
#                                                                              #
#                                    Option                                    #
################################################################################

import math
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

################################################################################
# Option                                                                       #
################################################################################
class Option:
    def __init__(self, type, strike, dividend, volatility,
                 stock_price, interest_rate, time_to_maturity):
        self.type = type
        self.strike = strike
        self.dividend = dividend
        self.volatility = volatility
        self.stock_price = stock_price
        self.interest_rate = interest_rate
        self.time_to_maturity = time_to_maturity

    ############################################################################
    def __repr__(self):
        return ("Option: {"
            + "\n  type: " + str(self.type)
            + "\n  strike: " + str(self.strike)
            + "\n  dividend: " + str(self.dividend)
            + "\n  volatility: " + str(self.volatility)
            + "\n  stock_price: " + str(self.stock_price)
            + "\n  interest_rate: " + str(self.interest_rate)
            + "\n  time_to_maturity: " + str(self.time_to_maturity)
            + "\n  d1: " + str(self.d1)
            + "\n  d2: " + str(self.d2)
            + "\n  delta: " + str(self.delta)
            + "\n  gamma: " + str(self.gamma)
            + "\n  vega: " + str(self.vega)
            + "\n  theta: " + str(self.theta)
            + "\n  price: " + str(self.price) + "\n}"
        )

    ############################################################################
    def reset(self):
        self._d1 = None
        self._d2 = None
        self._price = None
        self._delta = None
        self._gamma = None
        self._vega = None
        self._theta = None
        self._parity = None

    ############################################################################
    # Plot                                                                     #
    ############################################################################
    @staticmethod
    def plot(options, x_axis, y_axis, x_start, x_end, x_samples, save_to):
        is_inverted = False
        if (x_end < x_start):
            x_start, x_end = x_end, x_start
            is_inverted = True

        x_values = np.linspace(x_start, x_end, x_samples)
        y_values = {}

        for (i, option) in enumerate(options):
            option = copy.copy(option)
            key = str(i+1) + ". " + option.type
            y_values[key] = []
            for x in x_values:
                setattr(option, x_axis, x)
                y = getattr(option, y_axis)
                y_values[key].append(y)

        df = pd.DataFrame(data=y_values, index=x_values)

        fig = df.plot(style=[
            ("-" if (option.type == "CALL") else "--") for option in options
        ])
        if (is_inverted): fig.invert_xaxis()
        plt.title("Options: " + x_axis + " x " + y_axis)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.grid()
        plt.legend(loc=(1.05, 0.5))
        plt.tight_layout()
        plt.savefig(save_to)

    ############################################################################
    # Inputs                                                                   #
    ############################################################################
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if (value != "CALL" and value != "PUT"):
            raise ValueError("Invalid option type!")
        self._type = value
        self.reset()

    ############################################################################
    @property
    def strike(self):
        return self._strike

    @strike.setter
    def strike(self, value):
        if (value <= 0):
            raise ValueError("Invalid strike!")
        self._strike = value
        self.reset()

    ############################################################################
    @property
    def dividend(self):
        return self._dividend

    @dividend.setter
    def dividend(self, value):
        if (value < 0):
            raise ValueError("Invalid dividend!")
        self._dividend = value
        self.reset()

    ############################################################################
    @property
    def volatility(self):
        return self._volatility

    @volatility.setter
    def volatility(self, value):
        if (value <= 0):
            raise ValueError("Invalid volatility!")
        self._volatility = value
        self.reset()

    ############################################################################
    @property
    def stock_price(self):
        return self._stock_price

    @stock_price.setter
    def stock_price(self, value):
        if (value < 0):
            raise ValueError("Invalid stock price!")
        self._stock_price = value
        self.reset()

    ############################################################################
    @property
    def interest_rate(self):
        return self._interest_rate

    @interest_rate.setter
    def interest_rate(self, value):
        if (value < 0):
            raise ValueError("Invalid interest rate!")
        self._interest_rate = value
        self.reset()

    ############################################################################
    @property
    def time_to_maturity(self):
        return self._time_to_maturity

    @time_to_maturity.setter
    def time_to_maturity(self, value):
        if (value < 0):
            raise ValueError("Invalid time to maturity!")
        self._time_to_maturity = value
        self.reset()

    ############################################################################
    # Outputs                                                                  #
    ############################################################################
    @property
    def d1(self):
        if (self._d1 is None): self.calculate_d1()
        return self._d1

    def calculate_d1(self):
        S = self.stock_price
        K = self.strike
        T = self.time_to_maturity
        r = self.interest_rate
        q = self.dividend
        sigma = self.volatility
        if (S == 0 or T == 0):
            self._d1 = float("NaN")
        else:
            self._d1 = (math.log(S/K) + (r - q + (sigma**2)/2)*T) \
                     / (sigma*math.sqrt(T))

    ############################################################################
    @property
    def d2(self):
        if (self._d2 is None): self.calculate_d2()
        return self._d2

    def calculate_d2(self):
        T = self.time_to_maturity
        sigma = self.volatility
        self._d2 = self.d1 - sigma*math.sqrt(T)

    ############################################################################
    @property
    def delta(self):
        if (self._delta is None): self.calculate_delta()
        return self._delta

    def calculate_delta(self):
        S = self.stock_price
        T = self.time_to_maturity
        q = self.dividend
        if (S == 0 or T == 0):
            self._delta = float("NaN")
        else:
            if (self.type == "CALL"):
                self._delta = math.exp(-q*T)*norm.cdf(self.d1)
            else: # PUT
                self._delta = -math.exp(-q*T)*norm.cdf(-self.d1)

    ############################################################################
    @property
    def gamma(self):
        if (self._gamma is None): self.calculate_gamma()
        return self._gamma

    def calculate_gamma(self):
        S = self.stock_price
        T = self.time_to_maturity
        q = self.dividend
        sigma = self.volatility
        if (S == 0 or T == 0):
            self._gamma = float("NaN")
        else:
            self._gamma = math.exp(-q*T)*norm.pdf(self.d1) \
                        / (sigma*S*math.sqrt(T))

    ############################################################################
    @property
    def vega(self):
        if (self._vega is None): self.calculate_vega()
        return self._vega

    def calculate_vega(self):
        S = self.stock_price
        T = self.time_to_maturity
        q = self.dividend
        self._vega = math.exp(-q*T)*S*math.sqrt(T)*norm.pdf(self.d1)

    ############################################################################
    @property
    def theta(self):
        if (self._theta is None): self.calculate_theta()
        return self._theta

    def calculate_theta(self):
        S = self.stock_price
        K = self.strike
        T = self.time_to_maturity
        r = self.interest_rate
        q = self.dividend
        sigma = self.volatility
        if (S == 0 or T == 0):
            self._theta = float("NaN")
        else:
            if (self.type == "CALL"):
                self._theta = -math.exp(-q*T)*S*norm.pdf(self.d1)*sigma \
                            / (2*math.sqrt(T)) \
                            + q*math.exp(-q*T)*S*norm.cdf(self.d1) \
                            - r*K*math.exp(-r*T)*norm.cdf(self.d2)
            else: # PUT
                self._theta = -math.exp(-q*T)*S*norm.pdf(self.d1)*sigma \
                            / (2*math.sqrt(T)) \
                            - q*math.exp(-q*T)*S*norm.cdf(-self.d1) \
                            + r*K*math.exp(-r*T)*norm.cdf(-self.d2)

    ############################################################################
    @property
    def price(self):
        if (self._price is None): self.calculate_price()
        return self._price

    def calculate_price(self):
        S = self.stock_price
        K = self.strike
        T = self.time_to_maturity
        r = self.interest_rate
        q = self.dividend
        if (self.type == "CALL"):
            if (S == 0):
                self._price = 0
            else:
                if (T == 0):
                    self._price = max(S - K, 0)
                else:
                    self._price = math.exp(-q*T)*S*norm.cdf(self.d1) \
                                - math.exp(-r*T)*K*norm.cdf(self.d2)
        else: # PUT
            if (S == 0):
                self._price = K*math.exp(-r*T)
            else:
                if (T == 0):
                    self._price = max(K - S, 0)
                else:
                    self._price = math.exp(-r*T)*K*norm.cdf(-self.d2) \
                                - math.exp(-q*T)*S*norm.cdf(-self.d1)

    ############################################################################
    @property
    def parity(self):
        if (self._parity is None): self.calculate_parity()
        return self._parity

    def calculate_parity(self):
        parity = copy.copy(self)
        parity._type = "PUT" if (self.type == "CALL") else "CALL"
        parity._price = None
        parity._delta = None
        parity._theta = None
        parity._parity = self
        self._parity = parity

################################################################################

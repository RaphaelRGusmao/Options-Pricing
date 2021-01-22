################################################################################
#                               Options Pricing                                #
#                              Raphael R. Gusmão                               #
#                                                                              #
#                                     Main                                     #
################################################################################

from option import Option

################################################################################
# Main                                                                         #
################################################################################
def main():
    option1 = Option(
        type = "CALL",
        strike = 10.00,
        dividend = 0.05,
        volatility = 0.5,
        stock_price = 10.00,
        interest_rate = 0.02,
        time_to_maturity = 0.5
    )
    option2 = Option(
        type = "CALL",
        strike = 10.00,
        dividend = 0.05,
        volatility = 0.5,
        stock_price = 10.00,
        interest_rate = 0.02,
        time_to_maturity = 0.25
    )
    option3 = Option(
        type = "CALL",
        strike = 10.00,
        dividend = 0.05,
        volatility = 0.5,
        stock_price = 10.00,
        interest_rate = 0.02,
        time_to_maturity = 0.05
    )
    Option.plot(
        options = [
            option1, option1.parity,
            option2, option2.parity,
            option3, option3.parity
        ],
        x_axis = "stock_price", y_axis = "price",
        x_start = 0, x_end = 20, x_samples = 500,
        save_to = "images/test.png",
    )

if __name__ == "__main__":
    main()

################################################################################

from statistics import mean

def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
        (((mean(xs)*mean(xs)) - mean(xs*xs)) + 0.000001))
    
    b = mean(ys) - m*mean(xs)
    
    return m, b

def calculate_regression(xs, ys):
    m, b = best_fit_slope_and_intercept(xs,ys)
    regression_line_dem = [(m*x)+b for x in xs]
    return regression_line_dem

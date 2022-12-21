from math import sqrt

def symmetrize_errors(delta_plus, delta_minus):
    semi_diff = (delta_plus + delta_minus)/2
    average = (delta_plus - delta_minus)/2
    se_delta = semi_diff
    se_sigma = sqrt(average*average + 2*semi_diff*semi_diff)
    return se_delta, se_sigma

def percentage_to_absolute(percentage, value):
    percentage = float(percentage.replace("%", ""))
    absolute = percentage * value * 0.01
    return absolute

from math import floor, sin

# Proficiency: Linear Function
# Creates linear function in the form of output = m * input + b
def p_linear(input,m,b):
    return floor(m*input + b)
	
# Proficiency: Sinusoidal Linear Function
# Creates sinusoidal linear function in the form of amplitude * sin(2pi*input/period) + m * input + b
def p_sinusoidal_linear(input,m,b,amplitude,period):
    return floor(amplitude*sin(2*3.14159*input/period) + m*input + b)

# Proficiency： Inverse function bounded by asymptote
# y_intersect: When input is 0, we can control the output to be the y-intersect. This is the initial value
# upperbound: upperbound on the output value
# x_half: The x-value for y to reach upperbound/2.  This roughly helps us control the speed of growth.
def p_increasing_bounded(input,y_intersect,upperbound,x_half):
    a = 0.5*upperbound*(x_half + 1)/(y_intersect - upperbound)
    return floor(a*(y_intersect - u)/(x + 1) + upperbound)
	

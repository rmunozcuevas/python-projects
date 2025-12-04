import billboard
from billboard import chart

# chart = billboard.ChartData('hot-100', date='2016-03-26')
# print(chart)

top_hundred = billboard.ChartData('hot-100')
print(top_hundred)

song = chart[0]
song
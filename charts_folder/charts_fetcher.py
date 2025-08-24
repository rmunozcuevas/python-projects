
import billboard

chart = billboard.ChartData('hot-100')
print(chart.title)         # e.g. "The Hot 100"
print("TOP SONG RIGHT NOW",chart[0].title, "-", chart[0].artist)





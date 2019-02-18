#good_perf.py
#####python -m cProfile good_perf.py
```
{'2013': 5911, '2014': 5854, '2015': 5994, '2016': 5762, '2017': 5789, '2018': 5811}
'ao' was found 63395 times
0:00:04.023405
44233 function calls (44216 primitive calls) in 4.029 seconds
 ```

#poor_perf.py
#####python -m cProfile poor_perf.py
```
{'2013': 5911, '2014': 5854, '2015': 5994, '2016': 5762, '2017': 5789, '2018': 5811}
'ao' was found 63395 times
1087287 function calls (1087270 primitive calls) in 11.910 seconds
 ```
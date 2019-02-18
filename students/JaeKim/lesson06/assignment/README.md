#good_perf.py
#####python -m cProfile good_perf.py
```
{'2013': 5911, '2014': 5854, '2015': 5994, '2016': 5762, '2017': 5789, '2018': 5811}
'ao' was found 63395 times
0:00:04.190300
         44233 function calls (44216 primitive calls) in 4.199 seconds
 ```

#poor_perf.py
#####python -m cProfile poor_perf.py
```
{'2013': 5911, '2014': 5854, '2015': 5994, '2016': 5762, '2017': 11600, '2018': 0}
'ao' was found 63395 times
         1087287 function calls (1087270 primitive calls) in 9.720 seconds
         ```
         
         
44572 function calls (44549 primitive calls) in 4.096 seconds
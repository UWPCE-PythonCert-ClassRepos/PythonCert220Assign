1. Initial poor_perf.py output data and time it took to run the loop one time
	C:\Users\Zach\UWPYTHON\PythonCert220Assign\students\Zach Cooper\lesson06>python -m cProfile poor_perf.py
	{'2013': 1025, '2014': 1013, '2015': 1111, '2016': 1023, '2017': 2029, '2018': 0}
	'ao' was found 63395 times
	20.464950117999997
         	1085304 function calls (1085280 primitive calls) in 20.474 seconds
2. Changed a typo for the year in year_count. Intitially returned '2018': 0 but now returns '2018': 5811.
3. Added a simple test to assert that my year_count and 'ao' count where equal.
4. Added code to skip the header. The header was breaking the code when we are trying to convert the date string
   using datetime.
5. Used datetime in a list comprehension to convert the dates strings into date objects. Result using datetime 	
   comprehension was: 43.636000302 seconds

6. The issue with my first comprehension was it was converting date strings into date objects for first loop, then 
   looping through a second time to count the dates, and the an additional time to count 'ao' in the file. So I added
   converted the list comprehension back into a a for loop and added all operations into this so they can be 
   performed in a single loop and not three. Overall output:
	{'2013': 5911, '2014': 5854, '2015': 5994, '2016': 5762, '2017': 5789, '2018': 5811}
	ao was found 63395 times
	35.434349213 seconds.
7. The issue using datetime is that it takes so much time converting all of the date strings into date objects. It has
   to convert 1 million records in the file before it can start counting and that is counterintuitive to being fast.
   Using cProfile you can see where the time is being used up:
	 1000001   17.639    0.000   32.750    0.000 _strptime.py:318(_strptime)
               1    0.000    0.000    0.001    0.001 _strptime.py:49(__init__)
         1000001    2.933    0.000   35.683    0.000 _strptime.py:574(_strptime_datetime)
   
   There is two ways to think about this. If you realistically need to only iterate and use this file once or twice
   then using datetime is a good idea because we are not always guaranteed a clean set of dates that are all in
   the same date format as this file is so using datetime output a clean set of data. On the other hand, its really
   slow and if you know that all of your dates are intially in the correct format, it would be quickest to
   just to leave them in string format as the output time will be substantially quicker. It is all up the the client
   and what they are looking for.

9. Pylint Results:
	-------------------------------------------------------------------
	Your code has been rated at 10.00/10 (previous run: 8.95/10, +1.05)
	
8. Tried playing around with pypy but it has an interesting setup in Windows so I wasnt able to run my good_perf
   file in its shell. I believe it is a direct PATH issue.

9. Created an alt_good_perf.py to try the script without convert date strings to date objects.
   Output Data:
	{'2015': 5994, '2013': 5911, '2014': 5854, '2016': 5762, '2017': 5789, '2018': 5811}
	'ao' was found 63395 times
	8.722618477

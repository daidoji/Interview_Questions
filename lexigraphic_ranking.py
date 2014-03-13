#!/usr/bin/python

# This script should provide a lexigraphic ranking of strings amongst every possible permutation of that string
# Assumes lexigraphic ordering of all capital letters for simplicity

import sys
from math import factorial
from string import upper
from itertools import groupby

if( sys.argv[1] ):
	user_input = upper( str( sys.argv[1] ) )
else:
	print "You must input a string if you'd like to rank it"

# Make char count map 
def build_char_ranks( in_str ):
	ranks = []

	for i, c in enumerate( in_str ) : 
		chars_smaller = filter( lambda x: c > x, in_str[i+1:] )

		cnt_chars_less_than = len( chars_smaller )
		fact_candidates = filter( lambda x: x > 1, [ len( list(group) ) for key, group in groupby(chars_smaller) ] )
		rank_divisor = reduce( lambda x,y: factorial(x) * factorial(y), fact_candidates, 1 )

		ranks.append( [cnt_chars_less_than, rank_divisor] )

	return ranks

# This will rank the string
def rank_str( user_input ):
	ranks = build_char_ranks( user_input )
	
	j = 0
	fact_cache = 0
	tot_sum = 0

	while(ranks):
		(rnk, rnk_divisor) = tuple(ranks.pop())

		fact_cache = fact_cache * j
		tot_sum = tot_sum + ( rnk * ( fact_cache ) ) / rnk_divisor
		
		j = j + 1 

		if( fact_cache == 0 ): 
			fact_cache = fact_cache + 1

	tot_sum = tot_sum + 1
  
	return tot_sum

print "Input: %s Rank: %d" % ( user_input, rank_str( user_input ) )

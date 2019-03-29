#!/bin/bash

if [[ test.csv -nt /tmp/g2p_lex-test.txt ]]; then
	echo "creating tmp test-pair file..."
	cat test.csv | cut -d "," -f 1 > /tmp/g2p_lex-test.txt
fi

# if source is newer than compiled, recompile
if [[ g2p.twolc -nt g2p.hfst ]]; then
	echo "compiling hfst file..."
	hfst-twolc -i g2p.twolc -o g2p.tmp.hfst
	echo "creating base FST with universal language..."
	echo "?* ;" | hfst-regexp2fst -o univ.hfst
	echo "compose-intersecting twolc rules with universal FST..."
	hfst-compose-intersect univ.hfst g2p.tmp.hfst > g2p.hfst
	echo "converting to optimized lookup format..."
	hfst-fst2fst -O -i g2p.hfst -o g2p.hfstol
fi

echo "running test entries..."
cat /tmp/g2p_lex-test.txt | hfst-lookup g2p.hfstol 2>/dev/null >/tmp/output_g2p_hfst.txt

echo "To see output from test.csv, use..."
echo "less /tmp/output_g2p_hfst.txt"

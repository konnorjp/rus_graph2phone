# create tmp test-pair file
cat test.csv | cut -d "," -f 1 > /tmp/g2p_lex-test.txt

# compiles FST
printf "read-grammar g2p.twolc
compile
intersect
y
g2p-all
save-binary g2p.xfst
lex-test-file /tmp/g2p_lex-test.txt /tmp/output_g2p_xfst.txt
quit\n" | twolc

xfst -e "load stack < g2p.xfst" \
     -e "invert net" \
     -e "save stack g2p.lookup.xfst" \
     -stop

echo -e "\nYou can use 'lookup g2p.lookup.xfst' to test arbitrary strings.\n"

echo -e "To see output from test.csv, 'less /tmp/output_g2p_xfst.txt'\n"

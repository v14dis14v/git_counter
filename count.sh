git log --pretty=format:==%an --numstat | \
 sed -r '/==.*/{s/^==//;h;D};/^$/D;s/-/0/g;s/\t[^\t]+$//;G;s/(.*)\n(.*)/\2\t\1/' \
 | awk -F '\t' '{add[$1]+=$2;del[$1]+=$3} END {for (i in add) {print i,add[i],del[i]}}'

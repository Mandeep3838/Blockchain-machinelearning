#! /bin/bash

i=4
j=3
z=1
arr=(a b)

echo ${arr[$z]}

# if [ $z == $((i%j)) ]
# then
#     echo "yes"
# else
#     echo "no"
# fi

if [ $j -le 4 ]
then
    echo "yes"
fi
python3 trab2CBC.py -t 1800 -hr 0 -se 0 -of output/wi/0.png < testCases/wi29.tsp > output/wi/0.txt &
python3 trab2CBC.py -t 1800 -hr 0 -se 1 -of output/wi/1.png < testCases/wi29.tsp > output/wi/1.txt & 
python3 trab2CBC.py -t 1800 -hr 0 -se 2 -of output/wi/2.png < testCases/wi29.tsp > output/wi/2.txt &

for job in `jobs -p`
do
echo $job
    wait $job || let "FAIL+=1"
done
#python3 trab2CBC.py -t 1800 -hr 0 -se 0 -of output/wi/3.png < testCases/wi29.tsp > output/wi/3.txt

: '
python3 trab2CBC.py -t 1800 -hr 0 -se 0 -of output/wi/0.png < testCases/wi29.tsp > output/wi/0.txt &
python3 trab2CBC.py -t 1800 -hr 0 -se 1 -of output/wi/1.png < testCases/wi29.tsp > output/wi/1.txt & 
python3 trab2CBC.py -t 1800 -hr 0 -se 2 -of output/wi/2.png < testCases/wi29.tsp > output/wi/2.txt &

for job in `jobs -p`
do
echo $job
    wait $job || let "FAIL+=1"
done
'

: '
python3 trab2CBC.py -t 1800 -hr 0 -se 0 -of output/dj/0.png < testCases/dj38.tsp > output/dj/0.txt &
python3 trab2CBC.py -t 1800 -hr 0 -se 1 -of output/dj/1.png < testCases/dj38.tsp > output/dj/1.txt & 
python3 trab2CBC.py -t 1800 -hr 0 -se 2 -of output/dj/2.png < testCases/dj38.tsp > output/dj/2.txt &

for job in `jobs -p`
do
echo $job
    wait $job || let "FAIL+=1"
done
'

: '
python3 trab2CBC.py -t 1800 -hr 0 -se 0 -of output/qa/0.png < testCases/qa194.tsp > output/qa/0.txt &
python3 trab2CBC.py -t 1800 -hr 0 -se 1 -of output/qa/1.png < testCases/qa194.tsp > output/qa/1.txt & 
python3 trab2CBC.py -t 1800 -hr 0 -se 2 -of output/qa/2.png < testCases/qa194.tsp > output/qa/2.txt &

for job in `jobs -p`
do
echo $job
    wait $job || let "FAIL+=1"
done
'

: '
python3 trab2CBC.py -t 1800 -hr 0 -se 0 -of output/uy/0.png < testCases/uy734.tsp > output/uy/0.txt
python3 trab2CBC.py -t 1800 -hr 0 -se 1 -of output/uy/1.png < testCases/uy734.tsp > output/uy/1.txt
python3 trab2CBC.py -t 1800 -hr 0 -se 2 -of output/uy/2.png < testCases/uy734.tsp > output/uy/2.txt
'

: 'Inicio dos testes com heuristica'

python3 trab2CBC.py -t 1800 -hr 1 -se 0 -of output/qa/7.png < testCases/qa194.tsp > output/qa/7.txt &
python3 trab2CBC.py -t 1800 -hr 1 -se 1 -of output/qa/8.png < testCases/qa194.tsp > output/qa/8.txt &
python3 trab2CBC.py -t 1800 -hr 1 -se 2 -of output/qa/9.png < testCases/qa194.tsp > output/qa/9.txt &

for job in `jobs -p`
do
echo $job
    wait $job || let "FAIL+=1"
done

: '
python3 trab2CBC.py -t 1800 -hr 1 -se 0 -of output/wi/4.png < testCases/wi29.tsp > output/wi/4.txt &
python3 trab2CBC.py -t 1800 -hr 1 -se 1 -of output/wi/5.png < testCases/wi29.tsp > output/wi/5.txt &
python3 trab2CBC.py -t 1800 -hr 1 -se 2 -of output/wi/6.png < testCases/wi29.tsp > output/wi/6.txt &

for job in `jobs -p`
do
echo $job
    wait $job || let "FAIL+=1"
done
'


: ' 
python3 trab2CBC.py -t 1800 -hr 1 -se 0 -of output/dj/4.png < testCases/dj38.tsp > output/dj/4.txt &
python3 trab2CBC.py -t 1800 -hr 1 -se 1 -of output/dj/5.png < testCases/dj38.tsp > output/dj/5.txt &
python3 trab2CBC.py -t 1800 -hr 1 -se 2 -of output/dj/6.png < testCases/dj38.tsp > output/dj/6.txt &

for job in `jobs -p`
do
echo $job
    wait $job || let "FAIL+=1"
done
'

: '
python3 trab2CBC.py -t 1800 -hr 1 -se 0 -of output/qa/4.png < testCases/qa194.tsp > output/qa/4.txt &
python3 trab2CBC.py -t 1800 -hr 1 -se 1 -of output/qa/5.png < testCases/qa194.tsp > output/qa/5.txt &
python3 trab2CBC.py -t 1800 -hr 1 -se 2 -of output/qa/6.png < testCases/qa194.tsp > output/qa/6.txt &

for job in `jobs -p`
do
echo $job
    wait $job || let "FAIL+=1"
done
'

: '
python3 trab2CBC.py -t 1800 -hr 1 -se 0 -of output/uy/4.png < testCases/uy734.tsp > output/uy/4.txt 
python3 trab2CBC.py -t 1800 -hr 1 -se 1 -of output/uy/5.png < testCases/uy734.tsp > output/uy/5.txt 
python3 trab2CBC.py -t 1800 -hr 1 -se 2 -of output/uy/6.png < testCases/uy734.tsp > output/uy/6.txt 
'

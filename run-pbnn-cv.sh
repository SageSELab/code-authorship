num_of_folds=$1

for i in $(seq 0 $((num_of_folds - 1)))
do
    python ../../pbnn-training.py --fold=$i --h_config_no=1
done

for i in $(seq 0 $((num_of_folds - 1)))
do
    python ../../pbnn-training.py --fold=$i --h_config_no=2
done

for i in $(seq 0 $((num_of_folds - 1)))
do
    python ../../pbnn-training.py --fold=$i --h_config_no=3
done

for i in $(seq 0 $((num_of_folds - 1)))
do
    python ../../pbnn-training.py --fold=$i --h_config_no=4
done

for i in $(seq 0 $((num_of_folds - 1)))
do
    python ../../pbnn-training.py --fold=$i --h_config_no=5
done
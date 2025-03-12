num_of_folds=$1

for i in $(seq 0 $((num_of_folds - 1)))
do
    python ../../codellama-fine-tuning.py --model_path=codellama/CodeLlama-7b-hf --fold=$i --max_context_length=2500 --h_config_no=1
done


for i in $(seq 0 $((num_of_folds - 1)))
do
    python ../../codellama-fine-tuning.py --model_path=codellama/CodeLlama-7b-hf --fold=$i --max_context_length=2500 --h_config_no=2
done


for i in $(seq 0 $((num_of_folds - 1)))
do
    python ../../codellama-fine-tuning.py --model_path=codellama/CodeLlama-7b-hf --fold=$i --max_context_length=2500 --h_config_no=3
done

for i in $(seq 0 $((num_of_folds - 1)))
do
    python ../../codellama-fine-tuning.py --model_path=codellama/CodeLlama-7b-hf --fold=$i --max_context_length=2500 --h_config_no=4
done

for i in $(seq 0 $((num_of_folds - 1)))
do
    python ../../codellama-fine-tuning.py --model_path=codellama/CodeLlama-7b-hf --fold=$i --max_context_length=2500 --h_config_no=5
done

for i in $(seq 0 $((num_of_folds - 1)))
do
    python ../../codellama-fine-tuning.py --model_path=codellama/CodeLlama-7b-hf --fold=$i --max_context_length=2500 --h_config_no=6
done
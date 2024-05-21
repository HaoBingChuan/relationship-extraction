export finetuned_model=./checkpoint/model_best_aiStudioKE


python -u -m paddle.distributed.launch --gpus "1" finetune.py \
    --device gpu \
    --logging_steps 10 \
    --save_steps 100 \
    --eval_steps 100 \
    --seed 42 \
    --model_name_or_path uie-m-large \
    --output_dir $finetuned_model \
    --train_path data/aiStudioKE/train.txt \
    --dev_path data/aiStudioKE/dev.txt \
    --max_seq_length 512  \
    --per_device_eval_batch_size 8 \
    --per_device_train_batch_size  8 \
    --num_train_epochs 50 \
    --learning_rate 1e-5 \
    --do_train \
    --do_eval \
    --do_export \
    --export_model_dir $finetuned_model \
    --label_names "start_positions" "end_positions" \
    --overwrite_output_dir \
    --disable_tqdm True \
    --metric_for_best_model eval_f1 \
    --load_best_model_at_end  True \
    --save_total_limit 1 \








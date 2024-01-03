# Direct Training Command

python3 train_lora.py --run_name dow30v3-llama2-5e-5lr-qkvogud --base_model llama2 --dataset dow30v3-20200101-20231220-llama-data --max_length 1024 --batch_size 1 --gradient_accumulation_steps 16 --learning_rate 5e-5 --num_epochs 5 --log_interval 10 --warmup_ratio 0.03 --scheduler constant --evaluation_strategy steps --ds_config config.json
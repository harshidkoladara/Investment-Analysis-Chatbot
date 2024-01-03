export NCCL_IGNORE_DISABLED_P2P=1
export TRANSFORMERS_NO_ADVISORY_WARNINGS=1
export TOKENIZERS_PARALLELISM=0


CUDA_VISIBLE_DEVICES=0, 1  deepspeed --master_port 61000 \
# --include localhost:0 \
train_lora.py \
--run_name dow30-llama2-custom \
--base_model llama2 \
--dataset dow30v3-20200101-20231220-llama-data \
--max_length 1024 \
--batch_size 1 \
--gradient_accumulation_steps 16 \
--learning_rate 5e-5 \
--num_epochs 5 \
--log_interval 10 \
--warmup_ratio 0.03 \
--scheduler constant \
--evaluation_strategy steps \
--ds_config config.json
CUDA_VISIBLE_DEVICES=1 python opensora/sample/sample_t2v.py \
    --model_path /storage/ongoing/new/Open-Sora-Plan/bs2_20node_73000k_480p_61x480p_lr1e-4_snr5_noioff0.02_ema_rope_uditultra122_qknorm_ds222_mt5xxl_sucai288w/checkpoint-7000/model_ema \
    --version 65x512x512 \
    --num_frames 61 \
    --height 480 \
    --width 640 \
    --cache_dir "cache_dir" \
    --text_encoder_name google/mt5-xxl \
    --text_encoder_name google/mt5-xxl \
    --text_prompt examples/prompt_list_0.txt \
    --ae CausalVAEModel_4x8x8 \
    --ae_path "/storage/dataset/test140k" \
    --save_img_path "./sample_video_ema_61x480p_k333_s222_cfg4.5_step100" \
    --fps 24 \
    --guidance_scale 4.5 \
    --num_sampling_steps 100 \
    --enable_tiling \
    --max_sequence_length 512 \
    --sample_method DPMSolverMultistep \
    --model_3d
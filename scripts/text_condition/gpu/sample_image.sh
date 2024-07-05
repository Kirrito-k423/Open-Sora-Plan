CUDA_VISIBLE_DEVICES=1 python opensora/sample/sample_t2v.py \
    --model_path /storage/ongoing/new/Open-Sora-Plan/custom_image_weight \
    --version 65x512x512 \
    --num_frames 1 \
    --height 480 \
    --width 640 \
    --cache_dir "cache_dir" \
    --text_encoder_name google/mt5-xxl \
    --text_prompt examples/prompt_list_0.txt \
    --ae CausalVAEModel_4x8x8 \
    --ae_path "/storage/dataset/test140k" \
    --save_img_path "sample_image_fp32_73000_cfg2.5_step20_480p_pos_neg_convert" \
    --fps 24 \
    --guidance_scale 2.5 \
    --num_sampling_steps 20 \
    --enable_tiling \
    --max_sequence_length 512 \
    --sample_method DPMSolverMultistep \
    --model_3d
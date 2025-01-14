# coding=utf-8
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Mapping, Any
from logging import getLogger

import torch
from torch import nn
from megatron.training.arguments import core_transformer_config_from_args
from megatron.training import get_args

from mindspeed_mm.models.predictor import PredictModel
from mindspeed_mm.models.diffusion import DiffusionModel
from mindspeed_mm.models.ae import AEModel
from mindspeed_mm.models.text_encoder import TextEncoder
from mindspeed_mm.utils.utils import get_dtype

logger = getLogger(__name__)


class SoRAModel(nn.Module):
    """
    Instantiate a video generation model from config.
    SoRAModel is an assembled model, which may include text_encoder, video_encoder, predictor, and diffusion model

    Args:
        config (dict): the general config for Multi-Modal Model
        {
            "ae": {...},
            "text_encoder": {...},
            "predictor": {...},
            "diffusion": {...},
            "load_video_features":False,
            ...
        }
    """

    def __init__(self, config):
        super().__init__()
        self.config = core_transformer_config_from_args(get_args())
        self.weight_dtype = get_dtype(config.weight_dtype)
        self.load_video_features = config.load_video_features
        self.load_text_features = config.load_text_features
        if not self.load_video_features:
            self.ae = AEModel(config.ae).eval()
            self.ae.requires_grad_(False)
        if not self.load_text_features:
            self.text_encoder = TextEncoder(config.text_encoder).eval()
            self.text_encoder.to(self.weight_dtype)
            self.text_encoder.requires_grad_(False)
            self.text_encoder_2 = None
            if config.get("text_encoder_2", None) is not None:
                self.text_encoder_2 = TextEncoder(config.text_encoder_2).eval()
                self.text_encoder_2.to(self.weight_dtype)
                self.text_encoder_2.requires_grad_(False)

        self.predictor = PredictModel(config.predictor).get_model().to(self.weight_dtype)
        self.diffusion = DiffusionModel(config.diffusion).get_model()

    def set_input_tensor(self, input_tensor):
        self.predictor.set_input_tensor(input_tensor)

    def forward(
        self, 
        video, 
        video_mask=None, 
        prompt_ids=None, 
        prompt_mask=None, 
        prompt_ids_2=None, 
        prompt_mask_2=None, 
        **kwargs
    ):
        """
        video: raw video tensors, or ae encoded latent
        prompt_ids: tokenized input_ids, or encoded hidden states
        video_mask: mask for video/image
        prompt_mask: mask for prompt(text)
        """
        with torch.no_grad():
            # Visual Encode
            if self.load_video_features:
                latents = video
            else:
                latents = self.ae.encode(video)
            # Text Encode
            if self.load_text_features:
                prompt = prompt_ids
                prompt_2 = prompt_ids_2
            else:
                B, N, L = prompt_ids.shape
                prompt_ids = prompt_ids.view(-1, L)
                prompt_mask = prompt_mask.view(-1, L)
                prompt = self.text_encoder.encode(prompt_ids, prompt_mask)
                prompt = prompt.view(B, N, L, -1)
                prompt_mask = prompt_mask.view(B, 1, L)

                if self.text_encoder_2 is not None and prompt_ids_2 is not None:
                    B_, N_, L_ = prompt_ids_2.shape
                    prompt_ids_2 = prompt_ids_2.view(-1, L_)
                    prompt_mask_2 = prompt_mask_2.view(-1, L_)
                    prompt_2 = self.text_encoder_2.encode(prompt_ids_2, prompt_mask_2)
                    prompt_2 = prompt_2.view(B_, N_, -1)
        # print("--------------------------shape--------------------------")
        # print(f"latent: {latents.shape}, prompt: {prompt.shape}, prompt_2: {prompt_2.shape}, video_mask: {video_mask.shape}, prompt_mask: {prompt_mask.shape}, prompt_mask_2: {prompt_mask_2.shape}")
        # print("--------------------------dtype--------------------------")
        # print(f"latent: {latents.dtype}, prompt: {prompt.dtype}, prompt_2: {prompt_2.dtype}, video_mask: {video_mask.dtype}, prompt_mask: {prompt_mask.dtype}, prompt_mask_2: {prompt_mask_2.dtype}")
        # print("--------------------------device--------------------------")
        # print(f"latent: {latents.device}, prompt: {prompt.device}, prompt_2: {prompt_2.device}, video_mask: {video_mask.device}, prompt_mask: {prompt_mask.device}, prompt_mask_2: {prompt_mask_2.device}")
        latents = latents.to(self.weight_dtype)

        noised_latents, noise, timesteps = self.diffusion.q_sample(latents, model_kwargs=kwargs, mask=video_mask)

        model_output = self.predictor(
            noised_latents,
            attention_mask=video_mask,
            timestep=timesteps,
            encoder_hidden_states=prompt,
            encoder_attention_mask=prompt_mask,
            pooled_projections=prompt_2,
            **kwargs,
        )
        return model_output, latents, noised_latents, timesteps, noise, video_mask

    def compute_loss(
        self, model_output, latents, noised_latents, timesteps, noise, video_mask
    ):
        """compute diffusion loss"""
        loss_dict = self.diffusion.training_losses(
            model_output=model_output,
            x_start=latents,
            x_t=noised_latents,
            noise=noise,
            t=timesteps,
            mask=video_mask,
        )
        return loss_dict
    
    def train(self, mode=True):
        self.predictor.train()

    def state_dict_for_save_checkpoint(self, prefix="", keep_vars=False):
        """Customized state_dict"""
        return self.predictor.state_dict(prefix=prefix, keep_vars=keep_vars)
    
    def load_state_dict(self, state_dict: Mapping[str, Any], strict: bool = False):
        """Customized load."""
        if not isinstance(state_dict, Mapping):
            raise TypeError(f"Expected state_dict to be dict-like, got {type(state_dict)}.")
        
        missing_keys, unexpected_keys = self.predictor.load_state_dict(state_dict, strict)

        if missing_keys is not None:
            logger.info(f"Missing keys in state_dict: {missing_keys}.")
        if unexpected_keys is not None:
            logger.info(f"Unexpected key(s) in state_dict: {unexpected_keys}.")

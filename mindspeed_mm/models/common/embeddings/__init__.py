# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# --------------------------------------------------------
# References:
# get_3d_sincos_pos_embed:   https://github.com/PKU-YuanGroup/Open-Sora-Plan
# get_3d_sincos_pos_embed_from_grid: https://github.com/PKU-YuanGroup/Open-Sora-Plan
# get_2d_sincos_pos_embed: https://github.com/PKU-YuanGroup/Open-Sora-Plan
# get_2d_sincos_pos_embed_from_grid: https://github.com/PKU-YuanGroup/Open-Sora-Plan
# get_1d_sincos_pos_embed: https://github.com/PKU-YuanGroup/Open-Sora-Plan
# get_1d_sincos_pos_embed_from_grid: https://github.com/PKU-YuanGroup/Open-Sora-Plan
# VideoPatchEmbed2D: https://github.com/PKU-YuanGroup/Open-Sora-Plan
# OverlapPatchEmbed2D: https://github.com/PKU-YuanGroup/Open-Sora-Plan
# OverlapPatchEmbed3D: https://github.com/PKU-YuanGroup/Open-Sora-Plan
# PatchEmbed3D: https://github.com/hpcaitech/Open-Sora/
# PatchEmbed2DP: https://github.com/PKU-YuanGroup/Open-Sora-Plan
# PatchEmbed2D: https://github.com/PKU-YuanGroup/Open-Sora-Plan
# TimestepEmbedder:    https://github.com/hpcaitech/Open-Sora/
# LabelEmbbedder:   https://github.com/hpcaitech/Open-Sora/
# --------------------------------------------------------

from .common_embeddings import CaptionEmbedder, LabelEmbedder, TimestepEmbedder, SizeEmbedder
from .patch_embeddings import (
    OverlapPatchEmbed2D,
    OverlapPatchEmbed3D,
    PatchEmbed3D,
    VideoPatchEmbed2D,
    PatchEmbed2D,
)
from .pos_embeddings import (
    PositionEmbedding2D,
    get_1d_sincos_pos_embed,
    get_2d_sincos_pos_embed,
    get_3d_sincos_pos_embed,
)

from .rope import (
    PositionGetter3D,
    RoPE3D,
    apply_rotary_emb
)

__all__ = [
    "CaptionEmbedder", "LabelEmbedder", "TimestepEmbedder", "SizeEmbedder",
    "OverlapPatchEmbed2D", "OverlapPatchEmbed3D", "PatchEmbed3D", "VideoPatchEmbed2D", "PatchEmbed2D",
    "PositionEmbedding2D", "get_1d_sincos_pos_embed", "get_2d_sincos_pos_embed", "get_3d_sincos_pos_embed",
    "PositionGetter3D", "RoPE3D", "apply_rope1d",
]
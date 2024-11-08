from torch import nn
from megatron.training.utils import print_rank_0

from mindspeed_mm.models.common.checkpoint import load_checkpoint
from .dits import VideoDiT, Latte, STDiT, STDiT3, VideoDitSparse

PREDICTOR_MODEL_MAPPINGS = {
    "videodit": VideoDiT,
    "videoditsparse": VideoDitSparse,
    "latte": Latte,
    "stdit": STDiT,
    "stdit3": STDiT3,
}


class PredictModel(nn.Module):
    """
    The backnone of the denoising model
    PredictModel is the factory class for all unets and dits

    Args:
        config[dict]: for Instantiating an atomic methods
    """

    def __init__(self, config):
        super().__init__()
        model_cls = PREDICTOR_MODEL_MAPPINGS[config.model_id]
        self.predictor = model_cls(**config.to_dict())
        if config.from_pretrained is not None:
            load_checkpoint(self.predictor, config.from_pretrained)
            print_rank_0("load predictor's checkpoint sucessfully")

    def get_model(self):
        return self.predictor

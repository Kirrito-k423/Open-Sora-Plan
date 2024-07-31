from torch import nn

from .dits import DiT, Latte


PREDICTOR_MODEL_MAPPINGS = {
    "dit": DiT,
    "latte": Latte,
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
        self.predictor = model_cls(config)

    def get_model(self):
        return self.predictor
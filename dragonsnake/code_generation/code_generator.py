import ast as _ast

from dragonsnake.utils import throw_feature_not_supported


class CodeGenerator:
    @property
    def target_format(self) -> str:
        return self._target_format

    @target_format.setter
    def target_format(self, value: str):
        self._target_format = str(value)

    def __init__(self, target_format):
        self.target_format = target_format

    def generate_module(self, module: _ast.Module) -> str:
        return ""

    def throw_feature_not_supported(self, category: str, feature: object):
        namespace = "generator/" + self.target_format
        throw_feature_not_supported(feature, namespace=namespace, category=category)

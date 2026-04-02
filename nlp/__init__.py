# Mongolian NLP Toolkit
# 蒙古文 NLP 工具包

from .mongolian_tokenizer import MongolianTokenizer
from .mongolian_pos_tagger import MongolianPOSTagger
from .mongolian_parser import MongolianParser

__version__ = '1.0.0'
__author__ = 'Mongolian AI Team'

__all__ = [
    'MongolianTokenizer',
    'MongolianPOSTagger',
    'MongolianParser',
]

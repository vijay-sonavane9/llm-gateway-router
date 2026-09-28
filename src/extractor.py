import tiktoken
import re
import numpy as np

_tokenizer = tiktoken.get_encoding("cl100k_base")

def extract_features(prompt: str) -> np.ndarray:
    char_count = len(prompt)
    if char_count == 0:
        return np.zeros((1, 5))
        
    token_count = len(_tokenizer.encode(prompt))
    has_code_block = 1.0 if "```" in prompt else 0.0
    question_count = float(prompt.count("?"))
    multistep = float(len(re.findall(r'(first|then|finally|step|compare)', prompt.lower())))
    
    # Must match the training column order
    return np.array([[token_count, char_count, has_code_block, question_count, multistep]])
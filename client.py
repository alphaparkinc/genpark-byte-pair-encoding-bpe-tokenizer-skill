"""
Autonomous Agent Byte-Pair Encoding (BPE) Tokenizer Skill
Pure Python Standard Library implementation.
"""
from typing import List, Dict, Tuple, Any

class BPETokenizer:
    """
    Byte-Pair Encoding (BPE) subword tokenizer.
    """
    def __init__(self, num_merges: int = 15):
        self.num_merges = num_merges
        self.merges = {}

    def train(self, corpus: List[str]):
        vocab = [list(w) + ["</w>"] for w in corpus]
        for _ in range(self.num_merges):
            pairs = {}
            for word in vocab:
                for i in range(len(word) - 1):
                    p = (word[i], word[i + 1])
                    pairs[p] = pairs.get(p, 0) + 1
            if not pairs:
                break
            best_pair = max(pairs, key=pairs.get)
            if pairs[best_pair] <= 1:
                break
            self.merges[best_pair] = "".join(best_pair)

            new_vocab = []
            for word in vocab:
                i = 0
                new_word = []
                while i < len(word):
                    if i < len(word) - 1 and (word[i], word[i + 1]) == best_pair:
                        new_word.append("".join(best_pair))
                        i += 2
                    else:
                        new_word.append(word[i])
                        i += 1
                new_vocab.append(new_word)
            vocab = new_vocab

    def tokenize(self, word: str) -> List[str]:
        tokens = list(word) + ["</w>"]
        for p, replacement in self.merges.items():
            i = 0
            new_tokens = []
            while i < len(tokens):
                if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == p:
                    new_tokens.append(replacement)
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
        return tokens

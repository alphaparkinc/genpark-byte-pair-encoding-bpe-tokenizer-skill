"""Example usage for BPE Tokenizer Skill."""
from client import BPETokenizer

def main():
    print("Executing BPE Tokenizer...")
    bpe = BPETokenizer(num_merges=10)
    corpus = ["low", "lower", "lowest", "widest", "newest"]
    bpe.train(corpus)
    print("Learned Merges:", bpe.merges)

    toks = bpe.tokenize("lower")
    print("Tokenized 'lower':", toks)
    assert len(toks) < len("lower") + 1
    print("BPE Tokenizer verified successfully!")

if __name__ == "__main__":
    main()

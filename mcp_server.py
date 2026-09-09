"""MCP Server for BPE Tokenizer Skill."""
import json
import sys
from client import BPETokenizer

def main():
    tokenizer = BPETokenizer()
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [
                            {
                                "name": "train_bpe",
                                "description": "Train BPE subword merges on corpus",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "corpus": {"type": "array", "items": {"type": "string"}},
                                        "num_merges": {"type": "integer"}
                                    },
                                    "required": ["corpus"]
                                }
                            },
                            {
                                "name": "tokenize_word",
                                "description": "Tokenize word with trained BPE merges",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"word": {"type": "string"}},
                                    "required": ["word"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "train_bpe":
                    t = BPETokenizer(args.get("num_merges", 15))
                    t.train(args["corpus"])
                    tokenizer = t
                    out = {"merges_learned": len(t.merges)}
                else:
                    toks = tokenizer.tokenize(args["word"])
                    out = {"tokens": toks}
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(out)}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()

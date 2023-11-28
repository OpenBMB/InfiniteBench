import json
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from eval_utils import (
    dump_jsonl,
    create_prompt,
    load_data,
    get_answer,
    DATA_NAME_TO_MAX_NEW_TOKENS,
)
from args import parse_args


MAX_POSITION_ID = 128 * 1024
TRUNCATE_LEN = 128 * 1024


def truncate_input(input: list, max_length: int, manner="middle"):
    if len(input) <= max_length:
        return input
    if manner == "middle":
        split = max_length // 2
        return input[0:split] + input[-split:]
    else:
        return None


def truncate_by_tokens(input, tok, max_tokens, manner: str = "middle"):
    tokens = tok.encode(input)
    len_before = len(tokens)
    print(f"Length before: {len_before}")
    tokens = truncate_input(tokens, max_length=max_tokens, manner=manner)
    len_after = len(tokens)  # type: ignore
    print(f"Length after: {len_after}")
    assert len_after <= len_before
    assert len_after <= max_tokens
    return tok.decode(tokens, skip_special_tokens=True)


def generate(model, tokenizer, prompt: str, max_tokens: int) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(
        inputs["input_ids"],
        max_new_tokens=max_tokens,
        pad_token_id=tokenizer.eos_token_id,
    )
    output_text = tokenizer.decode(
        output[0].tolist(), skip_special_tokens=True
    )
    return output_text


def get_pred(
    model,
    tok,
    input_text: str,
    max_tokens: int,
    verbose: bool = False,
) -> str:
    """
    Truncate down to 128k then make inference.
    """
    print("Truncating...")
    input_text = truncate_by_tokens(input_text, tok, max_tokens)
    if verbose:
        print("# chars:", len(input_text))
        print("=============== Input ===============")
        print(input_text[:200])
        print("...")
        print(input_text[-200:])
        print("=====================================")
    output = generate(model, tok, input_text, max_tokens=max_tokens)
    if verbose:
        print("Prediction:", output)
    return output


def load_model(model_name=None, device: str = "cuda"):
    if model_name is None:
        model_name = "RWKV/rwkv-4-world-7b"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map=device,
        torch_dtype=torch.bfloat16,
        # local_files_only=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
    )
    return model, tokenizer


if __name__ == "__main__":
    model_name = "rwkv"
    args = parse_args()
    print(json.dumps(vars(args), indent=2))
    max_tokens = DATA_NAME_TO_MAX_NEW_TOKENS[args.task]
    # Model
    print("Loading model and tokenizer...")
    model, tok = load_model(args.model_path, args.device)
    result_dir = Path(args.output_dir, model_name)
    # Load data
    print(f"Loading data from {args.data_dir}, task: {args.task}")
    examples = load_data(args.task, args.data_dir)
    result_dir.mkdir(exist_ok=True, parents=True)
    if args.stop_idx is None:
        args.stop_idx = len(examples)
        output_path = result_dir / f"preds_{args.task}.jsonl"
    else:
        output_path = (
            result_dir
            / f"preds_{args.task}_{args.start_idx}-{args.stop_idx}.jsonl"  # noqa
        )
    preds = []
    print("==== Evaluation ====")
    print(f"# examples: {len(examples)}")
    print(f"Start index: {args.start_idx}")
    print(f"Stop index: {args.stop_idx}")
    for i in range(args.start_idx, args.stop_idx):
        eg = examples[i]
        input_text = create_prompt(eg, args.task, model_name, args.data_dir)
        print(f"====== Example {i} ======")
        pred = get_pred(
            model,
            tok,
            input_text,
            max_tokens=max_tokens,
            verbose=args.verbose,
        )
        preds.append(
            {
                "id": i,
                "pred": pred,
                "label": get_answer(eg, args.task),
            }
        )
        dump_jsonl(preds, output_path)

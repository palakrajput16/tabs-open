# 01: Why do AI agents need memory?

Code for the Tabs Open post **Why Do AI Agents Need Memory?** (link to the post goes here once it's live).

## What this is

A tiny simulation that compares two ways of answering questions about the same documents:

- **Stateless:** re-reads every document for every question.
- **Stateful:** reads the documents once, saves the facts in a small memory store, then answers from the store.

It prints how many "tokens" each design uses, so you can see how the cost grows.

## Run it

You only need Python 3. There's nothing to install.

```
python agent_memory_demo.py
python agent_memory_demo.py --repeat 10
```

The first runs 5 questions. The second repeats those 5 questions 10 times, so 50 in total.

## What you should see

| Questions | Stateless | Stateful | Difference |
| --- | --- | --- | --- |
| 5 | 10,910 tokens | 2,201 tokens | about 5x |
| 50 | 109,100 tokens | 2,372 tokens | about 46x |

The full output is in `sample_output.txt`. You'll get the same numbers because the script uses a fixed random seed.

## What this is not

This is a toy. It shows the **shape** of the cost, not how a real model behaves.

- "Tokens" are just word counts.
- A keyword lookup stands in for the model, so there's no real language model and no accuracy being measured.
- It is not Letta or MemGPT. It's a simplified picture of the idea of reading once and remembering.

## Where the ideas come from

- [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)
- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [Letta docs: Agent memory & architecture](https://docs.letta.com/guides/agents/architectures/memgpt)

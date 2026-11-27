"""
Stateless vs stateful agent: a toy cost demo.

No API key needed, no libraries to install.
It simulates the COST STRUCTURE of two designs, not real model quality.
"Tokens" here are just word counts, and a keyword lookup stands in for the model.

Run:
    python agent_memory_demo.py              # 5 questions
    python agent_memory_demo.py --repeat 10  # 50 questions (5 questions x 10)
"""

import argparse
import random

random.seed(7)  # fixed seed, so everyone gets the same fake documents

# ---------- fake document set ----------
FILLER = ("the parties agree that all obligations shall continue in force "
          "unless otherwise stated in writing by both sides").split()


def make_doc(name, facts, n_filler_lines=60):
    lines = [" ".join(random.choices(FILLER, k=12)) for _ in range(n_filler_lines)]
    for key, value in facts.items():
        lines.insert(random.randrange(len(lines)), f"FACT {key}: {value}")
    return name, "\n".join(lines)


DOCS = dict([
    make_doc("contract_a.txt", {"renewal_date": "2027-03-01", "notice_period": "60 days"}),
    make_doc("contract_b.txt", {"governing_law": "India", "payment_terms": "net 30"}),
    make_doc("contract_c.txt", {"liability_cap": "2x annual fees", "auto_renew": "yes"}),
])

BASE_QUESTIONS = ["renewal_date", "payment_terms", "liability_cap", "notice_period", "auto_renew"]


def tokens(text):
    return len(text.split())


# ---------- design 1: stateless ----------
def run_stateless(questions):
    total, rows = 0, []
    for q in questions:
        cost, answer = 0, None
        for _, text in DOCS.items():          # re-reads EVERYTHING each time
            cost += tokens(text)
            for line in text.splitlines():
                if line.startswith(f"FACT {q}:"):
                    answer = line.split(": ", 1)[1]
        total += cost
        rows.append((q, answer, cost))
    return total, rows


# ---------- design 2: stateful (a tiny memory store) ----------
class MemoryStore:
    def __init__(self):
        self.facts = {}                        # key -> (value, source)

    def write(self, key, value, source):
        self.facts[key] = (value, source)

    def read(self, key):
        return self.facts.get(key)


def run_stateful(questions):
    memory, total, rows = MemoryStore(), 0, []

    # pay ONCE to read and understand the documents
    ingest_cost = 0
    for name, text in DOCS.items():
        ingest_cost += tokens(text)
        for line in text.splitlines():
            if line.startswith("FACT "):
                key, value = line[5:].split(": ", 1)
                memory.write(key, value, name)
    total += ingest_cost

    # after that, questions hit memory, not the documents
    for q in questions:
        value, source = memory.read(q)
        cost = tokens(f"{q} {value} {source}")
        total += cost
        rows.append((q, f"{value}  (from {source})", cost))
    return total, rows, ingest_cost


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stateless vs stateful agent cost demo")
    parser.add_argument("--repeat", type=int, default=1,
                        help="repeat the 5 questions this many times (default 1)")
    args = parser.parse_args()
    questions = BASE_QUESTIONS * args.repeat
    show_rows = args.repeat == 1               # keep long runs readable

    s_total, s_rows = run_stateless(questions)
    m_total, m_rows, ingest = run_stateful(questions)

    print(f"{len(questions)} questions\n")

    print("STATELESS: re-reads every document for every question")
    if show_rows:
        for q, a, c in s_rows:
            print(f"  {q:<14} -> {a:<14} cost: {c:>5} tokens")
    print(f"  TOTAL: {s_total} tokens\n")

    print(f"STATEFUL: reads once ({ingest} tokens), then asks memory")
    if show_rows:
        for q, a, c in m_rows:
            print(f"  {q:<14} -> {a:<28} cost: {c:>3} tokens")
    print(f"  TOTAL: {m_total} tokens\n")

    print(f"Stateful used {s_total / m_total:.1f}x fewer tokens on this toy task.")

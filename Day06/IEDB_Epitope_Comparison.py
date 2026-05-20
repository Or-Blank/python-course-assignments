#pip install biopython
from Fetch_Epitopes import fetch_epitopes_for_organism
from Organism_Selection import ORG1, ORG2
from Bio import pairwise2
from itertools import product
from collections import Counter


def pick_top_n(epitopes, n=10):
    return sorted(epitopes, key=lambda e: e["score"], reverse=True)[:n]


def align_and_metrics(seq1, seq2):
    aln = pairwise2.align.globalxx(seq1, seq2, one_alignment_only=True)[0]
    aligned1, aligned2, score, start, end = aln
    identity = sum(a == b for a, b in zip(aligned1, aligned2)) / len(aligned1)
    return float(score), float(identity)


def compare_group(epitopes):
    results = []
    for i in range(len(epitopes)):
        for j in range(i + 1, len(epitopes)):
            s1 = epitopes[i]["sequence"]
            s2 = epitopes[j]["sequence"]
            sim, ident = align_and_metrics(s1, s2)
            results.append({"seq1": s1, "seq2": s2, "similarity": sim, "identity": ident})
    return results


def compare_cross(group1, group2):
    results = []
    for e1, e2 in product(group1, group2):
        s1 = e1["sequence"]
        s2 = e2["sequence"]
        sim, ident = align_and_metrics(s1, s2)
        results.append({"seq1": s1, "seq2": s2, "similarity": sim, "identity": ident})
    return results


def print_top_epitopes(org, epitopes):
    print(f"\n=== Top {len(epitopes)} epitopes for {org} ===")
    for i, e in enumerate(epitopes, start=1):
        print(f"#{i:2d}  seq={e['sequence']}  assays={e['assays']}  refs={e['refs']}  score={e['score']}")


def print_comparisons(title, comparisons, max_rows=20):
    print(f"\n=== {title} (showing up to {max_rows}) ===")
    for i, c in enumerate(comparisons[:max_rows], start=1):
        print(f"{i:2d}. seq1={c['seq1']}  seq2={c['seq2']}  similarity={c['similarity']:.1f}  identity={c['identity']:.3f}")


def print_best_cross_pair(cross):
    best = max(cross, key=lambda c: (c["similarity"], c["identity"]))
    print("\n=== Most similar cross-organism pair ===")
    print(f"seq1:      {best['seq1']}")
    print(f"seq2:      {best['seq2']}")
    print(f"similarity {best['similarity']:.1f}")
    print(f"identity   {best['identity']:.3f}")


def main():
    print(f"Fetching epitopes for {ORG1}...")
    epi1_all = fetch_epitopes_for_organism(ORG1)
    print(f"  Retrieved {len(epi1_all)} epitopes")

    print(f"\nFetching epitopes for {ORG2}...")
    epi2_all = fetch_epitopes_for_organism(ORG2)
    print(f"  Retrieved {len(epi2_all)} epitopes")

    top1 = pick_top_n(epi1_all, 10)
    top2 = pick_top_n(epi2_all, 10)

    print_top_epitopes(ORG1, top1)
    print_top_epitopes(ORG2, top2)

    within1 = compare_group(top1)
    within2 = compare_group(top2)

    print_comparisons(f"Within-group comparisons for {ORG1}", within1)
    print_comparisons(f"Within-group comparisons for {ORG2}", within2)

    cross = compare_cross(top1, top2)
    print_comparisons(f"Cross-organism comparisons ({ORG1} vs {ORG2})", cross)
    print_best_cross_pair(cross)


if __name__ == "__main__":
    main()

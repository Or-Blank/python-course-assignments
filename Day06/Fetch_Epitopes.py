import requests

IEDB_BASE_URL = "https://query-api.iedb.org"


def fetch_epitopes_for_organism(organism_name: str, limit: int = 200):
    """
    Fetch epitope records for a given organism from IEDB.
    Returns a list of dicts with:
      sequence, assays, refs, score
    """

    params = {
        "parent_source_antigen_organism_name": f"eq.{organism_name}",
        "select": "structure,tcell_ids,bcell_ids,mhc_ids,reference_ids",
        "limit": limit,
    }

    url = f"{IEDB_BASE_URL}/epitope_search"
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    epitopes = []
    for item in data:
        seq = item.get("structure")
        if not seq:
            continue

        tcell = item.get("tcell_ids") or []
        bcell = item.get("bcell_ids") or []
        mhc = item.get("mhc_ids") or []
        refs = item.get("reference_ids") or []

        assay_count = len(tcell) + len(bcell) + len(mhc)
        reference_count = len(refs)
        score = assay_count + reference_count

        epitopes.append({
            "sequence": seq,
            "assays": assay_count,
            "refs": reference_count,
            "score": score
        })

    return epitopes

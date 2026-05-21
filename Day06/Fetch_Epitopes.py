import requests

IEDB_BASE_URL = "https://query-api.iedb.org"


def fetch_epitopes_for_organism(organism_name: str, limit: int = 200):
    """
    Fetch epitope records for a given organism from IEDB.
    Returns a list of dicts with:
      sequence, assays, refs, score
    """

    url = f"{IEDB_BASE_URL}/epitope_search"
    select = "linear_sequence,tcell_ids,bcell_ids,reference_ids"

    candidate_filters = [
        ("source_organism_name", f"eq.{organism_name}"),
        ("source_organism_names", f"eq.{{{organism_name}}}"),
        ("parent_source_antigen_source_org_names", f"eq.{{{organism_name}}}"),
    ]

    if organism_name.isdigit():
        taxon_value = f"eq.{{NCBITaxon:{organism_name}}}"
        candidate_filters.insert(0, ("source_organism_iris", taxon_value))
    elif organism_name.startswith("NCBITaxon:"):
        taxon_value = f"eq.{{{organism_name}}}"
        candidate_filters.insert(0, ("source_organism_iris", taxon_value))

    data = []
    for field, value in candidate_filters:
        params = {field: value, "select": select, "limit": limit}
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            if data:
                break
        except (requests.exceptions.RequestException, ValueError):
            continue

    epitopes = []
    for item in data:
        seq = item.get("linear_sequence")
        if not seq:
            continue

        tcell = item.get("tcell_ids") or []
        bcell = item.get("bcell_ids") or []
        refs = item.get("reference_ids") or []

        assay_count = len(tcell) + len(bcell)
        reference_count = len(refs)
        score = assay_count + reference_count

        epitopes.append({
            "sequence": seq,
            "assays": assay_count,
            "refs": reference_count,
            "score": score
        })

    return epitopes

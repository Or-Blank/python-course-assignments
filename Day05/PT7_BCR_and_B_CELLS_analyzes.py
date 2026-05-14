import pandas as pd

def analyze_bcell_excel(path_to_excel):
    df = pd.read_excel(path_to_excel, engine='openpyxl')
    df['cluster_annotated'] = df['cluster_annotated'].fillna('Unknown')

    # ---------------------------------------------------------
    # 1. Rank clones based on clone_count
    # ---------------------------------------------------------
    clone_rank = (
        df.groupby("Clone_id")["Clone_count"]
        .sum()
        .reset_index()
        .sort_values("clone_count", ascending=False)
        .reset_index(drop=True)
    )
    clone_rank["rank"] = clone_rank.index + 1
    clone_rank = clone_rank.set_index('rank')

    # ---------------------------------------------------------
    # 2. For each clone: table of cluster_annotated counts + %
    # ---------------------------------------------------------
    clone_cluster_tables = {}

    for clone in df["clone_id"].unique():
        sub = df[df["clone_id"] == clone]

        # Count clusters within this clone
        cluster_counts = (
            sub["cluster_annotated"]
            .value_counts()
            .reset_index(name='count')
            .rename(columns={"index": "cluster_annotated"})
        )

        # Add percentage within clone
        cluster_counts["percent_within_clone"] = (
            cluster_counts["count"] / cluster_counts["count"].sum() * 100
        )

        clone_cluster_tables[clone] = cluster_counts

    # ---------------------------------------------------------
    # 3. Global cluster_annotated table (% of all cells)
    # ---------------------------------------------------------
    global_cluster = (
        df["cluster_annotated"]
        .value_counts()
        .reset_index(name='count')
        .rename(columns={"index": "cluster_annotated"})
    )
    global_cluster["percent_of_all_cells"] = (
        global_cluster["count"] / global_cluster["count"].sum() * 100
    )

    return clone_rank, clone_cluster_tables, global_cluster


# ---------------------------------------------------------
# Example usage:
# ---------------------------------------------------------
clone_rank, clone_cluster_tables, global_cluster = analyze_bcell_excel("Day05/PT7_Final_Combined_Table.xlsx")

print("\n Ranked Clones by Clone Count:")
print(clone_rank)

print("\n Cell Type Percentages of all cells:")
print(global_cluster)

print("\n=== Example: Cluster table for clone PT7_sJRC_138_G1G2 ===")
print(clone_cluster_tables["PT7_sJRC_138_G1G2"])

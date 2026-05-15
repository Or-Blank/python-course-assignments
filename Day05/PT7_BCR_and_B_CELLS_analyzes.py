import pandas as pd
import matplotlib.pyplot as plt

def analyze_bcell_excel(path_to_excel):
    df = pd.read_excel(path_to_excel, engine='openpyxl')
    df['cluster_annotated'] = df['cluster_annotated'].fillna('Unknown')

    clone_rank = (
        df.groupby("clone_id")["clone_count"]
        .sum()
        .reset_index()
        .sort_values("clone_count", ascending=False)
        .reset_index(drop=True)
    )
    clone_rank["rank"] = clone_rank.index + 1
    clone_rank = clone_rank.set_index('rank')
    
    global_cluster = (
        df["cluster_annotated"]
        .value_counts()
        .reset_index(name='count')
        .rename(columns={"index": "cluster_annotated"})
    )
    global_cluster["percent_of_all_cells"] = (
        global_cluster["count"] / global_cluster["count"].sum() * 100
    ).round(2)

    clone_cluster_tables = {}

    for clone in df["clone_id"].unique():
        sub = df[df["clone_id"] == clone]

        cluster_counts = (
            sub["cluster_annotated"]
            .value_counts()
            .reset_index(name='count')
            .rename(columns={"index": "cluster_annotated"})
        )

        cluster_counts["percent_within_clone"] = (
            cluster_counts["count"] / cluster_counts["count"].sum() * 100
        ).round(2)

        clone_cluster_tables[clone] = cluster_counts


    return clone_rank, clone_cluster_tables, global_cluster


def plot_table(df, title, filename):
    fig, ax = plt.subplots(figsize=(12, max(4, len(df) * 0.5)))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_text_props(fontweight='bold')
    plt.title(title, fontsize=14, fontweight='bold')
    plt.savefig(filename, bbox_inches='tight', dpi=150)
    plt.close()


clone_rank, clone_cluster_tables, global_cluster = analyze_bcell_excel("Day05/PT7_Final_Combined_Table.xlsx") #Change the path if your file is in a different location or has a different name, the best will be to just put the file in the same folder as this script and then just use the name of the file in the brackets on this line.

print("\n Ranked Clones by Clone Count:")
print(clone_rank)

print("\n Cell Type Percentages of all Cells:")
print(global_cluster)

print("\n Cluster table for clone PT7_Nm57_127_A1A2G1G2G3M") #If you want another clone, just change the name in the brackets for the one you want to see - Based on the clone_id column in the original excel file
print(clone_cluster_tables["PT7_Nm57_127_A1A2G1G2G3M"]) #Also here, if you want another clone, just change the name in the brackets for the one you want to see - Based on the clone_id column in the original excel file

print("\nNote: The above tables are being saved as images in your folder, please wait.")

# Generate the tables images and excel file
plot_table(global_cluster, "Cell Type Percentages of all Cells", "Day05/global_clusters.png")
plot_table(clone_cluster_tables["PT7_Nm57_127_A1A2G1G2G3M"], "Cluster table for clone PT7_Nm57_127_A1A2G1G2G3M", "Day05/example_clone.png")
clone_rank.to_excel("Day05/clone_rank.xlsx", index=True)

print("\nTable images and excel file saved to Day05/ directory.") #Change the Day05/ directory to the name of the folder you are working in if you are not working in a folder named Day05

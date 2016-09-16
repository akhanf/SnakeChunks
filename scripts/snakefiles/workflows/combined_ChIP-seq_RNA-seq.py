## This is just a draft

"""
This is a prototype of combined workflow using Snakemake's subworkflow feature. 
It requires to use Snakemake 3.8.1+

Command to run the combined workflow is currently:
    snakemake -s gene-regulation/scripts/snakefiles/workflows/combined_ChIP-seq_RNA-seq.py -p --configfile gene-regulation/examples/Combined_ChIP-seq_RNA-seq --nolock

I have yet to understand exactly just why I need to use this nolock option.

Author:
    Claire Rioualen
"""

# Subworkflows
subworkflow chip:
    workdir: config["ChIP_seq"]["directory"]
    snakefile: config["ChIP_seq"]["snakefile"]
    configfile: config["ChIP_seq"]["configfile"]

subworkflow rna:
    workdir: config["RNA_seq"]["directory"]
    snakefile: config["RNA_seq"]["snakefile"]
    configfile: config["RNA_seq"]["configfile"]


## Test include
#include: os.path.join(config["ChIP_seq"]["snakefile"])

# Combined workflow
VENN = "/data/analyses/Combined_ChIP-seq_RNA-seq/venn.png"

rule all:
    input: VENN

rule venn:
    """This draft rule takes 3 inputs and creates a Venn Diagram:
        - a gene_list generated by the ChIP-seq workflow (genes intersecting with peaks associated with FNR binding, see dataset GSE41187)
        - a gene_list generated by the RNA-seq workflow (genes differentially expressed in FNR mutants, see dataset GSE41190)
        - a gene_list manually generated from RegulonDB data (genes regulated by the FNR regulon, according to curated database RegulonDB)
    """
    input:
        regulon_genes = "/data/analyses/RegulonDB_gene_list.tab",
        chip_genes = chip("/data/analyses/ChIP-seq_SE_GSE41187/results/peaks/GSM1010219_vs_GSM1010224/homer-fdr0.001/GSM1010219_vs_GSM1010224_sickle_bowtie2_homer-fdr0.001_intersect_annot_gene_list.tab"),
        rna_genes = rna("/data/analyses/RNA-seq_PE_GSE41190/results/diffexpr/edgeR/subread-align_edgeR_gene_list.tab")
    output: "/data/analyses/Combined_ChIP-seq_RNA-seq/venn.png"
    run:
        R("""
library(VennDiagram)

chip <- as.vector(read.table("{input.chip_genes}")[,1])
rna <- as.vector(read.table("{input.rna_genes}")[,1])
regulon <- as.vector(read.table("{input.regulon_genes}")[,1])

venn.plot <- venn.diagram(list(ChIP=chip, RNA=rna, Regulon=regulon), filename="{output}", imagetype="png", fill=rainbow(3))
""")
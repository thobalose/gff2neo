"""
Variant Processing
"""
import sys

import pandas
from bioservices import KEGG

from gff2neo.dbconn import create_known_mutation_nodes

kegg = KEGG(verbose=False)


def process_mutation_file(in_file):
    """
    Process mutation file
    :param in_file:
    :return:
    """
    drugbank_dict, drugbank_id = dict(), None
    if in_file and in_file.endswith(".txt"):
        sys.stdout.write("\nAdding known mutations...")
        with open(in_file) as in_file:
            cset_name = str(in_file).split('/')[-1]
            vset_name = "doi.org/10.1186/s13073-015-0164-0"
            vset_owner = "Coll et al"
            for line in in_file:
                tab_split = line.split('\t')
                drug_name = tab_split[0].lower()
                if drug_name not in drugbank_dict.values():
                    k_drug = kegg.find("drug", str(drug_name))
                    drug_id = k_drug.split('\t')[0]
                    drug_info = kegg.parse(kegg.get(drug_id))
                    dblinks = drug_info.get("DBLINKS", None)
                    if dblinks:
                        drugbank_id = dblinks.get("DrugBank", None)
                        if drugbank_id:
                            drugbank_dict[drugbank_id] = drug_name
                else:
                    for drug_id, name in drugbank_dict.items():
                        if drug_name == name:
                            drugbank_id = drug_id

                variant_pos = tab_split[1]
                ref_allele = tab_split[2]
                alt_allele = tab_split[3]
                if "_promoter" in tab_split[4]:
                    promoter = tab_split[4]
                    gene_name = tab_split[4].strip("_promoter")
                else:
                    gene_name = tab_split[4]
                # amino acid change
                consequence = tab_split[5]
                print(drug_name.capitalize(), gene_name.capitalize(), consequence.capitalize())
                create_known_mutation_nodes(chrom="Chr1", pos=variant_pos, ref_allele=str(ref_allele),
                                            alt_allele=str(alt_allele), gene=gene_name,
                                            pk=str(vset_name) + str(variant_pos), consequence=consequence,
                                            vset_name=vset_name, vset_owner=vset_owner, cset_name=cset_name,
                                            drugbank_id=drugbank_id, drug_name=drug_name)

    elif in_file and in_file.endswith(".xlsxw"):
        sys.stdout.write("\nAdding known mutations...")
        df = pandas.read_excel(in_file, sheetname='resistance').fillna("")
        values = df.values
        vset_owner = "Manson et al"
        vset_name = "doi.org/10.1038/ng.3767"
        cset_name = str(in_file).split('/')[-1]
        for mutation in values:
            drug_res_to = mutation[0]
            variant_pos = mutation[1].split(":")[0]
            loc_in_seq = mutation[4]
            ref_allele = mutation[1].split(":")[1].split("->")[0]
            alt_allele = mutation[1].split(":")[1].split("->")[1]
            gene_name = mutation[2]
            # amino acid change
            consequence = mutation[4]
            print(drug_res_to.capitalize(), gene_name.capitalize(), consequence.capitalize())
            create_known_mutation_nodes(chrom="Chr1", pos=variant_pos, ref_allele=str(ref_allele),
                                        alt_allele=str(alt_allele), loc_in_seq=str(loc_in_seq),
                                        gene=gene_name, pk=str(vset_name) + str(variant_pos),
                                        consequence=consequence, vset_name=vset_name, vset_owner=vset_owner,
                                        cset_name=cset_name)

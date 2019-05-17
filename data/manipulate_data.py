import pandas as pd


def get_bigg_to_kegg_map(file_in: str, file_out: str, kegg_ids_to_remove: list):
    """
    Given a chem_xref.tsv file from MetaNetX, which contains metabolite identifiers in multiple databases, take
    all bigg ids and kegg ids and match them based on the common MetaNetX_id.
    Write the resulting map bigg to kegg ids into file_out as a .csv.

    Args:
        file_in (str): path chem_xref.tsv file from MetaNetX.

    Returns:
        None
    """

    met_data_df = pd.read_csv(file_in, sep='\t', comment='#', header=None)
    col_names = ['id', 'metanetx_id', 'evidence', 'name']
    met_data_df.columns = col_names

    bigg_data_df = met_data_df[met_data_df['id'].str.match('bigg:[^M]')]
    bigg_data_df['id'].replace(regex='bigg:', value='', inplace=True)
    bigg_data_df = bigg_data_df[['id', 'metanetx_id', 'name']]

    kegg_data_df = met_data_df[met_data_df['id'].str.match('kegg:C[^M]')]
    kegg_data_df = kegg_data_df[['id', 'metanetx_id', 'name']]
    kegg_data_df['id'].replace(regex='kegg:', value='', inplace=True)
    kegg_data_df = kegg_data_df[~kegg_data_df['id'].isin(kegg_ids_to_remove)]

    joined_met_data_df = bigg_data_df.join(kegg_data_df.set_index('metanetx_id'), rsuffix='_kegg', how='left',
                                           on='metanetx_id')

    joined_met_data_df.to_csv(file_out, index=False)


def remove_entries(file_in, entries_to_remove):
    return 0


file_in = 'chem_xref.tsv'  # MNXref Version 2018/09/14
file_out = 'map_bigg_to_kegg_ids.csv'
kegg_ids_to_remove = ['C01328', 'C00661']

get_bigg_to_kegg_map(file_in, file_out, kegg_ids_to_remove)
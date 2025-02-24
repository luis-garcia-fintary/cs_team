import pandas as pd
import ast
import sys

def main(file_path, file_path_output_life, file_path_output_non_life):

    def split_dataframe(df: pd.DataFrame):
        def is_dict_string(value):
            try:
                return isinstance(ast.literal_eval(value), dict)
            except (ValueError, SyntaxError):
                return False
        
        def convert_to_dict(value):
            try:
                return ast.literal_eval(value) if is_dict_string(value) else value
            except (ValueError, SyntaxError):
                return value
        
        df['Agent commissions'] = df['Agent commissions'].apply(convert_to_dict)
        df_dict = df[df['Agent commissions'].apply(lambda x: isinstance(x, dict))].reset_index(drop=True)
        df_other = df[~df['Agent commissions'].apply(lambda x: isinstance(x, dict))].reset_index(drop=True)
        
        return df_dict, df_other

    def df_dict_flat(df):
        df_output = pd.DataFrame(columns=df.columns)
        for i in range(len(df)):
            for key,value in df['Agent commissions'][i].items():
                if key != 'total':
                    df_output = pd.concat([df_output, df.loc[[i]]], ignore_index=True)
                    max_len_df_output = len(df_output)-1
                    df_output['Premium amount'][max_len_df_output] = 0
                    df_output['Commission amount'][max_len_df_output] = 0
                    df_output['Notes'][max_len_df_output] = 'Personal'
                    df_output['Agents'][max_len_df_output] = key
                    df_output['Agent commissions'][max_len_df_output] = value
                    if key in df['Agent commission payout rate'][i]:
                        df_output['Agent commission payout rate'][max_len_df_output] = ast.literal_eval(df['Agent commission payout rate'][i])[key]
                    if key in df['Agent commissions log'][i]:
                        df_output['Agent commissions log'][max_len_df_output] = ast.literal_eval(df['Agent commissions log'][i])[key]
        return df_output

    def df_joiner(df1, df2):
        return pd.concat([df1, df2], ignore_index=True)

    def summary_by_policy_type(df):
        df[['Premium amount', 'Commission amount', 'Agent commissions']] = df[
            ['Premium amount', 'Commission amount', 'Agent commissions']].apply(pd.to_numeric, errors='coerce')

        df_aggregated = df.groupby(['Agents', 'Notes'], as_index=False)[
        ['Premium amount', 'Commission amount', 'Agent commissions']].sum()
        return df_aggregated

    def summary_by_carrier(df):
        df[['Premium amount', 'Commission amount']] = df[
            ['Premium amount', 'Commission amount']].apply(pd.to_numeric, errors='coerce')

        df_aggregated = df.groupby(['Carrier/MGA'], as_index=False)[
        ['Premium amount', 'Commission amount']].sum()
        return df_aggregated

    # Life products
    df = pd.read_csv(file_path).fillna('')
    df = df[df['Product type'].isin(['Life', 'Life*'])]

    df_dict, df_no_dict = split_dataframe(df)

    df_new = df_joiner(df_no_dict, df_dict_flat(df_dict))
    df_policy_type = summary_by_policy_type(df_new)
    df_carrier = summary_by_carrier(df_new)

    with pd.ExcelWriter(file_path_output_life, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='raw_original', index=False)
        df_new.to_excel(writer, sheet_name='raw_transformed', index=False)
        df_policy_type.to_excel(writer, sheet_name='summary_by_policy_type', index=False)
        df_carrier.to_excel(writer, sheet_name='summary_by_carrier', index=False)


    # Non-Life products
    df = pd.read_csv(file_path).fillna('')
    df = df[~df['Product type'].isin(['Life', 'Life*'])]

    df_dict, df_no_dict = split_dataframe(df)

    df_new = df_joiner(df_no_dict, df_dict_flat(df_dict))
    df_policy_type = summary_by_policy_type(df_new)
    df_carrier = summary_by_carrier(df_new)

    with pd.ExcelWriter(file_path_output_non_life, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='raw_original', index=False)
        df_new.to_excel(writer, sheet_name='raw_transformed', index=False)
        df_policy_type.to_excel(writer, sheet_name='summary_by_policy_type', index=False)
        df_carrier.to_excel(writer, sheet_name='summary_by_carrier', index=False)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python trailstone_xlsx_summaries.py <input_csv> <output_life> <output_non_life>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
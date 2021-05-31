import pandas as pd

filename = r'C:\Users\eduar\OneDrive\Área de Trabalho\Antoine\assets\antoine_list_df.csv'
df = pd.read_csv(filename, index_col=0)
c_name = 'Argon'
compound_formula = 'H2O'

c_name = c_name.lower()
data = df.loc[df['Composto'] == c_name]

formula = data['Formula'].values[0]
print((formula))
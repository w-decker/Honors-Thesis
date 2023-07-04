# import pandas
import pandas as pd

# load in list
df = pd.read_csv('structured_orders.csv', delimiter=',')
order1 = list(df['Order 1'])
order2 = list(df['Order 2'])

# generate emperical TPM
eTPM = pd.crosstab(pd.Series(order1[:-1]), pd.Series(order1[1:]), normalize=True, dropna=False) # just checks order1

# Reindex columns and rows to include all syllables
eTPM = eTPM.reindex(order1, columns=order1, fill_value=0.0)

print(eTPM)

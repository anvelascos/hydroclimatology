import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def dividir_variables():
    xls_data = pd.ExcelFile('hc_data.xlsx')
    nombres_vars = xls_data.sheet_names

    for nombre_var in nombres_vars:
        print(nombre_var)
        nombre_salida = nombre_var + '_data.xlsx'
        df_datos_var = xls_data.parse(nombre_var, index_col='Fecha')
        df_datos_var.to_excel(nombre_salida, nombre_var)


xls_ts1 = pd.ExcelFile('TS_1_data.xlsx')
df_ts1 = xls_ts1.parse('TS_1', index_col='Fecha')
print(df_ts1.shape)

xls_catalogo = pd.ExcelFile('Catalogo_G2.xlsx')
df_estaciones_ts = xls_catalogo.parse('TS_1', index_col='Estacion')

mis_estaciones = df_estaciones_ts.index
df_ts1_g2 = df_ts1[mis_estaciones]
print(df_ts1_g2.shape)
nom_archivo_ts = 'TS_1_data_G2.xlsx'
# df_ts1_g2.to_excel(nom_archivo_ts, 'TS_1')  # exportar a excel

meses = range(1, 13)
df_prom_lp = pd.DataFrame(index=meses, columns=mis_estaciones)
# print(df_prom_lp)

for mes in meses:
    df_ts1_mes = df_ts1_g2[df_ts1_g2.index.month == mes]
    df_prom_lp.loc[mes] = df_ts1_mes.mean()


for mes in meses:
    print("\nMes: " + str(mes))
    df_tmp_reg = df_estaciones_ts.copy()
    df_tmp_reg[mes] = df_prom_lp.loc[mes]
    print(df_tmp_reg.shape)
    df_tmp_reg.dropna(axis=0, how='any', inplace=True)
    # df_tmp_reg.drop(54025010, axis=0)
    print(df_tmp_reg.shape)
    # plt.scatter(df_tmp_reg['Elevacion'], df_tmp_reg[mes])
    # nombre_figura = 'figs/Regresion_' + str(mes)
    # plt.savefig(nombre_figura)

    reg_results = stats.linregress(df_tmp_reg['Elevacion'], df_tmp_reg[mes])
    alpha = reg_results[0]
    beta = reg_results[1]
    corr = reg_results[2]
    r2 = corr ** 2
    print("\nDatos de la regresion\nalpha = " + str(alpha) + '\nbeta = ' + str(beta) + '\nCorr = ' +
          str(corr) + '\nR2 = ' + str(r2))


    # plt.show()
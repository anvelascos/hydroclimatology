import pandas as pd
from scipy import stats


def serieagrupos(sr_entrada):
    df_entrada = pd.DataFrame(sr_entrada)
    df_entrada['Year'] = df_entrada.index.year
    df_entrada['Mes'] = df_entrada.index.month
    gm_salida = df_entrada.pivot(index='Year', columns='Mes')

    return gm_salida


def gruposaserie(gm_entrada):
    sr_entrada = gm_entrada.unstack()
    df_confecha = sr_entrada.reset_index()
    df_confecha['Fecha_str'] = df_confecha['Year'].astype(str) + '-' + df_confecha['Mes'].astype(str) + '-01'
    df_confecha['Fecha'] = pd.to_datetime(df_confecha['Fecha_str'])
    df_confecha.set_index(df_confecha['Fecha'], inplace=True)

    return df_confecha[0]




def pruebaanomalos(df_input, alpha=0.05, two_tail=True):
    """
    This function applies the Grubbs' Test for outliers in a dataframe and returns two dataframes, the first one
    without outliers and the second one just for the outliers
    :param df_input: Pandas dataframe with series to test.
    :param alpha: Significance level [5% as default].
    :param two_tail: Two tailed distribution [True as default].
    :return: tuple with two dataframes, the first one without outliers and the second one just for outliers.
    """
    df_try = df_input.copy()
    df_output = pd.DataFrame(index=df_input.index, columns=df_input.columns)
    df_outliers = pd.DataFrame(data=0, index=df_input.index, columns=df_input.columns)

    if two_tail:
        alpha /= 2

    while not df_outliers.isnull().values.all():
        mean = df_try.mean()
        std = df_try.std()
        n = len(df_try)
        tcrit = stats.t.ppf(1 - (alpha / (2 * n)), n - 2)
        zcrit = (n - 1) * tcrit / (n * (n - 2 + tcrit ** 2)) ** .5
        df_outliers = df_try.where(((df_try - mean) / std) > zcrit)
        df_output.update(df_input[df_outliers.isnull() == False])
        df_try = df_try[df_outliers.isnull()]

    return df_try, df_output


def calcular_faltantes():
    lista_variables = ['BS_4']  # , 'EV_4', 'HR_1', 'PT_4', 'QL_1', 'TS_1']

    xls_salida = pd.ExcelWriter('results/01_consistencia.xlsx')  # Archivo para guardar resultados

    for variable in lista_variables:
        print('Variable analizada: ' + variable)
        ruta_datos = '../data/' + variable + '_data.xlsx'
        xls_data = pd.ExcelFile(ruta_datos)  # Archivo de los datos de la variable
        df_variable = xls_data.parse(variable, index_col='Fecha')
        estaciones = df_variable.columns
        idx_resultados = pd.Index(estaciones, name='Estacion')
        col_resultados = ['Inicio', 'Fin', 'Longitud', 'Faltantes', 'Faltantes [%]', 'Cumple']
        df_resultados = pd.DataFrame(index=idx_resultados, columns=col_resultados)

        for estacion in estaciones:
            sr_estacion = df_variable[estacion]

            gm_estacion = serieagrupos(sr_estacion)
            gm_limpio, gm_anomalos = pruebaanomalos(gm_estacion)
            sr_limpio = gruposaserie(gm_limpio)

            sr_sin_vacios = sr_limpio.dropna()
            fecha_inicio = sr_sin_vacios.index.min()
            fecha_final = sr_sin_vacios.index.max()
            datos_existentes = len(sr_sin_vacios)
            idx_completo = pd.date_range(start=fecha_inicio, end=fecha_final, freq='MS')
            datos_totales = len(idx_completo)
            faltantes = datos_totales - datos_existentes
            faltantes_por = 100 * float(faltantes) / datos_totales
            cumple = datos_totales > 360 and faltantes_por < 30

            df_resultados.loc[estacion, 'Inicio'] = fecha_inicio
            df_resultados.loc[estacion, 'Fin'] = fecha_final
            df_resultados.loc[estacion, 'Longitud'] = datos_totales
            df_resultados.loc[estacion, 'Faltantes'] = faltantes
            df_resultados.loc[estacion, 'Faltantes [%]'] = faltantes_por
            df_resultados.loc[estacion, 'Cumple'] = cumple

            print('\nEstacion: ' + str(estacion))
            print('Incio: ' + str(fecha_inicio))
            print('Fin: ' + str(fecha_final))
            print('Longitud: ' + str(datos_totales))
            print('Faltantes: ' + str(faltantes) + ' (' + str(round(faltantes_por, 2)) + '%)')

        df_resultados.to_excel(xls_salida, variable)

    xls_salida.save()


calcular_faltantes()

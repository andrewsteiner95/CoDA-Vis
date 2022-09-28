def xrf_element_map_panel_maker(xrf_df,
                                xrf_file,
                                header_columns=2,
                                scale=2,
                                scale_type='symlog',
                                colour_ramp='magma'):

    # Import required packages
    import altair as alt
    import pandas as pd

    # Disable max rows on Altair
    alt.data_transformers.disable_max_rows()

    # Create an empty list
    map_list = []

    element_names = xrf_df.columns.values.tolist()
    del element_names[:header_columns]

    # Loop that builds a heatmap for each element in the column_names list (defined during data import above).
    for element in element_names:
        element_map = alt.Chart(xrf_df,
                                width=((len(pd.read_csv(xrf_file, delimiter=';', header=None).columns)) * scale),
                                height=((len(pd.read_csv(xrf_file, delimiter=';', header=None).index)) * scale)
                                ).mark_rect().encode(
            x=alt.X('x:O', axis=alt.Axis(labels=False, tickSize=0, title="")),
            y=alt.Y('y:O', axis=alt.Axis(labels=False, tickSize=0, title="")),
            color=alt.Color(element, title=element + " (wt. %)", scale=alt.Scale(type=scale_type, scheme=colour_ramp)),
            tooltip=alt.Tooltip(element_names)
        )
        map_list.append(element_map)

    # Vertically concatenates each plot. To concatenate horizontally, use alt.hconcat
    panel = alt.vconcat(*map_list).resolve_scale(color='independent')

    return panel


def xrf_rgb_map_maker(xrf_df,
                      xrf_file,
                      element_1,
                      element_2,
                      element_3,
                      header_columns=2,
                      scale=2,
                      threshold_1=0.05,
                      threshold_2=0.05,
                      threshold_3=0.05,
                      colour_1='red',
                      colour_2='green',
                      colour_3='blue',
                      opacity_1=1,
                      opacity_2=0.7,
                      opacity_3=0.3):

    # Import required packages
    import altair as alt
    import pandas as pd

    # Disable max rows on Altair
    alt.data_transformers.disable_max_rows()

    element_names = xrf_df.columns.values.tolist()
    del element_names[:header_columns]

    element_dict = {element_1: [threshold_1, colour_1, opacity_1],
                    element_2: [threshold_2, colour_2, opacity_2],
                    element_3: [threshold_3, colour_3, opacity_3]}

    map_list = []

    for element, variables in element_dict.items():

        element_max = xrf_df[element].max()
        mask = variables[0]
        opacity_max = variables[2]

        colour_map = alt.Chart(xrf_df,
                               width=((len(pd.read_csv(xrf_file, delimiter=';', header=None).columns)) * scale),
                               height=((len(pd.read_csv(xrf_file, delimiter=';', header=None).index)) * scale)
                               ).mark_rect(color=(variables[1])).encode(
            x=alt.X('x:O', axis=alt.Axis(labels=False, tickSize=0, title="")),
            y=alt.Y('y:O', axis=alt.Axis(labels=False, tickSize=0, title="")),
            opacity=alt.Opacity(element,
                                title=element + " (wt. %)",
                                scale=alt.Scale(type='symlog',
                                                domain=[0, mask, element_max],
                                                range=[0, 0, opacity_max]
                                                )
                                ),
            tooltip=alt.Tooltip(element_names)
        )

        map_list.append(colour_map)

    rgb_map = alt.layer(*map_list).resolve_scale(opacity='independent')

    return rgb_map


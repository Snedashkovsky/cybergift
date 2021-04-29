import pandas as pd
from IPython.core.display import display, HTML
from math import log10
import matplotlib.pyplot as plt
import matplotlib as mpl


def calculate_and_display_rules(
        distribution_df: pd.DataFrame,
        initial_boundary: float,
        percentage_levels: tuple,
        value_column: str,
        value_name: str,
        address_column: str):
    """
    Calculate rule boundaries in according with percentage levels
    :param distribution_df: Source DataFrame
    :param initial_boundary: Minimum value of analyzed parameter that should be included in analysis
    :param percentage_levels: Cumulative sum boundaries by addresses share
    :param value_column: Column name of analyzed parameter
    :param value_name: Name of analyzed parameter for inserting in the rules
    :param address_column: Column name of addresses number
    :return: Rule Boundaries
    """

    distribution_slice_df = distribution_df[distribution_df[value_column] > initial_boundary].copy()

    total_addresses = distribution_slice_df[address_column].sum()

    address_cumsum_perc_column = address_column + '_cumsum_percentage'
    distribution_slice_df.loc[:, address_cumsum_perc_column] = \
        distribution_slice_df[address_column].cumsum() / total_addresses
    # Calculate of rule boundaries
    boundaries = [initial_boundary]
    for percentage_level in percentage_levels:
        boundary = distribution_slice_df.iloc[
            distribution_slice_df[address_cumsum_perc_column].map(
                lambda x: abs(x - percentage_level)).argmin()][value_column]
        boundaries.append(round(boundary))
    # Calculate of address number by suggested grades
    addresses_by_grade = [distribution_slice_df[
                              (distribution_slice_df[value_column] > boundaries[0]) & (
                               distribution_slice_df[value_column] <= boundaries[1])][address_column].sum(),
                          distribution_slice_df[
                              (distribution_slice_df[value_column] > boundaries[1]) & (
                               distribution_slice_df[value_column] <= boundaries[2])][address_column].sum(),
                          distribution_slice_df[
                              distribution_slice_df[value_column] > boundaries[2]][address_column].sum()]
    # Rules for displaying
    rules = [f'{boundaries[0]} < {value_name} <= {boundaries[1]}',
             f'{boundaries[1]} < {value_name} <= {boundaries[2]}',
             f'{boundaries[2]} < {value_name}']
    df_data = [[i + 1,
                rule,
                addresses_by_grade[i],
                round(addresses_by_grade[i] / total_addresses * 100, 1)]
               for i, rule in enumerate(rules)]

    print(f'Suggestion of Rules: \n')
    display(
        HTML(
            pd.DataFrame(df_data,
                         columns=['Grade', 'Rule', 'Addresses', 'Percentage of Addresses'])
                .to_html(index=False, notebook=True, show_dimensions=False)))
    return boundaries


def show_distribution_chart(
        distribution_df: pd.DataFrame,
        boundaries: list,
        level_line_shift: float,
        max_show_value: float,
        value_column: str,
        value_chart_label: str,
        value_transform_func,
        address_column: str,
        address_chart_label: str,
        address_transform_func,
        chart_title: str):
    """
    Show chart with value distribution by addresses and boundaries
    :param distribution_df: Source DataFrame
    :param boundaries: Rule Boundaries
    :param level_line_shift: Shift for correct display of grade boundaries
    :param max_show_value: Maximum value of analyzed parameter that should be shown
    :param value_column: Column name of analyzed parameter
    :param value_chart_label: Value label for chart
    :param value_transform_func: Transformation function for analyzed parameter column
    :param address_column: Column name of number of addresses
    :param address_chart_label: Addresses number label for the chart
    :param address_transform_func: Transformation function for number of addresses column
    :param chart_title: Chart Title
    :return: None
    """

    address_transform_column = address_column + '_transform'
    value_transform_column = value_column + '_transform'
    distribution_df.loc[:, address_transform_column] = distribution_df[address_column].map(address_transform_func)
    distribution_df.loc[:, value_transform_column] = distribution_df[value_column].map(value_transform_func)

    mpl.rcParams['figure.figsize'] = (20.0, 9.0)
    fig, ax = plt.subplots()
    # Grade Boundaries vertical lines
    for boundary in boundaries:
        ax.axvline(address_transform_func(boundary + level_line_shift), 0, 0.9,
                   label='Grade Boundaries', color='red')
    # Distribution bar chart
    ax.plot(distribution_df[distribution_df[value_column] < max_show_value][value_transform_column],
            distribution_df[distribution_df[value_column] < max_show_value][address_transform_column],
            color='blue', marker='o', linestyle='dashed', linewidth=1, markersize=4)

    ax.set_ylabel(address_chart_label, fontsize=16)
    ax.set_xlabel(value_chart_label, fontsize=16)
    ax.set_title(chart_title, fontsize=18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["bottom"].set_position(("data", -0.25))

    plt.show()


def grade_boundaries_analysis(
        distribution_df: pd.DataFrame,
        chart_title: str,
        value_column: str,
        value_name: str,
        value_chart_label: str,
        value_transform_func=lambda x: log10(x) if x > 1 else 0.1,
        address_column: str = 'number_of_addresses',
        address_chart_label: str = 'Number of addresses, Log10',
        address_transform_func=lambda x: log10(x) if x > 1 else 0.1,
        percentage_levels: tuple = (0.89, 0.97),
        max_show_value: float = 200,
        level_line_shift: float = 0.5,
        initial_boundary: float = 0.0):
    """
    Calculate rule boundaries in according with percentage levels and display distribution
    :param distribution_df: Source DataFrame
    :param chart_title: Chart title
    :param value_column: Column name of analyzed parameter
    :param value_name: Name of analyzed parameter for inserting in the rules
    :param value_chart_label: Name of analyzed parameter for the chart
    :param value_transform_func: Transformation function for analyzed parameter column
    :param address_column: Column name of addresses number
    :param address_chart_label: Addresses number label for the chart
    :param address_transform_func: Transformation function for number of addresses column
    :param percentage_levels: Cumulative sum boundaries by addresses share
    :param max_show_value:  Maximum value of analyzed parameter that should be shown
    :param level_line_shift: Shift for correct display of grade boundaries
    :param initial_boundary: Minimum value of analyzed parameter that should be included in analysis
    :return: Rule boundaries
    """

    # Prepare DataFrame
    distribution_df = distribution_df.sort_values([value_column]).reset_index()

    boundaries = calculate_and_display_rules(
        distribution_df=distribution_df,
        initial_boundary=initial_boundary,
        percentage_levels=percentage_levels,
        value_column=value_column,
        value_name=value_name,
        address_column=address_column)

    show_distribution_chart(
        distribution_df=distribution_df,
        boundaries=boundaries,
        level_line_shift=level_line_shift,
        max_show_value=max_show_value,
        value_column=value_column,
        value_chart_label=value_chart_label,
        value_transform_func=value_transform_func,
        address_column=address_column,
        address_chart_label=address_chart_label,
        address_transform_func=address_transform_func,
        chart_title=chart_title)

    return boundaries

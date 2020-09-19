"""
Created by: Philip P
Created on: 23 May 2020
Exploratory data analysis into csv downloaded from habitdash.com

# TODO: clean up this and sort out the plotting framework for charts,
# TODO: try to fit a function for modelling strain using some AI to minimise the errors
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pd.set_option("display.max_columns", 10)
pd.set_option("display.width", 600)


def clean_input_data(input_data: pd.DataFrame,
                     is_flat_file: bool = True) -> pd.DataFrame:
    """Method to clean input Whoop dataframe from HabitDash.com

    Args:
        input_data: Input csv titled "YYYY-MM-DD Habit Dash (flat file).csv", sourced from
        habitdash.com and exported as ZIP file containing the aforementioned csv
        is_flat_file: If False, use the DataFrame from the habitdash.com API

    Returns:
        pd.DataFrame: Cleaned data with columns ['date', 'field', 'value']
    """
    if is_flat_file:
        assert 'date' in input_data.columns, "Input data does not have a valid 'date' column"

        print(f"Reading input data, {input_data['date'].nunique()} "
              f"days worth of data...")

        # rename the field column
        new_field_name_map = {k: k.replace("whoop_", "") for k in input_data['field'].unique()}

        input_data['field'] = input_data['field'].map(new_field_name_map)
        input_data.drop('source', axis=1, inplace=True)
        input_data['date'] = pd.to_datetime(input_data['date'])
    else:
        print("Haven't yet configured cleaning WHOOP data from habitdash.com API...")

    return input_data


if __name__ == "__main__":
    # -----------------
    # READ & CLEAN DATA
    # -----------------
    data_dir = "/Users/philip_p/Documents/whoop/"

    habit_dash_df = pd.read_csv(f"{data_dir}/2020-06-12 Habit Dash (flat file).csv")
    cleaned_df = clean_input_data(input_data=habit_dash_df)
    cleaned_df['date'].min()

    # exploratory data analysis at the file
    # cleaned_df['field'].nunique()  # 31 measures
    # macro_fields = {x.split("_")[0] for x in cleaned_df['field'].unique()}

    recovery_metrics_df = cleaned_df.loc[cleaned_df['field'].isin(
        ['recovery_score', 'recovery_rhr', 'recovery_hrv', 'sleep_score_total'])]

    recovery_metrics_pivoted = pd.pivot(
        data=recovery_metrics_df,
        index='date',
        columns='field'
    )
    recovery_metrics_pivoted.columns = list(recovery_metrics_pivoted.columns.get_level_values(1))
    recovery_metrics_pivoted['status'] = pd.cut(x=recovery_metrics_pivoted['recovery_score'],
                                                bins=[0, 33, 67, 100],
                                                labels=['red', 'yellow', 'green'])

    # --------
    # PLOTTING
    # --------

    # recovery score (response) v HRV (independent)
    hrv_ax = sns.scatterplot(
        x='recovery_hrv',
        y='recovery_score',
        data=recovery_metrics_pivoted,
        hue='status',
        palette=['red', 'orange', 'green']
    )
    hrv_ax.set_title("WHOOP Correlation: HRV v Recovery Score")
    # plt.savefig(os.path.join(os.getcwd(), 'images', 'hrv_recovery_scatterplot.png'))

    # recovery score (response) v Resting Heart Rate (independent)
    rhr_ax = sns.scatterplot(
        x='recovery_rhr',
        y='recovery_score',
        data=recovery_metrics_pivoted,
        hue='status',
        palette=['red', 'orange', 'green']
    )
    rhr_ax.set_title("WHOOP Correlation: RHR v Recovery Score")
    # plt.savefig(os.path.join(os.getcwd(), 'images', 'recovery_rhr_scatterplot.png'))

    # recovery score (response) v sleep score (independent)
    sleep_ax = sns.scatterplot(
        x='sleep_score_total',
        y='recovery_score',
        data=recovery_metrics_pivoted,
        hue='status',
        palette=['red', 'orange', 'green']
    )
    sleep_ax.set_title("WHOOP Correlation: Sleep Score v Recovery Score")
    # plt.savefig(os.path.join(os.getcwd(), 'images', 'recovery_sleep score_scatterplot.png'))

    # -------------
    # ROUGH IDEA OF LOOKING AT PCA - principal component analysis
    # -------------
    # recovery (for next day) is response variable, inputs are HRV, sleep score, RHR

    from sklearn.preprocessing import StandardScaler

    features = ['recovery_hrv', 'recovery_rhr', 'sleep_score_total']
    x = recovery_metrics_pivoted.loc[:, features].values
    y = recovery_metrics_pivoted.loc[:, 'recovery_score'].values

    x = StandardScaler().fit_transform(x)

    from sklearn.decomposition import PCA

    pca = PCA(n_components=2)  # fit to two main principal components

    principal_components = pca.fit_transform(x)
    principal_df = pd.DataFrame(
        data=principal_components,
        columns=['pc_one', 'pc_two']
    )

    final_df = pd.concat([principal_df, recovery_metrics_pivoted['recovery_score']], axis=1)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title('2 component PCA', fontsize=20)

    targets = ['']

    # look at correlation between HRV, sleep performance and RHR and Recovery score
    from scipy.stats import spearmanr, pearsonr

    hrv_corr, _ = spearmanr(recovery_metrics_pivoted['recovery_hrv'],
                            recovery_metrics_pivoted['recovery_score'])
    hrv_corr_pearson, _ = pearsonr(recovery_metrics_pivoted['recovery_hrv'],
                                   recovery_metrics_pivoted['recovery_score'])
    rhr_corr, _ = spearmanr(recovery_metrics_pivoted['recovery_rhr'],
                            recovery_metrics_pivoted['recovery_score'])
    sleep_performance_corr, _ = spearmanr(recovery_metrics_pivoted['sleep_score_total'],
                                          recovery_metrics_pivoted['recovery_score'])

    pca_df_detailed = recovery_metrics_pivoted.copy(True)
    pca_df_detailed['status'] = pd.cut(x=pca_df_detailed['recovery_score'],
                                       bins=[0, 33, 67, 100],
                                       labels=['red', 'yellow', 'green'])
    recovery_metrics_pivoted.corr()


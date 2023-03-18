import json
import matplotlib as mpl
import pandas as pd
from boto3 import Session
import converter as ct
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
import numpy as np


def connect():
    """
    Connect to a pre-configured aws profile.
    See documentation for profile set-up and requirements.
    Returns a session object.
    """
    session = Session(profile_name="connector")
    s3_resource = session.resource('s3')

    # test connection
    try:
        print('S3 buckets:')
        for bucket in s3_resource.buckets.all():
            print(bucket.name)
    except Exception as e:
        print(e)

    ce = session.client('ce')

    return ce


def get_usage(ce, start, end):
    """
    Get cost and usage data for the desired timeframe (max 6 months).
    Unblended cost and usage data is aggregated by month.
    Takes a boto session object and timeframe start and end dates
    (as strings) for parameters.
    Returns the usage data in json format.
    """
    TimePeriod = {'Start': start, 'End': end}

    # get bucket cost and usage data
    costs = ce.get_cost_and_usage(
        TimePeriod=TimePeriod,
        Granularity='MONTHLY',
        Metrics=['UNBLENDED_COST', "USAGE_QUANTITY"],
        Filter={
            'Dimensions': {
                "Key": "SERVICE",
                "Values": ['S3']
            }
        }
    )
    return costs


def json_2_csv(js):
    """
    Takes a json object containing the cost and usage output and saves it as a csv.
    Returns the flattened data in tabular format as a dataframe.
    """

    # save cost and usage data as a csv
    json_string = json.dumps(js, indent=2)
    with open("usage.json", "w") as outfile:
        outfile.write(json_string)

    # call the converter module to flatten the json output into a dataframe
    df = ct.json_to_dataframe(js)
    # export results to a csv
    df.to_csv(r"usage.csv", encoding='utf-8', index=False)

    return df


def plot_results(df):
    """
    Visualize S3 bucket cost trends over time. Takes a dataframe of the usage data as a parameter.
    """
    demo = df
    # convert date strings to date data type
    demo['ResultsByTime.TimePeriod.Start'] = pd.to_datetime(demo['ResultsByTime.TimePeriod.Start'])

    # make sure the most recent month is first
    sdf = demo.sort_values(by=['ResultsByTime.TimePeriod.Start'], ascending=False).reset_index(drop=True)

    # # x axis will be date and y will be cost
    x = sdf['ResultsByTime.TimePeriod.Start']
    y = sdf['ResultsByTime.Total.UnblendedCost.Amount']
    cur = sdf['ResultsByTime.Total.UnblendedCost.Unit'][1]

    # plot
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(8, 6))

    # format dates
    month_locator = mdates.MonthLocator(interval=1)
    year_month_formatter = mdates.DateFormatter("%Y-%m")
    ax.xaxis.set_major_locator(month_locator)
    ax.xaxis.set_major_formatter(year_month_formatter)

    # add axis labels and a title
    plt.xlabel('Month', fontsize=15)
    plt.ylabel('Usage Cost (' + cur + ')', fontsize=15)
    plt.title(' Monthly S3 Cost ', fontsize=20, loc='center', pad=20)

    ax.plot(x, y)
    fig.autofmt_xdate()
    plt.savefig("useage.jpg")


def eval(df):
    """
    Report on trends and make some predictions based on historic use.
    Takes a dataframe of the cost explorer data as a parameter.
    """
    demo = df
    # convert date strings to date data type
    demo['ResultsByTime.TimePeriod.Start'] = pd.to_datetime(demo['ResultsByTime.TimePeriod.Start'])

    # make sure the most recent month is first
    sdf = demo.sort_values(by=['ResultsByTime.TimePeriod.Start'], ascending=False).reset_index(drop=True)
    m1 = sdf['ResultsByTime.Total.UnblendedCost.Amount'][1]
    m2 = sdf['ResultsByTime.Total.UnblendedCost.Amount'][2]

    if m2 > m1:
        sign = '(-)'
    else:
        sign = '(+)'

    # print some summary metrics/ recent data
    print('The total unblended cost for last month was $' + str(m1) + '.')
    print('This represents a change of ' + sign + ' $' + str(round(m1 - m2, 2)) + ' from the previous month.\n')

    x = demo['ResultsByTime.TimePeriod.Start']
    y = demo['ResultsByTime.Total.UnblendedCost.Amount']
    xy = {'Month': x, 'Cost': y}
    dfxy = pd.DataFrame(xy).dropna()
    dfxy['Time'] = np.arange(len(dfxy.index))

    # Training data
    X_ = dfxy.loc[:, ['Time']]  # features
    Y_ = dfxy.loc[:, 'Cost']  # target

    # Predict the cost for next month
    model = LinearRegression(fit_intercept=False)
    model.fit(X_, Y_)
    x_next = X_ + 1
    y_new = model.predict(x_next)
    next_mo = y_new[-1]

    # Get the overall trend
    if y_new[-1] > y_new[-2]:
        trend = 'rising.'
    elif y_new[-1] < y_new[-2]:
        trend = 'declining.'
    else:
        trend = 'steady.'

    print('S3 costs have been ' + trend)
    print('If current trends continue, the cost for next month will be approximately $' + str(round(next_mo)) + '.')


def demo_only():
    """
    Runs the evaluation and visualization components with sample data.
    No AWS account or connector is required to test this functionality.
    """
    print('Using the sample data set to demonstrate reporting and visualization of S3 bucket usage.')
    demo = pd.read_csv('example_data.csv')
    plot_results(demo)
    eval(demo)


def main():
    first = '2022-07-01'
    last = '2023-01-01'
    conn = connect()
    jsn = get_usage(conn, first, last)
    results = json_2_csv(jsn)
    plot_results(results)
    eval(results)


demo_only()
#main()

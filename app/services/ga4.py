from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest


PROPERTY_ID = "527487985"


def get_hpb_clicks():

    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[{"name": "sessionSourceMedium"}],
        metrics=[{"name": "sessions"}],
        date_ranges=[{"start_date": "today", "end_date": "today"}],
    )

    response = client.run_report(request)

    for row in response.rows:

        if "google / organic" in row.dimension_values[0].value:
            return int(row.metric_values[0].value)

    return 0
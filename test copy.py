import ga4_reporting as ga4
import pandas as pd
from config import (ga4_dim_banners,ga4_metr_banners,ga4_dim_ed_sign_up_users,ga4_metr_ed_sign_up_users,ga4_dim_ed_search,ga4_metr_ed_search,ga4_dim_funnel,ga4_metr_funnel)



# test_gf = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]], columns=["a","b","c"])
# respons =  test_gf.empty
# print()


# # response, response_rows_count, offset_int = test_object.ga4_run_report_request(100000,dimension_list=ga4_dim_ecom,metric_list=ga4_metr_ecom)
# # print(response)
# # test_object.ga4_response_to_df()
# # test_object.ga4_report_qouta_to_df()
# # test_object.ga4_overwriting_old_qouta_excel()
# # test_object.ga4_overwriting_old_exls_report()

# test_object = ga4.GA4Report("ga4_funnel2")
# test_object.at_start_date = "2023-02-01"
# test_object.at_end_date = "2023-02-28"
# test_object.at_ga4_dim_list = ga4_dim_funnel
# test_object.at_ga4_metr_list = ga4_metr_funnel
# test_object.at_offset = 0
# test_object.ga4_all_rows_to_df()




import re
import urllib.parse
df = pd.read_excel("C:/Users/User/Desktop/python/123.xlsx")
df.loc[(df["customEvent:session_number_event"] == "(not set)")|(df["customEvent:session_number_event"] == ""), "customEvent:session_number_event"] = 0
df = df.groupby(["date","eventName","browser","deviceCategory","sessionSourceMedium"]).agg({
"customEvent:user_id_event": "count",
"customEvent:client_id_event": "count",
"customEvent:session_id_event": "count",
"customEvent:session_number_event": "mean",
"eventCount" : "sum"
}).reset_index()
df.to_excel("ga4_funnel123.xlsx", index=False)
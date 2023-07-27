import ga4_reporting as ga4
import pandas as pd
import re
import urllib.parse
from config import (ga4_dim_ed_search,ga4_metr_ed_search)



# test_gf = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]], columns=["a","b","c"])
# respons =  test_gf.empty
# print()
test_object = ga4.GA4Report("ga4_ed_terms")

# # response, response_rows_count, offset_int = test_object.ga4_run_report_request(100000,dimension_list=ga4_dim_ecom,metric_list=ga4_metr_ecom)
# # print(response)
# # test_object.ga4_response_to_df()
# # test_object.ga4_report_qouta_to_df()
# # test_object.ga4_overwriting_old_qouta_excel()
# # test_object.ga4_overwriting_old_exls_report()

test_object.at_start_date = "2023-01-01"
test_object.at_end_date = "2023-02-23"
test_object.at_ga4_dim_list = ga4_dim_ed_search
test_object.at_ga4_metr_list = ga4_metr_ed_search
test_object.ga4_all_rows_to_df()

df = pd.read_excel("C:/Users/User/Desktop/python/ga4_ed_terms.xlsx")
urls = df["pagePathPlusQueryString"]
new_terms = []
for i in urls:
    i = urllib.parse.unquote(i)
    i = urllib.parse.unquote_plus(i)
    i = str(i).lower()
    i = re.findall("/.*query=(.*)", i)
    i = ''.join(i)
    new_terms.append(i)
print(new_terms[1:5])
df.insert(0, "terms", new_terms)
df.drop(["pagePathPlusQueryString"], axis=1, inplace=True)
df.groupby(["terms"]).sum()
df.to_excel("ga4_new_terms.xlsx",index=False)
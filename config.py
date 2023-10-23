sourcePatterns = {
    'Google': '^.*_google.*',
    'Fb/Inst': '^.*(_fb|_inst).*',
    'Mytarget': '^.*_mytarget.*',
    'Tiktok': '^.*_tiktok.*',
    'Vk': '^.*_vk.*',
    'Ok': '^.*_ok.*',
    'Yandex': '^.*_yandex.*',
    'Telegram': '^.*_telegram.*',
    'Twitter': '^.*_twitter.*'
}


DIM_KUFAR_REPORT = "ym:s:date,ym:s:<attribution>UTMSource,ym:s:<attribution>UTMCampaign,ym:s:<attribution>UTMMedium,ym:s:<attribution>UTMContent,ym:s:<attribution>UTMTerm,ym:s:purchaseID"
METR_KUFAR_REPORT = "ym:s:visits,ym:s:users,ym:s:ecommercePurchases,ym:s:ecommerce<currency>ConvertedRevenue"

DIM_EDADEAL_REPORT = "ym:s:<attribution>UTMCampaign"
METR_EDADEAL_REPORT = "ym:s:visits,ym:s:users,ym:s:ecommercePurchases,ym:s:ecommerce<currency>ConvertedRevenue"

DIM_CAMPAIGN_REPORT = "ym:s:date,ym:s:<attribution>UTMCampaign"
METR_CAMPAIGN_REPORT = "ym:s:visits,ym:s:users,ym:s:ecommercePurchases,ym:s:ecommerce<currency>ConvertedRevenue"



COAST_SHEET_ID = "1wJu2BI5SbtVJ64q3L3Fu0fUOe9JMU7D6-OxDYbTKhnQ"
COAST_SHEET_RANGE = "'Для рассчетов'!A1:J"
REPORT_SHEET_RANGE = "'Сведенный отчет'!A1:Z"


PLAN_CONFIG = {
    'PLAN_SHEET_ID' : '1_kqqoPJWbOd5hYlYm3cFeB5aKbS4e0SSvukWQGjCaKE',
    'PREVIOUS_MONTH' : {'SHEET_RANGE': "'Для выгрузки Сентябрь'!A1:G",
                        'START_DATE' : "2023-09-01",
                        'END_DATE' : "2023-09-30"},
    'CURRENT_MONTH' : {'SHEET_RANGE': "'Для выгрузки Октябрь'!A1:G",
                        'START_DATE' : "2023-10-01",
                        'END_DATE' : "2023-10-31"},
    'NEXT_MONTH' : {'SHEET_RANGE': "'Для выгрузки Ноябрь'!A1:G",
                        'START_DATE' : "2023-11-01",
                        'END_DATE' : "2023-11-30"},
}

FACT_SHEET_ID = "19ILZ3UQggDNJveiDoOy9ZRjLU6OM1TFlUiEilHCtbbM"

KUFAR_SHEET_ID = "1d8XewCdHB0BAdXx0ihWj1zt9BtJQqhotiEbzg_s4134"
KUFAR_SHEET_RANGE = "'Kufar auto report'!A1:L"


BANNER_SHEET_ID = "1LWKyoobAxqN5vtD-lICJvslmA1L9nO3syhm6gSzdr3s"
BANNER_SHEET_ED_RANGE = "'NEW ED'!A1:L"
BANNER_SHEET_EM_RANGE = "'NEW EM'!A1:L"
BANNER_REPORT_SHEET_RANGE = "'Для отчетов'!A1:P"

PAGE_VIEWS_SHEET_ID = "1tz061j_CvCzn3OKtBXN66ZBOGf3B5f4wrqxULq7YGSs"
PAGE_VIEWS_RANGE = "'ED_EM'!A1:H"


# "'Лист26'!A1:J"


# field_name = "eventName"
# filters_value = "purchase|refund"
# filters_value = "search|search_complete|search_complete_select|search_select|add_shipping_info|add_payment_info|add_to_cart|begin_checkout|purchase|refund|remove_from_cart|repeat_order|select_item|view_cart|view_item|view_item_list"
filters_value_funnel = "add_shipping_info|add_payment_info|add_to_cart|begin_checkout|purchase|refund|remove_from_cart|repeat_order|select_item|view_cart|view_item|view_item_list"
filters_value_transaction = "purchase"

# field_name = "sessionSourceMedium"
# filters_value = "(.*email.*)|(.*viber.*)"

field_name = "eventName"
filters_value = "search.*"

field_name1 = "itemPromotionId"
filters_value1 = "(.*productsluck.*)|(.*146.*)"

# field_name = "itemPromotionId"
# filters_value = ".*4952"

# default report parameters
ga4_dim_default = [
    # "eventName",
    "date",
    # "pagePath",
    # "unifiedPagePathScreen",
    # "fullPageUrl",
    # "pagePathPlusQueryString",
    # "landingPagePlusQueryString",
    # "itemListId",
    # "itemListName",
    # "customEvent:hit_timestamp",
    # "customEvent:session_id_event",
    # "customEvent:session_number_event",
    # "customEvent:client_id_event",
    # "customEvent:user_id_event",
]

ga4_metr_default = [
    # "itemsViewedInList",
    # "itemsClickedInList",
    # "itemsViewed",
    # "",
    # "eventCount",
    "screenPageViews",
    # "sessions",
    # "newUsers",
    # "totalUsers"
]

# for sign_up users report
ga4_dim_ed_sign_up_users = [
    # "date",
    # "customEvent:sign_up_date",
    # "eventName",
    # "browser",
    # "deviceCategory",
    # "sessionSource",
    # "sessionMedium",
    # "sessionCampaignName",
    "customEvent:user_id_event"
]

ga4_metr_ed_sign_up_users = ["eventCount", "totalPurchasers"]

# for banners report
ga4_dim_banners = [
    "date",
    "pagePath",
    # "itemId",
    # "itemName",
    "itemPromotionCreativeName",
    "itemPromotionId",
    # "itemVariant"
]

ga4_metr_banners = [
    # "eventCount",
    "itemsViewedInPromotion",
    "itemsClickedInPromotion"
]

# for ecommerce

ga4_dim_ecom = ["date", "itemId", "itemName", "itemBrand"]

ga4_metr_ecom = [
    "itemsViewed", "itemsAddedToCart", "itemsPurchased", "itemRevenue"
]

ga4_dim_ed_campaign = ["pagePath", "sessionCampaignName"]

ga4_metr_ed_campaign = ["screenPageViews", "sessions", "totalUsers"]

ga4_dim_ed_search = [
    "eventName",
    "customEvent:hit_timestamp",
    "customEvent:user_id_event",
    "customEvent:search_term",
    # "customEvent:ga_session_id_event",
    # "customEvent:ga_session_number_event",
    "customEvent:session_id_event",
    "customEvent:session_number_event",
    "customEvent:client_id_event",
]

ga4_metr_ed_search = [
    "eventCount",
    # "screenPageViews",
    # "sessions",
    # "totalUsers"
]

ga4_dim_List = [
    "itemListId",
    "itemListName",
    "itemId",
    # "itemName",
    # "browser",
    # "deviceCategory",

    # "customEvent:user_id_event",
    # "customEvent:session_id_event",
    # "customEvent:session_number_event",
    # "customEvent:client_id_event",
    # "customEvent:hit_timestamp",
    # "pagePath",
    # "customEvent:hit_timestamp",
    # "customEvent:user_id_event",
    # "customEvent:search_term",
    # "customEvent:session_id_event",
    # "customEvent:session_number_event",
    # "customEvent:client_id_event",
]

ga4_metr_List = [
    "itemsViewedInList",
    "itemsClickedInList",
    "itemsAddedToCart",
    "itemsPurchased",
    "itemRevenue",
    # "eventCount",

    # "",
    # "itemListViewEvents",
    # "itemListClickEvents"
    # "screenPageViews",
    # "sessions",
    # "totalUsers"
]

ga4_dim_funnel = [
    "date",
    "eventName",
    "browser",
    "deviceCategory",
    "sessionSourceMedium",
    "sessionCampaignName",
    "customEvent:user_id_event",
    "customEvent:client_id_event",
    # "customEvent:ga_session_id_event",
    # "customEvent:ga_session_number_event",
    "customEvent:session_id_event",
    # "customEvent:session_number_event",
]

ga4_metr_funnel = [
    "eventCount",
    "purchaseRevenue",
    # "itemListViewEvents",
    # "itemListClickEvents"
    # "screenPageViews",
    # "sessions",
    # "totalUsers"
]

# Для сверки транзакций
ga4_dim_transaction = [
    # "eventName",
    "date",
    # "transactionId",
    # "sessionSourceMedium",
    "sessionCampaignName"
]

ga4_metr_transaction = [
    # "eventCount",
    #
    "ecommercePurchases",
    #
    # "sessions",
    "transactions",
    "purchaseRevenue",
]

# Выгрузка для отчета по рассылкам
ga4_dim_transaction_email = [
    "date", "landingPagePlusQueryString", "sessionSourceMedium",
    "sessionCampaignName"
]

ga4_metr_transaction_email = [
    "screenPageViews",
    "sessions",
    "transactions",
    "ecommercePurchases",
    "purchaseRevenue",
]

# Запросы из рекламы
ga4_dim_sessionManualTerm = [
    "sessionSourceMedium",
    "sessionCampaignName",
    "sessionManualTerm",
]

ga4_metr_sessionManualTerm = [
    "sessions",
    "transactions",
    "purchaseRevenue",
]

# Запросы и сессии
ga4_dim_search_term = [
    "eventName",
    "customEvent:hit_timestamp",
    # "customEvent:user_id_event",
    "customEvent:search_term",
    # "customEvent:session_id_event",
    # "customEvent:session_number_event",
    "customEvent:client_id_event",
]

ga4_metr_search_term = [
    "eventCount",
    # "screenPageViews",
    # "sessions",
    # "totalUsers",
    # "transactions",
    # "purchaseRevenue",
]

# Кастомный отчет
ga4_dim_custom = [
    # "sessionSourceMedium",
    # "sessionCampaignName",
    # # "landingPagePlusQueryString",
    "eventName",
    "itemListId",
    "itemListName",
]

ga4_metr_custom = [
    # "screenPageViews",
    # "sessions",
    # "transactions",
    # "purchaseRevenue",
    # "eventCount",
    # "totalUsers"
]

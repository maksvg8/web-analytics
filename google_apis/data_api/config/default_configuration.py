


# field_name = "eventName"
# filters_value = "purchase|refund"
# filters_value = "search|search_complete|search_complete_select|search_select|add_shipping_info|add_payment_info|add_to_cart|begin_checkout|purchase|refund|remove_from_cart|repeat_order|select_item|view_cart|view_item|view_item_list"
filters_value_funnel = "add_shipping_info|add_payment_info|add_to_cart|begin_checkout|purchase|refund|remove_from_cart|repeat_order|select_item|view_cart|view_item|view_item_list"
filters_value_transaction = "purchase"

email_field_name = "sessionSourceMedium"
email_filters_value = "(.*email.*)|(.*viber.*)"

card_field_name = "eventName"
card_filters_value = "(add_to_cart)|(purchase)"

search_field_name = "eventName"
search_filters_value = "search.*"

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
    "customEvent:client_id_event"
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
    "date",
    "customEvent:hit_timestamp",
    "eventName",
    # "eventName",
    # "browser",
    # "deviceCategory",
    # "sessionSource",
    # "sessionMedium",
    # "sessionCampaignName",
    "customEvent:user_id_event"
]

ga4_metr_ed_sign_up_users = ["eventCount"]
# , "totalPurchasers"

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

DIM_KUFAR_REPORT = "ym:s:date,ym:s:<attribution>UTMSource,ym:s:<attribution>UTMCampaign,ym:s:<attribution>UTMMedium,ym:s:<attribution>UTMContent,ym:s:<attribution>UTMTerm,ym:s:purchaseID"
METR_KUFAR_REPORT = "ym:s:visits,ym:s:users,ym:s:ecommercePurchases,ym:s:ecommerce<currency>ConvertedRevenue"

DIM_EDADEAL_REPORT = "ym:s:<attribution>UTMCampaign"
METR_EDADEAL_REPORT = "ym:s:visits,ym:s:users,ym:s:ecommercePurchases,ym:s:ecommerce<currency>ConvertedRevenue"

DIM_CAMPAIGN_REPORT = "ym:s:date,ym:s:<attribution>UTMCampaign"
METR_CAMPAIGN_REPORT = "ym:s:visits,ym:s:users,ym:s:ecommercePurchases,ym:s:ecommerce<currency>ConvertedRevenue"

DIM_BANNER_REPORT = "ym:pv:date,ym:pv:URLParamNameAndValue"
METR_BANNER_REPORT = "ym:pv:pageviews,ym:pv:users"

DIM_CATEGORY_REPORT = "ym:pv:date,ym:pv:URLPath"
METR_CATEGORY_REPORT = "ym:pv:pageviews,ym:pv:users"

METR_ED_REGISTRATION = ',ym:s:goal256492353reaches'
METR_EM_REGISTRATION = ',ym:s:goal283412623reaches'

FILTER_EM_KUFAR = "ym:s:<attribution>UTMCampaign=='em_katalog_tovarov'"
FILTER_EDADEAL = "ym:s:<attribution>UTMCampaign=='ed_em_katalog_tovarov_rb_edadeal'"

FILTER_ED_CAMPAIGN = "ym:s:<attribution>UTMCampaign=~'.*_ed_.*' AND NOT(ym:s:<attribution>UTMCampaign=~'.*(blogg|smm_|emall|edostavka).*')"
FILTER_EM_CAMPAIGN = "ym:s:<attribution>UTMCampaign=~'.*_em_.*' AND NOT(ym:s:<attribution>UTMCampaign=~'.*(blogg|smm_|emall|edostavka).*')"

FILTER_ED_BANNER = "ym:pv:URLParamNameAndValue=~'ed_ban.*'"
FILTER_EM_BANNER = "ym:pv:URLParamNameAndValue=~'em_ban.*'"

FILTER_CATEGORY = "ym:pv:URLPath=~'^/categ.*' OR ym:pv:URLPath=='/'"
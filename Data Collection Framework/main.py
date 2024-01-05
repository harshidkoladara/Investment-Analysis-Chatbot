# from news.collect_news import CollectNews
    
# start_date = "2024-01-05"
# end_date = "2024-01-06"
# config = {
#     "use_proxy": "us_free",
#     "max_retry": 5,
#     "proxy_pages": 5,
#     "token": "clsplg9r01qv99446bogclsplg9r01qv99446bp0"
# }

# news_downloader = CollectNews(config)                      # init
# news_downloader.download_date_range_stock(start_date, end_date, stock='AAPL')    # Download headers
# news_downloader.gather_content()                                  # Download contents
# df = news_downloader.dataframe
# selected_columns = ["headline", "content"]
# print(df[selected_columns])



from announcements.collect_announcements import CollectAnnouncements

start_date = "2020-01-01"
end_date = "2020-06-01"
stock = "AAPL"
config = {
    "use_proxy": "us_free",
    "max_retry": 5,
    "proxy_pages": 3,
}
downloader = CollectAnnouncements(config)
downloader.download_date_range_stock(start_date, end_date, stock = stock)
df = downloader.dataframe
selected_columns = ["file_date", "display_names", "content"]
print(df[selected_columns])

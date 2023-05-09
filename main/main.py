from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sentiment_analyer import flair_sentiment_analyser


investing_com_url = 'https://in.investing.com/equities/' #url to fetch news headlines

#static list has been created to traverse url through the required companies news data
news_link = ['infosys','tata-consultancy-services','wipro-ltd','hcl-technologies','tech-mahindra','niit-technologies-ltd','lt-technology-services-ltd-ns','larsen-toubro-infotech-ltd',
           'mphasis','persistent-systems','tata-consultancy-services','axis-bank','bajaj-finserv-limited','cholamandalam-inv.-and-finance','hdfc-asset-management-company-ltd','hdfc-bank-ltd','hdfc-standard-life','housing-development-finance',
           'icici-bank-ltd','icici-lombard','icici-prudential-life-insurance-com','indian-energy-exchange-ltd','kotak-mahindra-bank','muthoot-finance-ltd',
           'power-finance-corporation','rural-electrification','state-bank-of-india','sbi-cards-and-payment-services-ltd','sbi-life-insurance','shriram-transport-finance',
            'abbott-india-ltd','alkem-laboratories-ltd','aurobindo-pharma','biocon','cipla','divis-laboratories','dr-reddys-laboratories','gland-pharma','gsk-pharmaceuticals','granules-india-ltd','laurus-labs-ltd','lupin','natco-pharma-ltd','pfizer-ltd','sanofi-india-ltd','sun-pharma-advanced-research','torrent-pharmaceuticals','cadila-healthcare']

#static dictionary is used to assign sector to companies
ticker_sector_dict={"MBFL":"IT","TCS" :"IT","COFO":"IT","INFY":"IT","WIPR":"IT","LTEH":"IT","LTIM":"IT","HCLT":"IT","PERS":"IT","TEML":"IT","BJFN":"FINANCE","AXBK":"FINANCE","BJFS":"FINANCE","CHLA":"FINANCE","HDFA":"FINANCE","HDBK":"FINANCE","HDFL":"FINANCE","HDFC":"FINANCE","ICBK":"FINANCE","ICIL":"FINANCE","ICIR":"FINANCE","IIAN":"FINANCE","KTKM":"FINANCE","MUTT":"FINANCE","PWFC":"FINANCE","RECM":"FINANCE","SBI":"FINANCE","SBIC":"FINANCE","SBIL":"FINANCE","SHMF":"FINANCE","ABOT":"PHARMA","ALKE":"PHARMA","ARBN":"PHARMA","BION":"PHARMA","CIPL":"PHARMA","DIVI":"PHARMA","REDY":"PHARMA","GLAD":"PHARMA","GLAX":"PHARMA","GRAN":"PHARMA","LAUL":"PHARMA","LUPN":"PHARMA","NATP":"PHARMA","PFIZ":"PHARMA","SANO":"PHARMA","SUN":"PHARMA","TORP":"PHARMA","ZYDU":"PHARMA"}


news_data ={}
news_tables = {}
parsed_news=[]

#below for loop will traverse to list of companies list and create a dictinary of HTML tags
for link in news_link:
    url = investing_com_url + link
    req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}) 
    response = urlopen(req)
    html = BeautifulSoup(response)# Read the contents of the file into 'html'
    ticker=html.find("div",{"class":"group-title-and-options-buttons"}).find("h2").get_text().split()[0]
    news_table = html.find("ul", {"class": "common-articles-list"})
    news_data[ticker]=news_table #ticker wise data is stored in the dictionary

#below for loop will traverse to each HTML data and store the text into a list
for ticker,news_data in news_data.items():
    for news in news_data.find_all("div",{"class":"content"}):
        text_data = news.a.get_text()
        date_data = news.time.find_next_sibling().get_text()
        sector=ticker_sector_dict[ticker]
        parsed_news.append([ticker,sector,date_data,text_data])



dataflair_df=flair_sentiment_analyser(parsed_news)

engine = create_engine('postgresql://postgres:root@localhost:5432/findata_sentimentanalysis')
dataflair_df.to_sql('stock_news_sentiment_scores', engine,if_exists='append', index=False)



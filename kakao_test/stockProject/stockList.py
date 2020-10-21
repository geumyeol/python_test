

"""
1. Top 50
2. PER 30% 미만
3. PBR 5 미만
4. ROE 10 이상
5. 3개월 / 1년 / 3년
"""
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

# import sys
# sys.stdout = open('naver_stock_1to50.txt', 'w')
Total_Message = []

PER_BASE = 30
PBR_BASE = 5
ROE_BASE = 10

Request_Count = 0

idx = 1
Total_Message = []

for page_num in range(1,5):

    url = "https://finance.naver.com/sise/sise_market_sum.nhn?page="+"%d"%(page_num)

    # print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    stock_head = soup.find("thead").find_all("th")
    data_head = [head.get_text() for head in stock_head]
    data_head.pop()

    stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
    stockTop50_corp = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("a", attrs={"class": "tltle"})
    result_str = ""

    data_header = ['회사명']

    for stock in stockTop50_corp:
        corp_Message = []
        stock_name = stock.get_text()
        stock_link = "https://finance.naver.com/"+stock["href"]
        # print(stock_link)

        flag = 1

        sub_res = requests.get(stock_link)
        sub_soup = BeautifulSoup(sub_res.text, 'lxml')

        sub_thead = sub_soup.find("table", attrs={"class":"tb_type1 tb_num tb_type1_ifrs"})

        if sub_thead is not None:
            sub_thead = sub_thead.find("thead").find_all("th", attrs={"scope":"col"})
        else:
            continue
        """ 위 코드로 return None 값에 대한 예외처리
        
        if str(stock_name).find("KO2DEX") >= 0 or \
                        str(stock_name).find("맥쿼리인프라") >= 0 or \
                        str(stock_name).find("TIGER") >= 0 or \
                        str(stock_name).find("롯데리츠") >= 0 or \
                        str(stock_name).find("티와이홀딩스") >= 0 or \
                        str(stock_name).find("제이알글로벌리츠") >= 0 or \
                        str(stock_name).find("200") >= 0:

                    continue
                """


        img_link_list = ['month3', 'year', 'year3']
        img_link = sub_soup.find("img", attrs={"id": "img_chart_area"})['src']

        # print(stock_name)

        if idx==1:
            result_str = sub_soup.find("th", attrs={"class": "h_th2 th_cop_anal5 b_line"}).get_text()
            data_header.append(result_str)

            for value in sub_thead:
                str__ = value.get_text().strip()
                if (str__.startswith("20")):
                    result_str += str__
                    data_header.append(str__)

            idx += 1
            # print(data_header)

        # ParamList = ['매출액', '영업이익', '당기순이익', 'ROE(지배주주)', 'PER(배)', 'PBR(배)']
        ParamList = ['ROE(지배주주)', 'PER(배)', 'PBR(배)']

        for idx, pText in enumerate(ParamList):

            param = " ".join(sub_soup.find('strong', text=pText).parent['class'])
            # print (param)
            result_message = getDataOfParam(idx, stock_name, param)
            corp_Message.extend(result_message)
            if len(result_message) != 0 :
                temp = result_message.pop()
                if temp.startswith("@@"):
                    flag = 0
                    # img1 = img_link.replace("day", img_link_list[0])
                    # img2 = img_link.replace("day", img_link_list[1])
                    # img3 = img_link.replace("day", img_link_list[2])
                    # Total_Message.append(temp)
                    # Total_Message.append(img1)
                    # Total_Message.append(img2)
                    # Total_Message.append(img3)

                    break

            # Total_Message.extend(result_message)
            # print (len(result_message))
            # print(result_message)

        # img_link_list = ['month3', 'year', 'year3']
        # img_link = sub_soup.find("img", attrs={"id": "img_chart_area"})['src']

        if flag == 0:

            continue

        if corp_Message:
            Request_Count += 1
            Total_Message.append("<a href='"+stock_link+"'>"+ stock_name+"</a>")
            Total_Message.extend(corp_Message)
            img1 = img_link.replace("day", img_link_list[0])
            img2 = img_link.replace("day", img_link_list[1])
            img3 = img_link.replace("day", img_link_list[2])
            Total_Message.append("<br>[3개월]<br><img src='"+img1+"'>")
            Total_Message.append("[1년]<br><img src='"+img2+"'>")
            Total_Message.append("[3년]<br><img src='"+img3+"'>")
            Total_Message.append("")

        # writer.writerow(stock_name)
        # writer.writerow(result_str)
        # print(stock_name)
        # print(result_str)


print("\n".join(Total_Message))

# E-mail 전송
# -*-coding:utf-8-*-


import requests
import xlwt


class Lagou_job(object):
    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false&isSchoolJob=0'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Mobile Safari/537.36',
            'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=',
            'Cookie': '换成你自己的cookie'
        }

    def get_job_list(self, page):
        self.data = {
            'first': 'true',
            'pn': page,
            'kd': 'python'
        }
        res = requests.post(self.url, data=self.data, headers=self.headers)
        result = res.json()
        # print(result)  # debug
        jobs = result['content']['positionResult']['result']
        return jobs

    def make_els(self):
        excelTabel = xlwt.Workbook()  # 创建excel对象
        # 如果对一个单元格重复操作，会引发
        # returns error:
        # Exception: Attempt to overwrite cell:
        # sheetname=u'sheet 1' rowx=0 colx=0
        # 所以在打开时加cell_overwrite_ok=True 解决
        sheet_1 = excelTabel.add_sheet('lagouByLi', cell_overwrite_ok=True)
        sheet_1.write(0, 0, 'companyFullName')
        sheet_1.write(0, 1, 'city')
        sheet_1.write(0, 2, 'district')
        sheet_1.write(0, 3, 'jobNature')
        sheet_1.write(0, 4, 'positionName')
        sheet_1.write(0, 5, 'salary')
        sheet_1.write(0, 6, 'secondType')
        sheet_1.write(0, 7, 'workYear')
        sheet_1.write(0, 8, 'companySize')
        sheet_1.write(0, 9, 'education')
        n = 1  # 写入xls文件行数
        for page in range(1, 31):  # 前30页
            for job in self.get_job_list(page=page):
                if '1-3' in job['workYear'] and '全职' in job['jobNature'] and '本科' in job['education']:
                    sheet_1.write(n, 0, job['companyFullName'])
                    sheet_1.write(n, 1, job['city'])
                    sheet_1.write(n, 2, job['district'])
                    sheet_1.write(n, 3, job['jobNature'])
                    sheet_1.write(n, 4, job['positionName'])
                    sheet_1.write(n, 5, job['salary'])
                    sheet_1.write(n, 6, job['secondType'])
                    sheet_1.write(n, 7, job['workYear'])
                    sheet_1.write(n, 8, job['companySize'])
                    sheet_1.write(n, 9, job['education'])
                    n += 1

        # 保存文件
        excelTabel.save('lagou_byLi.xls')


if __name__ == '__main__':
    lagou_job = Lagou_job()
    # lagou_job.get_job_list(1)  # debug
    lagou_job.make_els()

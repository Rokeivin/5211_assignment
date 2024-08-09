import datetime
import os
import smtplib
from email import encoders
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# !!TODO: 在使用程序前请更改确认存储数据表的相对位置！！

def classify_products(products):
    product_dict = {}
    # 分析每个产品名
    for product in products:
        # 分离出汉字部分和数字部分
        if product[-1] != '号':
            name = product
            number = ''
        else:
            index = next(i for i, ch in enumerate(product[:]) if ch.isdigit())
            name = product[:index]
            number = product[index:]
        # 添加到字典中
        if name in product_dict:
            product_dict[name].append(number)
        else:
            product_dict[name] = [number, ]
    merged_products = []
    for name, numbers in product_dict.items():
        if len(numbers) > 1:
            merged_products.append(f"{name}{'、'.join(numbers)}")
        else:
            merged_products.append(f"{name}{numbers[0]}")

    return "、".join(merged_products)


def send_daily_email(user, password, to_addrs):
    date = datetime.date.today().strftime('%Y%m%d')
    # ! ! TODO: 这里是一个需要修改的路径
    attachment_path = 'C:\\Users\\DELL\\Desktop\\估值代码\\客户估值表\\估值表'

    smtp_server = "mail.kysec.cn"
    smtp_port = 465
    from_email = 'kysec_otc@kysec.cn'  # 发件人邮箱
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    # 实际发送、接收邮件配置
    server.login(user, password)
    count = 0
    for addrs in to_addrs:
        if count > 10:
            count = 0
            # 重新建立连接
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(user, password)
        msg = MIMEMultipart()
        words = classify_products(to_addrs[addrs][0])
        msg['Subject'] = Header(f'{words}-' + f'估值表{date}', 'utf-8')
        body = MIMEText(f'''
    <p>尊敬的管理人、托管人：</p>
     <p style='text-indent: 2em;'> 今日{words}交易合约估值，详见附件估值表</p>
    ''', 'html', _charset="utf-8")
        msg.attach(body)
        msg['From'] = '"=?utf-8?B?5byA5rqQ5Zy65aSW6KGN55Sf5ZOB?=" <kysec_otc@kysec.cn>'
        for file_name in to_addrs[addrs][0]:
            with open(os.path.join(attachment_path, file_name + f'-估值表{date}.xlsx'), 'rb') as file:
                part = MIMEApplication(file.read(), Name=file_name + f'-估值表{date}.xlsx')
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment', filename=file_name + f'-估值表{date}.xlsx')
                msg.attach(part)

        msg['To'] = Header(addrs)
        if len(to_addrs[addrs][1]) > 0:
            msg['Cc'] = ','.join(to_addrs[addrs][1])
            server.sendmail(from_email, addrs.split(',') + msg['Cc'].split(','), msg.as_string())
            count += len(addrs.split(',')) + len(msg['Cc'].split(','))
        else:
            server.sendmail(from_email, addrs.split(','), msg.as_string())
            count += len(addrs.split(','))
        print(f'成功向邮箱{addrs}发送日报信息')
    server.quit()


def send_weekly_email(user, password, to_addrs):
    date = datetime.date.today().strftime('%Y%m%d')
    # ! ! TODO: 这里是一个需要修改的路径
    attachment_path = 'C:\\Users\\DELL\\Desktop\\估值代码\\客户估值表\\估值表\\招商财富'
    # 由于qq邮箱的特性，需要针对qq邮箱使用不同的编码方式
    smtp_server = "mail.kysec.cn"
    smtp_port = 465
    from_email = 'kysec_otc@kysec.cn'  # 发件人邮箱
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    # 实际发送、接收邮件配置
    server.login(user, password)
    count = 0
    for addrs in to_addrs:
        if count > 10:
            count = 0
            # 重新建立连接
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(user, password)
        msg = MIMEMultipart()
        words = classify_products(to_addrs[addrs][0])
        msg['Subject'] = Header(f'{words}' + f'估值表{date}', 'utf-8')
        body = MIMEText(f'''
    <p> 您好，{words}今日估值表，详见附件。</p>
    ''', 'html', _charset="utf-8")
        msg.attach(body)
        msg['From'] = '"=?utf-8?B?5byA5rqQ5Zy65aSW6KGN55Sf5ZOB?=" <kysec_otc@kysec.cn>'
        for file_name in to_addrs[addrs][0]:
            with open(os.path.join(attachment_path, file_name + f'估值表{date}.xlsx'), 'rb') as file:
                part = MIMEApplication(file.read(), Name=file_name + f'估值表{date}.xlsx')
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment', filename=file_name + f'估值表{date}.xlsx')
                msg.attach(part)

        msg['To'] = Header(addrs)
        if len(to_addrs[addrs][1]) > 0:
            msg['Cc'] = ','.join(to_addrs[addrs][1])
        # server.sendmail(from_email, addrs.split(','), msg.as_string())
            server.sendmail(from_email, addrs.split(',') + msg['Cc'].split(','), msg.as_string())
            count += len(addrs.split(',')) + len(msg['Cc'].split(','))
        else:
            server.sendmail(from_email, addrs.split(','), msg.as_string())
            count += len(addrs.split(','))
        print(f'成功向邮箱{addrs}发送周报信息')
    server.quit()


my_user = ''
my_password = ''   # 定期更新：安全设置-客户端安全登录
# 在这里填写每个邮箱需要接收的信息，以下仅为测试用
# ! ! TODO: 这里需要根据实际邮箱和对应产品（收件人；产品；抄送人）
daily_to_addrs = {'abama01@abmzcgl.com,otct@abmzcgl.com,jianghw@abmzcgl.com,yywb@cmschina.com.cn': [['阿巴马智选尊享1号'], []],
                  'valuation@alpha2capital.com,acsy_otc@alpha2capital.com,gztg@ebscn.com,gzwb@ebscn.com': [['安诚数盈安越嘉盈','安诚数盈安越浦盈'], []],
                  'funddata@pbcjsc.com,tgdata@pbcjsc.com': [['安诚数盈长泽'], ['valuation@alpha2capital.com']],
                 'liuzx@bhhjamc.com,bhhjcwb@126.com,cxywtd@163.com,tuoguanhs1@psbcszfh.com': [['渤海汇金智增红利1号'], []],
                 'bhhjcwb@126.com,tjzctgb@citicbank.com,cxywtd@163.com': [['渤海汇金智增红利2号'], []],
                 'tgjzwj@haitong.com,wbjzwj@haitong.com,jedi@jediam.com': [['金澹添盈1号'], []],
                 'cwysp@tg.gtja.com,operation@techsharpe.cn,dj@techsharpe.cn,ztx@techsharpe.cn,hty@techsharpe.cn,ljz@techsharpe.cn': [['天算顺势63号'], []],
                 'tqcp@cjsc.com,funddata@cjsc.com.cn,tgdata@cjsc.com.cn': [['天相1号'], []],
                 'TYOTC@tianyfund.cn,data@tianyfund.cn,PIFvaluation@citics.com,custodiandata@citics.com': [['添益智信1号'], []],
                 'derivatives@tongyigroup.cn,gzwb@ebscn.com,gztg@ebscn.com': [['通怡明曦8号'], []],
                 'yywb@cmschina.com.cn': [['紫薇3号', '紫薇13号'], []],
                 'yywb@cmschina.com.cn,17170101@qq.com,305464861@qq.com,1875664560@qq.com,starry9819@163.com': [['紫薇19号'], []],
                   }
weekly_to_addrs = {'FA_Non-stndMangGrp@cmfchina.com': [['招商财富新利19号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富新利24号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富新利26号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富新利27号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富新利28号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富新利31号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富新利33号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富新利39号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富新利51号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富新利52号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富新利53号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富招利53号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富招利55号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富招利112号'], []],
                   'FA_Non-stndMangGrp@cmfchina.com': [['招商财富招利128号'], []],
                   }

# daily_to_addrs = {'jingzhe-luo@Outlook.com,shiyuanzhe@kysec.cn': [['紫薇3号','紫薇13号'], ['839349768@qq.com', 'wangruiqi@kysec.cn']]}
# weekly_to_addrs = {'jingzhe-luo@Outlook.com,shiyuanzhe@kysec.cn': [['招商财富新利20号','招商财富新利21号'], ['839349768@qq.com', 'wangruiqi@kysec.cn']]}

# 发送日报
# send_daily_email(my_user, my_password, daily_to_addrs)

# 发送周报，无需周报时将本句进行注释即可
send_weekly_email(my_user, my_password, weekly_to_addrs)

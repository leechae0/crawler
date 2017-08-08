# -*coding :utf-8-*-

import arrow
import re

nowDate = arrow.utcnow().to('Asia/Seoul').format('YYYY-MM-DD HH:mm:ss')
print(nowDate)

except_word = ['(TV)']



a = '(TV)Flab 카카오닙스 총 18통'


for word in except_word:
    b = a.replace(word,'')
    print(b)
    print(re.sub("[0-9]통", "", b))

    # print(b)


# print(a.replace('\0-9',''))
# print(re.sub("[0-9]종","",a))

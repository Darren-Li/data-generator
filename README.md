# data-generator（数据模拟/生成器）

## 快速模拟真实业务场景数据
Fast simulation of real business scenario data

自定义快速实现贴合真实场景的数据模拟/生成，帮助你更好地实现产品性能测试、演示环境搭建、BI报表设计和Demo搭建。
Customized rapid implementation of data simulation/generation in accordance with the real scene, to help you better achieve product performance testing, demonstration environment, BI report design and Demo construction.

## 支持的字段类型
1. 支持基础类型字段生成，如：数字，序号，ID，布尔值，时间，日期，文本等
2. 支持人口统计相关信息生成，如：姓名，性别，年龄等
3. 支持模拟手机号码，邮箱，身份证号码，银行卡号等PII数据
4. 支持公司信息模拟，如：公司名称，公司类型，公司地址，公司邮箱，职位
5. 支持地理位置数据生成，如：省份，城市，区县，街道等
6. 支持按自定义列表随机生成数据，或按照指定概率生成
7. 支持网络数据生成，如：IP，URL，MAC ID
8. 支持**级联数据**生成，如：省份-城市-区县，如生成“江苏省-南京市-浦口区”实现数据一致，也支持按照自定义字典生成级联数据
9. 支持**维度笛卡尔积**生成，如：需要笛卡尔积“部门”（产品部，分析部，运营部）和“学历”（本科，硕士）实现全维度交叉，在BI demo设计中更好展示数据
10. 支持设置字段缺失率

## 支持的数据导出格式
1. 支持多种数据导出格式：EXCEL，CSV，JSON，HTML
2. 支持以压缩文件格式导出

## 联系我们
对该脚本使用的任何问题和建议，敬请提交 issue，以便跟踪处理和经验沉淀共享。你也可以扫描下面的二维码，加入我们的**微信群**，以获得更快速的响应。
<div align=center>
    <img src="https://user-images.githubusercontent.com/20476924/179728256-321c0cb5-d7c4-47f7-af02-23652cf61c35.jpg" width="200" alt="微信扫码添加">
</div>

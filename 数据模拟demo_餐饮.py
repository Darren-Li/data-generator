# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:00:37 2022

@author: lwq07
"""

import os

# 切换到data_generator脚本目录下，导出数据也在这个目录下
path = r'D:\Darren\Work\3 数据模拟器\code'
os.chdir(path)
import data_generator as dg


locale_args=['zh_CN']
row_num=10000
miss_value=None

fun_params = [
    {"fun": "seq_id", "params": {"col_name": "品牌名称", "prefix": "brand-", "display_format": "dup", "start_num": 1, "end_num": 1}},
    {"fun": "seq_id", "params": {"col_name": "门店名称", "prefix": "shop-", "display_format": "duo", "start_num": 1, "end_num": 30}},
    {"fun": "udf_sequence", "params": {"col_name": "来源类型", "ext_words": ["直营店"]}},
    {"fun": "phone_number", "params": {"col_name": "联系方式", "display_foramt": 1}},
    {"fun": "udf_sequence", "params": {"col_name": "门店状态", "ext_words": ["营业"]}},
    {"fun": "date_between", "params": {"col_name": "统计日期", "start_date": '-7d'}},
    {"fun": "udf_sequence", "params": {"col_name": "口味偏好", "ext_words": ["肉", "素"],
                                        "cartesian_product": 1}},
    {"fun": "udf_sequence2", "params": {"col_name": "会员等级", 
                                        "ext_words": {"非会员": 3, "一星会员数": 5, "二星会员数": 2.5, 
                                                      "三星会员数": 2, "四星会员数": 1.5, "五星会员数": 1},
                                        "cartesian_product": 1}},
    {"fun": "udf_sequence", "params": {"col_name": "消费频次", "ext_words": ["未消费", "1次", "2次", "3-5次", "5次以上"],
                                        "cartesian_product": 1}},
    {"fun": "number", "params": {"col_name": "客单价", "min": 30, "max": 100}},
    {"fun": "number", "params": {"col_name": "会员数", "min": 100, "max": 10000}}
    ]


# 联级字段创建
address_list = [{"province": "北京市", "city": "北京市", "district": "朝阳区", 
                 "street": "朝阳北路", "street_address": "朝阳北路北京长楹龙湖西区4层",
                 "sales_area": "华北"},
                {"province": "北京市", "city": "北京市", "district": "昌平区", 
                 "street": "回龙观镇", "street_address": "回龙观镇龙域中心A座昌发展万科广场4楼",
                 "sales_area": "华北"},
                {"province": "北京市", "city": "北京市", "district": "海淀区", 
                 "street": "北清路", "street_address": "北清路81号院2号楼A102",
                 "sales_area": "华北"},
                
                {"province": "上海市", "city": "上海市", "district": "浦东新区", 
                 "street": "祖冲之路", "address": "祖冲之路1239弄长泰广场地下一层西区",
                 "sales_area": "华南"},
                {"province": "上海市", "city": "上海市", "district": "闵行区", 
                 "street": "申长路", "address": "申长路688号（虹桥天地购物中心B1层）",
                 "sales_area": "华南"},
                {"province": "江苏省", "city": "上海市", "district": "杨浦区", 
                 "street": "唐山路", "address": "唐山路1018号（宝地广场B1层）",
                 "sales_area": "华南"},
                {"province": "江苏省", "city": "上海市", "district": "长宁区", 
                 "street": "长宁路", "address": "长宁区长宁路1123号（长宁来福士B1层K01-K11）",
                 "sales_area": "华南"}
    ]

cascade_list = address_list

cascade_params = [{"fun": "province", "col_name": "省份", "miss_rate": 0}, 
                  {"fun": "city", "col_name": "城市", "miss_rate": 0},
                  {"fun": "district", "col_name": "区县", "miss_rate": 0},
                  {"fun": "street", "col_name": "街道", "miss_rate": 5},
                  {"fun": "address", "col_name": "详细地址", "miss_rate": 15},
                  {"fun": "sales_area", "col_name": "销售大区", "miss_rate": 0}]

df = dg.generate(locale_args, row_num, miss_value,
                 fun_params=fun_params,
                 cascade = "Y",
                 cascade_params_lists=[{"cascade_list": cascade_list,
                                        "cascade_params": cascade_params
                                        }]
                 )


file_name = "data/喜家德门店数据汇总"
os.chdir("..")
dg.write_out(df, file_name, "CSV", encoding="utf-8")



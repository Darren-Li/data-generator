import sys
import time
import random
import math
import pandas as pd
from collections import ChainMap
from itertools import product
import copy
# import re
from faker import Faker
from faker.providers import internet

# https://faker.readthedocs.io/en/master/index.html


__version__ = "1.0.2"
__author__ = "子清"

address_list = [{"province": "北京市", "city": "北京市", "district": "朝阳区", 
                 "street": "东亿国际传媒产业园", "street_address": "东亿国际传媒产业园三期C座4层"},
                {"province": "上海市", "city": "上海市", "district": "虹口区", 
                 "street": "花园路128号德必运动LOFT产业园", "address": "花园路128号德必运动LOFT产业园7街区A座"},
                {"province": "江苏省", "city": "南京市", "district": "江北新区", 
                 "street": "星火路14号长峰大厦", "address": "星火路14号长峰大厦1号楼8层802室"}
                ]

address_params = [{"fun": "province", "col_name": "省份", "miss_rate": 0},
                  {"fun": "city", "col_name": "城市", "miss_rate": 0}
                  ]

fun_params = [{"fun": "person_name", "params": {"col_name": "full_name"}, "cartesian_product": 0},
              {"fun": "gender", "params": {"col_name": "gender"}, "cartesian_product": 0},
              {"fun": "age", "params": {"col_name": "age", "min": 22, "max": 65}, "cartesian_product": 0}
              ]


class DataGenerator(object):
    """
    data generator created by ziqing
    """
    def __init__(self, locale_args=['zh_CN'], row_num=100, miss_value=None,
                 cascade_list=address_list, cascade_params=address_params):
        self.fake = Faker(locale_args)
        self.locale_args = locale_args
        self.row_num = row_num
        self.miss_value = miss_value
        
    def set_missing_values(self, v, miss_rate):
        """
        set miss rate

        Parameters
        ----------
        v : TYPE
            DESCRIPTION.
        miss_rate : TYPE
            DESCRIPTION. 0~1 stands for decimals, 1~100 stands for integers!

        Returns
        -------
        v : TYPE
            DESCRIPTION.

        """
        if miss_rate<0 or miss_rate >100:
            sys.exit("miss rate must be between 0 and 100. 0~1 stands for decimals, 1~100 stands for integers!")
        elif miss_rate > 1:
            miss_rate /= 100
        
        miss_records = math.floor(self.row_num * miss_rate)
        for i in range(0, miss_records):
            while True:
                rand_ix = random.randint(0, self.row_num-1)
                if v[rand_ix]:
                    v[rand_ix] = self.miss_value
                    break
        return v

    # ID
    def seq_id(self, col_name="seq_id", prefix="xxx-", display_format="unique",
               start_num=1000000, end_num=999999):
        """
        generate sequence ids, unique ids or duplicate ids.

        Parameters
        ----------
        col_name : TYPE, optional
            DESCRIPTION. The default is "seq_id".
        prefix : TYPE, optional
            DESCRIPTION. The default is "xxx-".
        display_format : TYPE, optional
            DESCRIPTION. The default is "unique", will generate unique sequence ids. 
            others will generate duplicate sequence ids.
        start_num : TYPE, optional
            DESCRIPTION. The default is 1000000. row number + 1000000, 
            will generate ids like "xxx-1000001", "xxx-1001126". 
        end_num : TYPE, optional
            DESCRIPTION. The default is 999999. For generating dup ids, 
            can specify the range of ids, from start_num + 0 to start_num + end_num

        Returns
        -------
        dict
            DESCRIPTION.

        """
        if display_format == "unique":
            v = [prefix+str(start_num+i) for i in range(self.row_num)]
        else:
            if end_num < self.row_num:
                v = [prefix+str(start_num+random.randint(0, end_num-1)) for i in range(self.row_num)]
            else:
                v = [prefix+str(start_num+random.randint(0, self.row_num-1)) for i in range(self.row_num)]
        return {col_name: v}

    # number
    def number(self, col_name="number", min=0, max=100, step=1, miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(int(round(random.randint(min, max)/step, 0)*step))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def float_number(self, col_name="float_number", min=0, max=100, ndigits=2,
                        miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(round(random.uniform(min, max), ndigits))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def gauss(self, col_name="gauss", mu=0, sigma=1, ndigits=2, miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(round(random.gauss(mu, sigma), ndigits))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def boolean(self, col_name="boolean", display_foramt=0, miss_rate=0):
        if display_foramt == 0:
            c = ["是", "否"]
        elif display_foramt == 1:
            c = ["false", "true"]
        elif display_foramt == 2:
            c = [1, 0]
        elif display_foramt == 3:
            c = ["Yes", "No"]
        else:
            c = ["Y", "N"]
        v = []
        for _ in range(self.row_num):
            v.append(random.choice(c))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    # only valid for USD
    def pricetag(self, col_name="pricetag", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.pricetag())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    # date and time
    def date(self, col_name="date", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.date(pattern='%Y-%m-%d', end_datetime=None))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def date_between(self, col_name="date_between", 
                     start_date='-3y', end_date='today', miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.date_between(start_date=start_date,
                                            end_date=end_date))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def date_time_between(self, col_name="date_time_between", 
                          start_date='-3y', end_date='now',  miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.date_time_between(start_date=start_date,
                                                 end_date=end_date))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    # person
    def person_name(self, col_name="person_name", display_foramt=1,
                    miss_rate=0):
        v = []
        for _ in range(self.row_num):
            if display_foramt == 1:
                v.append(self.fake.name())
            elif display_foramt == 2:
                v.append(self.fake.last_name())
            else:
                v.append(self.fake.first_name())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def user_name(self, col_name="user_name", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.user_name())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def gender(self, col_name="gender", miss_rate=0):
        if len(self.locale_args) > 1:
            c = ["男", "女", "male", "female"]
        elif self.locale_args == ['zh_CN']:
            c = ["男", "女"]
        else:
            c = ["male", "female"]
        v = []
        for _ in range(self.row_num):
            v.append(random.choice(c))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def age(self, col_name="age", min=22, max=65, miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(random.randint(min, max))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    # Chinese personal identity code
    def ssn(self, col_name="ssn", display_foramt=0, miss_rate=0):
        v = []
        for _ in range(self.row_num):
            if display_foramt == 0:
                v.append(self.fake.ssn())
            elif display_foramt == 1:
                vv = self.fake.ssn()
                v.append(vv[:6] + 8*"*" + vv[-4:])
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def phone_number(self, col_name="phone_number", display_foramt=0, 
                     miss_rate=0):
        v = []
        for _ in range(self.row_num):
            if display_foramt == 0:
                v.append(self.fake.phone_number())
            elif display_foramt == 1:
                vv = self.fake.phone_number()
                v.append(vv[:3] + 4*"*" + vv[-4:])
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def email(self, col_name="email", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.email())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def safe_email(self, col_name="safe_email", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.safe_email())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def company_email(self, col_name="company_email", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.company_email())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def job(self, col_name="job", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.job())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    # location
    def province(self, col_name="province", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.province())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def city(self, col_name="city", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.city())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def postcode(self, col_name="postcode", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.postcode())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def district(self, col_name="district", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.district())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def street_address(self, col_name="street_address", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.street_address())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def address(self, col_name="address", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.address())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    # company
    def company(self, col_name="company", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.company())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def company_prefix(self, col_name="company_prefix", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.company_prefix())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def company_suffix(self, col_name="company_suffix", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.company_suffix())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    # text
    def text(self, col_name="text", max_nb_chars=200, ext_words=None, 
             miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.text(max_nb_chars, ext_words))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    # internet
    def ipv4(self, col_name="ipv4", miss_rate=0):
        self.fake.add_provider(internet)
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.ipv4_private())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def url(self, col_name="url", miss_rate=0):
        self.fake.add_provider(internet)
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.url())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    def mac_address(self, col_name="mac_address", miss_rate=0):
        self.fake.add_provider(internet)
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.mac_address())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    # finance
    def credit_card_number(self, col_name="credit_card_number", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.credit_card_number())
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}

    # color
    def color_name(self, col_name="color_name", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.color_name())
        v = self.set_missing_values(v, miss_rate=0)
        return {col_name: v}

    # automobile
    def license_plate(self, col_name="license_plate", miss_rate=0):
        v = []
        for _ in range(self.row_num):
            v.append(self.fake.license_plate())
        v = self.set_missing_values(v, miss_rate=0)
        return {col_name: v}

    # user defined
    def udf_sequence(self, col_name="udf_sequence", ext_words=[], 
                     miss_rate=0):
        """
        user defined data generation

        Parameters
        ----------
        col_name : TYPE, optional
            DESCRIPTION. The default is "udf_sequence".
        ext_words : TYPE, optional
            DESCRIPTION. The default is [].
        miss_rate : TYPE, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        dict
            DESCRIPTION.

        """
        v = []
        for _ in range(self.row_num):
            v.append(random.choice(ext_words))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}
    
    def udf_sequence2(self, col_name="udf_sequence2", ext_words={},
                      miss_rate=0):
        """
        user defined data generation, weights will not work under this function

        Parameters
        ----------
        col_name : TYPE, optional
            DESCRIPTION. The default is "udf_sequence2".
        ext_words : TYPE, optional
            DESCRIPTION. The default is {}.
        miss_rate : TYPE, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        dict
            DESCRIPTION.

        """
        v = []
        for _ in range(self.row_num):
            v.extend(random.choices(list(ext_words.keys()), 
                                    weights=list(ext_words.values()), k=1))
        v = self.set_missing_values(v, miss_rate)
        return {col_name: v}
    
    def cascade_gen(self, cascade_list=address_list, cascade_params=address_params):
        """
        cascade data generator(级联数据生成器)

        Parameters
        ----------
        cascade_list : TYPE, optional
            DESCRIPTION. The default is address_list.
        cascade_params : TYPE, optional
            DESCRIPTION. The default is address_params.

        Returns
        -------
        v : TYPE
            DESCRIPTION.

        """
        col_calls = ["cas_v{}".format(i+1) for i, j in enumerate(cascade_params)]
        col_calls = "=[]\n".join(col_calls) + "=[]"
        exec(col_calls)
        
        for _ in range(self.row_num):
            i = random.choice(cascade_list)
            cas_calls = ["cas_v{}.append(i.get('{}'))".format(i+1, j.get("fun")) for i, j in enumerate(cascade_params)]
            cas_calls = "\n".join(cas_calls)
            exec(cas_calls)
            
            cas_dicts = ["'cas_{}': cas_v{}".format(j.get("col_name"), i+1) for i, j in enumerate(cascade_params)]
            cas_dicts = "{" + ", ".join(cas_dicts) + "}"
        
        v = eval(cas_dicts)
        v = {i: v.get(i) for i in list(v.keys())[::-1]}
        
        for i, j in enumerate(cascade_params):
            miss_rate = j.get("miss_rate")
            v["cas_{}".format(j.get("col_name"))] = self.set_missing_values(v.get("cas_{}".format(j.get("col_name"))), miss_rate)
        return v


def generate(locale_args=['zh_CN'], row_num=100, miss_value=None,
             fun_params=fun_params,
             cascade = "N",
             cascade_params_lists=[{"cascade_list": address_list,
                                    "cascade_params": address_params}]
             ):
    """
    generate data by your requirements

    Parameters
    ----------
    locale_args : TYPE, optional
        DESCRIPTION. The default is ['zh_CN'].
    row_num : TYPE, optional
        DESCRIPTION. The default is 100.
    miss_value : TYPE, optional
        DESCRIPTION. The default is None.
    fun_params : TYPE, optional
        DESCRIPTION. The default is [{"fun": "person_name", "params": {"col_name": "full_name"}},
                                     {"fun": "gender", "params": {"col_name": "gender"}},
                                     {"fun": "age", "params": {"col_name": "age", "min": 22, "max": 65}}].
    cascade : TYPE, optional
        DESCRIPTION. The default is "N".
    cascade_params_lists : TYPE, optional
        DESCRIPTION. The default is [{"cascade_list": [
            {"province": "北京市", "city": "北京市", "district": "朝阳区",
             "street": "东亿国际传媒产业园", "street_address": "东亿国际传媒产业园三期C座4层"},
            {"province": "上海市", "city": "上海市", "district": "虹口区",
             "street": "花园路128号德必运动LOFT产业园", "address": "花园路128号德必运动LOFT产业园7街区A座"},
            {"province": "江苏省", "city": "南京市", "district": "江北新区",
             "street": "星火路14号长峰大厦", "address": "星火路14号长峰大厦1号楼8层802室"}], 
            "cascade_params": [{"fun": "province", "col_name": "省份", "miss_rate": 0},
                               {"fun": "city", "col_name": "城市", "miss_rate": 0}]}].
    
    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    start = time.time()
    gen = DataGenerator(locale_args, row_num, miss_value)
    
    # 1. cartesian product(笛卡尔积字段生成)
    fun_params_tmp = copy.deepcopy(fun_params)
    cp_names = []
    cp_v = []
    for i in fun_params_tmp:
        if i.get("params").get("cartesian_product") == 1:
            cp_names.append(i.get("params").get("col_name"))
            v = i.get("params").get("ext_words")
            if type(v) == dict:
                cp_v.append(list(v.keys()))
            else:
                cp_v.append(v)
            fun_params.remove(i)
    
    py = ",".join(["cp_v[{}]".format(i) for i in range(len(cp_v))])
    py = "list(product(" + py + "))"
    cp_vv = eval(py)
    
    if len(cp_vv) > row_num:
        print("你所选的字段在进行笛卡尔积后总数据行数将超过所设置的需要生成的数据的最大行数（{}）的限制，系统将只生成最大行数行数据，笛卡尔积字段将不能完整返回！".format(row_num))
        cp_vv = cp_vv[:row_num]
        df_cartes = pd.DataFrame(cp_vv, columns=cp_names)
    else:
        df_cartes = pd.DataFrame(cp_vv, columns=cp_names)
        df_cartes = df_cartes.sample(n=row_num, replace=True).reset_index(drop=True)
        
    # 2. normal fields generation(常规字段生成)
    gen_calls = []
    cols = []
    for i, fp in enumerate(fun_params):
        cols.append("col_{0}".format(i+1))
        gen_calls.append("kwargs = {0} \ncol_{1} = gen.{2}(**kwargs)".format(fp.get("params"), i+1, fp.get("fun")))
    
    gen_calls = "\n".join(gen_calls)
    cols = ", ".join(cols)
    
    print(time.ctime(), "Start generating data")
    exec(gen_calls)
    
    # 3. cascade data generation(级联数据生成)
    cas_cols = {}
    if cascade != "N":
        for j, i in enumerate(cascade_params_lists):
            cascade_list = i.get("cascade_list")
            cascade_params = i.get("cascade_params")
            cas_tmp = gen.cascade_gen(cascade_list, cascade_params)
            cas_cols.update(cas_tmp)
    
    print(time.ctime(), "Data generation is finished, Start combining data")
    
    norm_cols = eval("dict(ChainMap(" + cols + "))")
    cas_cols.update(norm_cols)
    df = pd.DataFrame(cas_cols)
    ID = "序号" if locale_args == ['zh_CN'] else "ID"
    df[ID] = df.index + 1
    df = df.iloc[:, ::-1]
    df = df.join(df_cartes, rsuffix="_cartes")
    
    print("\nTotal time used(min): {}\n".format(round((time.time() - start)/60,2)))
    
    return df


def write_out(df, out_fn="out", file_type="CSV", encoding="utf-8",
              option="complex", zipped="N"):
    """
    write out the data, No zipped file for EXCEL and HTML type

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    out_fn : TYPE, optional
        DESCRIPTION. The default is "out".
    file_type : TYPE, optional
        DESCRIPTION. The default is "CSV".
    encoding : TYPE, optional
        DESCRIPTION. The default is "utf-8".
    option : TYPE, optional
        DESCRIPTION. The default is "complex".
    zipped : TYPE, optional
        DESCRIPTION. The default is "N".

    Returns
    -------
    None.

    """
    print(time.strftime("%Y-%m-%d %X", time.localtime()), "Writing the data!")

    # CSV file
    if file_type == "CSV" and zipped == "N":
        df.to_csv(out_fn+".csv", index=False, encoding=encoding)
    elif file_type == "CSV":
        compression_opts = dict(method='zip', archive_name=out_fn+'.csv')
        df.to_csv(out_fn+".zip", index=False, encoding=encoding,
                  compression=compression_opts)
    
    # EXCEL file
    elif file_type == "EXCEL":
        df.to_excel(out_fn+".xlsx", index=False, encoding=encoding)
    
    # JSON file
    elif file_type == "JSON" and zipped == "N":
            # simple model
        if option == "simple":
            df.to_json(out_fn+".json", orient='records',
                       force_ascii=False, indent=4, encoding=encoding)
        else:
            # complex model
            df.to_json(out_fn + ".json", orient='split',
                       force_ascii=False, index=False, indent=4,
                       encoding=encoding)
    elif file_type == "JSON":
        compression_opts = dict(method='zip', archive_name=out_fn+'.json')
        if option == "simple":
            df.to_json(out_fn+".zip", orient='records',
                       force_ascii=False, indent=4, encoding=encoding,
                       compression=compression_opts)
        else:
            df.to_json(out_fn + ".zip", orient='split',
                       force_ascii=False, index=False, indent=4,
                       encoding=encoding, compression=compression_opts)
    
    # HTML file
    elif file_type == "HTML":
        df.to_html(out_fn+".html", index=False, justify="left",
                   encoding=encoding)
    else:
        print('No such file type is provided!')


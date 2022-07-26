from redis import StrictRedis
import json
import glob

PRICE_DIVIDER=1e18
MAX_VALUE=0x3f3f3f3f

redis_conn = StrictRedis(host='127.0.0.1', port= 6379,decode_responses=True,charset='UTF-8', encoding='UTF-8')

#连接池方式连接Redis
# redis_pool = redis.ConnectionPool(host='127.0.0.1', port= 6379)
# redis_conn = redis.Redis(connection_pool= redis_pool)

#先清除目前Redis的数据便于测试
for key in redis_conn.keys():
    redis_conn.delete(key)

# 数据路径
filelists=glob.glob(".\data\*.json")
# 读取文件数据
for filelist in filelists:
    with open(filelist, encoding='UTF-8') as f:
        row_data = json.load(f)
        f.close()
    # 读取'data'这个key的数据并赋值给data_values
    data_values = row_data['data']
    list_of_nft_dict=[]
    for each_nft in data_values:
        address=each_nft['address']
        id=each_nft['id']
        priceInfo=each_nft['priceInfo']
        price=int(priceInfo['price'])/PRICE_DIVIDER
        #把数据按{key: address → value: { key: id → value: price}}格式存入Redis
        if redis_conn.hexists(address,id):
            if redis_conn.hget(address,id)!=price:
                redis_conn.hset(address,id,price)
        else:
            redis_conn.hset(address,id,price)

for address in redis_conn.keys():
#    print(address)
    min_price = MAX_VALUE
    collection_dict=redis_conn.hgetall(address)
    for id in collection_dict:
        price=float(collection_dict[id])
        if min_price>price:
            min_price=price
            min_id=id
    print(min_id,min_price)
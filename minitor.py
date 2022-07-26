import time
from redis import StrictRedis

MAX_VALUE=0x3f3f3f3f

redis = StrictRedis(host='localhost', port=6379,decode_responses=True,charset='UTF-8', encoding='UTF-8')

pubsub = redis.pubsub()

def event_handler(msg):
    print('Handler', msg)
    # handler=msg['data']
    # print(handler)
    # #本来是想通过返回的msg信息直接定位修改的id和price的，但是发现返回的msg里并不包含value里的值
    # if handler=='hset':
    #     address=msg['channel'][15:]
    #     collection_nft_dict=redis.hgetall(address)
    #     min_price = MAX_VALUE
    #     for id in collection_nft_dict:
    #         price=float(collection_nft_dict[id])
    #         if min_price>price:
    #             min_price=price
    #             min_id=id
    #     redis.hset(address,'floor_price',min_price)
    #     redis.hset(address,'floor_id',min_id)


pubsub.psubscribe(**{'__keyspace@0__:*': event_handler})

print('Starting message loop')
while True:
    message = pubsub.get_message()
    if message:
        print(message)
    else:
        time.sleep(0.01)
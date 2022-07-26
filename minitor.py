import time
from redis import StrictRedis

redis = StrictRedis(host='localhost', port=6379)

pubsub = redis.pubsub()

def event_handler(msg):
    def event_handler(msg):
        print('Handler', msg)
    #handler=msg['data']
    #本来是想通过返回的msg信息直接定位修改的id和price的，但是发现返回的msg里并不包含value里的值
    # if str(handler)=='hset':
    #     address=str(handler['channel'])[15:]
    #     redis.


pubsub.psubscribe(**{'__keyspace@0__:*': event_handler})

print('Starting message loop')
while True:
    message = pubsub.get_message()
    if message:
        print(message)
    else:
        time.sleep(0.01)
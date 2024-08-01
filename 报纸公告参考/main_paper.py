import traceback

import time
import api
import log
import paper

log.log_init(name="paper")
_time = 2

while True:
    _next = None
    try:
        # api.apiUrl = api.testUrl

        _param = {}
        _next = api.paper_queue_next(_param)
        # if _next is None:
        #     api.apiUrl = api.testUrl
        #     _next = api.corp_queue_next(_param)
        if _next is None:
            if _time < 60:
                _time = _time + 2
            continue
        _time = 2
        res = paper.deal_queue(queue=_next)
        if res is None:
            api.paper_queue_success(_next)
        else:
            _next["description"] = res
            api.paper_queue_fail(_next)
        time.sleep(1)
    except Exception as err:
        log.base.error(str(err))
        traceback.print_exc()
        if _next is not None:
            _next["description"] = str(err)
            api.paper_queue_fail(_next)
        time.sleep(1)
    finally:
        time.sleep(_time)

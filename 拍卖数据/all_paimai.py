from 阿里拍卖 import ali_paimai
from api_paimai import paper_queue_next, paper_queue_success

# value = paper_queue_next(webpage_url_list=["https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?disableNav=YES&page=1&pmid=2175852518_1653962822378&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879&path=27181431,27076131,25287064,27064540&spm=a2129.27064540.puimod-zc-focus-2021_2860107850.category-4-5&fcatV4Ids=[%22206067301%22]"])
# queue_id = value['id']
ali_paimai("1234")
# success_data = {
#                 'id': queue_id,
#                 'description': '数据获取成功',
#             }
# paper_queue_success(success_data)



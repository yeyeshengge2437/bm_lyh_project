# -*- coding: utf-8 -*-
from wechat_ocr.ocr_manager import OcrManager, OCR_MAX_TASK_ID

wechat_ocr_dir = r"C:\Users\24379\AppData\Roaming\Tencent\WeChat\XPlugin\Plugins\WeChatOCR\7079\extracted\WeChatOCR.exe"
wechat_dir = "C:\Program Files\Tencent\WeChat\[3.9.12.17]"
value = []


def ocr_result_callback(img_path: str, results: dict):
    data = results["ocrResult"]
    value.append(data)
    # return results["ocrResult"]


def main(ocr_manager, image_paths):
    for image_path in image_paths:
        ocr_manager.DoOCRTask(image_path)
    while ocr_manager.m_task_id.qsize() != OCR_MAX_TASK_ID:
        pass
    ocr_manager.KillWeChatOCR()



def identify_results(image_paths):
    """

    :param image_paths: 为列表
    :return:
    """
    ocr_manager = OcrManager(wechat_dir)
    # 设置WeChatOcr目录
    ocr_manager.SetExePath(wechat_ocr_dir)
    # 设置微信所在路径
    ocr_manager.SetUsrLibDir(wechat_dir)
    # 设置ocr识别结果的回调函数
    ocr_manager.SetOcrResultCallback(ocr_result_callback)
    # 启动ocr服务
    ocr_manager.StartWeChatOCR()
    code_lst = []
    main(ocr_manager, image_paths)
    return value


# print(identify_results("pdf_images_width_plus/page1_image1.jpeg"))
# print(identify_results(["pdf_images_width_plus/page1_image1.jpeg", "pdf_images_width_plus/page2_image1.jpeg"]))

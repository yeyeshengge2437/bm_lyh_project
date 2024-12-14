from DrissionPage import ChromiumPage, ChromiumOptions
import cv2

image = cv2.imread('img_2.png')
detector = cv2.QRCodeDetector()
data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
if data:
    print("检测到 QR 码，数据:", data)
else:
    print("未检测到 QR 码")
# page = ChromiumPage()
# page.set.download_path('D:\PYdata\BaiMi_project\公众号文章抓取')
# page.get(data)
# page.wait(2)
# page.ele("xpath=//i[contains(@class, 'docxiazai')]").click(by_js=True)
# # input()
# page.close()

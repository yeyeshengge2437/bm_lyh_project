from DrissionPage import ChromiumPage, ChromiumOptions
import cv2

image = cv2.imread('qrcode.png')
detector = cv2.QRCodeDetector()
data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
if data:
    print("QR Code detected, data:", data)
else:
    print("QR Code not detected")
page = ChromiumPage()
page.set.download_path('D:\PYdata\BaiMi_project\公众号文章抓取')
page.get(data)
page.wait(2)
page.ele("xpath=//i[contains(@class, 'docxiazai')]").click(by_js=True)
input()
page.close()

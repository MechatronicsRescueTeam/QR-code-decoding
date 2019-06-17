# uvoz potrebnih knjižnic 
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
 
# konstrukcija razčlenjevalnika argumentov in razčlenitev argumentov
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# initalizacija video prenosa
print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
vs = VideoStream(1).start()
time.sleep(2.0)
 
# odpiranje CSV dokumenta v katerega se bodo shranile najdene kode QR
csv = open(args["output"], "w")
found = set()

# glavna zanka
while True:
	# sprememba velikosti videa tako, da je maksimalna širina videa  
	# 400 slikovnih pik
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
 
	# iskanje kod v vsaki sliki videa in dešifriranje vseh kod
	barcodes = pyzbar.decode(frame)

	# loop over the detected barcodes
	for barcode in barcodes:
		# risanje kvadratov okoli zaznanih kod QR na sliki
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type
 
		# pisanje besedila, ki ga predstavlja posamezna koda QR
		text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		
		# če besedila kode še ni v CSV datoteki, zapišemo
		# časovni žig + kodo na disk
		if barcodeData not in found:
			csv.write("{},{}\n".format(datetime.datetime.now(),
				barcodeData))
			csv.flush()
			found.add(barcodeData)
			cv2.imwrite(str(barcodeData) + ".jpg", frame)
	# prikaz slike izhoda
	cv2.imshow("Barcode Scanner", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# če pritisnemo tipko "q" se zanka prekine
	if key == ord("q"):
		break
 
# zaprtje CSV datoteke
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()

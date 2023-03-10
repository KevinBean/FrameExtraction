import cv2
import config
import numpy as np
import time


cap = cv2.VideoCapture(config.videoPath)
success, frame = cap.read()
count = 0
success = True
prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

skip_frames = 600  # skip every other frame
counter = 0

# Calculate the threshold value based on 60% of total pixels
threshold = 0.008 * 0.008 * frame.shape[0] * frame.shape[1]
print(threshold)
while True:
    if counter % (skip_frames + 1) != 0:
        success = cap.grab()

        if not success:
            break
    else:
        print(counter)
        success, frame = cap.retrieve()
        if not success:
            break

        curr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(curr_frame, prev_frame)

        _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.erode(thresh, kernel, iterations=1)
        cnts, _ = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in cnts:
            if cv2.contourArea(contour) < 5000:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imwrite("frames/%d.png" % count, frame)
            print('Motion detected')
            print('%d. frame exported.' % count)
            count += 1
        # cv2.imshow('frame', frame)
        prev_frame = curr_frame
        cv2.waitKey(1)
    counter += 1

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# while success:
#   success,image = vidcap.read()

#   if not success:
#     break

#   cv2.imwrite("frames/%d.png" % count, image)
#   cv2.waitKey(1)
#   print('%d. frame exported.' % count)
#   count += 1
cap.release()
print('Frames exported to files successfully.')

import os
import cv2
import utils

# training_data 폴더 생성 및 그 내부에 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 폴더 생성
image = cv2.imread("images/3.png")
chars = utils.extract_chars(image)

for char in chars:
    cv2.imshow('Image', char[1])
    input = cv2.waitKey(0)
    resized = cv2.resize(char[1], (20, 20))

    if 48 <= input <= 57:  # 0 ~ 9
        name = str(input - 48)
        # os.walk는 하위의 폴더들을 탐색할 수 있게 해줍니다. (root, dirs, files)
        file_count = len(next(os.walk('./training_data/' + name + '/'))[2])
        cv2.imwrite('./training_data/' + str(input - 48) + '/' + str(file_count + 1) + '.png', resized)
    elif input == ord('a') or input == ord('b') or input == ord('c'):  # +, -, *
        name = str(input - ord('a') + 10)
        file_count = len(next(os.walk('./training_data/' + name + '/'))[2])
        cv2.imwrite('./training_data/' + str(input - ord('a') + 10) + '/' + str(file_count + 1) + '.png', resized)
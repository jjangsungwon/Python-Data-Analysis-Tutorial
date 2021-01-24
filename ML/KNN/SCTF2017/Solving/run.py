import numpy as np
import cv2
import utils
import requests
import shutil



FILE_NAME = "trained.npz"

# 각 글자의 (1 x 400) 데이터와 정답 (0 ~ 9, +, -, *)
with np.load(FILE_NAME) as data:
    train = data['train']
    train_labels = data['train_labels']
    knn = cv2.ml.KNearest_create()
    knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)


def check(test, train, train_labels):
    # 가장 가까운 K개의 글자를 찾아, 어떤 숫자에 해당하는지 찾습니다.
    ret, result, neighbors, dist = knn.findNearest(test, k=1)  # 각 숫자는 비슷한 모양이라 K = 1로 설정
    return result


def get_result(file_name):
    image = cv2.imread(file_name)
    chars = utils.extract_chars(image)
    result_string = ""
    for char in chars:
        matched = check(utils.resize20(char[1]), train, train_labels)
        if matched < 10:
            result_string += str(int(matched))
            continue
        if matched == 10:
            matched = '+'
        elif matched == 11:
            matched = '-'
        elif matched == 12:
            matched = '*'
        result_string += matched
    return result_string


host = "http://localhost:5000"
url = '/start'

# target_images 폴더 생성
with requests.Session() as s:
    answer = ''
    for i in range(0, 100):
        params = {'ans': answer}

        # 정답을 파라미터에 달아서 전송하여, 이미지 경로를 받아옵니다.
        response = s.post(host + url, params)
        print('Server Return:' + response.text)
        if i == 0:
            returned = response.text
            image_url = host + returned
            url = '/check'
        else:
            returned = response.json()
            # print(host, returned['url'])
            print(returned)
            image_url = host + returned['url']
        print('Problem ' + str(i) + ': ' + image_url)

        # 특정한 폴더에 이미지 파일을 다운로드 받습니다.
        response = s.get(image_url, stream=True)
        target_image = './target_images/' + str(i) + '.png'
        with open(target_image, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        # 다운로드 받은 이미지 파일을 분석하여 답을 도출합니다.
        answer_string = get_result(target_image)
        print('String: ' + answer_string)
        answer_string = utils.remove_first_0(answer_string)
        answer = str(eval(answer_string))
        print('Answer: ' + answer)
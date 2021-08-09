import albumentations as A
import cv2
import matplotlib.pyplot as plt
import os

path_save = "D:/Project/MachineLearning/NhanDienLogo/datasets/LogoTM/"

def visualize(image):
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)
    plt.show()

def aug(image):
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    transform = A.Compose(
        [
         A.CLAHE(),
         A.RandomRotate90(),
         A.Transpose(),
         A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.0,
                            rotate_limit=180),
         A.Blur(blur_limit=3),
         A.OpticalDistortion(),
         A.GridDistortion(),
         #A.HueSaturationValue()
         ])

    augmented_image = transform(image=image)['image']
    #visualize(augmented_image)
    return augmented_image

for i in range(14):
    allfile = os.listdir(path_save + str(i) + "/")
    sizefix = (700 - len(allfile))//3
    print(sizefix)
    size = []
    for file in allfile:
        img = cv2.imread(path_save + str(i) + "/" + file)
        size.append(img.shape[0])
    _, filesort = zip(*sorted(zip(size, allfile), reverse=True))
    for j in range(sizefix):
        image = cv2.imread(path_save + str(i) + "/" + filesort[j])
        for k in range(3):
            img = aug(image)
            name_file = filesort[j].split(".")[0]
            cv2.imwrite(path_save + str(i) + "/" + name_file  + "_" + str(k) + ".jpg", img)

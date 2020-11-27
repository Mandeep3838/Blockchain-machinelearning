from mnist import MNIST

mndata = MNIST('samples')

images,labels = mndata.load_training()
print(len(images))
print(len(labels))

images_t, labels_t = mndata.load_testing()
print(images_t.shape)
print(labels_t.shape)
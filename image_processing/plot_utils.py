from matplotlib import pyplot as plt


def plot_image(image, title):
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.title(title)
    plt.axis()
    plt.show()

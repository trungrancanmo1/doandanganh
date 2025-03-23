import matplotlib.pyplot as plt


def draw_temperature_chart():
    # fetch data from firestore
    data = [1, 2, 3, 4, 5]
    plt.figure(num='temperature', figsize=(500, 500))
    plt.plot(data=data)
    # save and store the image ???
    # plt.savefig('')
    plt.xlabel(xlabel='Time')
    plt.ylabel(ylabel='Temperature')
    plt.show()


def draw_light_chart():
    pass


def draw_humidity():
    pass


if __name__ == '__main__':
    # test packages
    pass
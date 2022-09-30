import matplotlib.pyplot as plt


fpr = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.045454545454545456, 0.045454545454545456, 0.09090909090909091, 0.13636363636363635, 0.18181818181818182, 0.18181818181818182, 0.36363636363636365, 1.0]
tpr = [0.0, 0.6666666666666666, 0.7222222222222222, 0.8055555555555556, 0.8333333333333334, 0.8888888888888888, 0.9166666666666666, 0.9166666666666666, 0.9444444444444444, 0.9444444444444444, 0.9722222222222222, 0.9722222222222222, 1.0, 1.0, 1.0]

# predicting of lr
fpr_lr = [0.0, 0.0, 0.0, 0.015625, 0.015625, 0.03125, 0.03125, 0.046875, 0.046875, 0.0625, 0.0625, 0.078125, 0.078125, 0.09375, 0.09375, 0.125, 0.125, 0.140625, 0.140625, 0.21875, 0.21875, 0.28125, 0.28125, 1.0]
tpr_lr = [0.0, 0.009259259259259259, 0.1574074074074074, 0.1574074074074074, 0.8611111111111112, 0.8611111111111112, 0.8888888888888888, 0.8888888888888888, 0.9074074074074074, 0.9074074074074074, 0.9351851851851852, 0.9351851851851852, 0.9444444444444444, 0.9444444444444444, 0.9537037037037037, 0.9537037037037037, 0.9722222222222222, 0.9722222222222222, 0.9814814814814815, 0.9814814814814815, 0.9907407407407407, 0.9907407407407407, 1.0, 1.0]

plt.plot(fpr, tpr)
plt.show()

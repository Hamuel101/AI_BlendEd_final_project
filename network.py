# importing nessessary files
import numpy as np
import matplotlib.pyplot as plt


class Network:
    # network class
    def __init__(self, loss_func):
        # creating the network
        self.layers = []
        self.loss = None
        self.dloss = None
        self.loss_func = loss_func

    def add(self, layer):
        # adding a layer to the network
        self.layers.append(layer)

    def forward_prop(self, inputs, test=False):
        # calls the forward prop function of each layer
        for layer in self.layers:
            output = layer.forward_prop(inputs, test=test)
            inputs = output
        self.output = output
        return output

    def Qloss(self, state, move):
        # gets the loss
        self.loss, self.dloss = self.loss_func(state, move)

    def Qback_prop(self, LR=0.01):
        # back props through the whole netork
        for layer in reversed(self.layers):
            self.dloss = layer.back_prop(self.dloss)

    # none of the following code is used in the agent, all of it is just here as failed attempts
    def Qtrain(self, x_train, y_train, x_test, y_test, epochs=25_000, LR=0.01):
        self.train_loss = []
        self.train_epoch = []
        self.test_loss = []
        self.test_epoch = []
        for epoch in range(epochs):
            outputs = self.forward_prop(x_train)
            self.loss, self.dloss = self.loss_func(y_train, outputs)
            self.back_prop(LR)
            self.train_loss.append(np.mean(self.loss))
            self.train_epoch.append(epoch)
            if epoch % 10 == 0:
                test_loss = self.test(x_test, y_test)
                self.test_loss.append(np.mean(test_loss))
                self.test_epoch.append(epoch)
            if epoch % 1000 == 0:
                print("for epoch: {} the loss is {}".format(epoch, np.mean(self.loss)))
        print("the final error is: {}".format(np.mean(self.loss)))

        plt.figure(figsize=(15, 5))
        plt.plot(self.train_epoch, self.train_loss, label="train")
        plt.plot(self.test_epoch, self.test_loss, label="test")
        plt.xlabel("Epoch")
        plt.ylabel("Error")
        plt.legend()
        plt.show()

    def back_prop(self, LR=0.01):
        for layer in reversed(self.layers):
            self.dloss = layer.back_prop(self.dloss, LR)

    def test(self, x_test, y_test, text=False):
        outputs = self.forward_prop(x_test, test=True)
        if text == True:
            for i in range(len(outputs)):
                print(
                    "{}    {}    {}".format(np.round(outputs[i]), y_test[i], outputs[i])
                )
        test_loss, test_dloss = self.loss_func(y_test, outputs)
        return test_loss

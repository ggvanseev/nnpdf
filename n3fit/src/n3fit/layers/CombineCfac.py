import tensorflow as tf
from tensorflow.keras.layers import Layer


class CombineCfacLayer(Layer):
    """
    Creates the combination layer of SIMUnet. 
    """

    def __init__(self, ncfacs):
        # Initialise a Layer instance
        super().__init__()

        init_value = tf.random_normal_initializer()
        self.w = tf.Variable(
            initial_value=init_value(shape=(ncfacs,), dtype="float32"),
            trainable=True,
        )

    def __call__(self, inputs, cfactor_values):
        return (1 + tf.reduce_sum(self.w[:, tf.newaxis] * cfactor_values, axis=0)) * inputs

import tensorflow as tf
from tensorflow.keras.layers import Layer


class CombineCfacLayer(Layer):
    """
    Creates the combination layer of SIMUnet. 
    """

    def __init__(self, ncfacs):
        """
        Parameters
        ----------
            ncfacs: number
                it is the number of Wilson coefficients that we are fitting 
        """
        # Initialise a Layer instance
        super().__init__()
        # Initialise a layer with `ncfacs` trainable edges
        # where `ncfacs` is the number of Wilson coefficients
        # to train.

        init_value = tf.random_normal_initializer()
        self.w = tf.Variable(
            initial_value=init_value(shape=(ncfacs,), dtype="float32"),
            trainable=True,
        )

    def __call__(self, inputs, cfactor_values):
        """
        Makes the forward pass.
        Parameters
        ----------
            inputs: number
                This is the SM theoretical prediction that comes after the FK convolution.
            cfactor_values: number
                This is a SMEFT C-factor stored in the theoryid. 
        Returns
        -------
            output: number
                This gives the SMEFT affected theoretical prediction
        """

        return (1 + tf.reduce_sum(self.w[:, tf.newaxis] * cfactor_values, axis=0)) * inputs

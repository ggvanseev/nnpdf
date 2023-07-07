from n3fit.backends import MetaLayer
from n3fit.backends import constraints
from n3fit.backends import operations as op


class Preprocessing(MetaLayer):
    """
    Computes preprocessing factor for the PDF.

    This layer generates a factor (1-x)^beta*x^(1-alpha) where both beta and alpha
    are model paramters that can be trained. If feature scaling is used, the preprocessing
    factor is x^(1-alpha).

    Alpha is initialized uniformly within the ranges allowed in the runcard and
    then it is only allowed to move between those two values (with a hard wall in each side)

    Alpha and, unless feature scaling is used, beta are initialized uniformly within
    the ranges allowed in the runcard and then they are only allowed to move between those two
    values (with a hard wall in each side)

    Parameters
    ----------
        flav_info: list
            list of dicts containing the information about the fitting of the preprocessing factor
            This corresponds to the `fitting::basis` parameter in the nnpdf runcard.
            The dicts can contain the following fields:
                `smallx`: range of alpha
                `largex`: range of beta
                `trainable`: whether these alpha-beta should be trained during the fit
                            (defaults to true)
        large_x: bool
            Whether large x preprocessing factor should be active
        seed: int
            seed for the initializer of the random alpha and beta values
    """

    def __init__(
        self,
        flav_info: list = None,
        seed: int = 0,
        large_x: bool = True,
        **kwargs,
    ):
        if flav_info is None:
            raise ValueError(
                "Trying to instantiate a preprocessing factor with no basis information"
            )
        self.flav_info = self._format_info(flav_info)
        self.num_flavors = len(flav_info)
        self.seed = seed
        self.initializer = "random_uniform"
        self.large_x = large_x

        self.alphas = []
        self.betas = []
        super().__init__(**kwargs)

    def generate_weight(self, name: str, kind: str, set_to_zero: bool = False):
        """
        Generates weights according to the flavour dictionary

        Parameters
        ----------
            name: str
                name to be given to the generated weight
            kind: str
                where to find the limits of the weight in the dictionary
            set_to_zero: bool
                set the weight to constant 0
        """
        constraint = None
        if set_to_zero:
            initializer = MetaLayer.init_constant(0.0)
            trainable = False
        else:
            minvals = self.flav_info[kind]['min']
            maxvals = self.flav_info[kind]['max']
            trainable = self.flav_info['trainable']
            # Set the initializer and move the seed one up
            initializer = MetaLayer.select_initializer(
                self.initializer, minval=minvals, maxval=maxvals, seed=self.seed
            )
            self.seed += 1
            # If we are training, constrain the weights to be within the limits
            if trainable:
                constraint = lambda w: op.clamp(w, minvals, maxvals)

        # Generate the new trainable (or not) parameter
        kernel_shape=(self.num_flavors,)
        newpar = self.builder_helper(
            name=name,
            kernel_shape=kernel_shape,
            initializer=initializer,
            trainable=trainable,
            constraint=constraint,
        )
        return newpar

    @staticmethod
    def create_constraint(self, minvals, maxvals):
        return lambda w: tf.reduce_min(tf.reduce_max(w, minvals), maxvals)

    def build(self, input_shape):
        self.alphas = self.generate_weight(name='alphas', kind='smallx')
        self.betas = self.generate_weight(name='betas', kind='largex', set_to_zero=not self.large_x)

        super(Preprocessing, self).build(input_shape)

    def call(self, x):
        """
        Compute preprocessing prefactor.

        Parameters
        ----------
            x: tensor(shape=[1,N,1])

        Returns
        -------
            prefactor: tensor(shape=[1,N,F])
                prefactors for the single batch dimension, all gridpoints, all flavors,
        """
        return x ** (1 - self.alphas) * (1 - x) ** self.betas

    @staticmethod
    def _format_info(flav_info):
        "Helper function that ideally becomes obsolete if flav_info format is changed"
        smallx_min = []
        smallx_max = []
        largex_min = []
        largex_max = []
        # have to restrict to either all trainable or none trainable
        trainable = True
        for flav_dict in flav_info:
            smallx_min.append(flav_dict["smallx"][0])
            smallx_max.append(flav_dict["smallx"][1])
            largex_min.append(flav_dict["largex"][0])
            largex_max.append(flav_dict["largex"][1])
            trainable = trainable and flav_dict.get("trainable", True)
        return {
            "smallx": {
                "min": op.numpy_to_tensor(smallx_min),
                "max": op.numpy_to_tensor(smallx_max),
            },
            "largex": {
                "min": op.numpy_to_tensor(largex_min),
                "max": op.numpy_to_tensor(largex_max),
            },
            "trainable": trainable,
        }

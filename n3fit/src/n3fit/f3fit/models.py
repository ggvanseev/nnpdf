import sys
from n3fit.layers import Preprocessing
from n3fit.backends import MetaLayer
from n3fit.backends.keras_backend.constraints import MinMaxWeight
from n3fit.backends import operations as op 

def tiny(): 
   return sys.float_info.min
def huge():
   return sys.float_info.max

class f3fit_model(MetaLayer):
   def __init__(self, model_name, seed=0, initializer="random_uniform", **kwargs): 
      self.model_name = model_name
      self.seed = seed
      self.output_dim = self.get_model_output_dim(model_name)
      self.initializer = initializer
      self.kernel = []
      super().__init__(**kwargs)

   def __config__(self):
      config = super().get_config()
      config.update({"model": self.model_name})
      config.update({"seed": self.seed})
      config.update({"initializer": self.initializer})
      return config

   def generate_weight(self, weight_name, ldo=tiny(), lup=huge(), trainable=True):
      initializer = MetaLayer.select_initializer(
              self.initializer, minval=ldo, maxval=lup, seed=self.seed)
      self.seed += 1
      # If we are training, constrain the weights to be within the limits
      weight_constraint = MinMaxWeight(ldo, lup)
      newpar = self.builder_helper(
         name=weight_name,
         kernel_shape=(1,),
         initializer=initializer,
         trainable=trainable,
         constraint=weight_constraint,
      )
      self.kernel.append(newpar)

   def build(self, input_shape):
      if self.model_name == "dummy": self.gen_wgt_dummy_model()
      super(f3fit_model, self).build(input_shape)

   def call(self, inputs, **kwargs):
      x = inputs[:,:,0:1]
      if self.model_name == "dummy": pdf_list = self.dummy_pdf_list(x)
      return op.concatenate(pdf_list, axis=-1)

# Dummy PDF model for testing etc
   def get_model_output_dim(self, model_name):
      if model_name == "dummy": return 8

   def gen_wgt_dummy_model(self):
      self.generate_weight("par1",-1,1)
      self.generate_weight("par2",-1,1)

   def dummy_pdf_list(self, x):
      pdf_list = []
      a = self.kernel[0][0]
      b = self.kernel[1][0]
      for i in range(8): pdf_list.append(x**a*(1-x)**b)
      return pdf_list

# A preprocessing layer
class f3Preproc(Preprocessing):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)

   def build(self, input_shape):
       # Run through the whole basis
       super(Preprocessing, self).build(input_shape)

   def call(self, inputs, **kwargs):
      x = inputs
      pdf_list = []
      for i in range(0,8):
         pdf_list.append(x)
      return op.concatenate(pdf_list, axis=-1)


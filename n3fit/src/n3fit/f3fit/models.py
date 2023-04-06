import sys
from n3fit.layers import Preprocessing
from n3fit.backends import MetaLayer
from n3fit.backends.keras_backend.constraints import MinMaxWeight
from n3fit.backends import operations as op 
from tensorflow.math import log

def tiny(): 
   return sys.float_info.min
def huge():
   return sys.float_info.max

class f3fit_model(MetaLayer):
   def __init__(self, model_name, seed=1, initializer="random_uniform", **kwargs): 
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
      if self.model_name == "hera": self.gen_wgt_hera_model()
      super(f3fit_model, self).build(input_shape)

   def call(self, inputs, **kwargs):
      x = inputs
      if self.model_name == "dummy": pdf_list = self.dummy_pdf_list(x)
      if self.model_name == "hera": pdf_list = self.hera_pdf_list(x)
      return op.concatenate(pdf_list, axis=-1)

# Dummy PDF model for testing etc
   def get_model_output_dim(self, model_name):
      if model_name == "dummy": return 8
      if model_name == "hera" : return 7 

   def gen_wgt_dummy_model(self):
      self.generate_weight("par1",-1,1)
      self.generate_weight("par2",-1,1)

   def dummy_pdf_list(self, x):
      pdf_list = []
      a = self.kernel[0][0]
      b = self.kernel[1][0]
      for i in range(8): pdf_list.append(x**a*(1-x)**b)
      return pdf_list

# Add the hera pdf
   def gen_wgt_hera_model(self):
      self.generate_weight("Bg",0.03,4)
      self.generate_weight("Cg",2,25)
      self.generate_weight("Fg",0.01,6.0)
      self.generate_weight("Gg",0.01,5)
      self.generate_weight("Buv",0.13,5.89)
      self.generate_weight("Cuv",0.4,10.8)
      self.generate_weight("Euv",0.1,6.8)
      self.generate_weight("Fuv",0.0,9)
      self.generate_weight("Guv",0.01,5.97)
      self.generate_weight("Bdv",0.05,3.05)
      self.generate_weight("Cdv",1.6,8.8)
      self.generate_weight("Aubar",0.01,3.2)
      self.generate_weight("Bubar",-2.5,3.2)
      self.generate_weight("Cubar",1,31)
      self.generate_weight("Dubar",5,100)
      self.generate_weight("Fubar",0.01,3.09)
      self.generate_weight("Cdbar",5,60)
      self.generate_weight("Ddbar",5,128)

   def hera_pdf_list(self, x):
      pdf_list = []

      Bg    = self.kernel[0][0]
      Cg    = self.kernel[1][0]    
      Fg    = self.kernel[2][0]
      Gg    = self.kernel[3][0]

      Buv   = self.kernel[4][0]
      Cuv   = self.kernel[5][0] 
      Euv   = self.kernel[6][0] 
      Fuv   = self.kernel[7][0] 
      Guv   = self.kernel[8][0] 

      Bdv   = self.kernel[9][0]
      Cdv   = self.kernel[10][0]

      Aubar = self.kernel[11][0]
      Bubar = self.kernel[12][0] 
      Cubar = self.kernel[13][0] 
      Dubar = self.kernel[14][0] 
      Fubar = self.kernel[15][0] 

      Adbar = Aubar
      Bdbar = Bubar
      Cdbar = self.kernel[16][0]
      Ddbar = self.kernel[17][0]
      Fdbar = Fubar

      pdf_list.append(x**(Buv)   *(1-x)**Cuv   *(1+Euv*x**2 +Fuv*log(x) +Guv * log(x)**2)) 
      pdf_list.append(Aubar*x**(Bubar) *(1-x)**Cubar *(1+Dubar*x+Fubar*log(x)))
      pdf_list.append(x**(Bdv)   *(1-x)**Cdv)
      pdf_list.append(Adbar*x**(Bdbar) *(1-x)**Cdbar *(1+Ddbar*x+Fdbar*log(x)))
      pdf_list.append(0.4/(1-0.4) * Adbar * x**(Bdbar) *(1-x)**Cdbar *(1+Ddbar*x+Fdbar*log(x)))
      pdf_list.append(0.4/(1-0.4) * Adbar * x**(Bdbar) *(1-x)**Cdbar *(1+Ddbar*x+Fdbar*log(x)))
      pdf_list.append(x**(Bg)    *(1-x)**Cg    *(1+Fg*log(x) +Gg*log(x)**2))
      return pdf_list

# A preprocessing layer
class f3Preproc(Preprocessing):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)

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
       # Run through the whole basis
      super(Preprocessing, self).build(input_shape)

   def call(self, inputs, **kwargs):
      x = inputs
      pdf_list = []

      pdf_list.append(x/x)
      pdf_list.append(x/x)
      pdf_list.append(x/x)
      pdf_list.append(x/x)
      pdf_list.append(x/x)
      pdf_list.append(x/x)
      pdf_list.append(x/x)

      return op.concatenate(pdf_list, axis=-1)


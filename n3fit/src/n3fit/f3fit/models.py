import sys
import logging
from n3fit.layers import Preprocessing
from n3fit.backends import constraints
from n3fit.backends import MetaLayer
from n3fit.backends.keras_backend.constraints import MinMaxWeight
from n3fit.backends import operations as op 
from tensorflow.math import log, sqrt
from tensorflow import constant as tfconstant
from tensorflow import print as tfprint


logger = logging.getLogger(__name__)

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

   # This function takes a string with the name of a weight as an input
   # and return the corresponding tensorflow variabel.
   def get_wgt(self, string):
      for i in range(len(self.kernel)):
         if '/'+string+':' in self.kernel[i].name : return self.kernel[i][0]
      logger.error(f"Weight %s does not exist", string)
      return 0



   def build(self, input_shape):
      if self.model_name == "dummy": self.gen_wgt_dummy_model()
      if self.model_name == "hera": self.gen_wgt_hera_model()
      if self.model_name == "cteq": self.gen_wgt_cteq_model()
      super(f3fit_model, self).build(input_shape)

   def call(self, inputs, **kwargs):
      x = inputs
      if self.model_name == "dummy": pdf_list = self.dummy_pdf_list(x)
      if self.model_name == "hera": pdf_list = self.hera_pdf_list(x)
      if self.model_name == "cteq": pdf_list = self.cteq_pdf_list(x)
      return op.concatenate(pdf_list, axis=-1)

# Dummy PDF model for testing etc
   def get_model_output_dim(self, model_name):
      if model_name == "dummy": return 8
      if model_name == "hera" : return 7 
      if model_name == "cteq" : return 7 

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
      self.generate_weight("Fg",0.01,6.0)
      self.generate_weight("Gg",0.01,5)
      self.generate_weight("Euv",0.1,6.8)
      self.generate_weight("Fuv",0.0,9)
      self.generate_weight("Guv",0.01,5.97)
      self.generate_weight("Dubar",5,100)
      self.generate_weight("Fubar",0.01,3.09)
      self.generate_weight("Ddbar",5,128)

   def hera_pdf_list(self, x):
      pdf_list = []

      Fg    = self.kernel[0][0]
      Gg    = self.kernel[1][0]

      Euv   = self.kernel[2][0] 
      Fuv   = self.kernel[3][0] 
      Guv   = self.kernel[4][0] 

      Dubar = self.kernel[5][0] 
      Fubar = self.kernel[6][0] 

      Ddbar = self.kernel[7][0]
      Fdbar = Fubar

      pdf_list.append((1+Euv*x**2 +Fuv*log(x) +Guv * log(x)**2)) 
      pdf_list.append(x/x)
      pdf_list.append((1+Dubar*x+Fubar*log(x))) # Aubar removed
      pdf_list.append(1+Ddbar*x+Fdbar*log(x)) # Adbar removed
      pdf_list.append(0.4/(1-0.4) *(1+Ddbar*x+Fdbar*log(x))) #Adbar removed
      pdf_list.append(0.4/(1-0.4) *(1+Ddbar*x+Fdbar*log(x))) #Adbar removed
      pdf_list.append(1+Fg*log(x) +Gg*log(x)**2)
      return pdf_list

   def gen_wgt_cteq_model(self):
      # generate the 8 Parameters for each of the valence quarks
      # Two of the eight parameters are defined in the preprocessing layer.
      # This model layer will only contain the coefficients of the 
      # polynomials
      self.generate_weight("c0_uv",-2,2.1)
      self.generate_weight("c1_uv",-2,2.1)
      self.generate_weight("c2_uv",-2,2.1)

      self.generate_weight("c0_dv",-2,2.1)
      self.generate_weight("c1_dv",-2,2.1)
      self.generate_weight("c2_dv",-2,2.1)
      
      # generate the parameters for the seaquarks
      
      self.generate_weight("b1_u",-2,2.1)
      self.generate_weight("b2_u",-2,2.1)
      self.generate_weight("b3_u",-2,2.1)
      self.generate_weight("b4_u",-2,2.1)
      
      self.generate_weight("b1_d",-2,2.1)
      self.generate_weight("b2_d",-2,2.1)
      self.generate_weight("b3_d",-2,2.1)
      self.generate_weight("b4_d",-2,2.1)
      

      self.generate_weight("g0",-2,0.1)
      self.generate_weight("e0",-2,0.1)
      self.generate_weight("e1",-2,0.1)

      self.generate_weight("a1_g",0.1,1.6)
      self.generate_weight("a2_g",2,11)
      self.generate_weight("a1_uv",0.1,1.0)
      self.generate_weight("a2_uv",0,10)
      self.generate_weight("a1_ubar",-0.2,2)
      self.generate_weight("a2_ubar",1,9)
      self.generate_weight("a2_dbar",1,9)

      self.generate_weight("c_s",0.01,2.0)
      self.generate_weight("a2_s",1,9)

   def cteq_pdf_list(self, x):
      pdf_list = []

      a1_uv = self.get_wgt("a1_uv")
      a1_dv = a1_uv
      a2_uv = self.get_wgt("a2_uv")
      a2_dv = a2_uv
      a1_ubar = self.get_wgt("a1_ubar")
      a1_dbar = a1_ubar
      a2_ubar = self.get_wgt("a2_ubar")
      a2_dbar = self.get_wgt("a2_dbar")
      a1_s    = a1_ubar
      a1_sbar = a1_ubar
      a2_s = self.get_wgt("a2_s")
      a2_sbar = a2_s
      a1_g = self.get_wgt("a1_g")
      a2_g = self.get_wgt("a2_g")

      c0_uv = self.get_wgt("c0_uv") 
      c1_uv = self.get_wgt("c1_uv")
      c2_uv = self.get_wgt("c2_uv")
      c3_uv = 1 + a1_uv /2
      c0_dv = self.get_wgt("c0_dv")
      c1_dv = self.get_wgt("c1_dv")
      c2_dv = self.get_wgt("c2_dv")
      c3_dv = 1 + a1_dv /2
      b1_u = self.get_wgt("b1_u")
      b2_u = self.get_wgt("b2_u")
      b3_u = self.get_wgt("b3_u")
      b4_u = self.get_wgt("b4_u")
      b1_d = self.get_wgt("b1_d")
      b2_d = self.get_wgt("b2_d")
      b3_d = self.get_wgt("b3_d")
      b4_d = self.get_wgt("b4_d")
      c_s   = self.get_wgt("c_s") 
      g0 = self.get_wgt("g0")
      e0 = self.get_wgt("e0")
      e1 = self.get_wgt("e1")

      y = sqrt(x)
      z = 2*sqrt(x)-x
      pdf_list.append(x**a1_uv *(1-x)**a2_uv *(c0_uv*(1-y)**4 +c1_uv*4*y*(1-y)**3 +c2_uv*6*y**2 *(1-y)**2 +c3_uv*4*y**3*(1-y) +y**4))
#      pdf_list.append(x**a1_ubar *(1-x)**a2_ubar *(b1_u*z + b2_u*z**2 + b3_u*z**3 + b4_u*z**4))
      pdf_list.append(x**a1_ubar *(1-x)**a2_ubar *(b1_u*(1-z)**4 + b2_u*4*z*(1-z)**3 + b3_u*6*z**2*(1-z)**2 + b4_u*z**4))
      pdf_list.append(x**a1_dv *(1-x)**a2_dv *(c0_dv*(1-y)**4 +c1_dv*4*y*(1-y)**3 +c2_dv*6*y**2 *(1-y)**2 +c3_dv*4*y**3*(1-y) +y**4))
      pdf_list.append(x**a1_dbar *(1-x)**a2_dbar *(b1_d*(1-z)**4 + b2_d*4*z*(1-z)**3 + b3_d*6*z**2*(1-z)**2 + b4_d*z**4))
#      pdf_list.append(x**a1_dbar *(1-x)**a2_dbar *(b1_d*z + b2_d*z**2 + b3_d*z**3 + b4_d*z**4))
      pdf_list.append(c_s*x**a1_s    *(1-x)**a2_s)
      pdf_list.append(c_s*x**a1_sbar *(1-x)**a2_sbar)
      pdf_list.append(x**a1_g * (1-x)**a2_g *(g0*(e0*(1-z)**2 +e1*2*z*(1-z)+z**2)))
      return pdf_list



# A preprocessing layer
class f3Preproc(MetaLayer):
   def __init__(self,
                model_name,
                flav_info=None,
                seed=0,
                initializer="random_uniform",
                large_x = True,
                **kwargs):
      if flav_info is None:
         raise ValueError("Trying to instantiate a preprocessing with no basis information")
      self.model_name = model_name
      self.flav_info = flav_info
      self.seed = seed
      self.output_dim = len(flav_info)
      self.initializer = initializer
      self.large_x = large_x
      self.kernel = []
      super().__init__(**kwargs)

   def generate_weight(self, weight_name, kind, dictionary, set_to_zero=False):
      weight_constraint = None
      if weight_name == "B_ubar": trainable = False
      if set_to_zero:
         initializer = MetaLayer.init_constant(0.0)
         trainable = False
      else:
         limits = dictionary[kind]
         ldo = limits[0]
         lup = limits[1]
         trainable = dictionary.get("trainable", True)
         # Set the initializer and move the seed one up
         initializer = MetaLayer.select_initializer(
            self.initializer, minval=ldo, maxval=lup, seed=self.seed
          )
         self.seed += 1
         # If we are training, constrain the weights to be within the limits
         if trainable:
            weight_constraint = constraints.MinMaxWeight(ldo, lup)

        # Generate the new trainable (or not) parameter
         newpar = self.builder_helper(
            name=weight_name,
            kernel_shape=(1,),
            initializer=initializer,
            trainable=trainable,
            constraint=weight_constraint,
         )
         logger.info("Appending parameter %s", weight_name)
         self.kernel.append(newpar)

   def get_wgt(self, string):
      for i in range(len(self.kernel)):
         if '/'+string+':' in self.kernel[i].name : return self.kernel[i][0]
      logger.error(f"Weight %s does not exist", string)
      return 0

   def build(self, input_shape):
       # Run through the whole basis
       if self.model_name == "hera":
          for flav_dict in self.flav_info:
             flav_name = flav_dict["fl"]
             B_name = f"B_{flav_name}"
             C_name = f"C_{flav_name}"
             self.generate_weight(B_name, "smallx", flav_dict)
             self.generate_weight(C_name, "largex", flav_dict, set_to_zero=not self.large_x)
       super(f3Preproc, self).build(input_shape)

   def call_cteq(self, inputs):
      x = inputs
      pdf_list = []
      for i in range(7): pdf_list.append(x/x)
      return op.concatenate(pdf_list, axis = -1)


   def call_hera(self, inputs):
      x = inputs
      pdf_list = []
      b_g    = self.get_wgt("B_g")
      c_g    = self.get_wgt("C_g")
      b_uv   = self.get_wgt("B_uv") 
      c_uv   = self.get_wgt("C_uv")
      b_dv   = self.get_wgt("B_dv") 
      c_dv   = self.get_wgt("C_dv")
      b_dbar = self.get_wgt("B_dbar")
      c_dbar = self.get_wgt("C_dbar")
      b_ubar = b_dbar
      c_ubar = self.get_wgt("C_ubar")
      b_s    = b_dbar
      c_s    = c_dbar
      b_sbar = b_dbar
      c_sbar = c_dbar
      
      pdf_list.append(x ** b_uv * (1-x) ** c_uv)
      pdf_list.append(x ** b_ubar * (1-x) ** c_ubar)
      pdf_list.append(x ** b_dv * (1-x) ** c_dv)
      pdf_list.append(x ** b_dbar * (1-x) ** c_dbar)
      pdf_list.append(x ** b_s * (1-x) ** c_s)
      pdf_list.append(x ** b_sbar * (1-x) ** c_sbar)
      pdf_list.append(x ** b_g * (1-x) ** c_g)
      return op.concatenate(pdf_list, axis=-1)


   def call(self, inputs, **kwargs):
      if self.model_name == "hera": return self.call_hera(inputs)
      if self.model_name == "cteq": return self.call_cteq(inputs)
      logger.error("Model %s is unknown.",self.model_name)
      return 0

   


# @title
class PC:


  def __init__(self, color, hardware, size):
    self.color = color
    self.hardware = hardware
    self.size = size

  def describe(self):
    print(f"This PC is made for {self.hardware}")

  def size (self):
    print(f"The size of this PC is: {self.size}")


#self: se utiliza para decirle a python a que objeto pertenecen los atributos.
# Create an instance using the class "table"
#Metodos se definen con def

PC1 = PC("black", "high performance", "55cmx55cm")
PC2 = PC("white", "Working", "15x25x30cm")
#We acces to the object (instance) "table 1" to call it is data
print(PC1.color)
print(PC2.hardware)
PC1.describe()
PC2.describe()

#Instance "table 2"
print(PC2.size)


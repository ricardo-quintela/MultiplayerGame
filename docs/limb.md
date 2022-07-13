# The Limb class
  
### \_\_init\_\_  
  
**Signature:**  
  
>```__init__(self, name: str = "") -> None```  
  
**Description:**  
  
>Constructor of the class Limb  
>  
>A limb is a set of bones that are ment to be attached and move together  
>The limb can be anchored to a fixed point  
  
**Arguments:**  
  
>```name``` (str, optional): the name of the limb. Defaults to "".  
>  
  
  
### setName  
  
**Signature:**  
  
>```setName(self, name: str)```  
  
**Description:**  
  
>Sets the name attribute to the given string  
  
**Arguments:**  
  
>```name``` (```str```): the new name  
>  
  
  
### add  
  
**Signature:**  
  
>```add(self, bone: Bone)```  
  
**Description:**  
  
>Adds a bone to the limb  
  
**Arguments:**  
  
>```bone``` (```Bone```): the bone to add  
>  
  
  
### fixate  
  
**Signature:**  
  
>```fixate(self, anchor)```  
  
**Description:**  
  
>Anchors the limb to a given point  
>  
>If the given point is a mutable object, then the limb will follow it as it changes  
  
**Arguments:**  
  
>```anchor``` (list, Vector2): the point to anchor the limb  
>  
  
  
### update  
  
**Signature:**  
  
>```update(self)```  
  
**Description:**  
  
>Updates all the bones in the skeleton  
  
  

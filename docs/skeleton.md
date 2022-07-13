# The Skeleton class
  
### \_\_init\_\_  
  
**Signature:**  
  
>```__init__(self) -> None```  
  
**Description:**  
  
>Constructor of the class skeleton  
>  
>A skeleton is a set of bones that can be customized and controlled all at once  
  
  
### newLimb  
  
**Signature:**  
  
>```newLimb(self, name: str = "")```  
  
**Description:**  
  
>Adds a new limb to the skeleton  
  
**Arguments:**  
  
>```name``` (str, optional): the name of the limb. Defaults to "".  
>  
  
  
### getBone  
  
**Signature:**  
  
>```getBone(self, name: str) -> Bone```  
  
**Description:**  
  
>Returns a bone on the skeleton by the given name  
  
**Arguments:**  
  
>```name``` (```str```): the name of the bone  
>  
  
**Raises:**  
  
>KeyError: if the bone doenst exist in the skeleton

  
  
**Returns:**  
  
>Bone: the bone on the skeleton
  
  
  
### getLimb  
  
**Signature:**  
  
>```getLimb(self, name: str) -> Limb```  
  
**Description:**  
  
>Returns a limb on the skeleton by the given name  
  
**Arguments:**  
  
>```name``` (```str```): the name of the limb  
>  
  
**Raises:**  
  
>KeyError: if the limb doenst exist in the skeleton

  
  
**Returns:**  
  
>Limb: the limb on the skeleton
  
  
  
### update  
  
**Signature:**  
  
>```update(self)```  
  
**Description:**  
  
>Updates all the bones in the skeleton  
  
  
### blit  
  
**Signature:**  
  
>```blit(self, canvas: Surface)```  
  
**Description:**  
  
>Draw all the bones on the given Surface  
  
**Arguments:**  
  
>```canvas``` (```Surface```): the Surface where to draw the bones  
>  
  
  
